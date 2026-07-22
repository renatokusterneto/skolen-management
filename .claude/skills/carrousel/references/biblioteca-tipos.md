# Biblioteca de Tipos de Slide — Skolen Carrossel

> Catálogo de todos os moldes visuais disponíveis no gerador.
> Cada tipo mapeia para um `"tipo"` no config.json.
> Use este arquivo na Etapa 4 do fluxo para decidir **como mostrar** cada papel do framework.

---

## Catálogo por categoria

### Capa / Hook — Slide 1

| Tipo no config | Nome | Quando usar | Campos obrigatórios |
|---|---|---|---|
| `cover` | Capa tipográfica | Afirmação de problema, padrão | `eyebrow`, `headline`, `subhead` |
| `capa-minicaso` | Capa com imagem | Humanizar, storytelling (Framework 5) — requer `image_url` | `eyebrow`, `headline`, `subhead`, `image_url` |

> **Nota:** `capa-numero`, `capa-polemica`, `capa-pergunta` são **estilos de copy** do slide `cover`, não tipos separados. A variação está no texto, não no molde. Use `cover` e varie o gancho conforme a seção "Estilos de copy para capa" abaixo.

---

### Texto — corpo e argumentação

| Tipo no config | Nome | Quando usar | Campos obrigatórios |
|---|---|---|---|
| `text` | Texto com label e body | Sintoma, estado desejado, qualquer papel narrativo | `label`, `headline`, `body` |
| `afirmacao` | Afirmação grande (sem body) | Quebra de crença, estado desejado impactante | `label`, `headline` |
| `citacao` | Citação de gestor | Prova social, humanizar, Framework 5 | `label`, `quote`, `author_name`, `author_role` |

---

### Dado / Visual — obrigatório em pelo menos 1 slide por carrossel

| Tipo no config | Nome | Quando usar | Campos obrigatórios |
|---|---|---|---|
| `number` | Número gigante | Custo, prova numérica simples | `label`, `stat`, `stat_label` |
| `grafico-barras` | Gráfico de barras | Comparação, evolução, concentração de risco | `label`, `headline`, `bars[]` |
| `calendario` | Calendário 12 meses | Sazonalidade, períodos críticos | `label`, `headline`, `meses_criticos[]`, `legenda` |

> **Regra Feature 2:** Os dois slides de número não podem ser ambos `number`. Se o carrossel tiver dois papéis de "custo/prova", um usa `number` e o outro usa `grafico-barras` ou `calendario`.

---

### Lista — enumeração e checagem

| Tipo no config | Nome | Quando usar | Campos obrigatórios |
|---|---|---|---|
| `app` | Mockup de app com features | Virada/solução, o que o produto monitora | `eyebrow`, `headline`, `features[]` |
| `checklist` | Lista com ícone de check | Framework 3 (lista com tensão), o que melhorou | `label`, `headline`, `items[]` |

---

### Produto / Transformação

| Tipo no config | Nome | Quando usar | Campos obrigatórios |
|---|---|---|---|
| `antes-depois` | Dois blocos antes/depois | Transformação de estado (Framework 4), prova | `label`, `headline`, `antes[]`, `depois[]` |
| `foto-card` | Imagem + texto lado a lado | Humanizar (pessoa), mostrar produto real, print anotado | `headline`, `imagem_tipo` + opcionais abaixo |

#### Campos do `foto-card`

| Campo | Obrigatório | Valores | Padrão |
|---|---|---|---|
| `headline` | sim | texto com `<em>` | — |
| `label` | não | texto curto | vazio |
| `body` | não | texto de apoio | vazio |
| `imagem` | não | `"Marketing/Assets/pessoas/foto.jpg"` | placeholder de marca |
| `imagem_tipo` | não | `pessoa` \| `produto` \| `print-anotado` \| `marca` | `produto` |
| `posicao` | não | `esquerda` \| `direita` | `esquerda` |

**`imagem_tipo` define o recorte visual:**
- `pessoa` → círculo com borda colorida (foto de diretor, professor, aluno)
- `produto` → retângulo com sombra e cantos arredondados (screenshot do app)
- `print-anotado` → retângulo com borda colorida + badge "Destaque"
- `marca` → quadrado neutro com fundo cinza (logo, ícone)

**Sem imagem:** se `imagem` for omitido ou o arquivo não existir, renderiza placeholder com bolinhas de marca — o layout não quebra.

**Assets ficam em:** `Marketing/Assets/produto/`, `Marketing/Assets/pessoas/`, `Marketing/Assets/marca/`

