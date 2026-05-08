# Guia de Campos — Carrossel Instagram Skolen
> 1080×1080px · Fonte Nunito · Todos os limites garantem que o layout não quebre

---

## SLIDE 01 — Cover

### Opções de arquivo

| Arquivo | Layout |
|---------|--------|
| `slide-01-cover.html` | Só texto, centralizado |
| `slide-01-cover-imagem.html` | Imagem vertical (esquerda) + texto (direita) |
| `slide-01-cover-imagem-b.html` | Imagem horizontal (topo) + texto (baixo) |
| `slide-01-cover-imagem-c.html` | Texto (topo) + imagem horizontal (baixo) |

### Campos editáveis

| Campo | Onde editar | Máx. caracteres | Exemplo atual |
|-------|-------------|-----------------|---------------|
| **Eyebrow** (título superior) | `.eyebrow` | **22 chars** | `Gestão Escolar` |
| **Headline** (título principal) | `<h1 class="headline">` | **55 chars** (com `<br>`) | `Sua escola ainda perde tempo com papel?` |
| **Subhead** (descrição) | `<p class="subhead">` | **65 chars** (com `<br>`) | `Descubra os 5 sinais que pedem modernização urgente` |
| **Seta** (texto fixo) | `.swipe-hint > span` | **22 chars** | `deslize para ver` |
| **Imagem** *(versões com imagem)* | atributo `src` da `<img>` | URL ou caminho local | `photo-....jpg` |

> **Headline na versão imagem (A):** máx. **35 chars por linha**, até 3 linhas  
> **Headline na versão imagem (B e C):** máx. **45 chars**, até 2 linhas

---

## SLIDE 02 — Texto

### Opções de arquivo

| Arquivo | Layout |
|---------|--------|
| `slide-02-text.html` | Label + Headline + Card com 3 bullets |
| `slide-02-text-sem-card.html` | Label + Headline + Texto corrido |
| `slide-02-text-sem-card-b.html` | Idem (cópia para conteúdo alternativo) |

### Campos editáveis

**`slide-02-text.html` (com card)**

| Campo | Onde editar | Máx. caracteres | Exemplo atual |
|-------|-------------|-----------------|---------------|
| **Label** (pílula superior) | `.label` | **18 chars** | `Sinal #1` |
| **Headline** | `<h2 class="headline">` | **40 chars** (com `<br>`) | `Tempo perdido em tarefas manuais` |
| **Bullet 1** | 1º `.bullet-item > span` | **32 chars** | `Dados digitados várias vezes` |
| **Bullet 2** | 2º `.bullet-item > span` | **32 chars** | `Erros e retrabalho frequentes` |
| **Bullet 3** | 3º `.bullet-item > span` | **32 chars** | `Gestão no apagar incêndios` |

**`slide-02-text-sem-card.html` (sem card)**

| Campo | Onde editar | Máx. caracteres | Exemplo atual |
|-------|-------------|-----------------|---------------|
| **Label** | `.label` | **18 chars** | `Sinal #1` |
| **Headline** | `<h2 class="headline">` | **40 chars** (com `<br>`) | `Tempo perdido em tarefas manuais` |
| **Texto corrido** | `<p class="body-text">` | **130 chars** (com `<br>`) | `Sua secretaria não pode gastar o dia inteiro em planilhas...` |

---

## SLIDE 03 — Número ou Texto

### Opções de arquivo

| Arquivo | Layout |
|---------|--------|
| `slide-03-number-social.html` | Número grande + label + divisor |
| `slide-03-text-sem-card.html` | Label + Headline + Texto corrido |
| `slide-03-text-sem-card-b.html` | Idem (cópia para conteúdo alternativo) |

### Campos editáveis

**`slide-03-number-social.html` (número)**

| Campo | Onde editar | Máx. caracteres | Exemplo atual |
|-------|-------------|-----------------|---------------|
| **Label** (topo) | `.label` | **30 chars** | `Sinal #2 · Inadimplência` |
| **Número/Stat** | `<div class="stat">` | **6 chars** | `68%` |
| **Descrição do stat** | `<h2 class="stat-label">` | **55 chars** (com `<br>`) | `de redução na inadimplência em menos de 60 dias` |

**`slide-03-text-sem-card.html` (texto)** → mesmos campos do slide 02 sem card

---

## SLIDE 04 — App ou Imagem

### Opções de arquivo

