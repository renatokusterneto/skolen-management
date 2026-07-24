"""
heygen_list_voices.py — lista vozes disponiveis na conta HeyGen (API v3), filtrando por idioma.

Uso:
    python heygen_list_voices.py --language Portuguese
    python heygen_list_voices.py --language Portuguese --gender female
"""
import argparse
import io
import os
import sys
from pathlib import Path

import requests

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

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
    raise RuntimeError("HEYGEN_API_KEY nao encontrada no ambiente ou .env")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--language", default=None, help="Ex: Portuguese")
    p.add_argument("--gender", default=None, choices=["male", "female"])
    args = p.parse_args()

    api_key = load_api_key()

    params = {"limit": 100, "engine": "starfish"}
    if args.language:
        params["language"] = args.language
    if args.gender:
        params["gender"] = args.gender

    resp = requests.get(
        f"{API_BASE}/v3/voices",
        headers={"X-Api-Key": api_key},
        params=params,
        timeout=30,
    )
    resp.raise_for_status()
    voices = resp.json().get("data", [])

    if args.language:
        voices = [v for v in voices if args.language.lower() in (v.get("language") or "").lower()]
    if args.gender:
        voices = [v for v in voices if (v.get("gender") or "").lower() == args.gender]

    print(f"{len(voices)} vozes encontradas:\n")
    for v in voices:
        print(f"  {v.get('voice_id')}  |  {v.get('name')}  |  {v.get('language')}  |  {v.get('gender')}")


if __name__ == "__main__":
    main()