---

### CTA — Slide 7

| Tipo no config | Nome | Quando usar | Campos obrigatórios |
|---|---|---|---|
| `cta` | CTA com botão | Padrão | `eyebrow`, `headline`, `subhead`, `button` |
| `cta-pergunta` | CTA com pergunta grande | Fundo de funil, quando o hook é retórico | `headline`, `subhead`, `button` |

---

## Estilos de copy para capa (slide `cover`)

O tipo é sempre `cover`, mas o gancho varia:

| Estilo | Descrição | Exemplo de headline |
|---|---|---|
| `capa-afirmacao` | Problema direto (padrão) | "Sua escola perde alunos antes de perceber." |
| `capa-numero` | Abre com dado impactante | "60% dos cancelamentos acontecem em 3 meses." |
| `capa-polemica` | Quebra de crença | "Ter dados não significa ter gestão." |
| `capa-pergunta` | Pergunta retórica | "Sua escola sabe quem está prestes a cancelar?" |
| `capa-minicaso` | Cenário narrativo curto | "Toda semana surgia um cancelamento. Ninguém sabia por quê." |

> **Regra Feature 4:** Registrar o estilo de capa usado no histórico. Não repetir em dois posts consecutivos.

---

### Teste Rápido / Diagnóstico — formato próprio, fora do fluxo de 7 slides fixos

| Tipo no config | Nome | Quando usar | Campos obrigatórios |
|---|---|---|---|
| `teste-capa` | Capa do teste | Slide 1 — sempre | `headline`, `subhead` |
| `teste-pergunta` | Pergunta Sim/Não | Slides 2 a N-2 (3 a 5 perguntas) | `headline` |
| `teste-resultado` | Placar + barra de risco | Penúltimo slide — sempre | `criterio`, `headline`, `segmentos`, `segmentos_total` |
| `teste-cta` | CTA final | Último slide — sempre | `headline`, `subhead`, `button` |

> Este é um **template fechado e independente**, não um framework de copy (1–7). Ver seção dedicada "Template: Teste Rápido / Diagnóstico" mais abaixo para o fluxo completo.

---

## Mapa: Framework → Papel → Tipos compatíveis

### Framework 1 — Hook → Pain → Agitate → Solution → CTA

| Slide | Papel | Tipos compatíveis |
|---|---|---|
| 01 | Hook | `cover` (estilos: afirmacao, pergunta, numero, polemica) |
| 02 | Pain | `text`, `afirmacao` |
| 03 | Agitate / Custo | `number`, `grafico-barras`, `calendario` |
| 04 | Solution / Produto | `app`, `antes-depois` |
| 05 | Reforço / Prova | `text`, `afirmacao`, `citacao` |
| 06 | Prova numérica | `number`, `grafico-barras` |
| 07 | CTA | `cta`, `cta-pergunta` |

### Framework 2 — Contrarian / Quebra de crença

| Slide | Papel | Tipos compatíveis |
|---|---|---|
| 01 | Afirmação polêmica | `cover` (estilo: polemica) |
| 02 | Explicação do erro | `text`, `afirmacao` |
| 03 | Nova forma de pensar | `afirmacao`, `text` |
| 04 | Prova | `number`, `grafico-barras`, `citacao` |
| 05 | Produto / Solução | `app`, `antes-depois` |
| 06 | Simplificação | `afirmacao` |
| 07 | CTA | `cta`, `cta-pergunta` |

### Framework 3 — Lista com tensão

| Slide | Papel | Tipos compatíveis |
|---|---|---|
| 01 | Dor inicial | `cover` (estilo: afirmacao, pergunta) |
| 02–06 | Itens 1–5 | `checklist`, `text` |
| 07 | CTA | `cta`, `cta-pergunta` |

> Para Framework 3, concentre os 5 itens em 1–2 slides de `checklist` (3 itens + 2 itens) mais slides de `text` para contextualizar.

### Framework 4 — Transformação de estado

| Slide | Papel | Tipos compatíveis |
|---|---|---|
| 01 | Estado atual ruim | `cover` (estilo: afirmacao, minicaso) |
| 02 | Sintoma | `text`, `afirmacao` |
| 03 | Custo | `number`, `grafico-barras`, `calendario` |
| 04 | Virada / Solução | `app`, `antes-depois` |
| 05 | Estado desejado | `text`, `afirmacao`, `citacao` |
| 06 | Prova | `grafico-barras`, `number` |
| 07 | CTA | `cta`, `cta-pergunta` |

