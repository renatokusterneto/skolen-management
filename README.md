# Skolen — Marketing & Vendas

Repositório central de Marketing e Vendas da Skolen. Centraliza produção de conteúdo, criativos, automações e publicação no Instagram.

---

## Estrutura

```
Skolen/
├── Marketing/
│   ├── Anuncios/          → Criativos de tráfego pago (Meta, Google, LinkedIn)
│   ├── Social/            → Conteúdo orgânico por data
│   │   ├── Carroussel/    → Carrosséis em HTML + PNGs exportados
│   │   └── Reels/         → Scripts e vídeos
│   ├── brand-guidelines   → Identidade visual
│   └── design-system      → Sistema de design
└── Vendas/                → Scripts, propostas, playbooks comerciais
```

---

## Configuração

### 1. Variáveis de ambiente

```bash
cp .env.example .env
```

Preencha o `.env` com suas credenciais (veja cada seção abaixo).

### 2. Google Sheets

A planilha controla o calendário de posts. Estrutura de abas:

| Aba | Uso |
|---|---|
| `pendentes` | Fila de publicação — o Zapier lê daqui |
| `abril_2026` … `dezembro_2026` | Histórico mensal de posts publicados |

**Colunas de cada aba:**

| Coluna | Descrição | Exemplo |
|---|---|---|
| `campaign_id` | Identificador único do post | `evasao-04-04` |
| `tipo` | Formato do conteúdo | `carrousel`, `reel`, `foto` |
| `titulo` | Título interno | `Evasão Invisível` |
| `data_postagem` | Data e hora agendada | `2026-05-15 09:00` |
| `caption` | Legenda completa com hashtags | `Sua escola perde...` |
| `cloudinary_urls` | URLs das imagens separadas por vírgula | `https://res.cloudinary.com/...` |
| `publicado` | Status de publicação | `TRUE` ou `FALSE` |

**Como adicionar um novo post:**
1. Suba as imagens para o Cloudinary na pasta `skolen/social/{campaign_id}/`
2. Adicione uma linha na aba `pendentes` com `publicado = FALSE`
3. O Zapier publica automaticamente no horário agendado e atualiza para `TRUE`

### 3. Cloudinary

As imagens dos posts ficam hospedadas no Cloudinary para que o Instagram possa acessá-las via URL pública.

Estrutura de pastas no Cloudinary:
```
skolen/
└── social/
    └── {campaign_id}/
        ├── slide-01.png
        ├── slide-02.png
        └── ...
```

### 4. Instagram / Meta

O token do Instagram expira em ~60 dias. Para renovar:

1. Acesse `developers.facebook.com/tools/explorer`
2. Selecione o app **Skolen** (ID: `1020557314307868`)
3. Gere novo token com as permissões:
   - `instagram_basic`
   - `instagram_content_publish`
   - `instagram_manage_comments`
   - `instagram_manage_insights`
   - `pages_show_list`
   - `pages_read_engagement`
4. Atualize `INSTAGRAM_ACCESS_TOKEN` no `.mcp.json`
5. Reinicie o Claude Code

---

## Fluxo de Automação (Zapier)

O Zapier publica os posts automaticamente no Instagram com base na planilha.

```
Schedule (a cada hora)
  → Google Sheets: busca linha onde publicado = FALSE na aba pendentes
  → Formatter: formata a data_postagem
  → Filter: verifica se data_postagem <= agora
  → Code (JS): separa as cloudinary_urls em array
  → Paths:
      ├── carrousel → publica carrossel no Instagram
      ├── reel      → publica reel no Instagram
      └── foto      → publica foto no Instagram
  → Google Sheets: atualiza publicado = TRUE
```

**Para configurar o Zapier:**

1. **Worksheet:** sempre apontar para a aba `pendentes`
2. **Lookup column:** `publicado`
3. **Lookup value:** `FALSE`
4. **Search from last row:** `False` (pega o mais antigo primeiro)

---

## Fluxo de Criação de Conteúdo

```
1. Criar slides em HTML  →  Marketing/Social/{nome-do-post}/slide-XX.html
2. Exportar para PNG     →  Marketing/Social/{nome-do-post}/pronto/slide-XX.png
3. Subir no Cloudinary   →  skolen/social/{campaign-id}/
4. Registrar na planilha →  aba pendentes com publicado = FALSE
5. Zapier publica        →  no horário definido em data_postagem
```

---

## Renovação Mensal

No início de cada mês:
1. Verificar se todos os posts do mês anterior estão com `publicado = TRUE`
2. A nova aba do mês (`maio_2026`, etc.) já existe — basta usar como histórico
3. Novos posts entram sempre pela aba `pendentes`
