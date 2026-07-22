# Guia de Campos — Carrossel Instagram Skolen
> 1080×1080px · Fonte Nunito · Todos os limites garantem que o layout não quebre

---

## Regra de equilíbrio visual (leia antes de escrever qualquer headline)

A quebra de linha (`<br>`) num headline **não é uma decisão de texto — é uma decisão visual.**
Uma linha muito curta isolada num headline quebra o ritmo e distrai o leitor.

### A regra dos 40%

Nenhuma linha pode ter menos de **40% do comprimento da linha mais longa** do mesmo campo.

```
ERRADO — "muito." fica isolado

  Sua equipe trabalha    <- 20 chars
  muito.                 <- 6 chars   <- 30% da maior = QUEBRA ERRADA
  Mas no lugar certo?    <- 19 chars

CERTO — duas linhas equilibradas

  Sua equipe trabalha muito.   <- 26 chars
  Mas no lugar certo?          <- 19 chars  (73% da maior = OK)
```

### Como aplicar na prática

1. Escreva o texto completo sem `<br>`.
2. Identifique o ponto de pausa natural (virgula, ponto, contraste de ideia).
3. Conte os chars de cada linha resultante.
4. Se a linha mais curta for menor que 40% da mais longa, mova o `<br>` uma palavra para frente ou para tras.
5. A palavra com `<em>` deve ficar **na ultima linha** — reforca o destaque visual.

### Exemplos rapidos

| Errado | Certo | Por que |
|--------|-------|---------|
| `Sua escola<br>perdeu alunos<br><em>sem perceber.</em>` | `Sua escola perdeu<br>alunos <em>sem perceber.</em>` | 2x `<br>` no cover deixa o texto minusculo |
| `O aluno ja<br>deu <em>sinais.</em>` | `O aluno ja deu <em>sinais.</em>` | Ambas as linhas sao curtas — melhor uma linha so |
| `Enxergar<br>antes de <em>perder.</em>` | `Enxergar antes<br>de <em>perder.</em>` | "Enxergar" isolado (9 chars) vs 20 = 45% — no limite, evitar |

### Checklist antes de salvar o config.json

- [ ] Nenhuma linha do headline tem menos de 40% da linha mais longa
- [ ] A palavra com `<em>` esta na ultima linha
- [ ] Headline do cover e CTA tem no maximo 1 `<br>`
- [ ] Subhead tem no maximo 1 `<br>`
- [ ] Nenhum campo ultrapassa o limite de caracteres da tabela do seu slide

---

## SLIDE 01 — Cover

| Campo | Max. total | Max. por linha | `<br>` permitido |
|-------|-----------|----------------|-----------------|
| **Eyebrow** | 22 chars | — | Nao |
| **Headline** | 55 chars | 30 chars | Max. 1 |
| **Subhead** | 65 chars | 35 chars | Max. 1 |

Exemplo valido:
```json
{
  "tipo": "cover",
  "eyebrow": "Gestao Escolar",
  "headline": "Sua escola ja perdeu<br>alunos <em>sem perceber.</em>",
  "subhead": "A evasao comeca antes do cancelamento."
}
```

---

## SLIDE 02 — Texto

| Campo | Max. total | Max. por linha | `<br>` permitido |
|-------|-----------|----------------|-----------------|
| **Label** | 22 chars | — | Nao |
| **Headline** | 40 chars | 22 chars | Max. 1 |
| **Body** | 130 chars | 45 chars | Max. 2 · quebrar em virgula ou ponto |

Exemplo valido:
```json
{
  "tipo": "text",
  "label": "O problema real",
  "headline": "A evasao comeca<br><em>antes do aviso.</em>",
  "body": "Quando o aluno cancela em dezembro,<br>o distanciamento <strong>comecou meses antes.</strong><br>Sua escola estava vendo esse sinal?"
}
```

---

## SLIDE 03 — Numero

| Campo | Max. total | Max. por linha | `<br>` permitido |
|-------|-----------|----------------|-----------------|
| **Label** | 30 chars | — | Nao |
| **Stat** | 6 chars | — | Nao |
| **Stat label** | 55 chars | 30 chars | Max. 1 · `<em>` na ultima linha |

Exemplo valido:
```json
{
  "tipo": "number",
  "label": "Quando a escola descobre",
  "stat": "8/10",
  "stat_label": "alunos deram sinais<br><em>antes de cancelar</em>"
}
```

---

## SLIDE 04 — App

| Campo | Max. total | Max. por linha | `<br>` permitido |
|-------|-----------|----------------|-----------------|
| **Eyebrow** | 30 chars | — | Nao |
| **Headline** | 38 chars | 22 chars | Max. 1 · regra 40% |
| **Feature 1/2/3** | 30 chars cada | — | Nao — cada feature e uma linha unica |

Exemplo valido:
```json
{
  "tipo": "app",
  "eyebrow": "O que passa invisivel",
  "headline": "Sinais que a escola<br><em>nao ve</em>",
  "features": [
    "Queda de presenca semanal",
    "Sem resposta a comunicados",
    "Menos engajamento no dia a dia"
  ]
}
```

---

## SLIDE 05 — Texto

Mesmos campos e regras do Slide 02.

---

## SLIDE 06 — Numero

Mesmos campos e regras do Slide 03.

---

## SLIDE 07 — CTA

