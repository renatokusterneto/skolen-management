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
    slide_idx = slide_idx % len(CIRCLE_SIZES)
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

def br_to_spans(text):
    """Converte <br> em <span display:block> para forçar quebra de linha exata."""
    parts = text.split("<br>")
    if len(parts) == 1:
        return text
    return "".join(f'<span style="display:block">{p}</span>' for p in parts)


def gen_cover(slide, dominant, idx):
    headline_html = br_to_spans(slide['headline'])
    css = circles_css(idx, dominant) + f"""
#body {{
  position:absolute; inset:0; display:flex; flex-direction:column;
  align-items:center; justify-content:center;
  padding:100px 110px 160px; text-align:center; z-index:2; gap:0;
}}
.eyebrow {{ font-size:22px; font-weight:800; color:var(--{dominant}); letter-spacing:2px; text-transform:uppercase; margin-bottom:36px; }}
.headline {{ font-size:72px; font-weight:900; color:var(--text); line-height:1.1; letter-spacing:-2px; margin-bottom:36px; }}
.headline em {{ font-style:normal; color:var(--{dominant}); }}
.subhead {{ font-size:34px; font-weight:700; color:var(--text); opacity:0.65; line-height:1.35; margin-bottom:64px; }}
.swipe-hint {{ display:flex; align-items:center; gap:12px; font-size:22px; font-weight:800; color:var(--{dominant}); letter-spacing:0.5px; }}
.swipe-hint .arrow {{ display:flex; align-items:center; justify-content:center; width:44px; height:44px; background:var(--{dominant}); border-radius:50%; }}"""

    body = f"""  <div id="body">
    <p class="eyebrow">{slide['eyebrow']}</p>
    <h1 class="headline">{headline_html}</h1>
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


def gen_cover_dm(slide, dominant, idx):
    """Cover DM — reproduz o sticker de "resposta" de pergunta do Instagram Stories:
    barra escura no topo com a pergunta-isca da Skolen, colada a uma caixa branca
    maior abaixo com a pergunta do gestor (simulando a resposta de um seguidor).
    Campo opcional `imagem`: se presente e o arquivo existir, vira o fundo full-bleed
    do slide (como um Story real), com um overlay escuro para dar contraste ao sticker.
    Formato "Pergunta que todo gestor já se fez"."""
    headline_html = br_to_spans(slide['headline'])
    prompt = slide.get('prompt', 'Pergunte algo sobre sua escola')
    img_uri = resolve_img_uri(slide.get("imagem", ""))

    bg_css = ""
    bg_html = ""
    body_extra_css = ""
    if img_uri:
        bg_css = f"""
#bg-photo {{ position:absolute; inset:0; z-index:0; }}
#bg-photo img {{ width:100%; height:100%; object-fit:cover; object-position:center top; }}
#bg-overlay {{ position:absolute; inset:0; z-index:1; background:linear-gradient(180deg, rgba(0,0,0,0.15) 0%, rgba(0,0,0,0.45) 100%); }}"""
        bg_html = f'  <div id="bg-photo"><img src="{img_uri}" alt=""></div>\n  <div id="bg-overlay"></div>'
        body_extra_css = "\n.swipe-hint { color:#FFFFFF !important; }\n.swipe-hint .arrow { background:#FFFFFF !important; }\n.swipe-hint .arrow path { stroke:#1A1A1A !important; }"

    css = circles_css(idx, dominant) + f"""
#body {{
  position:absolute; inset:0; display:flex; flex-direction:column;
  align-items:center; justify-content:center;
  padding:100px 90px 140px; text-align:center; z-index:2; gap:0;
}}
.dm-sticker {{
  width:100%; max-width:620px; border-radius:24px; overflow:hidden;
  box-shadow:0 20px 50px rgba(43,54,65,0.16);
  margin-bottom:64px;
  font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
}}
.dm-prompt {{
  background:#3A3A3A; padding:24px 32px; font-size:22px; font-weight:600;
  color:#FFFFFF; line-height:1.35;
}}
.dm-answer {{
  background:#FFFFFF; padding:36px 32px;
}}
.dm-headline {{ font-size:36px; font-weight:700; color:#1A1A1A; line-height:1.25; letter-spacing:-0.3px; }}
.dm-headline em {{ font-style:normal; color:var(--{dominant}); }}
.swipe-hint {{ display:flex; align-items:center; gap:12px; font-size:22px; font-weight:800; color:var(--{dominant}); letter-spacing:0.5px; }}
.swipe-hint .arrow {{ display:flex; align-items:center; justify-content:center; width:44px; height:44px; background:var(--{dominant}); border-radius:50%; }}{bg_css}{body_extra_css}"""

    body = f"""{bg_html}
  <div id="body">
    <div class="dm-sticker">
      <div class="dm-prompt">{prompt}</div>
      <div class="dm-answer">
        <h1 class="dm-headline">{headline_html}</h1>
      </div>
    </div>
    <div class="swipe-hint">
      <span>deslize para ver</span>
      <div class="arrow">
        <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
          <path d="M4 10H16M16 10L11 5M16 10L11 15" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </div>
    </div>
  </div>"""
    return wrap("Skolen — Slide Cover DM", css, body)


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
    <h2 class="stat-label">{br_to_spans(slide['stat_label'])}</h2>
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
    <h2 class="headline">{br_to_spans(slide['headline'])}</h2>
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


