# Registro de Content Discovery — Skolen

## Teste de validação — 2026-07-21

Primeiro teste ponta a ponta do fluxo `skolen-content-discovery` com o token Apify
(`APIFY_API_TOKEN_REELS`, saldo inicial ~US$3,81).

- **Ator:** `clockworks/tiktok-scraper`
- **Query:** hashtags `gestaoescolar`, `diretordeescola`, `secretariaescolar` + busca `"rotina de diretor de escola"`
- **maxItems:** 15 (retornou 20 pela paginação do ator)
- **Custo real:** US$0,149 (saldo restante ~US$3,66)
- **Raw salvo em:** `test-run-2026-07-21-raw.json`

### Curadoria aplicada (manual, validando os critérios da skill)

**Descartados — conteúdo delicado/notícia (fora do escopo situacional):**
- @aposttv — diretor investigado por assédio (notícia sensível, jamais usável)
- @draanabeatriz11 — acusação de agressão (notícia sensível)
- @bolderpodcast — caso de polêmica em DCE (notícia/polêmica)

**Descartados — tipo AULA (consultoria/curso, não situacional):**
- @mentora.de.lideres (2 vídeos) — formato ensinamento/consultoria de gestão
- @simonepds06, @escolagestaoeducacional (2 vídeos) — mesmo padrão

**Descartados — tração insuficiente (<1.000 views):**
- @aquarela.papelari41 (88 views), @simonearanha30 (152 views)

**Candidatos SITUACIONAL que avançariam para o Passo 4 (aprovação humana):**

| Autor | Views | Padrão sugerido | Observação |
|---|---|---|---|
| @rotadafe.br | 3,1M | MOTIVACIONAL | Maior tração da amostra; checar tom antes de aprovar |
| @lareya30 | 353K | SITUACAO-ESPECIFICA | Conteúdo em espanhol — fora do ICP BR, descartar na prática |
| @danilotavaressol | 40,9K | CAOS-OPERACIONAL | Falta de servidores/professores — tema de rotina real |
| @reinventandoaeducacao | 40,6K | MOMENTO-IDENTIFICACAO | Sala dos professores — identificação direta |
| @lzzago | 23,1K | MOTIVACIONAL | "Como não amar ser diretor" — tom positivo |
| @angerlania.b | 8,2K | MOMENTO-IDENTIFICACAO | Situação cotidiana de sorte com diretor |
| @telnuza | 6,4K | GAP-FORMACAO-REALIDADE | Expectativa x realidade do cargo |
| @alexandretuller0 | 6,0K | CAOS-OPERACIONAL | "Um dia como diretor" — rotina real |

### Conclusão do teste

- Pipeline Apify → scrape → curadoria funciona ponta a ponta.
- Custo por run pequeno (~20 itens) é baixo (~US$0,15) — dá margem para várias
  iterações antes de esgotar o crédito de teste.
- A amostra trouxe mais ruído de notícia/polêmica do que o esperado com hashtags
  genéricas — vale refinar keywords para termos mais situacionais/humor
  (ex: "bastidores da secretaria", "whatsapp de pais lotado") e não só cargo/hashtag
  institucional, que atrai também conteúdo jornalístico.
