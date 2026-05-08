# Skill: Static Ads Skolen

## Fluxo obrigatório — siga EXATAMENTE esta ordem

---

## PASSO 1 — Fazer as perguntas de briefing

Antes de qualquer coisa, pergunte ao usuário **todas as perguntas abaixo em uma única mensagem**:

> 1. **Tema / dor central** — Qual é o assunto do anúncio? (ex: inadimplência, matrícula, app dos pais, secretaria sobrecarregada)
> 2. **Etapa do funil** — É para atrair atenção nova (TOFU), gerar consideração (MOFU) ou empurrar para decisão (BOFU)? Se não souber, me diga o objetivo e eu escolho.
> 3. **Formatos desejados** — Story (1080×1920), Feed (1080×1080) ou os dois?
> 4. **Tipo de template** — Quer texto puro, número/estatística, app com mockup, depoimento de cliente, antes e depois (lista) ou antes e depois visual (com imagem)? Se não souber, me diga o objetivo e eu sugiro.
> 5. **Nome da pasta de saída** — Como quer nomear a pasta do anúncio? (ex: `Inadimplencia-TOFU`, `App-Pais-MOFU`, `Matricula-BOFU`)

Aguarde a resposta completa. Não avance sem ela.

---

## PASSO 2 — Escolher estratégia e escrever os textos

Com o briefing em mãos:

1. Leia `references/Estrutura-Ads.md` para escolher a estratégia de copy correta para o funil e template indicados.
2. Leia `references/GUIA-CAMPOS.md` para conhecer os limites de caracteres exatos de cada campo de cada template.
3. Escreva os textos de **todas as variações solicitadas** (feed, story, ou ambos), respeitando os limites do GUIA-CAMPOS.md.

**Regra:** uma mensagem por frame. Escolha um ângulo e vá fundo.

---

## PASSO 3 — Apresentar os textos e pedir aprovação

Apresente todos os textos num bloco único e organizado, separado por variação:

```
**[TIPO] — [FORMATO]**
Template: [nome do arquivo de referência]

- Eyebrow: ...
- Headline: ...
- Subhead: ...
(ou os campos do template escolhido)

---

**[TIPO] — [FORMATO]**
Template: [nome do arquivo de referência]

- Eyebrow: ...
- Headline: ...
- Subtext: ...
```

Depois pergunte:

> "Gostou dos textos? Pode aprovar ou me dizer o que ajustar."

Aguarde aprovação ou ajustes. Repita este passo até o usuário aprovar.

---

## PASSO 4 — Gerar os HTMLs

Após aprovação:

1. Escolha os templates corretos de `references/Templates/` conforme o GUIA-CAMPOS.md.
2. Crie a pasta de saída: `Marketing/Anuncios/[Nome-da-Pasta]/`
3. Gere os arquivos HTML dentro dessa pasta com os textos aprovados, um arquivo por variação.

**Nomenclatura dos arquivos:**
- `[tipo]-feed.html` → ex: `texto-feed.html`, `numero-story.html`, `depoimento-feed.html`

**IMPORTANTE — fonte local obrigatória:**
Nunca use Google Fonts CDN nos HTMLs gerados. O Chrome headless não carrega fontes de rede antes de tirar o screenshot.

Substitua sempre o bloco de Google Fonts por esta linha (com o caminho absoluto correto):
```html
<link rel="stylesheet" href="file:///Users/renatokusterneto/Skolen/.claude/skills/carrousel/fonts/nunito.css">
```

Os arquivos de fonte estão em `.claude/skills/carrousel/fonts/`.

---

## PASSO 5 — Criar o arquivo de descrição (.md)

Dentro da mesma pasta, crie um arquivo `descricao-ads.md` com:

```markdown
# Descrição — [Tema do Anúncio]

## Objetivo e funil

[TOFU / MOFU / BOFU] — [objetivo da campanha em 1 frase]

## Variações geradas

| Arquivo | Template | Formato | Funil |
|---------|----------|---------|-------|
| texto-feed.html | Text | 1080×1080 | TOFU |
| texto-story.html | Text | 1080×1920 | TOFU |

## Copy para legenda (se usado em orgânico)

[Adapte a headline e subhead do ad para formato de legenda: gancho + corpo + CTA. Inclua hashtags relevantes.]

## Hashtags sugeridas

#gestaoescolar #escolas #edtech #skolen #secretariaescolar #gestaoeducacional #softwareeducacional #directorescolar

## Sugestão de uso

[Indicar em qual etapa de funil usar cada variação, e se é para feed, stories ou ambos]
```

---

## PASSO 6 — Converter HTMLs em PNG

Após gerar os HTMLs, converta cada um em imagem PNG pronta para publicação.

### Criar pasta de saída

Crie a subpasta `pronto/` dentro da pasta do anúncio:
```
Marketing/Anuncios/[Nome-da-Pasta]/pronto/
```

### Dimensões por formato

| Formato | Largura | Altura |
|---------|---------|--------|
| Feed | 1080px | 1080px |
| Story | 1080px | 1920px |

### Converter cada HTML em PNG

**Feed (1080×1080):**
```bash
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --headless=new \
  --screenshot="Marketing/Anuncios/[Nome-da-Pasta]/pronto/[nome].png" \
  --window-size=1080,1080 \
  --hide-scrollbars \
  --disable-gpu \
  "file:///Users/renatokusterneto/Skolen/Marketing/Anuncios/[Nome-da-Pasta]/[nome]-feed.html"
```

**Story (1080×1920):**
```bash
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --headless=new \
  --screenshot="Marketing/Anuncios/[Nome-da-Pasta]/pronto/[nome].png" \
  --window-size=1080,1920 \
  --hide-scrollbars \
  --disable-gpu \
  "file:///Users/renatokusterneto/Skolen/Marketing/Anuncios/[Nome-da-Pasta]/[nome]-story.html"
```

Execute um comando por arquivo HTML gerado, ajustando `--window-size` conforme o formato.

**Se o Chrome não estiver disponível**, tente com Chromium:
```bash
chromium --headless=new --screenshot=... --window-size=1080,1080 ...
```

### Resultado esperado

```
Marketing/Anuncios/[Nome-da-Pasta]/
├── texto-feed.html
├── texto-story.html
├── numero-story.html
├── depoimento-feed.html
├── ... (demais variações)
├── descricao-ads.md
└── pronto/
    ├── texto-feed.png
    ├── texto-story.png
    ├── numero-story.png
    ├── depoimento-feed.png
    └── ...
```

---

## Regras gerais

- Nunca pule o passo de aprovação dos textos (Passo 3).
- Nunca crie HTMLs antes da aprovação dos textos.
- Respeite todos os limites de caracteres do GUIA-CAMPOS.md.
- Use sempre a identidade visual Skolen: fundo branco, fontes Nunito, cores `#F5C842` / `#5ECBA8` / `#E87DB0` / `#5A8ED4` / `#2B3641`.
- A pasta de destino sempre dentro de `Marketing/Anuncios/`.
- As imagens prontas sempre dentro da subpasta `pronto/`.
- O `--window-size` no Chrome deve corresponder exatamente ao formato do HTML (1080×1080 para feed, 1080×1920 para story).
- Fonte local obrigatória — nunca Google Fonts CDN nos HTMLs gerados.