def gen_afirmacao(slide, dominant, idx):
    """Afirmação grande — headline XL sem body, para quebra de crença ou estado desejado."""
    rgba = LABEL_RGBA[dominant]
    css = circles_css(idx, dominant) + f"""
#body {{
  position:absolute; inset:0; display:flex; flex-direction:column;
  align-items:center; justify-content:center;
  padding:80px 100px 120px; text-align:center; z-index:2; gap:0;
}}
.label {{ font-size:18px; font-weight:800; color:var(--{dominant}); letter-spacing:2.5px; text-transform:uppercase; margin-bottom:48px; background:{rgba}; padding:10px 24px; border-radius:999px; }}
.headline {{ font-size:76px; font-weight:900; color:var(--text); line-height:1.0; letter-spacing:-2px; margin-bottom:0; }}
.headline em {{ font-style:normal; color:var(--{dominant}); }}
.accent-bar {{ width:100px; height:6px; background:var(--{dominant}); border-radius:3px; margin:52px auto 0; }}"""

    body = f"""  <div id="body">
    <p class="label">{slide['label']}</p>
    <h2 class="headline">{br_to_spans(slide['headline'])}</h2>
    <div class="accent-bar"></div>
  </div>"""
    return wrap("Skolen — Slide Afirmação", css, body)


def gen_citacao(slide, dominant, idx):
    """Citação — depoimento ou frase de gestor com avatar e cargo."""
    css = circles_css(idx, dominant) + f"""
#body {{
  position:absolute; inset:0; display:flex; flex-direction:column;
  align-items:center; justify-content:center;
  padding:80px 100px 130px; text-align:center; z-index:2; gap:0;
}}
.label {{ font-size:18px; font-weight:800; color:var(--{dominant}); letter-spacing:2.5px; text-transform:uppercase; margin-bottom:48px; }}
.quote-mark {{ font-size:180px; font-weight:900; color:var(--{dominant}); opacity:0.15; line-height:0.7; margin-bottom:-20px; }}
.quote-text {{ font-size:52px; font-weight:800; color:var(--text); line-height:1.15; letter-spacing:-1px; margin-bottom:48px; }}
.quote-text em {{ font-style:normal; color:var(--{dominant}); }}
.author-row {{ display:flex; align-items:center; justify-content:center; gap:20px; }}
.avatar {{ width:64px; height:64px; border-radius:50%; background:linear-gradient(135deg, var(--{dominant}), var(--blue)); flex-shrink:0; }}
.author-info {{ text-align:left; }}
.author-name {{ font-size:22px; font-weight:900; color:var(--text); }}
.author-role {{ font-size:18px; font-weight:600; color:#8A95A3; }}"""

    body = f"""  <div id="body">
    <p class="label">{slide.get('label', 'Perspectiva do gestor')}</p>
    <div class="quote-mark">"</div>
    <p class="quote-text">{slide['quote']}</p>
    <div class="author-row">
      <div class="avatar"></div>
      <div class="author-info">
        <div class="author-name">{slide.get('author_name', 'Diretora Escolar')}</div>
        <div class="author-role">{slide.get('author_role', 'Escola de Inglês')}</div>
      </div>
    </div>
  </div>"""
    return wrap("Skolen — Slide Citação", css, body)


def gen_checklist(slide, dominant, idx):
    """Checklist — lista de 3–5 itens com ícone de check, para frameworks de lista."""
    rgba = LABEL_RGBA[dominant]
    items = slide.get("items", [])
    item_rows = "\n".join(
        f'        <li>\n'
        f'          <span class="check-icon" style="background:var(--{dominant})">'
        f'<svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M2 7L5.5 10.5L12 3.5" stroke="white" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
        f'</span>\n'
        f'          <span>{it}</span>\n'
        f'        </li>'
        for it in items
    )
    css = circles_css(idx, dominant) + f"""
#body {{
  position:absolute; inset:0; display:flex; flex-direction:column;
  align-items:center; justify-content:center;
  padding:80px 110px 120px; z-index:2; gap:0; text-align:left;
}}
.label {{ font-size:18px; font-weight:800; color:var(--{dominant}); letter-spacing:2.5px; text-transform:uppercase; margin-bottom:16px; background:{rgba}; padding:10px 24px; border-radius:999px; align-self:flex-start; }}
.headline {{ font-size:64px; font-weight:900; color:var(--text); line-height:1.0; letter-spacing:-2px; margin-bottom:52px; }}
.headline em {{ font-style:normal; color:var(--{dominant}); }}
.check-list {{ list-style:none; display:flex; flex-direction:column; gap:24px; width:100%; }}
.check-list li {{ display:flex; align-items:center; gap:20px; font-size:32px; font-weight:700; color:var(--text); line-height:1.2; }}
.check-icon {{ width:36px; height:36px; border-radius:50%; display:flex; align-items:center; justify-content:center; flex-shrink:0; }}"""

    body = f"""  <div id="body">
    <p class="label">{slide['label']}</p>
    <h2 class="headline">{slide['headline']}</h2>
    <ul class="check-list">
{item_rows}
    </ul>
  </div>"""
    return wrap("Skolen — Slide Checklist", css, body)


