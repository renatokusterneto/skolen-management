"""
heygen_save_session.py — roda UMA VEZ para abrir o Chrome logado no HeyGen
(conta da Skolen) e deixar a sessao pronta para heygen_gen_video_cdp.py.

Estrategia: abre o Chrome do sistema com remote debugging na porta 9222,
usando um profile isolado (nao mexe no seu Chrome normal), e conecta o
Playwright nele via CDP.

Uso:
  python heygen_save_session.py

1. Um Chrome sera aberto na pagina de login do HeyGen.
2. Faca login manualmente com a conta da Skolen.
3. Pressione Enter no terminal — a sessao fica salva no profile isolado
   (Temp\\skolen-heygen-playwright-profile) e sera reaproveitada automaticamente
   por heygen_gen_video_cdp.py em execucoes futuras.
"""
import sys
import time
import subprocess
from pathlib import Path

from playwright.sync_api import sync_playwright

CHROME_EXE = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
DEBUG_PORT = 9222
USER_DATA = r"C:\Users\felipe.fadel\AppData\Local\Temp\skolen-heygen-playwright-profile"


def main():
    if not Path(CHROME_EXE).exists():
        raise RuntimeError(f"Chrome nao encontrado em {CHROME_EXE}")

    print("Lancando Chrome com remote debugging...")
    proc = subprocess.Popen([
        CHROME_EXE,
        f"--remote-debugging-port={DEBUG_PORT}",
        f"--user-data-dir={USER_DATA}",
        "--no-first-run",
        "--no-default-browser-check",
        "https://app.heygen.com/login",
    ])
    time.sleep(3)

    try:
        with sync_playwright() as p:
            print(f"Conectando ao Chrome na porta {DEBUG_PORT}...")
            browser = p.chromium.connect_over_cdp(f"http://localhost:{DEBUG_PORT}")
            ctx = browser.contexts[0] if browser.contexts else browser.new_context()

            print("\nO Chrome esta aberto na pagina de login do HeyGen.")
            print("Faca login com a conta da Skolen.")
            print("Quando estiver logado e na pagina inicial, volte aqui.")
            input("  -> Pressione Enter para confirmar: ")

            n_cookies = len(ctx.cookies())
            print(f"\nSessao ativa no profile isolado ({n_cookies} cookies).")
            print(f"Profile: {USER_DATA}")
            print("Pronto para usar com heygen_gen_video_cdp.py.")

            browser.close()
    finally:
        proc.terminate()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Erro: {e}", file=sys.stderr)
        sys.exit(1)
