import os
from pathlib import Path
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[4]
load_dotenv(ROOT / ".env")

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
)


def upload_slides(pronto_dir: Path, campaign_id: str) -> list[str]:
    slides = sorted(pronto_dir.glob("*.png"))
    if not slides:
        raise FileNotFoundError(f"Nenhum PNG encontrado em {pronto_dir}")

    urls = []
    for slide in slides:
        result = cloudinary.uploader.upload(
            str(slide),
            folder=f"skolen/social/{campaign_id}",
            public_id=slide.stem,
            overwrite=True,
        )
        urls.append(result["secure_url"])
        print(f"  OK {slide.name}")

    return urls