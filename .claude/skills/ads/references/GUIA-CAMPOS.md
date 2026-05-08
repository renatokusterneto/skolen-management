# Guia de Campos — Static Ads Skolen
> Fonte Nunito · Todos os limites garantem que o layout não quebre

---

## TEXT — Texto / Hook

### Opções de arquivo

| Arquivo | Formato | Funil |
|---------|---------|-------|
| `Text/Text-1-feed.html` | 1080×1080px (Feed) | TOFU |
| `Text/text-1-story.html` | 1080×1920px (Story) | TOFU |

### Campos editáveis

**`Text-1-feed.html`**

| Campo | Onde editar | Máx. caracteres | Exemplo atual |
|-------|-------------|-----------------|---------------|
| **Eyebrow** | `<p class="eyebrow">` | **22 chars** | `Gestão Escolar` |
| **Headline** | `<h1 class="headline">` | **45 chars** (com `<br>`) | `6 horas por dia em tarefas manuais?` |
| **Subhead** | `<p class="subhead">` | **65 chars** (com `<br>`) | `Sua secretária merece trabalhar, não apagar incêndio.` |

> **Destaque em subhead:** usar `<strong>` renderiza na cor `--yellow`  
> **Destaque em headline:** usar `<em>` renderiza na cor `--pink`

---

**`text-1-story.html`**

| Campo | Onde editar | Máx. caracteres | Exemplo atual |
|-------|-------------|-----------------|---------------|
| **Eyebrow** | `<p class="eyebrow">` | **28 chars** | `Para Diretores de Escola` |
| **Question / Headline** | `<h1 class="question">` | **45 chars** (com `<br>`) | `Quantas horas sua secretária perde por semana?` |
| **Subtext** | `<p class="subtext">` | **95 chars** (com `<br>`) | `Matrículas, boletos e comunicados no manual são coisa do passado.` |

> **Destaque em question:** usar `<em>` renderiza na cor `--yellow`

---

## NUMBER — Número / Estatística

### Opções de arquivo

| Arquivo | Formato | Funil |
|---------|---------|-------|
| `Number/text-numero-story.html` | 1080×1920px (Story) | MOFU |

> Versão feed ainda não disponível nesta pasta.

### Campos editáveis

**`text-numero-story.html`**

| Campo | Onde editar | Máx. caracteres | Exemplo atual |
|-------|-------------|-----------------|---------------|
| **Eyebrow** | `<p class="eyebrow">` | **28 chars** | `Cobrança Automática` |
| **Número / Stat** | `<div class="stat">` | **6 chars** | `-68%` |
| **Descrição do stat** | `<h2 class="stat-label">` | **55 chars** (com `<br>`) | `Redução de inadimplência nos primeiros 60 dias` |
| **Subtext** | `<p class="subtext">` | **75 chars** (com `<br>`) | `Régua de cobrança automática do 1º ao último boleto em atraso.` |

> **Destaque em stat-label:** usar `<em>` renderiza na cor `--pink`  
> **Cor do número:** trocar `color: var(--pink)` na classe `.stat` por `--yellow`, `--teal` ou `--blue`

---

## APP — App com Mockup de Celular

### Opções de arquivo

| Arquivo | Formato | Funil |
|---------|---------|-------|
| `App/text-app.html` | 1080×1080px (Feed) | MOFU |
| `App/text-app-story.html` | 1080×1920px (Story) | MOFU |

### Campos editáveis

**`text-app.html` (feed)**

| Campo | Onde editar | Máx. caracteres | Exemplo atual |
|-------|-------------|-----------------|---------------|
| **Eyebrow** | `<p class="eyebrow">` | **22 chars** | `App para Famílias` |
| **Headline** | `<h2 class="headline">` | **40 chars** (com `<br>`) | `Seus pais merecem um app dedicado.` |
| **Feature 1** | 1º `<li>` da `.feature-list` | **30 chars** | `Comunicados instantâneos` |
| **Feature 2** | 2º `<li>` da `.feature-list` | **30 chars** | `Boletos e pagamentos` |
| **Feature 3** | 3º `<li>` da `.feature-list` | **30 chars** | `Notas e presença` |

> **Cor dos dots de feature:** trocar `background:var(--teal)` por `--pink`, `--blue` ou `--yellow` no atributo `style` de cada `.feature-dot`  
> **Destaque em headline:** usar `<em>` renderiza na cor `--blue`

---

**`text-app-story.html` (story)**

| Campo | Onde editar | Máx. caracteres | Exemplo atual |
|-------|-------------|-----------------|---------------|
| **Eyebrow** | `<p class="eyebrow">` | **22 chars** | `App para Famílias` |
| **Headline** | `<h2 class="headline">` | **40 chars** (com `<br>`) | `Seus pais merecem um app dedicado.` |
| **Feature 1** | 1º `<li>` da `.feature-list` | **30 chars** | `Comunicados instantâneos` |
| **Feature 2** | 2º `<li>` da `.feature-list` | **30 chars** | `Boletos e pagamentos` |
| **Feature 3** | 3º `<li>` da `.feature-list` | **30 chars** | `Notas e presença` |

> Mesmos campos e regras do feed. Layout empilhado: headline no topo, mockup no meio, features na base.

---

## DEPOIMENTO — Prova Social / Quote

### Opções de arquivo

| Arquivo | Formato | Funil |
|---------|---------|-------|
| `Depoimento/social-1-feed.html` | 1080×1080px (Feed) | MOFU |
| `Depoimento/social-1-story.html` | 1080×1920px (Story) | MOFU |

### Campos editáveis

**`social-1-feed.html`**

