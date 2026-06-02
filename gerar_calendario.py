import json
from pathlib import Path

with open("cloudinary_urls.json", encoding="utf-8") as f:
    urls = json.load(f)

CALENDAR = [
    # Semana 1 — Seg, Ter, Qui, Sex
    {"date": "19/05/2026", "day": "Segunda", "time": "18h00", "post": "Evasao-09-04",
     "title": "Evasao Escolar", "hook": "Sua escola ja perdeu alunos sem perceber?", "color": "#0D9488"},
    {"date": "20/05/2026", "day": "Terca",   "time": "18h00", "post": "Retencao-Ingles-11-04",
     "title": "Retencao · Ingles", "hook": "Sua escola de ingles vai perder alunos no final do ano.", "color": "#DB2777"},
    {"date": "22/05/2026", "day": "Quinta",  "time": "18h00", "post": "DadosVsVisao-14-05",
     "title": "Dados vs Visao", "hook": "Sua escola tem dados. Mas nao tem visao.", "color": "#CA8A04"},
    {"date": "23/05/2026", "day": "Sexta",   "time": "18h00", "post": "EquipeSemPrioridade-14-05",
     "title": "Equipe sem Prioridade", "hook": "Cada setor ve uma parte. Ninguem ve o todo.", "color": "#1D4ED8"},
    # Semana 2 — Seg, Ter, Qui, Sex
    {"date": "26/05/2026", "day": "Segunda", "time": "18h00", "post": "GestaoPreditiva-14-05",
     "title": "Gestao Preditiva", "hook": "Sua escola ainda reage. Poderia prever.", "color": "#DB2777"},
    {"date": "27/05/2026", "day": "Terca",   "time": "18h00", "post": "IndicacoesPerdidas-14-05",
     "title": "Indicacoes Perdidas", "hook": "O aluno insatisfeito nao indica. Nunca indicou.", "color": "#CA8A04"},
    {"date": "29/05/2026", "day": "Quinta",  "time": "18h00", "post": "Inadimplencia-14-05",
     "title": "Inadimplencia como Sinal", "hook": "Inadimplencia nao e so problema financeiro. E sinal.", "color": "#0D9488"},
    {"date": "30/05/2026", "day": "Sexta",   "time": "18h00", "post": "CustoRetrabalho-14-05",
     "title": "Custo do Retrabalho", "hook": "Sua equipe trabalha muito. Mas no lugar certo?", "color": "#1D4ED8"},
    # Semana 3 — Seg, Ter, Qui, Sex
    {"date": "02/06/2026", "day": "Segunda", "time": "18h00", "post": "EngajamentoRisco-14-05",
     "title": "Engajamento como Risco", "hook": "Frequencia nao e so presenca. E sinal de risco.", "color": "#CA8A04"},
    {"date": "03/06/2026", "day": "Terca",   "time": "18h00", "post": "GestaoPeloFeeling-14-05",
     "title": "Gestao pelo Feeling", "hook": "Intuicao nao e gestao. E risco disfarcado.", "color": "#1D4ED8"},
    {"date": "05/06/2026", "day": "Quinta",  "time": "18h00", "post": "ComunicacaoPais-14-05",
     "title": "Comunicacao com Pais", "hook": "O pai nao sabe. A escola tambem nao fala.", "color": "#0D9488"},
    {"date": "06/06/2026", "day": "Sexta",   "time": "18h00", "post": "EscolasQueCrescem-14-05",
     "title": "Escolas que Crescem", "hook": "Mesma cidade. Mesmo esforco. Uma cresce. A outra nao.", "color": "#DB2777"},
    # Semana 4 — apenas Segunda
    {"date": "09/06/2026", "day": "Segunda", "time": "18h00", "post": "Onboarding90Dias-14-05",
     "title": "Onboarding 90 Dias", "hook": "Os primeiros 90 dias definem quem fica.", "color": "#CA8A04"},
]

WEEK_LABELS = ["Semana 1", "Semana 2", "Semana 3", "Semana 4"]
WEEK_DATES  = ["19–23 maio", "26–30 maio", "02–06 junho", "09 junho"]

