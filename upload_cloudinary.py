import cloudinary
import cloudinary.uploader
import os
import json
from pathlib import Path

cloudinary.config(
    cloud_name="dbdtsbrmd",
    api_key="113671575275585",
    api_secret="VeA46TGQ2HcSzz0y31Sl4kl3v7g",
    secure=True,
)

BASE = Path("Marketing/Social")

# 13 posts a publicar (em ordem de postagem)
POSTS = [
    "Evasao-09-04",
    "Retencao-Ingles-11-04",
    "DadosVsVisao-14-05",
    "EquipeSemPrioridade-14-05",
    "GestaoPreditiva-14-05",
    "IndicacoesPerdidas-14-05",
    "Inadimplencia-14-05",
    "CustoRetrabalho-14-05",
    "EngajamentoRisco-14-05",
    "GestaoPeloFeeling-14-05",
    "ComunicacaoPais-14-05",
    "EscolasQueCrescem-14-05",
    "Onboarding90Dias-14-05",
]

results = {}

for post in POSTS:
    pronto = BASE / post / "pronto"
    if not pronto.exists():
        print(f"[SKIP] {post} — pasta pronto não encontrada")
        continue

    slides = sorted(pronto.glob("*.png"))
    if not slides:
        print(f"[SKIP] {post} — nenhum slide encontrado")
        continue

    print(f"\n[UPLOAD] {post} ({len(slides)} slides)")
    urls = []

    for slide in slides:
        public_id = f"skolen/social/{post}/{slide.stem}"
        response = cloudinary.uploader.upload(
            str(slide),
            public_id=public_id,
            overwrite=True,
            resource_type="image",
        )
        url = response["secure_url"]
        urls.append(url)
        print(f"  OK {slide.name} -> {url}")

    results[post] = urls

output_path = Path("cloudinary_urls.json")
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print(f"\nUpload concluido. URLs salvas em {output_path}")
print(f"   Total: {sum(len(v) for v in results.values())} slides em {len(results)} posts")