def gen_grafico_barras(slide, dominant, idx):
    """Gráfico de barras — até 6 barras com rótulo e valor, para mostrar comparação ou evolução."""
    bars = slide.get("bars", [])
    max_val = max((b.get("value", 0) for b in bars), default=1)

    bar_items = []
    for b in bars:
        pct = round((b.get("value", 0) / max_val) * 100)
        label_color = f"var(--{dominant})" if b.get("destaque") else "var(--gray-mid)"
        bar_items.append(
            f'        <div class="bar-col">\n'
            f'          <div class="bar-value" style="color:{label_color}">{b.get("label_val", "")}</div>\n'
            f'          <div class="bar-wrap"><div class="bar-fill" style="height:{pct}%;background:var(--{dominant if b.get("destaque") else "gray-light"})"></div></div>\n'
            f'          <div class="bar-label">{b.get("label", "")}</div>\n'
            f'        </div>'
        )

    css = circles_css(idx, dominant) + f"""
#body {{
  position:absolute; inset:0; display:flex; flex-direction:column;
  align-items:center; justify-content:center;
  padding:80px 90px 120px; z-index:2; gap:0; text-align:center;
}}
.label {{ font-size:18px; font-weight:800; color:#8A95A3; letter-spacing:2.5px; text-transform:uppercase; margin-bottom:24px; }}
.headline {{ font-size:60px; font-weight:900; color:var(--text); line-height:1.05; letter-spacing:-1.5px; margin-bottom:56px; }}
.headline em {{ font-style:normal; color:var(--{dominant}); }}
.chart {{ display:flex; align-items:flex-end; justify-content:center; gap:24px; width:100%; height:320px; }}
.bar-col {{ display:flex; flex-direction:column; align-items:center; gap:10px; flex:1; max-width:110px; height:100%; }}
.bar-value {{ font-size:24px; font-weight:900; color:var(--{dominant}); min-height:32px; }}
.bar-wrap {{ flex:1; width:100%; display:flex; align-items:flex-end; }}
.bar-fill {{ width:100%; border-radius:10px 10px 0 0; min-height:8px; transition:height 0.3s; }}
.bar-label {{ font-size:18px; font-weight:700; color:#8A95A3; text-align:center; line-height:1.2; }}"""

    body = f"""  <div id="body">
    <p class="label">{slide.get('label', '')}</p>
    <h2 class="headline">{slide['headline']}</h2>
    <div class="chart">
{''.join(bar_items)}
    </div>
  </div>"""
    return wrap("Skolen — Slide Gráfico de Barras", css, body)


def gen_calendario(slide, dominant, idx):
    """Calendário anual — 12 meses com meses críticos destacados (Feature 2 assinatura visual)."""
    meses_criticos = set(slide.get("meses_criticos", []))
    meses = ["Jan","Fev","Mar","Abr","Mai","Jun","Jul","Ago","Set","Out","Nov","Dez"]
    mes_items = []
    for i, m in enumerate(meses):
        n = i + 1
        if n in meses_criticos:
            mes_items.append(
                f'<div class="mes critico"><span class="mes-nome">{m}</span>'
                f'<span class="mes-icone">⚠</span></div>'
            )
        else:
            mes_items.append(f'<div class="mes"><span class="mes-nome">{m}</span></div>')

    css = circles_css(idx, dominant) + f"""
#body {{
  position:absolute; inset:0; display:flex; flex-direction:column;
  align-items:center; justify-content:center;
  padding:70px 90px 110px; z-index:2; gap:0; text-align:center;
}}
.label {{ font-size:18px; font-weight:800; color:#8A95A3; letter-spacing:2.5px; text-transform:uppercase; margin-bottom:24px; }}
.headline {{ font-size:58px; font-weight:900; color:var(--text); line-height:1.05; letter-spacing:-1.5px; margin-bottom:48px; }}
.headline em {{ font-style:normal; color:var(--{dominant}); }}
.cal {{ display:grid; grid-template-columns:repeat(6,1fr); gap:16px; width:100%; }}
.mes {{ display:flex; flex-direction:column; align-items:center; justify-content:center; gap:6px; background:#F4F5F7; border-radius:16px; padding:18px 8px; }}
.mes.critico {{ background:var(--{dominant}); }}
.mes-nome {{ font-size:22px; font-weight:800; color:#8A95A3; }}
.mes.critico .mes-nome {{ color:#fff; }}
.mes-icone {{ font-size:16px; }}
.legenda {{ margin-top:28px; display:flex; align-items:center; gap:12px; font-size:20px; font-weight:700; color:#8A95A3; }}
.leg-dot {{ width:18px; height:18px; border-radius:50%; background:var(--{dominant}); }}"""

    body = f"""  <div id="body">
    <p class="label">{slide.get('label', 'Sazonalidade de Risco')}</p>
    <h2 class="headline">{slide['headline']}</h2>
    <div class="cal">{''.join(mes_items)}</div>
    <div class="legenda"><div class="leg-dot"></div><span>{slide.get('legenda', 'Meses de maior risco de evasão')}</span></div>
  </div>"""
    return wrap("Skolen — Slide Calendário", css, body)