| Campo | Onde editar | Máx. caracteres | Exemplo atual |
|-------|-------------|-----------------|---------------|
| **Nome do autor** | `<p class="attr-name">` | **30 chars** | `Diretora Carla M.` |
| **Cargo / escola** | `<p class="attr-role">` | **40 chars** | `Escola Privada · Minas Gerais` |
| **Citação** | `<p class="quote-text">` | **80 chars** (com `<br>`) | `A secretária quis usar desde o primeiro dia.` |
| **Botão CTA** | `<button class="cta-btn">` | **28 chars** | `Agende uma demonstração` |

> **Destaque em citação:** usar `<em>` renderiza na cor `--pink`  
> **Avatar:** o elemento `.avatar` usa gradiente padrão. Para foto real, substituir por `<img>` com `border-radius:50%`

---

**`social-1-story.html`**

| Campo | Onde editar | Máx. caracteres | Exemplo atual |
|-------|-------------|-----------------|---------------|
| **Nome do autor** | `<p class="t5-attr-name">` | **30 chars** | `Diretora Carla M.` |
| **Cargo / escola** | `<p class="t5-attr-role">` | **40 chars** | `Escola Privada · Minas Gerais` |
| **Citação** | `<p class="t5-quote-text">` | **80 chars** (com `<br>`) | `A secretária quis usar desde o primeiro dia.` |
| **Botão CTA** | `<button class="t5-cta-btn">` | **28 chars** | `Agende uma demonstração` |

> Mesmos campos e regras do feed. As estrelas são fixas (5 estrelas amarelas) — remova os SVGs se quiser menos estrelas.

---

## ANTES E DEPOIS — Lista de Itens

### Opções de arquivo

| Arquivo | Formato | Funil |
|---------|---------|-------|
| `Antes e Depois/Antesedepois-feed.html` | 1080×1080px (Feed) | BOFU |
| `Antes e Depois/antesedepois-story.html` | 1080×1920px (Story) | BOFU |

### Campos editáveis

**Cabeçalho (ambos os formatos)**

| Campo | Onde editar | Máx. caracteres | Exemplo atual |
|-------|-------------|-----------------|---------------|
| **Título do header** | `<span class="header-title">` | **38 chars** | `Escolas antes e depois do` |

**Coluna "Antes" — itens com ✕**

| Campo | Onde editar | Máx. chars por item | Exemplo atual |
|-------|-------------|---------------------|---------------|
| **Item 1** | 1º `.t7-item` (feed) / `.col-item` (story) | **28 chars** | `WhatsApp sem controle` |
| **Item 2** | 2º item | **28 chars** | `Boletos no Excel` |
| **Item 3** | 3º item | **28 chars** | `Matrícula em papel` |
| **Item 4** | 4º item | **28 chars** | `Cobrança manual` |
| **Item 5** | 5º item | **28 chars** | `Pais sem acesso a notas` |
| **Item 6** | 6º item | **28 chars** | `Relatórios no papel` |

**Coluna "Com Skolen" — itens com ✓**

| Campo | Onde editar | Máx. chars por item | Exemplo atual |
|-------|-------------|---------------------|---------------|
| **Item 1** | 1º item da coluna after | **28 chars** | `App dos pais integrado` |
| **Item 2** | 2º item | **28 chars** | `Cobrança automática` |
| **Item 3** | 3º item | **28 chars** | `Matrícula online` |
| **Item 4** | 4º item | **28 chars** | `Régua de cobrança` |
| **Item 5** | 5º item | **28 chars** | `Notas e presença online` |
| **Item 6** | 6º item | **28 chars** | `Dashboard financeiro` |

> **Número de itens:** feed suporta até 6 por coluna; story suporta até 6 por coluna empilhadas verticalmente. Remova ou adicione blocos `.t7-item` / `.col-item` conforme necessário.  
> **Ícones:** fixos (`✕` e `✓`). Para trocar, edite o conteúdo dentro de `.t7-item-icon` / `.col-item-icon`.

---

## ANTES E DEPOIS VISUAL — Com Imagens

### Opções de arquivo

| Arquivo | Formato | Funil |
|---------|---------|-------|
| `antes-depois-visual/feed.html` | 1080×1080px (Feed) | BOFU |

> Versão story ainda não disponível nesta pasta.

### Campos editáveis

| Campo | Onde editar | Máx. caracteres | Exemplo atual |
|-------|-------------|-----------------|---------------|
| **Título linha 1** | 1º `<span class="header-title">` | **35 chars** | `Pais de alunos antes e depois` |
| **Título linha 2** | 2º `<span class="header-title">` (inline) | **10 chars** | `de usar o` |
| **Imagem "Antes"** | `<img src="...">` dentro de `.panel-before` | URL ou caminho local | `https://picsum.photos/seed/sad/520/700` |
| **Imagem "Com Skolen"** | `<img src="...">` dentro de `.panel-after` | URL ou caminho local | `https://picsum.photos/seed/happy/520/700` |

> **Filtro na imagem "Antes":** o atributo `filter:grayscale(60%)` deixa a imagem acinzentada. Para remover o efeito, apague essa propriedade.  
> **Labels dos painéis:** `Antes` e `Com Skolen` estão em `.panel-label-text` — edite diretamente se necessário.

---

## Regras gerais

- **Negrito / destaque** no texto: usar `<em>` (itálico desabilitado; renderiza na cor de destaque do template)
- **Quebra de linha manual:** usar `<br>` dentro das tags de texto
- **Cores disponíveis:** `--yellow` `#F5C842` · `--teal` `#5ECBA8` · `--pink` `#E87DB0` · `--blue` `#5A8ED4`
- **Não alterar** tamanhos de fonte, paddings ou estrutura HTML para garantir que o layout não quebre
- **Imagens externas:** substituir o atributo `src` da `<img>` por URL pública ou caminho local relativo
