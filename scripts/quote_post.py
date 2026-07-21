"""
quote_post.py — Gera um vídeo no estilo "quote post" do Instagram para a Skolen.

Uso:
    python scripts/quote_post.py --input "https://..." --text "Frase curta aqui"
    python scripts/quote_post.py --input video.mp4 --text "Frase curta aqui"
    python scripts/quote_post.py --input video.mp4 --text "Frase" --output saida.mp4

Output padrão: Marketing/Social/_video-reposts/quote_<timestamp>.mp4
"""

import argparse
import os
import subprocess
import tempfile
import time
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from pilmoji import Pilmoji

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).parent.parent
LOGO_IMG = REPO_ROOT / "Marketing" / "Assets" / "marca" / "logo.png"
FONT_DIR = REPO_ROOT / "assets" / "fonts"
FONT_PATH = FONT_DIR / "Nunito.ttf"

DEFAULT_OUT_DIR = REPO_ROOT / "Marketing" / "Social" / "_video-reposts"

# Identidade visual Skolen
BRAND_ACCENT = (94, 203, 168)  # #5ECBA8 (teal)
BRAND_DARK = (43, 54, 65)      # #2B3641

# Output canvas (9:16 Reels/Stories)
CANVAS_W = 1080
CANVAS_H = 1920


# ---------------------------------------------------------------------------
# Font download
# ---------------------------------------------------------------------------
NUNITO_URL = "https://github.com/google/fonts/raw/refs/heads/main/ofl/nunito/Nunito%5Bwght%5D.ttf"

def ensure_fonts():
    FONT_DIR.mkdir(parents=True, exist_ok=True)
    if not FONT_PATH.exists():
        print("Baixando fonte Nunito...")
        import requests
        r = requests.get(NUNITO_URL, allow_redirects=True)
        r.raise_for_status()
        FONT_PATH.write_bytes(r.content)
        print("Fonte baixada.")
    return True


# ---------------------------------------------------------------------------
# Video download (yt-dlp)
# ---------------------------------------------------------------------------
def download_video(url: str, dest_dir: Path) -> Path:
    dest_dir.mkdir(parents=True, exist_ok=True)
    out_template = str(dest_dir / "source.%(ext)s")
    subprocess.run(
        ["yt-dlp", "-f", "mp4/best[ext=mp4]/best", "-o", out_template, url],
        check=True,
    )
    for f in dest_dir.glob("source.*"):
        return f
    raise FileNotFoundError("yt-dlp não gerou arquivo de saída")