def gen_antes_depois(slide, dominant, idx):
    """Antes/depois — dois blocos lado a lado mostrando estado ruim vs estado desejado."""
    css = circles_css(idx, dominant) + f"""
#body {{
  position:absolute; inset:0; display:flex; flex-direction:column;
  align-items:center; justify-content:center;
  padding:70px 80px 110px; z-index:2; gap:0; text-align:center;
}}
.label {{ font-size:18px; font-weight:800; color:#8A95A3; letter-spacing:2.5px; text-transform:uppercase; margin-bottom:32px; }}
.headline {{ font-size:54px; font-weight:900; color:var(--text); line-height:1.05; letter-spacing:-1.5px; margin-bottom:44px; }}
.headline em {{ font-style:normal; color:var(--{dominant}); }}
.cols {{ display:flex; gap:24px; width:100%; }}
.col {{ flex:1; border-radius:24px; padding:40px 32px; display:flex; flex-direction:column; gap:16px; text-align:left; }}
.col-antes {{ background:#F4F5F7; border:2px solid #E8EAED; }}
.col-depois {{ background:var(--{dominant}); }}
.col-tag {{ font-size:14px; font-weight:900; letter-spacing:2px; text-transform:uppercase; margin-bottom:4px; }}
.col-antes .col-tag {{ color:#8A95A3; }}
.col-depois .col-tag {{ color:rgba(255,255,255,0.7); }}
.col-item {{ font-size:26px; font-weight:700; line-height:1.3; }}
.col-antes .col-item {{ color:#2B3641; }}
.col-depois .col-item {{ color:#fff; }}
.col-item::before {{ content:""; }}"""

    antes_items = "".join(
        f'<p class="col-item">✗ {it}</p>' for it in slide.get("antes", [])
    )
    depois_items = "".join(
        f'<p class="col-item">✓ {it}</p>' for it in slide.get("depois", [])
    )

    body = f"""  <div id="body">
    <p class="label">{slide.get('label', 'A diferença')}</p>
    <h2 class="headline">{slide['headline']}</h2>
    <div class="cols">
      <div class="col col-antes">
        <p class="col-tag">Sem Skolen</p>
        {antes_items}
      </div>
      <div class="col col-depois">
        <p class="col-tag">Com Skolen</p>
        {depois_items}
      </div>
    </div>
  </div>"""
    return wrap("Skolen — Slide Antes/Depois", css, body)


def gen_foto_card(slide, dominant, idx):
    """Foto card — imagem (pessoa, produto, print ou marca) ao lado do texto.
    Posição: 'esquerda' (padrão) ou 'direita'.
    imagem_tipo: 'pessoa' | 'produto' | 'print-anotado' | 'marca'
    Se imagem ausente/não encontrado → placeholder visual de marca.
    """
    rgba = LABEL_RGBA[dominant]
    posicao = slide.get("posicao", "esquerda")
    img_tipo = slide.get("imagem_tipo", "produto")
    img_uri = resolve_img_uri(slide.get("imagem", ""))

    # Estilos do bloco de imagem por tipo
    if img_tipo == "pessoa":
        img_block_css = f"""
.img-frame {{
  width: 340px; height: 340px; border-radius: 50%; overflow: hidden; flex-shrink: 0;
  border: 8px solid var(--{dominant}); box-shadow: 0 20px 60px rgba(43,54,65,0.18);
}}"""
        img_frame_style = "border-radius:50%;"
    elif img_tipo == "print-anotado":
        img_block_css = f"""
.img-frame {{
  width: 340px; height: 380px; border-radius: 20px; overflow: hidden; flex-shrink: 0;
  box-shadow: 0 24px 64px rgba(43,54,65,0.22);
  border: 3px solid var(--{dominant});
  position: relative;
}}
.img-badge {{
  position: absolute; top: -12px; right: -12px;
  background: var(--{dominant}); color: #fff;
  font-size: 13px; font-weight: 900; padding: 6px 14px; border-radius: 999px;
  letter-spacing: 1px; text-transform: uppercase;
}}"""
        img_frame_style = ""
    elif img_tipo == "marca":
        img_block_css = f"""
.img-frame {{
  width: 300px; height: 300px; border-radius: 24px; overflow: hidden; flex-shrink: 0;
  background: var(--gray-bg);
  display: flex; align-items: center; justify-content: center;
}}"""
        img_frame_style = "object-fit:contain; padding:24px;"
    else:  # produto (padrão) — sem frame, imagem flutua com drop-shadow
        img_block_css = f"""
.img-frame {{
  width: 400px; height: 440px; flex-shrink: 0; overflow: visible;
  display: flex; align-items: center; justify-content: center;
}}"""
        img_frame_style = "max-width:100%;max-height:100%;object-fit:contain;filter:drop-shadow(0 20px 40px rgba(43,54,65,0.18));"

    # Conteúdo do bloco de imagem: foto real ou placeholder
    if img_uri:
        img_content = f'<img src="{img_uri}" style="width:100%;height:100%;object-fit:cover;{img_frame_style}" alt="">'
        if img_tipo == "print-anotado":
            img_content += '<div class="img-badge">Destaque</div>'
    else:
        # Placeholder: grid de bolinhas de marca
        img_content = f"""
<div style="width:100%;height:100%;display:flex;align-items:center;justify-content:center;background:#F4F5F7;">
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;width:120px;height:120px;">
    <span style="display:block;border-radius:50%;background:var(--yellow);width:52px;height:52px;"></span>
    <span style="display:block;border-radius:50%;background:var(--teal);width:52px;height:52px;"></span>
    <span style="display:block;border-radius:50%;background:var(--pink);width:52px;height:52px;"></span>
    <span style="display:block;border-radius:50%;background:var(--blue);width:52px;height:52px;"></span>
  </div>
</div>"""

    # Layout: flex-direction depende da posição
    flex_direction = "row" if posicao == "esquerda" else "row-reverse"

    css = circles_css(idx, dominant) + img_block_css + f"""
#body {{
  position:absolute; inset:0; display:flex; align-items:center;
  flex-direction: {flex_direction};
  gap: 48px; padding: 72px 72px 120px; z-index:2;
}}
.text-side {{
  flex:1; display:flex; flex-direction:column; justify-content:center;
  text-align:left;
}}
.label {{ font-size:16px; font-weight:800; color:var(--{dominant}); letter-spacing:2.5px;
  text-transform:uppercase; margin-bottom:20px; background:{rgba};
  padding:8px 20px; border-radius:999px; align-self:flex-start; }}
.headline {{ font-size:52px; font-weight:900; color:var(--text); line-height:1.05;
  letter-spacing:-1px; margin-bottom:24px; }}
.headline em {{ font-style:normal; color:var(--{dominant}); }}
.body-text {{ font-size:28px; font-weight:700; color:var(--text); opacity:0.65;
  line-height:1.5; }}
.body-text strong {{ color:var(--text); opacity:1; font-weight:900; }}"""

    body = f"""  <div id="body">
    <div class="img-frame">{img_content}</div>
    <div class="text-side">
      <p class="label">{slide.get('label', '')}</p>
      <h2 class="headline">{slide['headline']}</h2>
      <p class="body-text">{slide.get('body', '')}</p>
    </div>
  </div>"""
    return wrap("Skolen — Slide Foto Card", css, body)


