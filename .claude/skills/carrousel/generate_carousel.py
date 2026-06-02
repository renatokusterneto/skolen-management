#!/usr/bin/env python3
"""
generate_carousel.py — Gera carrossel Skolen a partir de config.json

Usage:
    python .claude/skills/carrousel/generate_carousel.py <pasta_do_post>/config.json

    Exemplo:
    python .claude/skills/carrousel/generate_carousel.py Marketing/Social/Evasao-20-05/config.json

Estrutura esperada do config.json:
{
  "pasta": "Marketing/Social/Evasao-20-05",
  "cor_dominante": "teal",       // teal | pink | yellow | blue
  "slides": [
    {"tipo": "cover",  "eyebrow": "...", "headline": "...", "subhead": "..."},
    {"tipo": "text",   "label": "...",   "headline": "...", "body": "..."},
    {"tipo": "number", "label": "...",   "stat": "...",     "stat_label": "..."},
    {"tipo": "app",    "eyebrow": "...", "headline": "...", "features": ["...", "...", "..."]},
    {"tipo": "text",   "label": "...",   "headline": "...", "body": "..."},
    {"tipo": "number", "label": "...",   "stat": "...",     "stat_label": "..."},
    {"tipo": "cta",    "eyebrow": "...", "headline": "...", "subhead": "...", "button": "..."}
  ]
}

Notas de formatação nos textos:
  - Use <br> para quebra de linha
  - Use <em>palavra</em> para destacar na cor dominante
  - Use <strong>palavra</strong> para negrito extra no body-text
"""

import json
import os
import sys
import subprocess
from pathlib import Path

# ── Constantes ───────────────────────────────────────────────────────────────

FONT_HREF = "file:///c:/Users/felipe.fadel/skolen-management/.claude/skills/carrousel/fonts/nunito.css"

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

HEX = {
    "yellow": "#F5C842",
    "teal":   "#5ECBA8",
    "pink":   "#E87DB0",
    "blue":   "#5A8ED4",
}

LABEL_RGBA = {
    "yellow": "rgba(245,200,66,0.12)",
    "teal":   "rgba(94,203,168,0.12)",
    "pink":   "rgba(232,125,176,0.12)",
    "blue":   "rgba(90,142,212,0.12)",
}

# Círculos: (tamanho, deslocamento) por canto e por slide
# Formato: (tl_size, tr_size, bl_size, br_size,
#           tl_top, tl_left, tr_top, tr_right, bl_bottom, bl_left, br_bottom, br_right)
CIRCLE_SIZES = [
    (320, 220, 160, 240, -100, -100, -65, -65,  -45, -45,  -70, -70),  # slide 1
    (220, 200, 240, 200,  -65,  -65, -58, -58,  -70, -70,  -58, -58),  # slide 2
    (200, 180, 200, 220,  -58,  -58, -52, -52,  -58, -58,  -65, -65),  # slide 3
    (180, 220, 220, 240,  -52,  -52, -65, -65,  -65, -65,  -70, -70),  # slide 4
    (220, 200, 240, 200,  -65,  -65, -58, -58,  -70, -70,  -58, -58),  # slide 5
    (200, 240, 200, 220,  -58,  -58, -70, -70,  -58, -58,  -65, -65),  # slide 6
    (240, 180, 220, 280,  -70,  -70, -52, -52,  -65, -65,  -80, -80),  # slide 7
]

# Cores dos círculos por slide: "D" = cor dominante, demais são fixas
# Ordem: (TL, TR, BL, BR)
CIRCLE_COLORS = [
    ("D",      "yellow", "blue",   "D"),      # slide 1
    ("yellow", "D",      "D",      "blue"),   # slide 2
    ("D",      "pink",   "blue",   "yellow"), # slide 3
    ("pink",   "blue",   "yellow", "D"),      # slide 4
    ("blue",   "yellow", "pink",   "D"),      # slide 5
    ("yellow", "D",      "blue",   "D"),      # slide 6
    ("D",      "yellow", "blue",   "D"),      # slide 7
]

# ── Helpers ──────────────────────────────────────────────────────────────────

