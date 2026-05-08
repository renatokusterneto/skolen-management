# Skill: Carrossel Instagram Skolen

## Fluxo obrigatório — siga EXATAMENTE esta ordem

---

## PASSO 1 — Perguntar o tema

Antes de qualquer coisa, pergunte ao usuário:

> "Qual é o tema do carrossel?"

Aguarde a resposta. Não avance sem ela.

---

## PASSO 2 — Escolher o framework e escrever os textos

Com o tema em mãos:

1. Leia `references/Estrutura Carrosel.md` para escolher o framework mais adequado ao tema.
2. Leia `references/GUIA-CAMPOS.md` para entender os limites de caracteres de cada campo de cada slide.
3. Escreva os textos de **todos os 7 slides** respeitando os limites de caracteres do GUIA-CAMPOS.md.

---

## PASSO 3 — Apresentar todos os textos e pedir aprovação

Apresente todos os textos num bloco único e organizado, no seguinte formato:

```
**SLIDE 01 — Cover**
- Eyebrow: ...
- Headline: ...
- Subhead: ...

**SLIDE 02**
- Label: ...
- Headline: ...
- Texto: ...

... (todos os 7 slides)
```

Depois pergunte:

> "Gostou dos textos? Pode aprovar ou me dizer o que ajustar em cada slide."

Aguarde aprovação ou ajustes. Repita este passo até o usuário aprovar.

---

## PASSO 4 — Gerar os HTMLs

Após aprovação:

1. Escolha os templates adequados de `references/Carrousel Templates/` conforme o GUIA-CAMPOS.md.
2. Crie uma pasta em `Marketing/Social/TEMA-DD-MM/` (ex: `Evasao-04-04/`).
3. Gere os 7 arquivos HTML dentro dessa pasta com os textos aprovados.

**IMPORTANTE — fonte local obrigatória:**
Nunca use Google Fonts CDN nos HTMLs gerados. O Chrome headless não carrega fontes de rede antes de tirar o screenshot.

Substitua sempre o bloco de Google Fonts por esta linha (com o caminho absoluto correto):
```html
<link rel="stylesheet" href="file:///Users/renatokusterneto/Skolen/.claude/skills/carrousel/fonts/nunito.css">
```

Os arquivos de fonte já estão disponíveis em `.claude/skills/carrousel/fonts/`.

---

## PASSO 5 — Criar o arquivo de descrição (.md)

Dentro da mesma pasta, crie um arquivo `descricao-post.md` com:

```markdown
# Descrição — [Tema do Carrossel]

## Texto para legenda do Instagram

[Escreva aqui a legenda completa do post — use o copy do carrossel como base, adapte para formato de legenda com gancho, corpo e CTA. Inclua sugestão de hashtags relevantes para gestão escolar B2B.]

---

## Hashtags sugeridas

#gestaoescolar #escolas #edtech #skolen #retencaodealunos #gestaoeducacional #softwareeducacional #directorescolar

---

## Melhor horário para postar

[Sugerir horário baseado no público B2B: terças a quintas, entre 8h-9h ou 12h-13h]
```

---

## PASSO 6 — Converter HTMLs em imagens

Após gerar os HTMLs, execute o script de conversão para gerar as imagens prontas para publicação.

### Criar pasta de saída

Crie a subpasta `pronto/` dentro da pasta do carrossel:
```
Marketing/Social/TEMA-DD-MM/pronto/
```

### Converter cada HTML em PNG (1080×1080px)

Use o seguinte comando para cada slide (substitua os caminhos):

```bash
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --headless=new \
  --screenshot="Marketing/Social/TEMA-DD-MM/pronto/slide-01.png" \
  --window-size=1080,1080 \
  --hide-scrollbars \
  --disable-gpu \
  "file:///Users/renatokusterneto/Skolen/Marketing/Social/TEMA-DD-MM/slide-01-cover.html"
```

Execute para todos os 7 slides em sequência (slide-01 a slide-07).

**Se o Chrome não estiver disponível**, tente com Chromium:
```bash
chromium --headless=new --screenshot=... --window-size=1080,1080 ...
```

**Alternativa com Node/Puppeteer** (se disponível):
```bash
npx puppeteer browsers install chrome
node -e "
const puppeteer = require('puppeteer');
(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  await page.setViewport({ width: 1080, height: 1080 });
  await page.goto('file:///caminho/slide.html');
  await page.screenshot({ path: 'pronto/slide-01.png' });
  await browser.close();
})();
"
```

### Resultado esperado

```
Marketing/Social/TEMA-DD-MM/
├── slide-01-cover.html
├── slide-02-text.html
├── slide-03-...html
├── slide-04-...html
├── slide-05-...html
├── slide-06-...html
├── slide-07-cta.html
├── descricao-post.md
└── pronto/
    ├── slide-01.png
    ├── slide-02.png
    ├── slide-03.png
    ├── slide-04.png
    ├── slide-05.png
    ├── slide-06.png
    └── slide-07.png
```

---

## Regras gerais

- Nunca pule o passo de aprovação dos textos (Passo 3).
- Nunca crie HTMLs antes da aprovação dos textos.
- Respeite todos os limites de caracteres do GUIA-CAMPOS.md.
- Use sempre a identidade visual Skolen: fundo branco, fontes Nunito, cores #F5C842 / #5ECBA8 / #E87DB0 / #5A8ED4 / #2B3641.
- A pasta de destino sempre dentro de `Marketing/Social/`.
- As imagens prontas sempre dentro da subpasta `pronto/`.