def gen_cta_pergunta(slide, dominant, idx):
    """CTA com pergunta grande — variação do CTA padrão, abre com rhetorical question."""
    css = circles_css(idx, dominant) + f"""
#body {{
  position:absolute; inset:0; display:flex; flex-direction:column;
  align-items:center; justify-content:center;
  padding:100px 110px 140px; text-align:center; z-index:2; gap:0;
}}
.big-logo-mark {{ display:grid; grid-template-columns:1fr 1fr; gap:10px; width:88px; height:88px; margin-bottom:44px; }}
.big-logo-mark span {{ display:block; border-radius:50%; width:39px; height:39px; }}
.pergunta {{ font-size:72px; font-weight:900; color:var(--text); line-height:1.0; letter-spacing:-2px; margin-bottom:32px; }}
.pergunta em {{ font-style:normal; color:var(--{dominant}); }}
.subhead {{ font-size:32px; font-weight:700; color:var(--text); opacity:0.6; line-height:1.3; margin-bottom:64px; }}
.cta-btn {{ background:var(--{dominant}); color:var(--white); font-family:'Nunito',sans-serif; font-size:30px; font-weight:900; padding:24px 64px; border-radius:999px; border:none; box-shadow:0 16px 40px rgba(43,54,65,0.20); cursor:pointer; }}
#logo {{ position:absolute; bottom:52px; left:0; right:0; display:flex; align-items:center; justify-content:center; gap:14px; z-index:3; }}
.logo-text {{ font-size:36px; font-weight:900; color:var(--text); letter-spacing:-0.5px; }}
.lm {{ display:grid; grid-template-columns:1fr 1fr; gap:4px; width:40px; height:40px; }}
.lm span {{ display:block; border-radius:50%; width:17px; height:17px; }}"""

    body = f"""  <div id="body">
    <div class="big-logo-mark">
      <span style="background:var(--yellow)"></span><span style="background:var(--teal)"></span>
      <span style="background:var(--pink)"></span><span style="background:var(--blue)"></span>
    </div>
    <h2 class="pergunta">{br_to_spans(slide['headline'])}</h2>
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
    return wrap("Skolen — Slide CTA Pergunta", css, body)


def resolve_img_uri(img_path_raw):
    """Resolve um caminho de imagem (relativo ou absoluto) para file URI, ou '' se não existir."""
    if not img_path_raw:
        return ""
    p = Path(img_path_raw)
    if not p.is_absolute():
        p = Path("c:/Users/felipe.fadel/skolen-management") / p
    return p.as_uri() if p.exists() else ""


def gen_teste_capa(slide, dominant, idx):
    """Capa do Teste Rápido/Diagnóstico — título do teste + subtítulo/CTA de entrada.
    Campo opcional `imagem`: se presente e o arquivo existir, troca o layout centralizado
    por texto à esquerda + foto flutuante à direita (mesmo tratamento visual do foto-card produto).
    """
    img_uri = resolve_img_uri(slide.get("imagem", ""))

    if img_uri:
        css = circles_css(idx, dominant) + f"""
