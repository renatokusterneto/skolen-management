"""
heygen_gen_video_cdp.py — gera video no HeyGen via avatar-shots (mesmo fluxo
usado pela propria interface web), com modelo Avatar IV. Metodo alternativo
ao heygen_generate.py (API v3 oficial) — usar quando o resultado do Avatar IV
for visivelmente melhor que o da API publica.

Endpoint real: POST https://api2.heygen.com/v2/avatar/shortcut/submit
Autenticacao: cookies httpOnly via Chrome CDP (sessao logada no profile isolado)

Pre-requisito: rodar heygen_save_session.py uma vez antes (login manual na
conta HeyGen da Skolen). Se o Chrome do profile isolado nao estiver aberto,
este script lanca automaticamente com janela visivel.

Uso:
  python heygen_gen_video_cdp.py \
    --avatar-id "87289bc673fd4be2a0a275b5d11c1598" \
    --input-text "Roteiro que o avatar vai falar... com pausas assim." \
    --title "inadimplencia-gancho-01" \
    --out "../../../Marketing/Social/_video-gerados/inadimplencia-gancho-01.mp4"

Flags:
  --avatar-id            ID do avatar (padrao: avatar da Skolen)
  --voice-id             Voice ID HeyGen (obrigatorio — ver heygen_list_voices.py)
  --input-text           Roteiro. Use ... para pausas.
  --title                Titulo do video (aparece na biblioteca HeyGen)
  --out                  Caminho de saida do MP4 (obrigatorio)
  --orientation          portrait (padrao, 9:16) ou landscape (16:9)
  --resolution           1080p (padrao)
  --cross-ref-avatar-id  Avatar de referencia usado internamente pelo modelo
                         Avatar IV. Valor herdado do projeto vivavr-claude —
                         NAO CONFIRMADO para a conta da Skolen. Se o resultado
                         vier estranho (rosto/corpo errado), avisar antes de
                         reusar em producao.
"""
import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

CHROME_EXE = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
DEBUG_PORT = 9222
USER_DATA = r"C:\Users\felipe.fadel\AppData\Local\Temp\skolen-heygen-playwright-profile"
AVATAR_SHOTS_URL = "https://app.heygen.com/avatar/avatar-shots"

