# Skill: Carrossel Instagram Skolen

## Fluxo obrigatório — siga EXATAMENTE esta ordem

---

## PASSO 0 — Formato: framework de copy ou Teste Rápido/Diagnóstico?

Se o usuário pedir explicitamente um **"teste rápido"**, **"diagnóstico"**, **"quiz"** ou carrossel de perguntas Sim/Não, pule os Passos 1–6 (framework, estilo de capa, tipos por papel) e vá direto para o **PASSO ESPECIAL — Teste Rápido/Diagnóstico** no final deste arquivo. Esse formato tem estrutura própria e fixa, não usa os 7 frameworks de copy.

Caso contrário, siga o fluxo normal abaixo.

---

## PASSO 1 — Verificar histórico e perguntar o tema

Antes de qualquer coisa:

1. Leia `Marketing/Social/historico-posts.md` para ver:
   - Frameworks já usados nos últimos posts
   - Estilos de capa (`capa-afirmacao`, `capa-numero`, `capa-polemica`, `capa-pergunta`, `capa-minicaso`) usados recentemente
   - Ângulos já cobertos (para não repetir)
   - Cores dominantes usadas (para variar)

2. Pergunte ao usuário:

> "Qual é o tema do carrossel? E o objetivo de funil: topo, meio ou fundo?"

Se o usuário pedir que você defina o tema, escolha um **ângulo ainda não coberto** no histórico.

Aguarde a resposta antes de avançar.

---

## PASSO 2 — Escolher framework e estilo de capa (Features 3 e 4)

Com tema + funil em mãos:

### 2.1 — Escolher o framework (Feature 3 — Rotação)

1. Leia `references/Estrutura Carrosel.md` para ver as opções.
2. Identifique o framework usado no **post anterior** no histórico.
3. **Remova esse framework da lista de opções** — não repetir em dois posts consecutivos.
4. Escolha o framework mais adequado entre os restantes, respeitando o funil:
   - **Topo:** Framework 1 (Hook→Pain→Agitate→Solution→CTA) ou Framework 2 (Contrarian)
   - **Meio:** Framework 3 (Lista), Framework 4 (Transformação), Framework 6 (Problema invisível)
   - **Fundo:** Framework 7 (Prova + Demonstração), Framework 5 (Story)

### 2.2 — Escolher estilo de capa (Feature 4 — Variação de abertura)

1. Identifique o estilo de capa do **post anterior** no histórico.
2. **Não repita** o mesmo estilo de capa em dois posts consecutivos.
3. Escolha entre os estilos compatíveis com o framework:

| Estilo | Tipo no config | Quando faz sentido |
|---|---|---|
| `capa-afirmacao` | `cover` | Problema direto — topo de funil |
| `capa-numero` | `cover` | Impacto rápido com dado — qualquer funil |
| `capa-polemica` | `cover` | Quebra de crença — Framework 2 |
| `capa-pergunta` | `cover` | Provocar curiosidade — meio/fundo |
| `capa-minicaso` | `cover` | Humanizar — Framework 5 |

> Os estilos `capa-afirmacao` a `capa-minicaso` são estilos de **copy** do tipo `cover`. O tipo no config.json é sempre `"cover"` — o que varia é o texto da headline.

---

## PASSO 3 — Atribuir tipos de slide a cada papel (Features 1 e 2)

1. Leia `references/biblioteca-tipos.md` para ver o mapa **framework → papel → tipos compatíveis**.
2. Para cada um dos 7 slides, escolha o tipo dentro da lista compatível com o papel.
3. **Feature 2 — Camada visual obrigatória:** Verifique se há pelo menos 1 slide visual (categoria Dado ou Produto). Se não houver, converta o slide de papel "custo" ou "prova" para um tipo visual.
4. **Regra anti-monotonia:** Os dois slides de número (quando existem) não podem ser ambos `number`. Um deles deve ser `grafico-barras`, `calendario` ou `antes-depois`.

Tipos disponíveis:
- **Texto:** `text`, `afirmacao`, `citacao`
- **Dado (visual):** `number`, `grafico-barras`, `calendario`
- **Produto/Imagem (visual):** `app`, `antes-depois`, `foto-card`
- **Lista:** `checklist`
- **Capa:** `cover`
- **CTA:** `cta`, `cta-pergunta`