.img-frame {{ width: 380px; height: 460px; border-radius: 28px; overflow: hidden; flex-shrink: 0;
  box-shadow: 0 24px 64px rgba(43,54,65,0.20); }}
#body {{
  position:absolute; inset:0; display:flex; align-items:center;
  gap:56px; padding:90px 90px 140px; text-align:left; z-index:2;
}}
.text-side {{ flex:1; display:flex; flex-direction:column; justify-content:center; }}
.badge {{ font-size:20px; font-weight:800; color:var(--{dominant}); letter-spacing:2.5px; text-transform:uppercase;
  background:{LABEL_RGBA[dominant]}; padding:12px 28px; border-radius:999px; margin-bottom:32px; align-self:flex-start; }}
.headline {{ font-size:56px; font-weight:900; color:var(--text); line-height:1.1; letter-spacing:-1.5px; margin-bottom:28px; }}
.headline em {{ font-style:normal; color:var(--{dominant}); }}
.subhead {{ font-size:28px; font-weight:700; color:var(--text); opacity:0.65; line-height:1.35; margin-bottom:48px; }}
.swipe-hint {{ display:flex; align-items:center; gap:12px; font-size:20px; font-weight:800; color:var(--{dominant}); letter-spacing:0.5px; }}
.swipe-hint .arrow {{ display:flex; align-items:center; justify-content:center; width:40px; height:40px; background:var(--{dominant}); border-radius:50%; flex-shrink:0; }}"""

        body = f"""  <div id="body">
    <div class="img-frame"><img src="{img_uri}" style="width:100%;height:100%;object-fit:cover;" alt=""></div>
    <div class="text-side">
      <p class="badge">Teste Rápido</p>
      <h1 class="headline">{br_to_spans(slide['headline'])}</h1>
      <p class="subhead">{slide['subhead']}</p>
      <div class="swipe-hint">
        <span>responda deslizando</span>
        <div class="arrow">
          <svg width="18" height="18" viewBox="0 0 20 20" fill="none">
            <path d="M4 10H16M16 10L11 5M16 10L11 15" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </div>
      </div>
    </div>
  </div>"""
        return wrap("Skolen — Teste Capa", css, body)

    css = circles_css(idx, dominant) + f"""
#body {{
  position:absolute; inset:0; display:flex; flex-direction:column;
  align-items:center; justify-content:center;
  padding:100px 110px 160px; text-align:center; z-index:2; gap:0;
}}
.badge {{ font-size:20px; font-weight:800; color:var(--{dominant}); letter-spacing:2.5px; text-transform:uppercase;
  background:{LABEL_RGBA[dominant]}; padding:12px 28px; border-radius:999px; margin-bottom:40px; }}
.headline {{ font-size:68px; font-weight:900; color:var(--text); line-height:1.1; letter-spacing:-2px; margin-bottom:36px; }}
.headline em {{ font-style:normal; color:var(--{dominant}); }}
.subhead {{ font-size:32px; font-weight:700; color:var(--text); opacity:0.65; line-height:1.35; margin-bottom:64px; }}
.swipe-hint {{ display:flex; align-items:center; gap:12px; font-size:22px; font-weight:800; color:var(--{dominant}); letter-spacing:0.5px; }}
.swipe-hint .arrow {{ display:flex; align-items:center; justify-content:center; width:44px; height:44px; background:var(--{dominant}); border-radius:50%; }}"""

    body = f"""  <div id="body">
    <p class="badge">Teste Rápido</p>
    <h1 class="headline">{br_to_spans(slide['headline'])}</h1>
    <p class="subhead">{slide['subhead']}</p>
    <div class="swipe-hint">
      <span>responda deslizando</span>
      <div class="arrow">
        <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
          <path d="M4 10H16M16 10L11 5M16 10L11 15" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </div>
    </div>
  </div>"""
    return wrap("Skolen — Teste Capa", css, body)


def gen_teste_pergunta(slide, dominant, idx, num, total):
    """Slide de pergunta do Teste Rápido/Diagnóstico — pílulas fixas Sim/Não, numeração X/N."""
    css = circles_css(idx, dominant) + f"""
#body {{
  position:absolute; inset:0; display:flex; flex-direction:column;
  align-items:center; justify-content:center;
  padding:90px 110px 140px; text-align:center; z-index:2; gap:0;
}}
.progress {{ font-size:20px; font-weight:900; color:var(--gray-mid); letter-spacing:2px; margin-bottom:44px; }}
.progress em {{ font-style:normal; color:var(--{dominant}); }}
.headline {{ font-size:58px; font-weight:900; color:var(--text); line-height:1.2; letter-spacing:-1.5px; margin-bottom:72px; }}
.pills {{ display:flex; gap:28px; }}
.pill {{ font-size:30px; font-weight:900; padding:24px 72px; border-radius:999px; }}
.pill-sim {{ background:var(--{dominant}); color:var(--white); }}
.pill-nao {{ background:var(--gray-bg); color:var(--text); border:2px solid var(--gray-light); }}"""

    body = f"""  <div id="body">
    <p class="progress">Pergunta <em>{num}</em>/{total}</p>
    <h2 class="headline">{br_to_spans(slide['headline'])}</h2>
    <div class="pills">
      <div class="pill pill-sim">Sim</div>
      <div class="pill pill-nao">Não</div>
    </div>
  </div>"""
    return wrap("Skolen — Teste Pergunta", css, body)


def gen_teste_resultado(slide, dominant, idx):
    """Resultado do Teste Rápido/Diagnóstico — critério do placar, frase de diagnóstico,
    barra de risco contínua com marcador proporcional ao número de perguntas."""
    segmentos = max(int(slide.get("segmentos", 1)), 0)
    total_segmentos = max(int(slide.get("segmentos_total", 5)), 1)
    pct = round((segmentos / total_segmentos) * 100)

    css = circles_css(idx, dominant) + f"""
