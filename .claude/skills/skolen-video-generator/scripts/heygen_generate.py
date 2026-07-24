"""
heygen_generate.py — gera um video de avatar falando via API HeyGen v3 (POST /v3/videos).

Fluxo: submete avatar_id + script + voice_id (TTS nativo do HeyGen) -> poll de status -> download do MP4.

Uso:
    python heygen_generate.py \
        --avatar-id "09dae41419364c3599c1f1ca346d00e8" \
        --text "Roteiro que o avatar vai falar." \
        --voice-id "<voice_id>" \
        --out "../../../Marketing/Social/_video-gerados/nome-do-video.mp4"

Flags:
    --avatar-id     ID do avatar HeyGen (obrigatorio)
    --text          Roteiro a ser falado (obrigatorio)
    --voice-id      Voice ID HeyGen (obrigatorio — a API v3 nao aceita omitir.
                    Use heygen_list_voices.py --language Portuguese para escolher uma)
    --out           Caminho de saida do MP4 (obrigatorio)
    --aspect-ratio  "9:16" (padrao, Reels/Stories) ou "16:9" ou "1:1"
    --resolution    "720p" (padrao) ou "1080p" ou "4k"
    --background    Cor de fundo hex (padrao: #FFFFFF)
    --timeout       Timeout em segundos para o poll (padrao: 600)

Requer HEYGEN_API_KEY no ambiente (carregado de .env na raiz do repo).
"""
import argparse
import io
import os
import sys
import time
import urllib.request
from pathlib import Path

import requests

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

REPO_ROOT = Path(__file__).resolve().parents[4]
ENV_FILE = REPO_ROOT / ".env"

API_BASE = "https://api.heygen.com"


def load_api_key() -> str:
    key = os.environ.get("HEYGEN_API_KEY")
    if key:
        return key
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
            if line.strip().startswith("HEYGEN_API_KEY="):
                return line.split("=", 1)[1].strip()
    raise RuntimeError(
        "HEYGEN_API_KEY nao encontrada. Configure no .env na raiz do repo "
        "ou exporte a variavel de ambiente."
    )


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--avatar-id", required=True)
    p.add_argument("--text", required=True)
    p.add_argument("--voice-id", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--aspect-ratio", default="9:16", choices=["9:16", "16:9", "4:5", "5:4", "1:1", "auto"])
    p.add_argument("--resolution", default="720p", choices=["720p", "1080p", "4k"])
    p.add_argument("--background", default="#FFFFFF")
    p.add_argument("--timeout", type=int, default=600)
    return p.parse_args()


def submit_video(api_key: str, avatar_id: str, text: str, voice_id: str,
                  aspect_ratio: str, resolution: str, background: str) -> str:
    payload = {
        "type": "avatar",
        "avatar_id": avatar_id,
        "script": text,
        "voice_id": voice_id,
        "resolution": resolution,
        "aspect_ratio": aspect_ratio,
        "background": {"type": "color", "value": background},
        "output_format": "mp4",
    }

    resp = requests.post(
        f"{API_BASE}/v3/videos",
        headers={"X-Api-Key": api_key, "Content-Type": "application/json"},
        json=payload,
        timeout=60,
    )
    data = resp.json()
    if resp.status_code >= 400:
        raise RuntimeError(f"Falha ao submeter video: {resp.status_code} — {data}")

    video_id = data.get("data", {}).get("id") or data.get("data", {}).get("video_id")
    if not video_id:
        raise RuntimeError(f"video_id nao encontrado na resposta: {data}")

    print(f"video_id: {video_id}")
    return video_id


def poll_video(api_key: str, video_id: str, timeout_s: int) -> str:
    print(f"Aguardando renderizacao (timeout {timeout_s}s)...")
    deadline = time.time() + timeout_s

    while time.time() < deadline:
        resp = requests.get(
            f"{API_BASE}/v3/videos/{video_id}",
            headers={"X-Api-Key": api_key},
            timeout=30,
        )
        data = resp.json().get("data", {})
        status = data.get("status")
        elapsed = int(timeout_s - (deadline - time.time()))
        print(f"  [{elapsed}s] status: {status}")

        if status == "completed":
            video_url = data.get("video_url")
            if not video_url:
                raise RuntimeError(f"Status completed mas sem video_url: {data}")
            return video_url

        if status == "failed":
            raise RuntimeError(f"Geracao falhou: {data.get('failure_message') or data.get('failure_code')}")

        time.sleep(10)

    raise TimeoutError(f"Video {video_id} nao ficou pronto em {timeout_s}s")


def download_video(video_url: str, out_path: Path):
    out_path.parent.mkdir(parents=True, exist_ok=True)
    print(f"Baixando para {out_path}...")
    urllib.request.urlretrieve(video_url, out_path)
    size_mb = out_path.stat().st_size / 1024 / 1024
    print(f"Download concluido: {size_mb:.1f} MB")


def main():
    args = parse_args()
    api_key = load_api_key()
    out_path = Path(args.out)

    video_id = submit_video(
        api_key, args.avatar_id, args.text, args.voice_id,
        args.aspect_ratio, args.resolution, args.background,
    )
    video_url = poll_video(api_key, video_id, args.timeout)
    download_video(video_url, out_path)

    print(f"\nPronto! Video salvo em: {out_path}")
    print(f"video_id: {video_id}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Erro: {e}", file=sys.stderr)
        sys.exit(1)