DEFAULT_AVATAR_ID = "87289bc673fd4be2a0a275b5d11c1598"  # avatar padrao da Skolen
# Herdado do vivavr-claude — nao confirmado para a conta da Skolen.
DEFAULT_CROSS_REF_ID = "6d47a1c14f1842b995909d5c7076edc2"


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--avatar-id", default=DEFAULT_AVATAR_ID)
    p.add_argument("--voice-id", required=True)
    p.add_argument("--input-text", required=True)
    p.add_argument("--title", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--orientation", default="portrait", choices=["portrait", "landscape"])
    p.add_argument("--resolution", default="1080p")
    p.add_argument("--cross-ref-avatar-id", default=DEFAULT_CROSS_REF_ID)
    p.add_argument("--timeout", type=int, default=600)
    return p.parse_args()


def launch_chrome():
    import socket
    try:
        s = socket.create_connection(("localhost", DEBUG_PORT), timeout=1)
        s.close()
        print(f"Chrome ja rodando na porta {DEBUG_PORT}.")
        return None
    except OSError:
        pass

    if not Path(CHROME_EXE).exists():
        raise RuntimeError(f"Chrome nao encontrado em {CHROME_EXE}")

    print("Lancando Chrome com remote debugging...")
    proc = subprocess.Popen([
        CHROME_EXE,
        f"--remote-debugging-port={DEBUG_PORT}",
        f"--user-data-dir={USER_DATA}",
        "--no-first-run",
        "--no-default-browser-check",
        AVATAR_SHOTS_URL,
    ])
    time.sleep(4)
    return proc


def get_heygen_page(ctx):
    for page in ctx.pages:
        if "heygen.com" in page.url:
            if "avatar-shots" not in page.url:
                page.evaluate(f"() => {{ window.location.href = '{AVATAR_SHOTS_URL}'; }}")
                time.sleep(3)
            return page
    page = ctx.new_page()
    page.goto(AVATAR_SHOTS_URL, wait_until="commit", timeout=30000)
    time.sleep(3)
    return page


def create_video(page, avatar_id: str, voice_id: str, input_text: str,
                  title: str, orientation: str, resolution: str,
                  cross_ref_avatar_id: str) -> str:
    print(f"Criando video '{title}'...")

    result = page.evaluate(f"""async () => {{
        const payload = {{
            video_title: {json.dumps(title)},
            video_orientation: {json.dumps(orientation)},
            resolution: {json.dumps(resolution)},
            avatar_id: {json.dumps(avatar_id)},
            source_type: "avatar_video_shortcut_modal_with_avatar_iv",
            fit: "cover",
            audio_data: {{
                audio_type: "tts_pending",
                text: {json.dumps(input_text)},
                voice_id: {json.dumps(voice_id)}
            }},
            avatar_settings: {{
                use_avatar_iv_model: true,
                model: "tokyo_v2_1_pde",
                resolution: {json.dumps(resolution)},
                avatar_iv_more_expressive: true,
                prompt: "",
                cross_ref_avatar_id: {json.dumps(cross_ref_avatar_id)}
            }},
            enable_caption: false,
            create_new_avatar: false
        }};

        const r = await fetch('https://api2.heygen.com/v2/avatar/shortcut/submit', {{
            method: 'POST',
            credentials: 'include',
            headers: {{
                'Content-Type': 'application/json',
                'Accept': 'application/json, text/plain, */*'
            }},
            body: JSON.stringify(payload)
        }});

        const data = await r.json();
        return {{ status: r.status, body: JSON.stringify(data) }};
    }}""")

    print(f"  Resposta: {result['status']} — {result['body'][:200]}")

    if result['status'] != 200:
        raise RuntimeError(f"Erro ao criar video: {result['body']}")

    body = json.loads(result['body'])
    video_id = (body.get('data', {}).get('video_id')
                or body.get('data', {}).get('item_id')
                or body.get('video_id'))
    if not video_id:
        raise RuntimeError(f"video_id nao encontrado na resposta: {result['body']}")

    print(f"  video_id: {video_id}")
    return video_id


def poll_video(page, video_id: str, timeout_s: int) -> str:
    print(f"Aguardando conclusao do video (max {timeout_s}s)...")
    deadline = time.time() + timeout_s

    while time.time() < deadline:
        result = page.evaluate(f"""async () => {{
            const r = await fetch(
                'https://api2.heygen.com/v1/project/items/status?item_ids={video_id}',
                {{ credentials: 'include' }}
            );
            const data = await r.json();
            return {{ status: r.status, body: JSON.stringify(data) }};
        }}""")

        body = json.loads(result['body'])
        items = body.get('data', [])
        item_status = items[0].get('status', '') if items else ''
        elapsed = int(timeout_s - (deadline - time.time()))
        print(f"  [{elapsed}s] status: {item_status}")

        if item_status == 'completed':
            url_result = page.evaluate(f"""async () => {{
                const r = await fetch(
                    'https://api2.heygen.com/v1/project/items?limit=1&sort_key=created_ts&sort_order=desc&is_trash=false&item_types=heygen_video',
                    {{ credentials: 'include' }}
                );
                const data = await r.json();
                const item = (data?.data?.items || []).find(i => i.video_id === '{video_id}');
                return item?.video_url || item?.download_url || null;
            }}""")
            if url_result:
                print(f"  URL: {url_result[:70]}...")
                return url_result
            status_result = page.evaluate(f"""async () => {{
                const r = await fetch(
                    'https://api2.heygen.com/v1/video_status.get?video_id={video_id}',
                    {{ credentials: 'include' }}
                );
                const data = await r.json();
                return data?.data?.video_url || data?.data?.download_url || null;
            }}""")
            if status_result:
                print(f"  URL (fallback): {status_result[:70]}...")
                return status_result
            raise RuntimeError(f"Video completo mas URL nao encontrada para {video_id}")

        if item_status in ('failed', 'error'):
            raise RuntimeError(f"Geracao falhou: {body}")

        time.sleep(15)

    raise TimeoutError(f"Video {video_id} nao ficou pronto em {timeout_s}s")


def download_video(video_url: str, out_path: Path):
    import urllib.request
    print(f"Baixando video para {out_path}...")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    urllib.request.urlretrieve(video_url, out_path)
    size_mb = out_path.stat().st_size / 1024 / 1024
    print(f"  Download concluido: {size_mb:.1f} MB")


def main():
    args = parse_args()
    out_path = Path(args.out)

    chrome_proc = launch_chrome()
    video_id = None

    try:
        with sync_playwright() as p:
            print(f"Conectando ao Chrome na porta {DEBUG_PORT}...")
            browser = p.chromium.connect_over_cdp(f"http://localhost:{DEBUG_PORT}")
            ctx = browser.contexts[0] if browser.contexts else browser.new_context()

            page = get_heygen_page(ctx)
            print(f"Pagina: {page.url}")

            video_id = create_video(
                page,
                avatar_id=args.avatar_id,
                voice_id=args.voice_id,
                input_text=args.input_text,
                title=args.title,
                orientation=args.orientation,
                resolution=args.resolution,
                cross_ref_avatar_id=args.cross_ref_avatar_id,
            )

            video_url = poll_video(page, video_id, args.timeout)
            download_video(video_url, out_path)

            browser.close()
    finally:
        # Sempre encerra o Chrome lancado por este processo, mesmo se algo
        # falhar no meio — evita acumular janelas Chrome orfas.
        if chrome_proc:
            chrome_proc.terminate()

    print(f"\nPronto! Video salvo em: {out_path}")
    print(f"  video_id: {video_id}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Erro: {e}", file=sys.stderr)
        sys.exit(1)