BASE_CSS = """:root {
  --yellow: #F5C842; --teal: #5ECBA8; --pink: #E87DB0; --blue: #5A8ED4;
  --text: #2B3641; --white: #FFFFFF; --gray-bg: #F4F5F7;
  --gray-mid: #8A95A3; --gray-light: #E8EAED;
}
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html, body { margin: 0; padding: 0; width: 1080px; height: 1080px; overflow: hidden; }
body { font-family: 'Nunito', sans-serif; background: #FFFFFF; }
.circle { border-radius: 50%; position: absolute; }
#canvas { width: 1080px; height: 1080px; background: var(--white); position: relative; overflow: hidden; }"""


def resolve(token, dominant):
    return dominant if token == "D" else token


def circles_css(slide_idx, dominant):
    s = CIRCLE_SIZES[slide_idx]
    c = CIRCLE_COLORS[slide_idx]
    colors = [resolve(x, dominant) for x in c]
    return (
        f"#canvas .c-tl {{ width:{s[0]}px; height:{s[0]}px; background:var(--{colors[0]}); top:{s[4]}px; left:{s[5]}px; }}\n"
        f"#canvas .c-tr {{ width:{s[1]}px; height:{s[1]}px; background:var(--{colors[1]}); top:{s[6]}px; right:{s[7]}px; }}\n"
        f"#canvas .c-bl {{ width:{s[2]}px; height:{s[2]}px; background:var(--{colors[2]}); bottom:{s[8]}px; left:{s[9]}px; }}\n"
        f"#canvas .c-br {{ width:{s[3]}px; height:{s[3]}px; background:var(--{colors[3]}); bottom:{s[10]}px; right:{s[11]}px; }}"
    )


def circles_html():
    return (
        '  <div class="circle c-tl"></div>\n'
        '  <div class="circle c-tr"></div>\n'
        '  <div class="circle c-bl"></div>\n'
        '  <div class="circle c-br"></div>'
    )


def wrap(title, extra_css, body_html, font_href=FONT_HREF):
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<title>{title}</title>
<link rel="stylesheet" href="{font_href}">
<style>
{BASE_CSS}
{extra_css}
</style>
</head>
<body>
<div id="canvas">
{circles_html()}
{body_html}
</div>
</body>
</html>"""


# ── Geradores por tipo ────────────────────────────────────────────────────────

def gen_cover(slide, dominant, idx):
    css = circles_css(idx, dominant) + f"""
#body {{
  position:absolute; inset:0; display:flex; flex-direction:column;
  align-items:center; justify-content:center;
  padding:100px 110px 160px; text-align:center; z-index:2; gap:0;
}}
.eyebrow {{ font-size:22px; font-weight:800; color:var(--{dominant}); letter-spacing:2px; text-transform:uppercase; margin-bottom:36px; }}
.headline {{ font-size:84px; font-weight:900; color:var(--text); line-height:1.0; letter-spacing:-2px; margin-bottom:36px; }}
.headline em {{ font-style:normal; color:var(--{dominant}); }}
.subhead {{ font-size:34px; font-weight:700; color:var(--text); opacity:0.65; line-height:1.35; margin-bottom:64px; }}
.swipe-hint {{ display:flex; align-items:center; gap:12px; font-size:22px; font-weight:800; color:var(--{dominant}); letter-spacing:0.5px; }}
.swipe-hint .arrow {{ display:flex; align-items:center; justify-content:center; width:44px; height:44px; background:var(--{dominant}); border-radius:50%; }}"""

    body = f"""  <div id="body">
    <p class="eyebrow">{slide['eyebrow']}</p>
    <h1 class="headline">{slide['headline']}</h1>
    <p class="subhead">{slide['subhead']}</p>
    <div class="swipe-hint">
      <span>deslize para ver</span>
      <div class="arrow">
        <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
          <path d="M4 10H16M16 10L11 5M16 10L11 15" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </div>
    </div>
  </div>"""
    return wrap("Skolen — Slide Cover", css, body)


def gen_text(slide, dominant, idx):
    rgba = LABEL_RGBA[dominant]
    css = circles_css(idx, dominant) + f"""
