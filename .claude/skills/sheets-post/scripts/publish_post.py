import io
import re
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

from cloudinary_upload import upload_slides
from sheets_register import register_post


def _parse_descricao(md_path: Path) -> tuple[str, str]:
    text = md_path.read_text(encoding="utf-8")

    title_match = re.search(r"^#\s+(.+)", text, re.MULTILINE)
    titulo = title_match.group(1).strip() if title_match else md_path.parent.name

    # Tudo entre o primeiro H2 "Texto para legenda" e o próximo "---"
    caption_match = re.search(
        r"## Texto para legenda.*?\n\n(.+?)(?=\n---|\n##)", text, re.DOTALL
    )
    hashtag_match = re.search(r"## Hashtags sugeridas\n\n(.+?)(?=\n---|\Z)", text, re.DOTALL)

    caption = caption_match.group(1).strip() if caption_match else ""
    if hashtag_match:
        caption += "\n\n" + hashtag_match.group(1).strip()

    return titulo, caption


def _infer_tipo(pronto_dir: Path) -> str:
    exts = {f.suffix for f in pronto_dir.iterdir()}
    if ".mp4" in exts:
        return "reel"
    slides = list(pronto_dir.glob("*.png"))
    return "carrousel" if len(slides) > 1 else "foto"


def run(post_dir: Path, data_postagem: str) -> None:
    pronto_dir = post_dir / "pronto"
    descricao_path = post_dir / "descricao-post.md"

    if not pronto_dir.exists():
        raise FileNotFoundError(f"Pasta pronto/ não encontrada em {post_dir}")
    if not descricao_path.exists():
        raise FileNotFoundError(f"descricao-post.md não encontrado em {post_dir}")

    campaign_id = post_dir.name.lower().replace(" ", "-")
    tipo = _infer_tipo(pronto_dir)
    titulo, caption = _parse_descricao(descricao_path)

    print(f"\nPost: {titulo}")
    print(f"Tipo: {tipo} | Agendado: {data_postagem}\n")

    print("Cloudinary:")
    urls = upload_slides(pronto_dir, campaign_id)

    print("\nPlanilha:")
    register_post(campaign_id, tipo, titulo, data_postagem, caption, urls)

    print(f"\nConcluído. {len(urls)} imagem(ns) na fila para {data_postagem}.")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python publish_post.py <caminho-da-pasta> <data_postagem>")
        print('Ex: python publish_post.py "Marketing/Social/Evasao-04-04" "2026-05-20 09:00"')
        sys.exit(1)

    run(Path(sys.argv[1]), sys.argv[2])