# ---------------------------------------------------------------------------
# Frame builders
# ---------------------------------------------------------------------------
def build_header(draw_target_w: int) -> Image.Image:
    """Monta o header Skolen (logo + nome da conta) a partir do logo.png."""
    logo = Image.open(LOGO_IMG).convert("RGBA")
    header_h = int(draw_target_w * logo.height / logo.width)
    # Limita a altura do header pra não dominar o canvas (logo é um lockup largo)
    max_header_h = 140
    if header_h > max_header_h:
        header_h = max_header_h
        header_w = int(header_h * logo.width / logo.height)
    else:
        header_w = draw_target_w
    logo = logo.resize((header_w, header_h), Image.LANCZOS)

    canvas = Image.new("RGBA", (draw_target_w, header_h), (0, 0, 0, 0))
    canvas.paste(logo, ((draw_target_w - header_w) // 2, 0), logo)
    return canvas


def build_frame(text: str) -> tuple:
    """Build the white Instagram-style frame as a PIL image (RGBA)."""
    canvas = Image.new("RGBA", (CANVAS_W, CANVAS_H), (255, 255, 255, 255))
    draw = ImageDraw.Draw(canvas)

    # --- Header (logo Skolen) ---
    PADDING = 48
    header_target_w = CANVAS_W - PADDING * 2
    header = build_header(header_target_w)
    header_h = header.height
    canvas.paste(header, (PADDING + (header_target_w - header.width) // 2, 64), header)

    text_y = 64 + header_h + 48
    text_block_h = 0

    if text and text.strip():
        # --- Caption text ---
        font_size = 54
        font = ImageFont.truetype(str(FONT_PATH), font_size)

        max_text_w = CANVAS_W - PADDING * 2
        words = text.split()
        lines, current = [], ""
        for word in words:
            test = (current + " " + word).strip()
            if draw.textlength(test, font=font) <= max_text_w:
                current = test
            else:
                if current:
                    lines.append(current)
                current = word
        if current:
            lines.append(current)
        wrapped = "\n".join(lines)

        with Pilmoji(canvas) as pilmoji:
            pilmoji.text(
                (PADDING, text_y),
                wrapped,
                font=font,
                fill=BRAND_DARK + (255,),
                spacing=12,
            )

        bbox = draw.multiline_textbbox((PADDING, text_y), wrapped, font=font, spacing=12)
        text_block_h = bbox[3] - bbox[1]

    # --- Video zone: centered, rounded rect placeholder area ---
    video_top = text_y + text_block_h + 56
    video_w = int((CANVAS_W - PADDING * 2) * 0.85)
    video_left = (CANVAS_W - video_w) // 2
    video_h = min(int(video_w * 4 / 3), CANVAS_H - video_top - 80)

    draw_rounded_rect(draw, video_left, video_top, video_w, video_h, radius=32, fill=(240, 240, 240, 255))

    caption_y = video_top + video_h + 28

    return canvas, (video_left, video_top, video_w, video_h), caption_y


def draw_rounded_rect(draw, x, y, w, h, radius, fill):
    draw.rectangle([x + radius, y, x + w - radius, y + h], fill=fill)
    draw.rectangle([x, y + radius, x + w, y + h - radius], fill=fill)
    draw.ellipse([x, y, x + radius * 2, y + radius * 2], fill=fill)
    draw.ellipse([x + w - radius * 2, y, x + w, y + radius * 2], fill=fill)
    draw.ellipse([x, y + h - radius * 2, x + radius * 2, y + h], fill=fill)
    draw.ellipse([x + w - radius * 2, y + h - radius * 2, x + w, y + h], fill=fill)


# ---------------------------------------------------------------------------
# Whisper transcription
# ---------------------------------------------------------------------------
def transcribe_segments(video: Path) -> list:
    """Run Whisper tiny on video, return list of {start, end, text} dicts."""
    import json as _json
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        result = subprocess.run(
            ["whisper", str(video), "--model", "tiny", "--language", "pt",
             "--output_format", "json", "--output_dir", str(tmp)],
            capture_output=True, text=True,
        )
        json_files = list(tmp.glob("*.json"))
        if not json_files:
            return []
        data = _json.loads(json_files[0].read_text(encoding="utf-8"))
        return [{"start": s["start"], "end": s["end"], "text": s["text"].strip()}
                for s in data.get("segments", [])]


def _burn_captions(video: Path, segments: list, caption_y: int, output: Path):
    """Burn synchronized captions at caption_y using PIL frame overlay via cv2."""
    import cv2 as _cv2
    import numpy as _np

    cap = _cv2.VideoCapture(str(video))
    fps = cap.get(_cv2.CAP_PROP_FPS)
    w = int(cap.get(_cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(_cv2.CAP_PROP_FRAME_HEIGHT))

    tmp_no_audio = str(output) + "_noaudio.mp4"
    fourcc = _cv2.VideoWriter_fourcc(*"mp4v")
    writer = _cv2.VideoWriter(tmp_no_audio, fourcc, fps, (w, h))

    font = ImageFont.truetype(str(FONT_PATH), 36)
    frame_idx = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        t = frame_idx / fps

        active = next((s for s in segments if s["start"] <= t < s["end"]), None)
        if active:
            pil = Image.fromarray(_cv2.cvtColor(frame, _cv2.COLOR_BGR2RGB))
            draw = ImageDraw.Draw(pil)
            txt = active["text"]
            bbox = draw.textbbox((0, 0), txt, font=font)
            tw = bbox[2] - bbox[0]
            tx = (w - tw) // 2
            ty = caption_y
            pad = 8
            draw.rounded_rectangle(
                [tx - pad, ty - pad, tx + tw + pad, ty + (bbox[3] - bbox[1]) + pad],
                radius=6, fill=(255, 255, 255, 220)
            )
            draw.text((tx, ty), txt, font=font, fill=BRAND_DARK)
            frame = _cv2.cvtColor(_np.array(pil), _cv2.COLOR_RGB2BGR)

        writer.write(frame)
        frame_idx += 1

    cap.release()
    writer.release()

    subprocess.run([
        "ffmpeg", "-y",
        "-i", tmp_no_audio,
        "-i", str(video),
        "-map", "0:v", "-map", "1:a?",
        "-c:v", "libx264", "-preset", "fast", "-crf", "20",
        "-c:a", "copy",
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        str(output),
    ], check=True, capture_output=True)
    Path(tmp_no_audio).unlink(missing_ok=True)


def build_srt(segments: list, path: Path):
    """Write an SRT subtitle file from Whisper segments."""
    def fmt_time(s):
        h = int(s // 3600)
        m = int((s % 3600) // 60)
        sec = s % 60
        return f"{h:02d}:{m:02d}:{sec:06.3f}".replace(".", ",")

    with open(path, "w", encoding="utf-8") as f:
        for i, seg in enumerate(segments, 1):
            f.write(f"{i}\n")
            f.write(f"{fmt_time(seg['start'])} --> {fmt_time(seg['end'])}\n")
            f.write(f"{seg['text']}\n\n")


# ---------------------------------------------------------------------------
# ffmpeg compose
# ---------------------------------------------------------------------------
def compose_video(source_video: Path, text: str, output: Path, captions: bool = False):
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)

        frame_img, (vx, vy, vw, vh), caption_y = build_frame(text)
        frame_path = tmp / "frame.png"
        frame_img.save(frame_path)

        probe = subprocess.run(
            [
                "ffprobe", "-v", "error",
                "-select_streams", "v:0",
                "-show_entries", "stream=width,height,duration",
                "-of", "csv=p=0",
                str(source_video),
            ],
            capture_output=True, text=True, check=True,
        )
        parts = probe.stdout.strip().split(",")
        try:
            duration = float(parts[2])
        except (IndexError, ValueError):
            probe2 = subprocess.run(
                ["ffprobe", "-v", "error", "-show_entries", "format=duration",
                 "-of", "csv=p=0", str(source_video)],
                capture_output=True, text=True, check=True,
            )
            duration = float(probe2.stdout.strip())

        scale_filter = (
            f"scale={vw}:{vh}:force_original_aspect_ratio=increase,"
            f"crop={vw}:{vh}"
        )

        mask_path = tmp / "mask.png"
        _make_rounded_mask(vw, vh, radius=32, path=mask_path)

        srt_path = None
        segs = []
        if captions:
            print("Transcrevendo para legendas...", end=" ", flush=True)
            segs = transcribe_segments(source_video)
            if segs:
                srt_path = tmp / "captions.srt"
                build_srt(segs, srt_path)
                print(f"{len(segs)} segmentos")
            else:
                print("sem fala detectada")

        output.parent.mkdir(parents=True, exist_ok=True)

        intermediate = tmp / "intermediate.mp4"
        cmd1 = [
            "ffmpeg", "-y",
            "-loop", "1", "-framerate", "30", "-i", str(frame_path),
            "-i", str(source_video),
            "-i", str(mask_path),
            "-filter_complex", (
                f"[1:v]{scale_filter},format=rgba[vid];"
                f"[2:v]format=rgba[mask];"
                f"[vid][mask]alphamerge[vidmasked];"
                f"[0:v][vidmasked]overlay={vx}:{vy}[out]"
            ),
            "-map", "[out]",
            "-map", "1:a?",
            "-t", str(duration),
            "-c:v", "libx264", "-preset", "fast", "-crf", "20",
            "-c:a", "aac", "-b:a", "192k",
            "-pix_fmt", "yuv420p",
            str(intermediate),
        ]

        print(f"\nProcessando vídeo... ({duration:.1f}s)")
        subprocess.run(cmd1, check=True)

        if srt_path and srt_path.exists():
            print("Adicionando legendas sincronizadas...")
            _burn_captions(intermediate, segs, caption_y, output)
        else:
            import shutil
            shutil.copy2(str(intermediate), str(output))


def _make_rounded_mask(w: int, h: int, radius: int, path: Path):
    mask = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(mask)
    draw_rounded_rect(draw, 0, 0, w, h, radius=radius, fill=(255, 255, 255, 255))
    mask.save(path)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Quote Post Generator — Skolen")
    parser.add_argument("--input", "-i", required=True, help="URL ou caminho para arquivo MP4")
    parser.add_argument("--text", "-t", default=None, nargs="?", const="", help="Frase/legenda curta (omitir ou passar vazio = sem legenda)")
    parser.add_argument("--output", "-o", default=None, help="Caminho do MP4 de saída")
    parser.add_argument("--captions", action="store_true", help="Transcreve o vídeo com Whisper e adiciona legendas sincronizadas abaixo do frame")
    args = parser.parse_args()

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)

        src = Path(args.input)
        if not src.exists():
            print(f"Baixando vídeo de: {args.input}")
            src = download_video(args.input, tmp / "dl")

        if args.text is None:
            args.text = ""

        ensure_fonts()

        if args.output:
            out = Path(args.output)
        else:
            DEFAULT_OUT_DIR.mkdir(parents=True, exist_ok=True)
            ts = int(time.time())
            out = DEFAULT_OUT_DIR / f"quote_{ts}.mp4"

        print(f"Logo:    {LOGO_IMG}")
        print(f"Texto:   {args.text}")
        print(f"Input:   {src}")
        print(f"Output:  {out}")

        compose_video(src, args.text, out, captions=args.captions)

    print(f"\nPronto! Video salvo em:\n  {out}")


if __name__ == "__main__":
    main()
