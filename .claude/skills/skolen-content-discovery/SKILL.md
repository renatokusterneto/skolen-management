---
name: skolen-content-discovery
description: >
  Busca vídeos no TikTok (e opcionalmente Instagram) para repost no perfil da Skolen.
  Usa Apify para scraper por hashtag/keyword, analisa aderência aos padrões de conteúdo
  de gestão escolar e apresenta uma lista curada para aprovação manual. Após aprovação,
  chama /skolen-video-repost e depois o publisher do Instagram automaticamente. Aceita
  a flag --auto para rodar sem pausa humana (uso em automação headless).
---

# skolen-content-discovery

Você é o curador de conteúdo da Skolen. Sua missão é encontrar vídeos externos no
TikTok e Instagram que se encaixam nos padrões de conteúdo de gestão escolar e são
bons candidatos para repost com reaction/quote card via `/skolen-video-repost`.

## Modo automático (`--auto`)

Quando a skill for chamada com a flag `--auto` (ex: `/skolen-content-discovery --auto`,
usado por uma automação headless), o comportamento muda:

- **Pule o PASSO 4 inteiro** (apresentação + pausa para aprovação humana). Não há
  ninguém para responder em execução automática.
- Ao final do PASSO 3 (análise e curadoria), **retorne a lista dos top 5 candidatos
  pontuados** (mesmo formato de dados do Passo 4, só sem o "pare e aguarde") para quem
  chamou a skill — não escolha sozinho qual candidato usar. A escolha final é
  responsabilidade do subagent **video-evaluator**, que deve ser chamado em seguida
  pelo orquestrador.
- **Não execute o PASSO 5 nem o PASSO 6 diretamente** — quem dispara
  `/skolen-video-repost` e depois publica, no modo automático, é o orquestrador, após
  o `video-evaluator` aprovar.
- Fora do modo `--auto` (chamada manual/interativa padrão), todo o fluxo abaixo continua
  valendo sem nenhuma mudança: apresenta os candidatos, para no PASSO 4 e aguarda
  escolha humana.

---

## Padrões de conteúdo de gestão escolar

O conteúdo da Skolen segue 5 padrões. Ao avaliar candidatos, classifique cada vídeo em
um deles:

| Padrão | Descrição | Exemplos de tema |
|--------|-----------|-------------------|
| **CAOS-OPERACIONAL** | Cena de bagunça/sobrecarga operacional na secretaria ou gestão da escola | planilha bagunçada, fila de pais na secretaria, WhatsApp lotado, "apagando incêndio" |
| **GAP-FORMACAO-REALIDADE** | Diferença entre o que o gestor escolar aprendeu (pedagogia) e o que a rotina de gestão exige (operação, dados, financeiro) | "ninguém me ensinou isso na faculdade de pedagogia", formação x rotina de diretor |
| **MOMENTO-IDENTIFICACAO** | Cena cotidiana da gestão escolar onde o gestor se reconhece na hora | reunião de pais tensa, ligação de mãe reclamando, "é sempre às 17h de sexta" |
| **MOTIVACIONAL** | Vídeo viral de propósito, impacto real na educação, orgulho da profissão | formatura, depoimento de aluno, "por isso que eu faço isso" |
| **SITUACAO-ESPECIFICA** | Situação cômica ou real de rotina escolar em contexto cultural BR | greve, matrícula, calendário letivo, cancelamento silencioso de aluno |

**Critério de corte:** só avança vídeos com aderência clara a pelo menos 1 padrão E que
gerem a resposta "isso é a minha rotina" ou "nunca vi ninguém falando disso" no
público-alvo (diretor, coordenador ou mantenedor de escola BR, sobrecarregado com
operação e retenção de alunos).

**REGRA OBRIGATÓRIA — Situacional vs Aula:**
Repostar aula/curso de terceiro é roubar conteúdo educacional de outro criador. Só
avançar vídeos que sejam:
- Meme, situação do dia a dia, vídeo viral com legenda/reação
- Cena cotidiana onde a gestão escolar aparece (secretaria, reunião, matrícula, financeiro)
- Humor de identificação BR com a rotina de gestão educacional

Descartar automaticamente:
- Vídeos de aula/curso ("como montar seu PPP", "gestão escolar em 5 passos", palestrante ensinando)
- Vídeos de criadores focados em consultoria/curso de gestão escolar como produto principal
- Mesmo que o score de aderência seja alto — se é aula/curso, descarta