### Framework 5 — Story Carousel

| Slide | Papel | Tipos compatíveis |
|---|---|---|
| 01 | Situação inicial | `cover` (estilo: minicaso) |
| 02 | Conflito | `text`, `afirmacao` |
| 03 | Descoberta | `afirmacao`, `text` |
| 04 | Mudança de lógica | `app`, `antes-depois`, `text` |
| 05 | Transformação | `text`, `citacao` |
| 06 | Consolidação / Prova | `number`, `grafico-barras`, `afirmacao` |
| 07 | CTA | `cta`, `cta-pergunta` |

### Framework 6 — Problema invisível

| Slide | Papel | Tipos compatíveis |
|---|---|---|
| 01 | Falsa causa | `cover` (estilo: pergunta, polemica) |
| 02 | Quebra | `afirmacao`, `text` |
| 03 | Verdade oculta | `afirmacao`, `text` |
| 04 | Explicação | `text`, `grafico-barras`, `calendario` |
| 05 | Solução | `app`, `antes-depois` |
| 06 | Simplificação memorável | `afirmacao` |
| 07 | CTA | `cta`, `cta-pergunta` |

### Framework 7 — Prova + Demonstração

| Slide | Papel | Tipos compatíveis |
|---|---|---|
| 01 | Promessa | `cover` (estilo: numero, afirmacao) |
| 02 | Prova 1 | `number`, `grafico-barras` |
| 03 | Demonstração | `app`, `antes-depois` |
| 04 | Prova 2 / Citação | `citacao`, `number`, `grafico-barras` |
| 05 | Reforço lógico | `text`, `afirmacao` |
| 06 | Consolidação | `afirmacao`, `number` |
| 07 | CTA | `cta`, `cta-pergunta` |

---

## Campos por tipo — referência rápida para o config.json

### `afirmacao`
```json
{
  "tipo": "afirmacao",
  "label": "A virada",
  "headline": "Retenção não melhora<br>com <em>esforço.</em>"
}
```

### `citacao`
```json
{
  "tipo": "citacao",
  "label": "Perspectiva do gestor",
  "quote": "Quando comecei a ver<br>quem estava <em>em risco,</em><br>tudo mudou.",
  "author_name": "Diretora Escolar",
  "author_role": "Escola de Inglês, SP"
}
```

### `checklist`
```json
{
  "tipo": "checklist",
  "label": "O que muda",
  "headline": "Gestão com <em>visibilidade</em>",
  "items": [
    "Alunos em risco identificados antecipadamente",
    "Equipe sabe onde agir primeiro",
    "Evasão vira exceção, não rotina"
  ]
}
```

### `grafico-barras`
```json
{
  "tipo": "grafico-barras",
  "label": "Concentração do risco",
  "headline": "Evasão se concentra<br>em <em>poucos meses</em>",
  "bars": [
    {"label": "Jan", "label_val": "8%",  "value": 8},
    {"label": "Fev", "label_val": "5%",  "value": 5},
    {"label": "Jun", "label_val": "22%", "value": 22, "destaque": true},
    {"label": "Jul", "label_val": "18%", "value": 18, "destaque": true},
    {"label": "Dez", "label_val": "32%", "value": 32, "destaque": true},
    {"label": "Out", "label_val": "6%",  "value": 6}
  ]
}
```

### `calendario`
```json
{
  "tipo": "calendario",
  "label": "Sazonalidade de risco",
  "headline": "Esses meses pedem<br><em>atenção redobrada</em>",
  "meses_criticos": [6, 7, 12],
  "legenda": "Meses de maior risco de evasão"
}
```

### `antes-depois`
```json
{
  "tipo": "antes-depois",
  "label": "A diferença",
  "headline": "Gestão reativa<br>vs gestão <em>preditiva</em>",
  "antes": ["Descobre tarde", "Age sem prioridade", "Retenção cai"],
  "depois": ["Enxerga o risco cedo", "Equipe sabe onde agir", "Retém mais"]
}
```

### `cta-pergunta`
```json
{
  "tipo": "cta-pergunta",
  "headline": "Sua escola já consegue<br>ver quem está <em>em risco?</em>",
  "subhead": "Demonstração gratuita. Sem compromisso.",
  "button": "Falar com a Skolen"
}
```

---

## Template: Teste Rápido / Diagnóstico

Formato fixo e reutilizável, independente dos 7 frameworks de copy. Usado para carrosséis de autodiagnóstico ("sua escola tem risco de X?"), em vez de argumentação Hook/Pain/Solution.