| Arquivo | Layout |
|---------|--------|
| `slide-04-app.html` | Texto + lista de features + mockup de app |
| `slide-04-cover-imagem.html` | Imagem vertical (esquerda) + texto (direita) |
| `slide-04-cover-imagem-b.html` | Imagem horizontal (topo) + texto (baixo) |
| `slide-04-cover-imagem-c.html` | Texto (topo) + imagem horizontal (baixo) |

### Campos editáveis

**`slide-04-app.html`**

| Campo | Onde editar | Máx. caracteres | Exemplo atual |
|-------|-------------|-----------------|---------------|
| **Eyebrow** | `.eyebrow` | **30 chars** | `Sinal #3 · App para Famílias` |
| **Headline** | `<h2 class="headline">` | **38 chars** (com `<br>`) | `Pais conectados, escola organizada` |
| **Feature 1** | 1º `.feature-list li` | **30 chars** | `Comunicados em tempo real` |
| **Feature 2** | 2º `.feature-list li` | **30 chars** | `Boletos e pagamentos no app` |
| **Feature 3** | 3º `.feature-list li` | **30 chars** | `Notas e presença na palma da mão` |

**Versões com imagem** → mesmos campos do Slide 01 versões com imagem

---

## SLIDE 05 — Social (Quote) ou Texto

### Opções de arquivo

| Arquivo | Layout |
|---------|--------|
| `slide-05-number-social.html` | Quote limpa centralizada (sem card, sem avatar) |
| `slide-05-text-sem-card.html` | Label + Headline + Texto corrido |
| `slide-05-text-sem-card-b.html` | Idem (cópia para conteúdo alternativo) |

### Campos editáveis

**`slide-05-number-social.html` (quote)**

| Campo | Onde editar | Máx. caracteres | Exemplo atual |
|-------|-------------|-----------------|---------------|
| **Citação** | `<p class="quote-text">` | **85 chars** (com `<br>`) | `"Agora tenho tempo pra atender bem os pais, em vez de digitar planilha."` |
| **Autor** | `<p class="quote-author">` | **55 chars** | `Carla S., Secretária · Escola em Belo Horizonte` |

**`slide-05-text-sem-card.html`** → mesmos campos do slide 02 sem card

---

## SLIDE 06 — Número ou Texto

### Opções de arquivo

| Arquivo | Layout |
|---------|--------|
| `slide-06-number-social.html` | Número grande + label + divisor |
| `slide-06-text-sem-card.html` | Label + Headline + Texto corrido |
| `slide-06-text-sem-card-b.html` | Idem (cópia para conteúdo alternativo) |

### Campos editáveis

**`slide-06-number-social.html` (número)**

| Campo | Onde editar | Máx. caracteres | Exemplo atual |
|-------|-------------|-----------------|---------------|
| **Label** (topo) | `.label` | **30 chars** | `Sinal #5 · Matrículas` |
| **Número/Stat** | `<div class="stat">` | **6 chars** | `3×` |
| **Descrição do stat** | `<h2 class="stat-label">` | **55 chars** (com `<br>`) | `mais rápido para fechar matrículas online` |

**`slide-06-text-sem-card.html`** → mesmos campos do slide 02 sem card

---

## SLIDE 07 — CTA

### Opções de arquivo

| Arquivo | Layout |
|---------|--------|
| `slide-07-cta.html` | Fundo branco, headline, subhead, botão verde |

### Campos editáveis

| Campo | Onde editar | Máx. caracteres | Exemplo atual |
|-------|-------------|-----------------|---------------|
| **Eyebrow** (título superior) | `.eyebrow` | **28 chars** | `Transforme sua escola` |
| **Headline** | `<h2 class="headline">` | **45 chars** (com `<br>`) | `Pronto para modernizar sua gestão?` |
| **Subhead** (descrição) | `<p class="subhead">` | **55 chars** (com `<br>`) | `Demonstração gratuita em 30 minutos. Sem compromisso.` |
| **Botão** | `<button class="cta-btn">` | **28 chars** | `Agendar Demonstração` |

---

## Regras gerais

- **Negrito / destaque** no texto: usar `<em>` (itálico desabilitado, renderiza na cor de destaque do slide)  
  Ex: `perde tempo com <em>papel?</em>`
- **Quebra de linha manual**: usar `<br>` dentro das tags de texto
- **Cor dos bullets** (slides 02/04): trocar `background:var(--yellow)` por `--pink`, `--teal` ou `--blue`
- **Imagens**: substituir o atributo `src` da `<img>` por URL ou caminho local relativo
- **Não alterar** tamanhos de fonte, paddings ou estrutura HTML para garantir que o layout não quebre