> **`foto-card`** — exibe imagem (pessoa, produto, print ou marca) ao lado do texto. Se o campo `imagem` for omitido ou o arquivo não existir, renderiza placeholder de marca automaticamente. Assets ficam em `Marketing/Assets/`.

---

## PASSO 4 — Escrever os textos dos 7 slides

1. Leia `references/guia-campos.md` para os limites de caracteres, regra dos 40% e restrições de `<br>`.
2. Escreva os textos de **todos os 7 slides** respeitando os limites do guia.
3. **Para `foto-card`:** a headline tem no máximo **18 chars por linha** (fonte 52px, metade do slide). Escreva curto — headlines longas quebram em 3 linhas e quebram o layout.
4. **Para `afirmacao`:** a headline tem no máximo **20 chars por linha** (fonte 76px, slide inteiro). Prefira frases curtas e diretas.
5. **Para `cover`:** a headline tem no máximo **25 chars por linha** (fonte 72px). O `<br>` é obrigatório — sem ele o browser ignora a quebra.

### Regra crítica de quebra de linha

O `<br>` no config **não garante** a quebra se o texto for longo demais para a fonte. O browser sempre quebra antes do `<br>` quando necessário. A única forma de garantir 2 linhas exatas é **escrever textos curtos o suficiente para caberem**. Verifique sempre:

| Tipo | Fonte | Chars seguros por linha |
|---|---|---|
| `cover` | 72px | ≤ 25 chars |
| `afirmacao` | 76px | ≤ 20 chars |
| `foto-card` headline | 52px | ≤ 18 chars |
| `text` headline | 78px | ≤ 22 chars |
| `cta` / `cta-pergunta` headline | 72–78px | ≤ 25 chars |

---

## PASSO 5 — Checagem de qualidade pré-aprovação (Feature 5)

Antes de apresentar os textos, faça:

### 5.1 — Revisão de acentuação (pt-BR)

Corrija **todas** as palavras sem acento. Exemplos frequentes:
- `retencao` → `retenção`
- `Demonstracao` → `Demonstração`
- `Historico` → `Histórico`
- `Acao` → `Ação`
- `evasao` → `evasão`
- `gestao` → `gestão`
- `visao` → `visão`
- `automatica` → `automática`

> O config.json pode omitir acentos (Chrome renderiza corretamente), mas os textos apresentados para aprovação devem estar corretos.

### 5.2 — Glossário de marca

Nos slides 5–7 (estado desejado, prova e CTA), verifique se aparece **pelo menos um** destes termos de ganho:
- `retenção` / `reter`
- `engajamento`
- `crescimento`
- `previsibilidade`
- `visibilidade`
- `resultado`

Se nenhum aparecer nos slides finais, ajuste o copy do slide 5 ou o eyebrow/subhead do CTA.

---

## PASSO 6 — Apresentar todos os textos e pedir aprovação

Apresente num bloco único organizado, incluindo o tipo de slide escolhido:

```
**SLIDE 01 — Cover** [estilo: capa-numero]
- Eyebrow: ...
- Headline: ...
- Subhead: ...

**SLIDE 02 — [tipo]**
- Label: ...
- Headline: ...
- Texto: ...

... (todos os 7 slides)

---
Framework escolhido: Framework X — [nome]
Estilo de capa: capa-[estilo]
Cor dominante: [cor]
```

Depois pergunte:

> "Gostou dos textos? Pode aprovar ou me dizer o que ajustar em cada slide."

Aguarde aprovação ou ajustes. Repita este passo até o usuário aprovar.

---

## PASSO 7 — Gerar o config.json e executar o script

Após aprovação, **NÃO escreva HTMLs manualmente**. Use o gerador:

### 7.1 — Escrever o config.json

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
      "tipo": "grafico-barras",
      "label": "Concentração do risco",
      "headline": "Headline do gráfico<br>com <em>destaque</em>",
      "bars": [
        {"label": "Jan", "label_val": "8%",  "value": 8},
        {"label": "Jun", "label_val": "22%", "value": 22, "destaque": true},
        {"label": "Dez", "label_val": "32%", "value": 32, "destaque": true}
      ]
    },
    {
      "tipo": "app",
      "eyebrow": "Eyebrow do slide app",
      "headline": "Headline com<br><em>destaque</em>",
      "features": ["Feature um", "Feature dois", "Feature três"]
    },
    {
      "tipo": "afirmacao",
      "label": "A virada",
      "headline": "Retenção não melhora<br>com <em>esforço.</em>"
    },
    {
      "tipo": "number",
      "label": "Escolas que monitoram",
      "stat": "3×",
      "stat_label": "mais retenção<br><em>nos meses críticos</em>"
    },
    {
      "tipo": "cta",
      "eyebrow": "Prepare sua escola",
      "headline": "Quer ver seus<br><em>picos de risco?</em>",
      "subhead": "Demonstração gratuita. Sem compromisso.",
      "button": "Falar com a Skolen"
    }
  ]
}
```

**Cores disponíveis para `cor_dominante`:** `teal` | `pink` | `yellow` | `blue`

**Tipos disponíveis:**
- `cover`, `text`, `number`, `app`, `cta` ← tipos originais
- `afirmacao`, `citacao`, `checklist`, `grafico-barras`, `calendario`, `antes-depois`, `cta-pergunta` ← tipos novos

**Formatação nos textos:**
- `<br>` → quebra de linha
- `<em>texto</em>` → destaque na cor dominante
- `<strong>texto</strong>` → negrito extra (apenas no campo `body`)

> Para campos de config.json, é aceitável omitir acentos (o Chrome renderiza corretamente via UTF-8). Mas o texto apresentado para aprovação (Passo 6) deve ter acentuação correta.

> **Regra dos 40% — aplicada a todos os tipos:** Nenhuma linha pode ter menos de 40% do comprimento da linha mais longa. Isso se aplica a `cover`, `afirmacao`, `foto-card`, `text`, `cta` e `cta-pergunta`. Exemplo errado: `"Lista de alunos com<br><em>risco visível.</em>"` — "com" (3 chars) vs "Lista de alunos com" (19 chars) = 16%. Correto: `"Alunos com<br><em>risco visível.</em>"` — 10/14 = 71%.

> **`foto-card` sem frame para `imagem_tipo: "produto"`:** A imagem flutua diretamente sobre o fundo branco com drop-shadow leve. Não há borda nem caixa. Ideal para screenshots de app e mockups com fundo transparente.

### 7.2 — Executar o gerador

```bash
python .claude/skills/carrousel/generate_carousel.py Marketing/Social/TEMA-DD-MM/config.json
```

O script gera automaticamente:
- Os 7 HTMLs na pasta do post
- As 7 imagens PNG em `pronto/`

---

## PASSO 8 — Criar o arquivo de descrição (.md)

Dentro da mesma pasta, crie `descricao-post.md` com:

```markdown
# Descrição — [Tema do Carrossel]

## Texto para legenda do Instagram

[Legenda completa — gancho, corpo e CTA.]

---

## Hashtags sugeridas

#gestaoescolar #escolas #edtech #skolen #retencaodealunos #gestaoeducacional #softwareeducacional #directorescolar

---

## Melhor horário para postar

Terças a quintas, entre 8h–9h ou 12h–13h (público B2B: diretores e coordenadores)
```

---

## PASSO 9 — Atualizar o histórico

Após gerar o carrossel, adicione a entrada em `Marketing/Social/historico-posts.md`:

```markdown
### TEMA-DD-MM · Cor: [cor]
**Framework:** Framework X — [nome]
**Estilo de capa:** capa-[estilo]
**Ângulo:** [descrição do ângulo em 1 frase]
**Copy principal:** "[headline do slide 1]"
```

---

## Estrutura final esperada

```
Marketing/Social/TEMA-DD-MM/
├── config.json          ← único arquivo que Claude escreve
├── descricao-post.md
├── slide-01-cover.html  ← gerado pelo script
├── slide-02-*.html
├── slide-03-*.html
├── slide-04-*.html
├── slide-05-*.html
├── slide-06-*.html
├── slide-07-*.html
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

## Checklist de pré-publicação

- [ ] Framework **diferente** do post anterior (Feature 3)
- [ ] Estilo de capa **diferente** do post anterior (Feature 4)
- [ ] Pelo menos **1 slide visual** (Dado ou Produto) — ideal 2 (Feature 2)
- [ ] Os dois slides de número **não são ambos** `number` (Feature 2)
- [ ] **Zero palavras sem acento** nos textos aprovados (Feature 5)
- [ ] Pelo menos **um termo de ganho** (retenção/engajamento/crescimento/previsibilidade) nos slides 5–7 (Feature 5)
- [ ] O carrossel termina em **CTA**
- [ ] Identidade preservada: fundo branco, bolinhas nos cantos, fonte Nunito, paleta da marca
- [ ] Histórico atualizado em `historico-posts.md`