### Estrutura (5 a 7 slides, 1:1)

| Slide | Tipo | Papel |
|---|---|---|
| 1 | `teste-capa` | Título do teste + subtítulo/CTA de entrada |
| 2 a N-2 | `teste-pergunta` | 3 a 5 perguntas, sempre Sim/Não |
| N-1 | `teste-resultado` | Critério do placar + diagnóstico + barra de risco |
| N | `teste-cta` | Frase de virada + botão |

O gerador (`generate_carousel.py`) detecta automaticamente esse formato quando **todos** os slides do config usam tipos `teste-*` — não é preciso indicar nada além disso. A numeração "Pergunta X/N" nas perguntas é calculada sozinha a partir da contagem de slides `teste-pergunta`.

### O que é fixo (não varia entre edições)

- Numeração "Pergunta X/N" — calculada automaticamente
- Pílulas "Sim" (preenchida, cor dominante) / "Não" (contorno cinza) — mesmo estilo e posição em toda pergunta
- Barra de risco contínua no slide de resultado — sempre pill cinza de fundo com preenchimento na cor dominante
- Tipografia, cores, bolinhas de canto e raio de borda do design system Skolen (ver `guia-campos.md`)
- Estilo do botão de CTA final (pill, cor dominante, sombra)

### O que varia a cada novo teste

- Tema do teste (risco de evasão, engajamento de pais, uso de dados pela coordenação, etc.)
- Número de perguntas (3, 4 ou 5)
- O texto de cada pergunta
- O critério do placar e a frase de diagnóstico
- A frase de virada e o texto do botão do CTA

### Campos por tipo

#### `teste-capa`
```json
{
  "tipo": "teste-capa",
  "headline": "Sua escola tem risco<br>de <em>evasão?</em>",
  "subhead": "Responda 4 perguntas rápidas e descubra."
}
```

#### `teste-pergunta`
```json
{
  "tipo": "teste-pergunta",
  "headline": "A frequência de algum aluno<br>caiu nos últimos meses?"
}
```
> Não inclua numeração no texto — o script adiciona "Pergunta X/N" automaticamente. As pílulas Sim/Não são sempre renderizadas, não precisam ser especificadas no config.

#### `teste-resultado`
```json
{
  "tipo": "teste-resultado",
  "criterio": "2 ou mais respostas 'Sim'",
  "headline": "Sua escola tem sinais<br><em>ativos de risco.</em>",
  "segmentos": 3,
  "segmentos_total": 4
}
```
> `segmentos` = quantos sinais de risco a barra deve preencher (proporcional). `segmentos_total` = número de perguntas do teste. A barra preenche `segmentos / segmentos_total` da largura total.

#### `teste-cta`
```json
{
  "tipo": "teste-cta",
  "headline": "Quer ver esses sinais<br>antes de <em>virar evasão?</em>",
  "subhead": "Demonstração gratuita. Sem compromisso.",
  "button": "Falar com a Skolen"
}
```

### Exemplo de config.json completo (4 perguntas → 7 slides)

```json
{
  "pasta": "Marketing/Social/TesteEvasao-DD-MM",
  "cor_dominante": "pink",
  "slides": [
    {"tipo": "teste-capa", "headline": "Sua escola tem risco<br>de <em>evasão?</em>", "subhead": "Responda 4 perguntas rápidas e descubra."},
    {"tipo": "teste-pergunta", "headline": "A frequência de algum aluno<br>caiu nos últimos meses?"},
    {"tipo": "teste-pergunta", "headline": "Algum aluno ficou inadimplente<br>mais de uma vez?"},
    {"tipo": "teste-pergunta", "headline": "Pais pararam de responder<br>comunicados da escola?"},
    {"tipo": "teste-pergunta", "headline": "A equipe descobre cancelamentos<br>só depois que acontecem?"},
    {"tipo": "teste-resultado", "criterio": "2 ou mais respostas 'Sim'", "headline": "Sua escola tem sinais<br><em>ativos de risco.</em>", "segmentos": 3, "segmentos_total": 4},
    {"tipo": "teste-cta", "headline": "Quer ver esses sinais<br>antes de <em>virar evasão?</em>", "subhead": "Demonstração gratuita. Sem compromisso.", "button": "Falar com a Skolen"}
  ]
}
```

Para 3 ou 5 perguntas, adicione/remova blocos `teste-pergunta` — o total de slides (5 a 7) e a numeração se ajustam automaticamente.
