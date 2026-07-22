"""MCP server for OpenAI image generation (gpt-image-1 family).

Reads the API key from the OPENAI_API_KEY environment variable only.
Never hardcode the key here or log it — the key is injected via .mcp.json's
env block, which itself must stay out of git (see .gitignore).
"""
import base64
import os
from pathlib import Path
from typing import List

from mcp.server.fastmcp import FastMCP
from openai import OpenAI

mcp = FastMCP("openai-image")

REPO_ROOT = Path(__file__).resolve().parents[3]
OUTPUT_DIR = REPO_ROOT / "Marketing" / "Assets" / "gerado-ia"


def _client() -> OpenAI:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY nao encontrada no ambiente do servidor MCP. "
            "Configure-a em .mcp.json (bloco env) sem expor o valor em texto no codigo."
        )
    return OpenAI(api_key=api_key)


@mcp.tool()
def generate_image(
    prompt: str,
    filename: str,
    size: str = "1024x1024",
    quality: str = "high",
    model: str = "gpt-image-1",
) -> str:
    """Gera uma imagem via OpenAI e salva em Marketing/Assets/gerado-ia.

    Args:
        prompt: Descricao da imagem desejada, em detalhe.
        filename: Nome do arquivo de saida, sem extensao (ex: "carrossel-slide-1").
        size: Dimensao da imagem. Opcoes: 1024x1024, 1024x1536, 1536x1024, auto.
        quality: Qualidade: low, medium, high, auto.
        model: Modelo a usar (default gpt-image-1).
    """
    client = _client()
    result = client.images.generate(
        model=model,
        prompt=prompt,
        size=size,
        quality=quality,
        n=1,
    )
    image_b64 = result.data[0].b64_json
    image_bytes = base64.b64decode(image_b64)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    safe_name = "".join(c for c in filename if c.isalnum() or c in ("-", "_")) or "imagem"
    out_path = OUTPUT_DIR / f"{safe_name}.png"

    out_path.write_bytes(image_bytes)
    return f"Imagem salva em: {out_path}"


def _resolve_reference(path_str: str) -> Path:
    p = Path(path_str)
    if not p.is_absolute():
        p = REPO_ROOT / p
    if not p.exists():
        raise FileNotFoundError(f"Imagem de referencia nao encontrada: {p}")
    return p


@mcp.tool()
def generate_image_with_references(
    prompt: str,
    reference_images: List[str],
    filename: str,
    size: str = "1024x1024",
    quality: str = "high",
    model: str = "gpt-image-1",
) -> str:
    """Gera uma imagem via OpenAI usando uma ou mais imagens existentes como referencia visual
    (mockups do produto, fotos de pessoas etc.), via endpoint images.edit.

    Args:
        prompt: Instrucao de como combinar/adaptar as imagens de referencia.
        reference_images: Lista de caminhos (relativos ao repo ou absolutos) para as imagens
            de referencia, ex: ["Marketing/Assets/produto/app_boletim.png"].
        filename: Nome do arquivo de saida, sem extensao.
        size: Dimensao da imagem. Opcoes: 1024x1024, 1024x1536, 1536x1024, auto.
        quality: Qualidade: low, medium, high, auto.
        model: Modelo a usar (default gpt-image-1).
    """
    client = _client()
    ref_paths = [_resolve_reference(r) for r in reference_images]
    files = [open(p, "rb") for p in ref_paths]
    try:
        result = client.images.edit(
            model=model,
            image=files,
            prompt=prompt,
            size=size,
            quality=quality,
        )
    finally:
        for f in files:
            f.close()

    image_b64 = result.data[0].b64_json
    image_bytes = base64.b64decode(image_b64)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    safe_name = "".join(c for c in filename if c.isalnum() or c in ("-", "_")) or "imagem"
    out_path = OUTPUT_DIR / f"{safe_name}.png"

    out_path.write_bytes(image_bytes)
    return f"Imagem salva em: {out_path}"


if __name__ == "__main__":
    mcp.run()