#body {{
  position:absolute; inset:0; display:flex; flex-direction:column;
  align-items:center; justify-content:center;
  padding:100px 120px 120px; text-align:center; z-index:2; gap:0;
}}
.label {{ font-size:18px; font-weight:800; color:var(--{dominant}); letter-spacing:2.5px; text-transform:uppercase; margin-bottom:48px; background:{rgba}; padding:10px 24px; border-radius:999px; }}
.headline {{ font-size:78px; font-weight:900; color:var(--text); line-height:1.0; letter-spacing:-2px; margin-bottom:40px; }}
.headline em {{ font-style:normal; color:var(--{dominant}); }}
.body-text {{ font-size:36px; font-weight:700; color:var(--text); opacity:0.65; line-height:1.5; max-width:820px; }}
.body-text strong {{ color:var(--text); opacity:1; font-weight:900; }}"""

    body = f"""  <div id="body">
    <p class="label">{slide['label']}</p>
    <h2 class="headline">{slide['headline']}</h2>
    <p class="body-text">{slide['body']}</p>
  </div>"""
    return wrap("Skolen — Slide Text", css, body)


def gen_number(slide, dominant, idx):
    css = circles_css(idx, dominant) + f"""
#body {{
  position:absolute; inset:0; display:flex; flex-direction:column;
  align-items:center; justify-content:center;
  padding:80px 100px 130px; text-align:center; z-index:2; gap:0;
}}
.label {{ font-size:20px; font-weight:800; color:var(--gray-mid); letter-spacing:2.5px; text-transform:uppercase; margin-bottom:28px; }}
.stat {{ font-size:185px; font-weight:900; color:var(--{dominant}); line-height:0.85; letter-spacing:-6px; margin-bottom:28px; }}
.stat-label {{ font-size:42px; font-weight:800; color:var(--text); line-height:1.2; letter-spacing:-0.5px; margin-bottom:40px; }}
.stat-label em {{ font-style:normal; color:var(--{dominant}); }}
.divider {{ width:80px; height:5px; background:var(--{dominant}); border-radius:3px; margin:0 auto; }}"""

    body = f"""  <div id="body">
    <p class="label">{slide['label']}</p>
    <div class="stat">{slide['stat']}</div>
    <h2 class="stat-label">{slide['stat_label']}</h2>
    <div class="divider"></div>
  </div>"""
    return wrap("Skolen — Slide Number", css, body)


def gen_app(slide, dominant, idx):
    feats = slide.get("features", ["", "", ""])
    feat_colors = [dominant, "yellow", "blue"]

    feat_items = "\n".join(
        f'        <li>\n'
        f'          <span class="feature-dot" style="background:var(--{feat_colors[i]})"></span>\n'
        f'          {feats[i]}\n'
        f'        </li>'
        for i in range(len(feats))
    )

    css = circles_css(idx, dominant) + f"""
