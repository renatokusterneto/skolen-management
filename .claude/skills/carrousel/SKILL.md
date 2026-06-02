# Skill: Carrossel Instagram Skolen

## Fluxo obrigatório — siga EXATAMENTE esta ordem

---

## PASSO 1 — Verificar histórico e perguntar o tema

Antes de qualquer coisa:

1. Leia `Marketing/Social/historico-posts.md` para ver o que já foi publicado, quais ângulos foram usados e quais cores dominantes estão disponíveis.
2. Pergunte ao usuário:

> "Qual é o tema do carrossel?"

Se o usuário pedir que você defina o tema, escolha um ângulo **ainda não coberto** no histórico e uma cor dominante **ainda não usada recentemente**.

Aguarde a resposta antes de avançar.

---

## PASSO 2 — Escolher o framework e escrever os textos

Com o tema em mãos:

1. Leia `references/Estrutura Carrosel.md` para escolher o framework mais adequado ao tema.
2. Leia `references/guia-campos.md` para entender os limites de caracteres, a regra de equilíbrio visual (regra dos 40%) e as restrições de `<br>` por campo.
3. Escreva os textos de **todos os 7 slides** respeitando os limites e a regra de equilíbrio do guia-campos.md.

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

## PASSO 4 — Gerar o config.json e executar o script

Após aprovação dos textos, **NÃO escreva HTMLs manualmente**. Use o gerador:

### 4.1 — Escrever o config.json

Crie o arquivo `Marketing/Social/TEMA-DD-MM/config.json` com os textos aprovados:

```json
{
  "pasta": "Marketing/Social/TEMA-DD-MM",
  "cor_dominante": "teal",
  "slides": [
    {
      "tipo": "cover",
      "eyebrow": "Escolas de Inglês",
      "headline": "Headline principal<br>com <em>destaque</em>",
      "subhead": "Subtítulo de apoio aqui."
    },
    {
      "tipo": "text",
      "label": "Label do slide",
      "headline": "Headline do slide<br>com <em>destaque</em>",
      "body": "Texto corrido do slide.<br>Pode ter <strong>negrito</strong> e <br>quebras."
    },
    {
      "tipo": "number",
      "label": "Contexto do número",
      "stat": "68%",
      "stat_label": "descrição do número<br>em até duas linhas"
    },
    {
      "tipo": "app",
      "eyebrow": "Eyebrow do slide app",
      "headline": "Headline com<br><em>destaque</em>",
      "features": [
        "Feature um aqui",
        "Feature dois aqui",
        "Feature três aqui"
      ]
    },
    {
      "tipo": "text",
      "label": "Label do slide 5",
      "headline": "Headline do slide<br><em>5</em>",
      "body": "Texto do slide 5."
    },
    {
      "tipo": "number",
      "label": "Contexto do número 2",
      "stat": "3×",
      "stat_label": "descrição do número<br>do slide 6"
    },
    {
      "tipo": "cta",
      "eyebrow": "Eyebrow do CTA",
      "headline": "Headline do CTA<br>com <em>destaque</em>",
      "subhead": "Subtítulo do CTA aqui.",
      "button": "Texto do Botão"
    }
  ]
}
```

**Cores disponíveis para `cor_dominante`:** `teal` | `pink` | `yellow` | `blue`

**Formatação nos textos:**
- `<br>` → quebra de linha
- `<em>texto</em>` → destaque na cor dominante
- `<strong>texto</strong>` → negrito extra (apenas no campo `body`)

### 4.2 — Executar o gerador

```bash
python .claude/skills/carrousel/generate_carousel.py Marketing/Social/TEMA-DD-MM/config.json
```

O script gera automaticamente:
- Os 7 HTMLs na pasta do post
- As 7 imagens PNG em `pronto/`

---

## PASSO 5 — Criar o arquivo de descrição (.md)

Dentro da mesma pasta, crie um arquivo `descricao-post.md` com:

```markdown
# Descrição — [Tema do Carrossel]

## Texto para legenda do Instagram

[Escreva aqui a legenda completa do post — use o copy do carrossel como base, adapte para formato de legenda com gancho, corpo e CTA.]

---

## Hashtags sugeridas

#gestaoescolar #escolas #edtech #skolen #retencaodealunos #gestaoeducacional #softwareeducacional #directorescolar

---

## Melhor horário para postar

Terças a quintas, entre 8h–9h ou 12h–13h (público B2B: diretores e coordenadores)
```

---

## Estrutura final esperada

```
Marketing/Social/TEMA-DD-MM/
├── config.json          ← único arquivo que Claude escreve
├── descricao-post.md
├── slide-01-cover.html  ← gerado pelo script
├── slide-02-text.html
├── slide-03-number.html
├── slide-04-app.html
├── slide-05-text.html
├── slide-06-number.html
├── slide-07-cta.html
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
- **Nunca escreva HTMLs manualmente** — use sempre o script gerador.
- Respeite todos os limites de caracteres e a regra dos 40% do guia-campos.md.
- Use sempre a identidade visual Skolen: fundo branco, fontes Nunito, cores #F5C842 / #5ECBA8 / #E87DB0 / #5A8ED4 / #2B3641.
- A pasta de destino sempre dentro de `Marketing/Social/`.
- As imagens prontas sempre dentro da subpasta `pronto/`.
- Escolha a `cor_dominante` para diferenciar visualmente de posts recentes do mesmo tema.