def slides_html(post_key, color):
    post_urls = urls.get(post_key, [])
    if not post_urls:
        return "<p style='color:#888'>Sem slides</p>"
    imgs = ""
    for i, u in enumerate(post_urls):
        imgs += f'<img src="{u}" alt="Slide {i+1}" style="width:60px;height:60px;object-fit:cover;border-radius:6px;border:2px solid {color};flex-shrink:0;cursor:pointer;" onclick="openModal(\'{u}\')" title="Slide {i+1}" />'
    return f'<div style="display:flex;gap:6px;flex-wrap:wrap;margin-top:8px;">{imgs}</div>'

def card(entry, num):
    c = entry["color"]
    slides = slides_html(entry["post"], c)
    cloudinary_base = f"https://res.cloudinary.com/dbdtsbrmd/image/upload/skolen/social/{entry['post']}"
    return f'''
    <div style="background:#1a1a2e;border-radius:12px;padding:18px;border-left:4px solid {c};position:relative;transition:transform .15s;" onmouseover="this.style.transform='translateY(-2px)'" onmouseout="this.style.transform='none'">
      <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:10px;">
        <div>
          <span style="background:{c};color:#fff;font-size:11px;font-weight:700;padding:2px 8px;border-radius:20px;text-transform:uppercase;letter-spacing:.5px;">{entry["day"]}</span>
          <span style="background:#0f0f23;color:#aaa;font-size:11px;padding:2px 8px;border-radius:20px;margin-left:4px;">{entry["date"]}</span>
          <span style="background:#0f0f23;color:{c};font-size:11px;font-weight:700;padding:2px 8px;border-radius:20px;margin-left:4px;">&#128337; {entry["time"]}</span>
        </div>
        <span style="color:#555;font-size:12px;">#{num}</span>
      </div>
      <p style="margin:0 0 4px 0;font-weight:700;font-size:14px;color:#fff;">{entry["title"]}</p>
      <p style="margin:0 0 10px 0;font-size:12px;color:#aaa;font-style:italic;">"{entry["hook"]}"</p>
      {slides}
      <div style="margin-top:10px;">
        <a href="{cloudinary_base}/slide-01.png" target="_blank" style="font-size:11px;color:{c};text-decoration:none;border:1px solid {c};padding:3px 10px;border-radius:20px;">Ver no Cloudinary</a>
      </div>
    </div>'''

def week_section(week_idx, entries, offset=0):
    cards = "\n".join(card(e, i + 1 + offset) for i, e in enumerate(entries))
    # week_idx 4 has only 1 post
    grid_cols = f"repeat({len(entries)}, 1fr)"
    return f'''
  <div style="margin-bottom:40px;">
    <div style="display:flex;align-items:center;gap:12px;margin-bottom:16px;">
      <h2 style="margin:0;font-size:16px;color:#fff;font-weight:700;">{WEEK_LABELS[week_idx]}</h2>
      <span style="color:#555;font-size:13px;">{WEEK_DATES[week_idx]}</span>
      <div style="flex:1;height:1px;background:#222;"></div>
      <span style="color:#555;font-size:12px;">{len(entries)} post{"s" if len(entries) > 1 else ""}</span>
    </div>
    <div style="display:grid;grid-template-columns:{grid_cols};gap:14px;">
      {cards}
    </div>
  </div>'''

weeks_data = [
    CALENDAR[0:4],
    CALENDAR[4:8],
    CALENDAR[8:12],
    CALENDAR[12:13],
]

offsets = [0, 4, 8, 12]
weeks_html = "\n".join(week_section(i, w, offsets[i]) for i, w in enumerate(weeks_data))

html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<title>Calendario Editorial · Skolen</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ background: #0f0f23; color: #eee; font-family: 'Segoe UI', system-ui, sans-serif; padding: 32px 24px; }}
  a {{ transition: opacity .15s; }} a:hover {{ opacity: .8; }}
</style>
</head>
<body>

<!-- MODAL -->
<div id="modal" onclick="this.style.display='none'" style="display:none;position:fixed;inset:0;background:rgba(0,0,0,.92);z-index:9999;align-items:center;justify-content:center;">
  <img id="modal-img" src="" style="max-width:90vw;max-height:90vh;border-radius:12px;box-shadow:0 0 60px rgba(0,0,0,.8);" />
</div>

