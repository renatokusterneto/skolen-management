# Skill: Registrar Post na Planilha

Faz upload das imagens no Cloudinary e registra o post na aba `pendentes` da planilha.

---

## Quando usar

Após a pasta do post ter imagens prontas em `pronto/` e um `descricao-post.md`.

---

## Fluxo

### PASSO 1 — Identificar o post

Localize a pasta do post. Confirme que existem:
- Arquivos `.png` em `pronto/`
- Arquivo `descricao-post.md`

Se faltar qualquer um dos dois, avise e pare.

---

### PASSO 2 — Subir imagens no Cloudinary

Use as credenciais do `.env`. Estrutura de destino:

```
skolen/social/{campaign_id}/slide-01.png
skolen/social/{campaign_id}/slide-02.png
...
```

O `campaign_id` é o nome da pasta do post em kebab-case (ex: `evasao-04-04`).

```python
import cloudinary, cloudinary.uploader, os
from dotenv import load_dotenv
load_dotenv()

cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET')
)

slides = sorted([f for f in os.listdir(pronto_dir) if f.endswith('.png')])
urls = []
for slide in slides:
    r = cloudinary.uploader.upload(
        os.path.join(pronto_dir, slide),
        folder=f'skolen/social/{campaign_id}',
        public_id=slide.replace('.png', ''),
        overwrite=True
    )
    urls.append(r['secure_url'])
```

---

### PASSO 3 — Perguntar data e horário

Pergunte:

> "Qual a data e horário para publicar? (ex: 2026-05-20 09:00)"

Aguarde resposta antes de continuar.

---

### PASSO 4 — Registrar na planilha

Leia o `descricao-post.md` para extrair a legenda e hashtags.

Adicione uma linha na aba `pendentes`:

```python
from google.oauth2 import service_account
from googleapiclient.discovery import build

creds = service_account.Credentials.from_service_account_file(
    os.getenv('GOOGLE_SERVICE_ACCOUNT_FILE'),
    scopes=['https://www.googleapis.com/auth/spreadsheets']
)
service = build('sheets', 'v4', credentials=creds)

row = [[campaign_id, tipo, titulo, data_postagem, caption, ','.join(urls), 'FALSE']]
service.spreadsheets().values().append(
    spreadsheetId=os.getenv('GOOGLE_SHEETS_ID'),
    range='pendentes!A:G',
    valueInputOption='RAW',
    insertDataOption='INSERT_ROWS',
    body={'values': row}
).execute()
```

Valores da linha:
| Campo | Origem |
|---|---|
| `campaign_id` | Nome da pasta em kebab-case |
| `tipo` | `carrousel`, `reel` ou `foto` — inferir pelo conteúdo |
| `titulo` | Título do `descricao-post.md` |
| `data_postagem` | Resposta do Passo 3 |
| `caption` | Legenda + hashtags do `descricao-post.md` |
| `cloudinary_urls` | URLs geradas no Passo 2, separadas por vírgula |
| `publicado` | Sempre `FALSE` |

---

### PASSO 5 — Confirmar

Informe:
- Quantas imagens foram enviadas ao Cloudinary
- Data e horário agendado
- Que o post está na fila (`pendentes`) aguardando publicação