---

## Regras gerais

- Nunca pule o passo de aprovação dos textos (Passo 6).
- **Nunca escreva HTMLs manualmente** — use sempre o script gerador.
- Respeite todos os limites de caracteres e a regra dos 40% do guia-campos.md.
- Use sempre a identidade visual Skolen: fundo branco, fontes Nunito, cores #F5C842 / #5ECBA8 / #E87DB0 / #5A8ED4 / #2B3641.
- A pasta de destino sempre dentro de `Marketing/Social/`.
- As imagens prontas sempre dentro da subpasta `pronto/`.
- Escolha a `cor_dominante` para diferenciar visualmente de posts recentes do mesmo tema.

---

## PASSO ESPECIAL — Teste Rápido / Diagnóstico

Fluxo próprio para o formato de autodiagnóstico (perguntas Sim/Não + placar de risco). Não usa os 7 frameworks de copy — é uma estrutura fixa e reutilizável. Referência completa de campos e limites: `references/biblioteca-tipos.md` (seção "Template: Teste Rápido / Diagnóstico") e `references/guia-campos.md` (seção homônima).

### E1 — Perguntar tema e número de perguntas

> "Qual é o tema do teste (ex: risco de evasão, engajamento de pais, uso de dados pela coordenação)? E quantas perguntas — 3, 4 ou 5?"

Se o usuário pedir que você defina, escolha um ângulo ainda não coberto no `historico-posts.md` e use 4 perguntas como padrão.

### E2 — Escrever os textos

Estrutura: 1 `teste-capa` + N `teste-pergunta` (3 a 5) + 1 `teste-resultado` + 1 `teste-cta` = 5 a 7 slides.

1. **Capa:** título do teste (pergunta guarda-chuva) + subtítulo dizendo quantas perguntas tem.
2. **Perguntas:** uma dor/sintoma concreto por pergunta, sempre respondível com Sim/Não. Não numere manualmente — o gerador calcula "Pergunta X/N" sozinho.
3. **Resultado:** defina o `criterio` (ex: "2 ou mais respostas 'Sim'"), a frase de diagnóstico, e os campos `segmentos`/`segmentos_total` para a barra de risco (quantos "sins" preenchem a barra, sobre o total de perguntas).
4. **CTA:** frase de virada + botão, no mesmo padrão do `cta` normal.

Aplique a revisão de acentuação (pt-BR) e o glossário de marca (Passo 5.1–5.2) normalmente antes de apresentar.

### E3 — Apresentar e aprovar

Mesmo formato do Passo 6 — apresente todos os slides num bloco único, incluindo `segmentos`/`segmentos_total` do resultado, e aguarde aprovação.

### E4 — Gerar

Escreva o `config.json` só com tipos `teste-*` — o script detecta o formato automaticamente e não exige 7 slides fixos:

```json
{
  "pasta": "Marketing/Social/TesteTEMA-DD-MM",
  "cor_dominante": "pink",
  "slides": [
    {"tipo": "teste-capa", "headline": "...", "subhead": "..."},
    {"tipo": "teste-pergunta", "headline": "..."},
    {"tipo": "teste-pergunta", "headline": "..."},
    {"tipo": "teste-pergunta", "headline": "..."},
    {"tipo": "teste-pergunta", "headline": "..."},
    {"tipo": "teste-resultado", "criterio": "...", "headline": "...", "segmentos": 3, "segmentos_total": 4},
    {"tipo": "teste-cta", "headline": "...", "subhead": "...", "button": "..."}
  ]
}
```

Execute normalmente:
```bash
python .claude/skills/carrousel/generate_carousel.py Marketing/Social/TesteTEMA-DD-MM/config.json
```

### E5 — Descrição e histórico

Crie `descricao-post.md` (Passo 8) e registre no `historico-posts.md` (Passo 9) normalmente, indicando `**Formato:** Teste Rápido/Diagnóstico` no lugar de Framework/Estilo de capa.