#body {{
  position:absolute; inset:0; display:flex; flex-direction:column;
  align-items:center; justify-content:center;
  padding:90px 100px 130px; text-align:center; z-index:2; gap:0;
}}
.label {{ font-size:20px; font-weight:800; color:var(--gray-mid); letter-spacing:2.5px; text-transform:uppercase; margin-bottom:28px; }}
.criterio {{ font-size:32px; font-weight:800; color:var(--{dominant}); margin-bottom:36px; }}
.headline {{ font-size:52px; font-weight:900; color:var(--text); line-height:1.25; letter-spacing:-1px; margin-bottom:56px; }}
.headline em {{ font-style:normal; color:var(--{dominant}); }}
.risk-track {{ width:100%; max-width:640px; height:28px; background:var(--gray-bg); border-radius:999px; overflow:hidden; position:relative; margin-bottom:20px; }}
.risk-fill {{ height:100%; width:{pct}%; background:var(--{dominant}); border-radius:999px; }}
.risk-caption {{ font-size:20px; font-weight:700; color:var(--gray-mid); }}"""

    body = f"""  <div id="body">
    <p class="label">Resultado do teste</p>
    <p class="criterio">{slide['criterio']}</p>
    <h2 class="headline">{br_to_spans(slide['headline'])}</h2>
    <div class="risk-track"><div class="risk-fill"></div></div>
    <p class="risk-caption">{segmentos} de {total_segmentos} sinais de risco identificados</p>
  </div>"""
    return wrap("Skolen — Teste Resultado", css, body)


def gen_teste_cta(slide, dominant, idx):
    """CTA final do Teste Rápido/Diagnóstico — frase de virada + botão.
    Campo opcional `imagem`: se presente e o arquivo existir, troca o layout centralizado
    por texto à esquerda + foto/mockup flutuante à direita.
    """
    img_uri = resolve_img_uri(slide.get("imagem", ""))

    if img_uri:
        css = circles_css(idx, dominant) + f"""
.img-frame {{ width: 380px; height: 460px; border-radius: 28px; overflow: hidden; flex-shrink: 0;
  box-shadow: 0 24px 64px rgba(43,54,65,0.20); }}
#body {{
  position:absolute; inset:0; display:flex; align-items:center;
  gap:56px; padding:90px 90px 140px; text-align:left; z-index:2;
}}
.text-side {{ flex:1; display:flex; flex-direction:column; justify-content:center; }}
.big-logo-mark {{ display:grid; grid-template-columns:1fr 1fr; gap:8px; width:64px; height:64px; margin-bottom:32px; }}
.big-logo-mark span {{ display:block; border-radius:50%; width:28px; height:28px; }}
.headline {{ font-size:52px; font-weight:900; color:var(--text); line-height:1.1; letter-spacing:-1.5px; margin-bottom:24px; }}
.headline em {{ font-style:normal; color:var(--{dominant}); }}
.subhead {{ font-size:26px; font-weight:700; color:var(--text); opacity:0.6; line-height:1.3; margin-bottom:44px; }}
.cta-btn {{ background:var(--{dominant}); color:var(--white); font-family:'Nunito',sans-serif; font-size:26px; font-weight:900; padding:20px 48px; border-radius:999px; border:none; box-shadow:0 16px 40px rgba(43,54,65,0.20); letter-spacing:-0.3px; cursor:pointer; align-self:flex-start; }}
#logo {{ position:absolute; bottom:52px; left:0; right:0; display:flex; align-items:center; justify-content:center; gap:14px; z-index:3; }}
.logo-text {{ font-size:36px; font-weight:900; color:var(--text); letter-spacing:-0.5px; }}
.lm {{ display:grid; grid-template-columns:1fr 1fr; gap:4px; width:40px; height:40px; }}
.lm span {{ display:block; border-radius:50%; width:17px; height:17px; }}"""

        body = f"""  <div id="body">
    <div class="img-frame"><img src="{img_uri}" style="width:100%;height:100%;object-fit:cover;" alt=""></div>
    <div class="text-side">
      <div class="big-logo-mark">
        <span style="background:var(--yellow)"></span><span style="background:var(--teal)"></span>
        <span style="background:var(--pink)"></span><span style="background:var(--blue)"></span>
      </div>
      <h2 class="headline">{br_to_spans(slide['headline'])}</h2>
      <p class="subhead">{slide['subhead']}</p>
      <button class="cta-btn">{slide['button']}</button>
    </div>
  </div>
  <div id="logo">
    <div class="lm">
      <span style="background:var(--yellow)"></span><span style="background:var(--teal)"></span>
      <span style="background:var(--pink)"></span><span style="background:var(--blue)"></span>
    </div>
    <span class="logo-text">Skolen</span>
  </div>"""
        return wrap("Skolen — Teste CTA", css, body)

    css = circles_css(idx, dominant) + f"""
