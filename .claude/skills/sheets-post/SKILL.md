# Skill: Registrar Post na Planilha

Faz upload das imagens no Cloudinary e registra o post na aba `pendentes`.

## Pré-requisitos

A pasta do post deve ter:
- `pronto/` com os PNGs dos slides
- `descricao-post.md` com título, legenda e hashtags

Se faltar qualquer um, avise e pare.

---

## Fluxo

### 1 — Confirmar a pasta do post

Identifique o caminho da pasta (ex: `Marketing/Social/Evasao-04-04`).

### 2 — Perguntar data e horário

> "Qual a data e horário para publicar? (ex: 2026-05-20 09:00)"

Aguarde resposta antes de continuar.

### 3 — Executar

```bash
cd .claude/skills/sheets-post/scripts
python publish_post.py "<caminho-da-pasta>" "<data_postagem>"
```

Exemplo:
```bash
python publish_post.py "Marketing/Social/Evasao-04-04" "2026-05-20 09:00"
```

### 4 — Confirmar ao usuário

Informe quantas imagens foram enviadas e o horário agendado.

---

## Scripts

| Arquivo | Responsabilidade |
|---|---|
| `scripts/publish_post.py` | Entry point — orquestra o fluxo |
| `scripts/cloudinary_upload.py` | Upload dos PNGs para o Cloudinary |
| `scripts/sheets_register.py` | Registro da linha na aba `pendentes` |