| Campo | Max. total | Max. por linha | `<br>` permitido |
|-------|-----------|----------------|-----------------|
| **Eyebrow** | 28 chars | — | Nao |
| **Headline** | 45 chars | 25 chars | Max. 1 · `<em>` na ultima linha |
| **Subhead** | 55 chars | 30 chars | Max. 1 · regra 40% |
| **Button** | 28 chars | — | Nao |

Exemplo valido:
```json
{
  "tipo": "cta",
  "eyebrow": "Sua escola pode chegar antes",
  "headline": "Quer ver risco de<br><em>evasao antes?</em>",
  "subhead": "Mostre como o Skolen<br>funciona na pratica.",
  "button": "Solicitar Demonstracao"
}
```

---

## Formatacao inline

| Sintaxe | Efeito | Quando usar |
|---------|--------|-------------|
| `<em>texto</em>` | Cor dominante do slide | Palavra-chave da headline — sempre na ultima linha |
| `<strong>texto</strong>` | Negrito extra | Apenas no campo `body` do slide de texto |
| `<br>` | Quebra de linha | Seguir os limites por campo acima |

---

## SLIDE 01 — Cover DM (formato "Pergunta que todo gestor já se fez")

Variação do Cover que simula a caixinha de pergunta do Instagram Stories (retângulo branco arredondado com sombra + "rabinho" de balão). Usada como slide 1 do formato "Pergunta que todo gestor já se fez": a pergunta parece recebida via DM, mas é uma dúvida comum do setor, antecipada. Os slides 2–7 seguem os tipos normais (`text`, `number`, `app`, `cta`).

| Campo | Max. total | Max. por linha | `<br>` permitido |
|-------|-----------|----------------|-----------------|
| **Eyebrow** | 22 chars | — | Não |
| **Headline** | 70 chars | 32 chars | Max. 2 (a caixa comporta 3 linhas de texto) |
| **Subhead** | 55 chars | 35 chars | Não |

> Tom da pergunta: precisa soar como algo que um gestor diria de verdade — cru, um pouco inseguro. Evite perguntas com cara de propaganda ("Como o Skolen revolucionou minha escola?").

Exemplo válido:
```json
{
  "tipo": "cover-dm",
  "eyebrow": "Pergunta de gestor",
  "headline": "Como sei que um aluno<br>vai <em>cancelar</em> antes dele avisar?",
  "subhead": "Uma duvida que todo gestor ja teve"
}
```

---

## SLIDE foto-card

| Campo | Max. total | Max. por linha | `<br>` permitido |
|-------|-----------|----------------|-----------------|
| **Label** | 22 chars | — | Não |
| **Headline** | 36 chars | **18 chars** | Max. 1 · regra 40% |
| **Body** | 80 chars | 36 chars | Max. 1 |

> **Atenção:** O `foto-card` divide o slide 50/50 com a imagem. A área de texto tem ~490px de largura com fonte 52px — cada linha comporta no máximo **~18 caracteres**. Headlines longas quebram em 3 linhas e desestabilizam o layout. Escreva curto.

> **`imagem_tipo: "produto"`** — sem frame. A imagem flutua com drop-shadow direto sobre o fundo branco. Ideal para screenshots e mockups com fundo transparente. Os tipos `pessoa`, `print-anotado` e `marca` mantêm seus frames.

Exemplo válido:
```json
{
  "tipo": "foto-card",
  "posicao": "direita",
  "imagem": "Marketing/Assets/produto/aplicativo_view_aluno.png",
  "imagem_tipo": "produto",
  "label": "Na prática",
  "headline": "Boletim por aluno.<br><em>Em tempo real.</em>",
  "body": "O gestor passou a ver quem<br>precisava de atenção agora."
}
```

---

## Template Teste Rápido / Diagnóstico

### `teste-capa`

| Campo | Max. total | Max. por linha | `<br>` permitido |
|-------|-----------|----------------|-----------------|
| **Headline** | 55 chars | 30 chars | Max. 1 |
| **Subhead** | 65 chars | 35 chars | Não |

### `teste-pergunta`

| Campo | Max. total | Max. por linha | `<br>` permitido |
|-------|-----------|----------------|-----------------|
| **Headline** | 65 chars | 32 chars | Max. 1 |

> Escreva a pergunta como frase direta que se responde com Sim/Não. Evite perguntas compostas ("X e Y?") — uma ideia por pergunta.

### `teste-resultado`

| Campo | Max. total | Max. por linha | `<br>` permitido |
|-------|-----------|----------------|-----------------|
| **Criterio** | 40 chars | — | Não |
| **Headline** | 50 chars | 26 chars | Max. 1 · `<em>` na última linha |
| **Segmentos** | inteiro ≤ segmentos_total | — | — |
| **Segmentos_total** | inteiro = número de perguntas do teste | — | — |

### `teste-cta`

Mesmos campos e limites do tipo `cta` (ver Slide 07 — CTA acima), sem o campo `eyebrow`.

---

## O que nunca fazer

- Dois `<br>` em headline de cover ou CTA
- `<em>` em mais de uma palavra por headline
- Feature do slide app com `<br>` — cada feature e uma linha unica
- Headline com linha isolada de 1 a 2 palavras (`muito.` / `nao.` / `cedo.`)
- Subhead com 3 linhas — se nao couber em 2, corte o texto
