---
name: skolen-video-repost
description: >
  Gera um vídeo repost para a Skolen: monta o vídeo original dentro do template
  visual da marca (fundo branco, logo Skolen, quote em cima, vídeo emoldurado) e
  adiciona um CTA de texto. Aceita URL ou caminho MP4 como input.
---

# skolen-video-repost

---

## PASSO 1 — Identificar o input

O usuário pode passar:
- Um caminho para arquivo `.mp4` local
- Uma URL (Instagram, TikTok, YouTube, etc.) — baixar com `yt-dlp`

Se não passou input, pergunte.

---

## PASSO 2 — Gerar CTA

Transcreva o vídeo (Whisper, `tiny`, `--language pt`) para entender o contexto. Com
base no tema, gere **3 opções de CTA** em PT-BR e peça ao usuário para escolher uma
antes de continuar.

Regras para o CTA:
- Máx. 12 palavras
- Conecta diretamente a situação do vídeo à proposta da Skolen (gestão escolar sem caos, retenção de alunos, visibilidade da operação)
- Tom: direto, sem exagero
- Não fala mal do personagem/criador do vídeo original — brincar junto, não contra
- Termina com uma ação clara ("conhece a Skolen", "vê como a Skolen resolve isso", "fala com a gente")

Exemplos:
- "Se sua secretaria vive assim, a Skolen organiza isso pra você."
- "Rotina de diretor não precisa ser esse caos. Conhece a Skolen."
- "Gestão escolar sem sobressalto existe. É a Skolen."

---

## PASSO 3 — Gerar áudio do CTA (opcional)

Se o fluxo pedir narração do CTA (e não só texto no card), gere o áudio via TTS
disponível no projeto (ex: ElevenLabs, se configurado) e verifique a duração com
`ffprobe`. Esse passo é **opcional** — o template padrão do PASSO 4 já exibe o CTA
como texto, sem narração.

---

## PASSO 4 — Gerar o vídeo com template via quote_post.py

Use o script `scripts/quote_post.py` — ele gera o template completo com a identidade
visual Skolen: fundo branco, logo Skolen, quote em cima e vídeo emoldurado com cantos
arredondados.

```bash
cd "c:/Users/felipe.fadel/skolen-management"

python scripts/quote_post.py \
  --input "<caminho_do_video_baixado.mp4>" \
  --text "<CTA escolhido>" \
  --output "Marketing/Social/_video-reposts/reaction-<SLUG>.mp4"
```

Onde `<SLUG>` é um nome descritivo do vídeo (ex: `secretaria-caos`, `reuniao-pais`).

**Nota:** o script faz rehash internamente — não é necessário rehashar antes.

### Flag `--captions` — Legendas sincronizadas

Use quando o vídeo tem diálogo relevante que vale mostrar ao espectador (ex: alguém
narrando uma situação real de gestão escolar). Adiciona legenda sincronizada via
Whisper na área branca abaixo do frame:

```bash
python scripts/quote_post.py \
  --input "<caminho_do_video_baixado.mp4>" \
  --text "<CTA escolhido>" \
  --captions \
  --output "Marketing/Social/_video-reposts/reaction-<SLUG>.mp4"
```

**Como funciona:**
1. Transcreve o vídeo com Whisper (`tiny`, `--language pt`)
2. Gera segmentos com timestamps
3. Renderiza cada frase frame-a-frame na área branca abaixo do vídeo, usando PIL
4. Fonte Nunito, tamanho 36, cor escura, centralizada

**Quando usar:** vídeos onde a fala é o ponto principal.
**Quando não usar:** vídeos de ação/situação onde o áudio não é o foco, ou quando a
transcrição seria redundante.

---

## PASSO 5 — Registrar em Marketing/Social

Crie `Marketing/Social/_video-reposts/reaction-<SLUG>.md`:

```markdown
---
type: video-repost
skill: skolen-video-repost
tags: [skolen, video-repost, quote-post]
status: teste
data_postagem:
metricas:
---

# <CTA>

**Skill:** skolen-video-repost

---

## Vídeo

Arquivo: reaction-<SLUG>.mp4

## CTA

<CTA>
```

---

## PASSO 6 — Confirmar

Informe o caminho do vídeo gerado e da nota de registro.