#body {{
  position:absolute; inset:0; display:flex; flex-direction:column;
  align-items:center; justify-content:center;
  padding:100px 110px 140px; text-align:center; z-index:2; gap:0;
}}
.big-logo-mark {{ display:grid; grid-template-columns:1fr 1fr; gap:10px; width:88px; height:88px; margin-bottom:44px; }}
.big-logo-mark span {{ display:block; border-radius:50%; width:39px; height:39px; }}
.headline {{ font-size:70px; font-weight:900; color:var(--text); line-height:1.05; letter-spacing:-2px; margin-bottom:32px; }}
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
    <h2 class="headline">{br_to_spans(slide['headline'])}</h2>
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
    return wrap("Skolen — Teste CTA", css, body)


GENERATORS = {
    "cover":          gen_cover,
    "cover-dm":       gen_cover_dm,
    "text":           gen_text,
    "number":         gen_number,
    "app":            gen_app,
    "cta":            gen_cta,
    "afirmacao":      gen_afirmacao,
    "citacao":        gen_citacao,
    "checklist":      gen_checklist,
    "grafico-barras": gen_grafico_barras,
    "calendario":     gen_calendario,
    "antes-depois":   gen_antes_depois,
    "cta-pergunta":   gen_cta_pergunta,
    "foto-card":      gen_foto_card,
    "teste-capa":      gen_teste_capa,
    "teste-resultado": gen_teste_resultado,
    "teste-cta":       gen_teste_cta,
}

# Tipos que usam CIRCLE_SIZES/CIRCLE_COLORS fixos por índice 0-6 (frameworks padrão de 7 slides).
# O template "Teste Rápido/Diagnóstico" tem entre 5 e 7 slides (3 a 5 perguntas + capa + resultado + cta),
# então os círculos são resolvidos ciclando os padrões existentes em vez de exigir exatamente 7.
TESTE_TIPOS = {"teste-capa", "teste-pergunta", "teste-resultado", "teste-cta"}

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

def is_teste_diagnostico(slides):
    tipos = [s.get("tipo") for s in slides]
    return tipos and all(t in TESTE_TIPOS for t in tipos)


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

    teste = is_teste_diagnostico(slides)

    if teste:
        if not (5 <= len(slides) <= 7):
            print(f"Template Teste Rápido/Diagnóstico espera 5 a 7 slides, encontrado {len(slides)}")
            sys.exit(1)
        if slides[0].get("tipo") != "teste-capa" or slides[-1].get("tipo") != "teste-cta":
            print("Template Teste Rápido/Diagnóstico precisa começar em 'teste-capa' e terminar em 'teste-cta'")
            sys.exit(1)
    elif len(slides) != 7:
        print(f"Esperado 7 slides, encontrado {len(slides)}")
        sys.exit(1)

    pasta.mkdir(parents=True, exist_ok=True)
    pronto = pasta / "pronto"
    pronto.mkdir(exist_ok=True)

    print(f"Gerando carrossel em '{pasta}' (dominante: {dominant})\n")

    filenames = FILENAMES if not teste else [
        f"slide-{i+1:02d}-{s.get('tipo')}.html" for i, s in enumerate(slides)
    ]

    total_perguntas = sum(1 for s in slides if s.get("tipo") == "teste-pergunta")
    pergunta_num = 0

    for i, (slide, filename) in enumerate(zip(slides, filenames)):
        tipo = slide.get("tipo")

        if tipo == "teste-pergunta":
            pergunta_num += 1
            html = gen_teste_pergunta(slide, dominant, i, pergunta_num, total_perguntas)
        else:
            gen = GENERATORS.get(tipo)
            if not gen:
                print(f"  ERRO slide {i+1}: tipo '{tipo}' desconhecido")
                sys.exit(1)
            html = gen(slide, dominant, i)

        fpath = pasta / filename
        fpath.write_text(html, encoding="utf-8")
        print(f"  HTML  {filename}")

    print()

    # Converter para PNG via Chrome headless
    if not Path(CHROME).exists():
        print(f"Chrome não encontrado em: {CHROME}")
        print("HTMLs gerados. Converta manualmente.")
        return

    for i, filename in enumerate(filenames):
        html_path = (pasta / filename).resolve()
        png_path  = (pronto / f"slide-{i+1:02d}.png").resolve()
        url       = html_path.as_uri()

        subprocess.run(
            [CHROME, "--headless=new", f"--screenshot={png_path}",
             "--window-size=1080,1080", "--hide-scrollbars", "--disable-gpu", url],
            capture_output=True
        )
        print(f"  PNG   slide-{i+1:02d}.png")

    print(f"\nConcluído. {len(filenames)} slides em '{pronto}'")


if __name__ == "__main__":
    main()