#body {{
  position:absolute; inset:0; display:flex; align-items:center; justify-content:center;
  gap:70px; padding:80px 90px 130px; z-index:2;
}}
.left {{ flex:1; display:flex; flex-direction:column; justify-content:center; }}
.eyebrow {{ font-size:20px; font-weight:800; color:var(--{dominant}); letter-spacing:2px; text-transform:uppercase; margin-bottom:24px; }}
.headline {{ font-size:62px; font-weight:900; color:var(--text); line-height:1.05; letter-spacing:-1.5px; margin-bottom:48px; }}
.headline em {{ font-style:normal; color:var(--{dominant}); }}
.feature-list {{ list-style:none; display:flex; flex-direction:column; gap:18px; }}
.feature-list li {{ display:flex; align-items:center; gap:14px; font-size:24px; font-weight:700; color:var(--text); }}
.feature-dot {{ width:12px; height:12px; border-radius:50%; flex-shrink:0; }}
.phone-mockup {{ width:270px; height:490px; background:#1a2630; border-radius:36px; padding:16px 12px; box-shadow:0 32px 80px rgba(0,0,0,0.45); flex-shrink:0; }}
.phone-notch {{ width:80px; height:20px; background:#0d1820; border-radius:10px; margin:0 auto 12px; }}
.phone-screen {{ background:var(--white); border-radius:22px; height:calc(100% - 48px); overflow:hidden; display:flex; flex-direction:column; }}
.phone-topbar {{ background:var(--{dominant}); padding:14px 16px 10px; display:flex; align-items:center; gap:8px; }}
.phone-topbar-logo {{ display:grid; grid-template-columns:1fr 1fr; gap:2px; width:18px; height:18px; }}
.phone-topbar-logo span {{ display:block; border-radius:50%; }}
.phone-topbar-text {{ font-size:11px; font-weight:900; color:var(--white); }}
.phone-tabs {{ display:flex; border-bottom:2px solid var(--gray-light); background:var(--white); }}
.phone-tab {{ flex:1; padding:8px 4px; font-size:8px; font-weight:800; text-align:center; color:var(--gray-mid); }}
.phone-tab.active {{ color:var(--{dominant}); border-bottom:2px solid var(--{dominant}); margin-bottom:-2px; }}
.phone-content {{ flex:1; padding:12px 10px; display:flex; flex-direction:column; gap:8px; }}
.phone-card {{ background:var(--gray-bg); border-radius:8px; padding:10px; display:flex; align-items:center; gap:8px; }}
.phone-card-dot {{ width:10px; height:10px; border-radius:50%; flex-shrink:0; }}
.phone-card-lines {{ flex:1; display:flex; flex-direction:column; gap:4px; }}
.phone-line {{ height:5px; border-radius:3px; background:var(--gray-light); }}
.phone-line.short {{ width:60%; }}
.phone-notif {{ background:var(--{dominant}); border-radius:6px; padding:8px 10px; display:flex; align-items:center; gap:6px; }}
.phone-notif-icon {{ width:14px; height:14px; background:rgba(255,255,255,0.3); border-radius:50%; }}
.phone-notif-text {{ flex:1; display:flex; flex-direction:column; gap:3px; }}
.phone-notif-text .pl1 {{ height:4px; background:rgba(255,255,255,0.7); border-radius:2px; }}
.phone-notif-text .pl2 {{ height:4px; width:70%; background:rgba(255,255,255,0.4); border-radius:2px; }}"""

    body = f"""  <div id="body">
    <div class="left">
      <p class="eyebrow">{slide['eyebrow']}</p>
      <h2 class="headline">{slide['headline']}</h2>
      <ul class="feature-list">
{feat_items}
      </ul>
    </div>
    <div class="phone-mockup">
      <div class="phone-notch"></div>
      <div class="phone-screen">
        <div class="phone-topbar">
          <div class="phone-topbar-logo">
            <span style="background:var(--yellow)"></span><span style="background:var(--teal)"></span>
            <span style="background:var(--pink)"></span><span style="background:var(--blue)"></span>
          </div>
          <span class="phone-topbar-text">Skolen</span>
        </div>
        <div class="phone-tabs">
          <div class="phone-tab active">Risco</div>
          <div class="phone-tab">Alunos</div>
          <div class="phone-tab">Relatório</div>
        </div>
        <div class="phone-content">
          <div class="phone-notif">
            <div class="phone-notif-icon"></div>
            <div class="phone-notif-text"><div class="pl1"></div><div class="pl2"></div></div>
          </div>
          <div class="phone-card"><span class="phone-card-dot" style="background:var(--{dominant})"></span><div class="phone-card-lines"><div class="phone-line" style="background:var(--{dominant});opacity:0.5"></div><div class="phone-line short"></div></div></div>
          <div class="phone-card"><span class="phone-card-dot" style="background:var(--yellow)"></span><div class="phone-card-lines"><div class="phone-line" style="background:var(--yellow);opacity:0.5"></div><div class="phone-line short"></div></div></div>
          <div class="phone-card"><span class="phone-card-dot" style="background:var(--pink)"></span><div class="phone-card-lines"><div class="phone-line" style="background:var(--pink);opacity:0.4"></div><div class="phone-line short"></div></div></div>
          <div class="phone-card"><span class="phone-card-dot" style="background:var(--blue)"></span><div class="phone-card-lines"><div class="phone-line" style="background:var(--blue);opacity:0.4"></div><div class="phone-line short"></div></div></div>
        </div>
      </div>
    </div>
  </div>"""
    return wrap("Skolen — Slide App", css, body)


def gen_cta(slide, dominant, idx):
    css = circles_css(idx, dominant) + f"""
#body {{
  position:absolute; inset:0; display:flex; flex-direction:column;
  align-items:center; justify-content:center;
  padding:100px 110px 140px; text-align:center; z-index:2; gap:0;
}}
.big-logo-mark {{ display:grid; grid-template-columns:1fr 1fr; gap:10px; width:88px; height:88px; margin-bottom:44px; }}
.big-logo-mark span {{ display:block; border-radius:50%; width:39px; height:39px; }}
.eyebrow {{ font-size:22px; font-weight:800; color:var(--{dominant}); letter-spacing:2.5px; text-transform:uppercase; margin-bottom:32px; }}
.headline {{ font-size:78px; font-weight:900; color:var(--text); line-height:1.0; letter-spacing:-2px; margin-bottom:32px; }}
.headline em {{ font-style:normal; color:var(--{dominant}); }}
.subhead {{ font-size:32px; font-weight:700; color:var(--text); opacity:0.6; line-height:1.3; margin-bottom:64px; }}
.cta-btn {{ background:var(--{dominant}); color:var(--white); font-family:'Nunito',sans-serif; font-size:30px; font-weight:900; padding:24px 64px; border-radius:999px; border:none; box-shadow:0 16px 40px rgba(43,54,65,0.20); letter-spacing:-0.3px; cursor:pointer; }}
#logo {{ position:absolute; bottom:52px; left:0; right:0; display:flex; align-items:center; justify-content:center; gap:14px; z-index:3; }}
.logo-text {{ font-size:36px; font-weight:900; color:var(--text); letter-spacing:-0.5px; }}
.lm {{ display:grid; grid-template-columns:1fr 1fr; gap:4px; width:40px; height:40px; }}
.lm span {{ display:block; border-radius:50%; width:17px; height:17px; }}"""

    body = f"""  <div id="body">
    <div class="big-logo-mark">
      <span style="background:var(--yellow)"></span><span style="background:var(--teal)"></span>
      <span style="background:var(--pink)"></span><span style="background:var(--blue)"></span>
    </div>
    <p class="eyebrow">{slide['eyebrow']}</p>
    <h2 class="headline">{slide['headline']}</h2>
    <p class="subhead">{slide['subhead']}</p>
    <button class="cta-btn">{slide['button']}</button>
  </div>
  <div id="logo">
    <div class="lm">
      <span style="background:var(--yellow)"></span><span style="background:var(--teal)"></span>
      <span style="background:var(--pink)"></span><span style="background:var(--blue)"></span>
    </div>
    <span class="logo-text">Skolen</span>
  </div>"""
    return wrap("Skolen — Slide CTA", css, body)


GENERATORS = {
    "cover":  gen_cover,
    "text":   gen_text,
    "number": gen_number,
    "app":    gen_app,
    "cta":    gen_cta,
}

FILENAMES = [
    "slide-01-cover.html",
    "slide-02-text.html",
    "slide-03-number.html",
    "slide-04-app.html",
    "slide-05-text.html",
    "slide-06-number.html",
    "slide-07-cta.html",
]

# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print("Uso: python generate_carousel.py <pasta_do_post>/config.json")
        sys.exit(1)

    config_path = Path(sys.argv[1])
    if not config_path.exists():
        print(f"Arquivo não encontrado: {config_path}")
        sys.exit(1)

    with open(config_path, encoding="utf-8") as f:
        cfg = json.load(f)

    pasta     = Path(cfg["pasta"])
    dominant  = cfg["cor_dominante"]
    slides    = cfg["slides"]

    if dominant not in HEX:
        print(f"cor_dominante inválida: '{dominant}'. Use: teal | pink | yellow | blue")
        sys.exit(1)

    if len(slides) != 7:
        print(f"Esperado 7 slides, encontrado {len(slides)}")
        sys.exit(1)

    pasta.mkdir(parents=True, exist_ok=True)
    pronto = pasta / "pronto"
    pronto.mkdir(exist_ok=True)

    print(f"Gerando carrossel em '{pasta}' (dominante: {dominant})\n")

    for i, (slide, filename) in enumerate(zip(slides, FILENAMES)):
        tipo = slide.get("tipo")
        gen  = GENERATORS.get(tipo)
        if not gen:
            print(f"  ERRO slide {i+1}: tipo '{tipo}' desconhecido")
            sys.exit(1)

        html  = gen(slide, dominant, i)
        fpath = pasta / filename
        fpath.write_text(html, encoding="utf-8")
        print(f"  HTML  {filename}")

    print()

    # Converter para PNG via Chrome headless
    if not Path(CHROME).exists():
        print(f"Chrome não encontrado em: {CHROME}")
        print("HTMLs gerados. Converta manualmente.")
        return

    for i, filename in enumerate(FILENAMES):
        html_path = (pasta / filename).resolve()
        png_path  = (pronto / f"slide-0{i+1}.png").resolve()
        url       = html_path.as_uri()

        subprocess.run(
            [CHROME, "--headless=new", f"--screenshot={png_path}",
             "--window-size=1080,1080", "--hide-scrollbars", "--disable-gpu", url],
            capture_output=True
        )
        print(f"  PNG   slide-0{i+1}.png")

    print(f"\nConcluído. 7 slides em '{pronto}'")


if __name__ == "__main__":
    main()
