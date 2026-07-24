"""
elevenlabs_generate.py — gera um MP3 a partir de um roteiro em PT-BR via ElevenLabs.

Uso:
    python elevenlabs_generate.py \
        --text "Roteiro completo em pt-BR, com acentos." \
        --voice-id "FAgSMhKABxmP4D1rHv3L" \
        --out "../../../Marketing/Social/_video-gerados/nome-do-audio.mp3"

Requer ELEVENLABS_API_KEY no ambiente (carregado de .env na raiz do repo).
"""
import argparse
import io
import os
import sys
import time
from pathlib import Path

import requests

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

REPO_ROOT = Path(__file__).resolve().parents[4]
ENV_FILE = REPO_ROOT / ".env"

MODEL = "eleven_multilingual_v2"
VOICE_SETTINGS = {
    "stability": 0.28,
    "similarity_boost": 0.80,
    "style": 0.55,
    "use_speaker_boost": True,
    "speed": 0.92,
}


def load_api_key() -> str:
    key = os.environ.get("ELEVENLABS_API_KEY")
    if key:
        return key
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
            if line.strip().startswith("ELEVENLABS_API_KEY="):
                return line.split("=", 1)[1].strip()
    raise RuntimeError(
        "ELEVENLABS_API_KEY nao encontrada. Configure no .env na raiz do repo "
        "ou exporte a variavel de ambiente."
    )


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--text", required=True)
    p.add_argument("--voice-id", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--retries", type=int, default=6)
    return p.parse_args()


def elevenlabs_tts(text: str, voice_id: str, api_key: str, out_path: Path, retries: int):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json",
        "Accept": "audio/mpeg",
    }
    payload = {
        "text": text.strip(),
        "model_id": MODEL,
        "language_code": "pt",
        "voice_settings": VOICE_SETTINGS,
    }

    for attempt in range(1, retries + 1):
        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=60)
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
            wait = min(5 * attempt, 30)
            print(f"  timeout/conexao, aguardando {wait}s (tentativa {attempt}/{retries})...")
            time.sleep(wait)
            continue

        if resp.status_code == 200:
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_bytes(resp.content)
            return

        if resp.status_code == 429:
            wait = 2 ** attempt
            print(f"  rate-limit, aguardando {wait}s...")
            time.sleep(wait)
            continue

        raise RuntimeError(f"ElevenLabs {resp.status_code}: {resp.text[:300]}")

    raise RuntimeError(f"ElevenLabs falhou apos {retries} tentativas")


def main():
    args = parse_args()
    api_key = load_api_key()
    out_path = Path(args.out)

    print(f"Gerando audio (voz {args.voice_id})...")
    elevenlabs_tts(args.text, args.voice_id, api_key, out_path, args.retries)

    size_kb = out_path.stat().st_size / 1024
    print(f"Pronto! Audio salvo em: {out_path} ({size_kb:.0f} KB)")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Erro: {e}", file=sys.stderr)
        sys.exit(1)