<!-- HEADER -->
<div style="max-width:1100px;margin:0 auto 40px;">
  <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:8px;">
    <div>
      <h1 style="font-size:24px;font-weight:800;color:#fff;">Calendario Editorial</h1>
      <p style="color:#666;font-size:13px;margin-top:4px;">Skolen · Instagram · 19 maio – 09 junho 2026</p>
    </div>
    <div style="text-align:right;">
      <div style="font-size:28px;font-weight:900;color:#fff;">13</div>
      <div style="font-size:11px;color:#666;text-transform:uppercase;letter-spacing:1px;">posts agendados</div>
    </div>
  </div>

  <!-- LEGENDA DIAS -->
  <div style="display:flex;gap:8px;margin-top:16px;flex-wrap:wrap;">
    <div style="background:#1a1a2e;border:1px solid #222;padding:6px 14px;border-radius:20px;font-size:12px;color:#aaa;">
      <b style="color:#fff;">Seg / Ter / Qui / Sex</b> &nbsp;·&nbsp; 18h00
    </div>
    <div style="display:flex;gap:6px;align-items:center;margin-left:auto;">
      <span style="width:10px;height:10px;background:#0D9488;border-radius:50%;display:inline-block;"></span><span style="font-size:12px;color:#aaa;">teal</span>
      <span style="width:10px;height:10px;background:#DB2777;border-radius:50%;display:inline-block;margin-left:8px;"></span><span style="font-size:12px;color:#aaa;">pink</span>
      <span style="width:10px;height:10px;background:#CA8A04;border-radius:50%;display:inline-block;margin-left:8px;"></span><span style="font-size:12px;color:#aaa;">yellow</span>
      <span style="width:10px;height:10px;background:#1D4ED8;border-radius:50%;display:inline-block;margin-left:8px;"></span><span style="font-size:12px;color:#aaa;">blue</span>
    </div>
  </div>
</div>

<!-- SEMANAS -->
<div style="max-width:1100px;margin:0 auto;">
  {weeks_html}
</div>

<!-- TABELA RESUMO -->
<div style="max-width:1100px;margin:48px auto 0;">
  <h2 style="font-size:16px;color:#fff;margin-bottom:16px;">Resumo completo</h2>
  <table style="width:100%;border-collapse:collapse;font-size:13px;">
    <thead>
      <tr style="border-bottom:2px solid #222;">
        <th style="text-align:left;padding:8px 12px;color:#666;">#</th>
        <th style="text-align:left;padding:8px 12px;color:#666;">Data</th>
        <th style="text-align:left;padding:8px 12px;color:#666;">Dia</th>
        <th style="text-align:left;padding:8px 12px;color:#666;">Hora</th>
        <th style="text-align:left;padding:8px 12px;color:#666;">Post</th>
        <th style="text-align:left;padding:8px 12px;color:#666;">Hook</th>
        <th style="text-align:left;padding:8px 12px;color:#666;">Cloudinary</th>
      </tr>
    </thead>
    <tbody>
{''.join(f"""
      <tr style="border-bottom:1px solid #1a1a2e;">
        <td style="padding:10px 12px;color:#555;">{i+1}</td>
        <td style="padding:10px 12px;color:#fff;font-weight:600;">{e["date"]}</td>
        <td style="padding:10px 12px;"><span style="color:{e["color"]};font-weight:600;">{e["day"]}</span></td>
        <td style="padding:10px 12px;color:#aaa;">{e["time"]}</td>
        <td style="padding:10px 12px;color:#fff;">{e["title"]}</td>
        <td style="padding:10px 12px;color:#888;font-style:italic;max-width:280px;">{e["hook"]}</td>
        <td style="padding:10px 12px;">
          <a href="https://res.cloudinary.com/dbdtsbrmd/image/upload/skolen/social/{e['post']}/slide-01.png" target="_blank"
             style="color:{e["color"]};text-decoration:none;font-size:11px;">ver slides</a>
        </td>
      </tr>""" for i, e in enumerate(CALENDAR))}
    </tbody>
  </table>
</div>

<div style="max-width:1100px;margin:32px auto;color:#333;font-size:11px;text-align:center;">
  Gerado em 18/05/2026 · Skolen Marketing
</div>

<script>
function openModal(src) {{
  document.getElementById('modal-img').src = src;
  document.getElementById('modal').style.display = 'flex';
}}
</script>
</body>
</html>
"""

out = Path("calendario-editorial.html")
out.write_text(html, encoding="utf-8")
print(f"Calendario gerado: {out.resolve()}")