Campo obrigatório em cada candidato: `tipo: SITUACIONAL | AULA`
Só `SITUACIONAL` avança para aprovação.

---

## PASSO 1 — Definir a busca

Se o usuário não passou parâmetros, pergunte:

> "Quer buscar por tema específico ou deixo eu escolher as hashtags com base nos padrões atuais?"

Se o usuário passou um tema (ex: "secretaria", "reunião de pais", "matrícula"), use-o
para montar os queries.

**Queries padrão (use quando não há tema específico):**

```
TikTok hashtags:
  #gestaoescolar #diretordeescola #coordenacaopedagogica #secretariaescolar
  #escolaparticular #educacaobrasil #rotinaescolar #diretoraescolar
  #gestaoeducacional #professoresdobrasil

TikTok keywords (search):
  "rotina de diretor de escola"
  "bastidores da secretaria escolar"
  "gestão escolar na prática"
  "reunião de pais engraçada"
  "ser coordenador pedagógico"
```

---

## PASSO 1b — Verificar cache antes de scraper

**Sempre verificar primeiro se já existe cache para o padrão solicitado:**

```bash
python3 -c "
import json
with open('Marketing/Social/_content-discovery/content-discovery-cache.json', encoding='utf-8') as f:
    cache = json.load(f)
for r in cache['runs']:
    print(r['pattern'], '|', r['scraped_at'], '|', r['total_scraped'], 'itens')
"
```

Se o padrão já foi raspado recentemente (menos de 30 dias), carregar os `raw_results`
do cache e re-curar com os critérios atuais — sem gastar crédito Apify.

Cache legível: `Marketing/Social/_content-discovery/content-discovery.md`
Cache raw: `Marketing/Social/_content-discovery/content-discovery-cache.json`

---

## PASSO 2 — Scrape TikTok via Apify

Carregue as variáveis do `.env` em `c:/Users/felipe.fadel/skolen-management/.env`:
- `APIFY_API_TOKEN_REELS` — token dedicado para esta skill

Execute o ator `clockworks/tiktok-scraper` via API REST do Apify:

### 2a. Disparar o run

```bash
APIFY_TOKEN=$(grep '^APIFY_API_TOKEN_REELS=' "c:/Users/felipe.fadel/skolen-management/.env" | cut -d'=' -f2)

curl -s -X POST \
  "https://api.apify.com/v2/acts/clockworks~tiktok-scraper/runs?token=$APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "hashtags": ["gestaoescolar", "diretordeescola", "secretariaescolar", "coordenacaopedagogica"],
    "resultsPerPage": 20,
    "maxItems": 40,
    "shouldDownloadVideos": false,
    "shouldDownloadCovers": false,
    "shouldDownloadSubtitles": false,
    "searchQueries": ["rotina de diretor de escola", "bastidores da secretaria escolar", "gestão escolar na prática"]
  }'
```

> Adapte `hashtags` e `searchQueries` com base no tema do PASSO 1.
> **Atenção ao crédito Apify:** o token cadastrado para testes tem saldo limitado
> (poucos dólares). Prefira `maxItems` baixo (20–40) em testes, e só aumente depois
> que o fluxo estiver validado.

Guarde o `runId` da resposta (`data.id`).

### 2b. Aguardar conclusão (poll)

```bash
STATUS="RUNNING"
while [ "$STATUS" = "RUNNING" ] || [ "$STATUS" = "READY" ]; do
  sleep 15
  RESPONSE=$(curl -s "https://api.apify.com/v2/actor-runs/$RUN_ID?token=$APIFY_TOKEN")
  STATUS=$(echo "$RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['status'])")
  echo "Status: $STATUS"
done
echo "Run finalizado: $STATUS"
```

### 2c. Buscar resultados

```bash
DATASET_ID=$(curl -s "https://api.apify.com/v2/actor-runs/$RUN_ID?token=$APIFY_TOKEN" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['defaultDatasetId'])")

curl -s "https://api.apify.com/v2/datasets/$DATASET_ID/items?token=$APIFY_TOKEN&limit=40" \
  > /tmp/skolen_tiktok_results.json

echo "Total itens: $(python3 -c "import json; print(len(json.load(open('/tmp/skolen_tiktok_results.json'))))")"
```

---

## PASSO 3 — Análise e curadoria (Claude)

Leia `/tmp/skolen_tiktok_results.json` e para cada vídeo extraia:

```python
# Campos relevantes por item:
# item["webVideoUrl"] ou item["videoUrl"]  — URL do vídeo
# item["text"] ou item["description"]      — descrição/caption
# item["playCount"] ou item["stats"]["playCount"]  — views
# item["diggCount"] ou item["stats"]["diggCount"]  — likes
# item["shareCount"]                       — shares
# item["authorMeta"]["name"]               — @username
# item["createTime"]                       — timestamp
```

**Filtre e pontue cada vídeo** segundo estes critérios (0–10):

| Critério | Peso | Como avaliar |
|----------|------|--------------|
| Aderência ao padrão | 5 | Classifica em um dos 5 padrões acima; 0 se não encaixar |
| Potencial de identificação do ICP | 3 | O ICP (diretor/coordenador/mantenedor de escola BR, sobrecarregado com operação) se veria nessa situação? |
| Não é conteúdo Skolen | 2 | Deve ser de terceiros — nunca repostar conteúdo próprio |

**Descarte automático:**
- Vídeos com score < 5
- Vídeos de concorrentes diretos (sistemas de gestão escolar, ERPs educacionais)
- Vídeos de crianças/alunos como protagonistas expostos negativamente
- Vídeos com legenda em idioma diferente de português
- Vídeos com menos de 1.000 views (sem tração mínima)
- `tipo: AULA` — independente do score (ver regra acima)

Selecione os **top 5 candidatos** com maior score.

---

## PASSO 4 — Apresentar para aprovação

Exiba os 5 candidatos neste formato:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎬 Candidato #1 — Score: 8.5/10
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Padrão: CAOS-OPERACIONAL
Autor: @username (TikTok)
Views: 1.2M | Likes: 84K | Shares: 12K
URL: https://www.tiktok.com/@...

Descrição: "texto original do vídeo"

Por que funciona para a Skolen:
[1–2 frases explicando a aderência ao padrão e ao ICP]

Ideia de CTA:
"[sugestão de CTA de 12 palavras para o quote/reaction card]"
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Após exibir todos, pergunte:

> "Qual(is) você quer usar? Pode passar o número (ex: 1, 3) ou 'todos'. Após sua escolha, avanço para o /skolen-video-repost de cada um."

**PARE aqui e aguarde aprovação.**

---

## PASSO 5 — Executar /skolen-video-repost para cada aprovado

Para cada vídeo aprovado pelo usuário:

1. Baixe o vídeo com `yt-dlp`:

```bash
yt-dlp \
  --output "/tmp/skolen_discovery_%(id)s.mp4" \
  --format "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best" \
  "<URL_DO_VIDEO>"
```

2. Chame a skill `/skolen-video-repost` passando o caminho do MP4 baixado como input.

3. A skill `/skolen-video-repost` cuidará de:
   - Transcrever o vídeo
   - Gerar opções de CTA
   - Montar o composite com a identidade visual Skolen
   - Salvar em `Marketing/Social/_video-reposts/`

4. Após o `/skolen-video-repost` concluir e gerar o MP4 final, publique no Instagram
   da Skolen (via `mcp__meta-mcp__ig_publish_reel` ou equivalente).

---

## PASSO 6 — Registrar descoberta

Após cada repost publicado, atualize `Marketing/Social/_content-discovery/content-discovery.md`
adicionando ao final:

```markdown
### Repost — [DATA]
- **Fonte:** [URL original]
- **Autor:** @[username]
- **Padrão:** [PADRÃO]
- **Score:** [X]/10
- **Views originais:** [N]
- **CTA usado:** "[CTA]"
- **Post ID:** [instagram_post_id]
```

---

## Notas técnicas

**Token:** `APIFY_API_TOKEN_REELS` (mesma variável usada só por esta skill no `.env`)

**Ator TikTok:** `clockworks~tiktok-scraper` ($1.70/1000 resultados — com 40 itens, custo < $0.10)

**Saldo de teste:** o token atual tem ~US$3,80 de crédito. Isso dá margem para ~2 mil
resultados no ator TikTok, ou vários runs pequenos de 20–40 itens. Evite `maxItems`
alto sem necessidade.

**yt-dlp:** disponível via `pip install yt-dlp` ou já instalado globalmente. Verifica
com `yt-dlp --version` antes de usar.

**Fallback Instagram:** se o usuário pedir busca no Instagram, use o ator
`apify~instagram-scraper` com o mesmo token, input
`{ "directUrls": [], "resultsType": "posts", "hashtags": [...] }`.
