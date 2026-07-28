---
name: skolen-video-generator
description: >
  Gera um vídeo de avatar falando (HeyGen) para a Skolen a partir de um roteiro em
  PT-BR. Usa TTS nativo do HeyGen — sem dependências externas de áudio. Use quando o
  usuário pedir para gerar um vídeo com avatar, um vídeo de porta-voz, ou um reel
  falado pela Skolen. Aceita a flag --news para o template de notícia (CTA = manchete
  traduzida, cards de citação com fonte e highlight, avatar no rodapé) a partir de um
  achado do skolen-news-radar.
---

# skolen-video-generator

Gera um vídeo de avatar HeyGen falando um roteiro em português, pronto para publicar
como Reel/Story ou usar como matéria-prima de um anúncio.

Avatar padrão da Skolen: `87289bc673fd4be2a0a275b5d11c1598`
(fundo branco, se mistura bem com o fundo do template de vídeos — se o usuário não
especificar outro `avatar_id`, use este).

Há dois fluxos:
- **Padrão** (PASSO 1 a 5 abaixo) — avatar falando sozinho, sem overlay de texto.
- **`--news`** (seção dedicada no fim deste arquivo) — template de notícia: CTA
  (manchete traduzida) no topo, cards de citação da matéria com fonte e marca-texto
  no meio, avatar no rodapé. Use quando o pedido for para transformar um achado do
  radar de notícias em vídeo.

Há dois **métodos** de geração (ambos alimentam os fluxos acima):
- **API oficial** (`heygen_generate.py`, PASSO 3) — usa a API pública v3 do HeyGen
  com `HEYGEN_API_KEY`. Estável, documentado, mas não expõe o modelo Avatar IV.
- **CDP/Avatar IV** (`heygen_gen_video_cdp.py`) — mesmo endpoint interno que a
  própria interface web do HeyGen usa, via Chrome controlado por Playwright (CDP),
  reaproveitando cookies de uma sessão logada. Usa o modelo Avatar IV
  (`tokyo_v2_1_pde`, `avatar_iv_more_expressive: true`), que costuma render mais
  natural que a API v3. **Ainda em validação para a Skolen** — ver seção
  "Método CDP/Avatar IV" no fim deste arquivo antes de usar em produção.

---

## PASSO 1 — Coletar o tema

Se não informado, pergunte:
1. **Tema/ângulo** — sobre o que o avatar vai falar? (ex: inadimplência, retenção de
   alunos, rotina da secretaria, um dado ou insight de gestão escolar)
2. **Objetivo** — awareness, consideração ou conversão?
3. **Avatar** — usar o padrão (`87289bc673fd4be2a0a275b5d11c1598`) ou outro `avatar_id`?

---

## PASSO 2 — Escrever roteiro e aguardar aprovação

Escreva **3 opções de roteiro**, seguindo o tom da Skolen (educativo, próximo,
direto — ver `Marketing/Social/CLAUDE.md`).

**Duração alvo: 20-30 segundos = ~45-65 palavras** (ritmo de fala do TTS HeyGen é
próximo de 150 palavras/minuto).

Estrutura sugerida:
```
[GANCHO]   ~8 palavras  — situação ou dado que prende atenção nos 3 primeiros segundos
[CORPO]    ~35 palavras — desenvolve o problema/insight, conecta à realidade do gestor escolar
[CTA]      ~12 palavras — ação clara ("conhece a Skolen", "fala com a gente", "vê como funciona")
```

Regras de copy:
- PT-BR com acentuação completa e correta (o TTS do HeyGen pronuncia melhor com
  acentos — nunca escreva o roteiro sem acento)
- Tom direto, sem exagero, sem jargão de tecnologia
- Fala como gestor para gestor — não como vendedor
- Terminar com uma ação clara conectada à proposta da Skolen

Formato de apresentação:

---

**Opção 1 — [ângulo]**
> [roteiro completo]
*XX palavras — ~XXs*

**Opção 2 — [ângulo]**
> ...

**Opção 3 — [ângulo]**
> ...

---

Conte as palavras antes de exibir. **Aguarde o usuário escolher** antes de avançar.

---

## PASSO 3 — Gerar o vídeo

```bash
cd "c:/Users/felipe.fadel/skolen-management"

python .claude/skills/skolen-video-generator/scripts/heygen_generate.py \
  --avatar-id "87289bc673fd4be2a0a275b5d11c1598" \
  --text "<roteiro escolhido, com acentos>" \
  --aspect-ratio "9:16" \
  --out "Marketing/Social/_video-gerados/avatar-simples/<AAAA-MM>/<slug>/raw.mp4"
```

Onde `<slug>` é um nome descritivo em kebab-case (ex: `inadimplencia-gancho-01`) e
`<AAAA-MM>` é o ano-mês corrente (ex: `2026-07`). Ver "Organização das pastas de
vídeo" no fim deste arquivo para o layout completo.

Flags opcionais:
- `--voice-id <id>` — força uma voz específica. Sem essa flag, usa a voz padrão do
  avatar. Para listar vozes em português:
  ```bash
  python .claude/skills/skolen-video-generator/scripts/heygen_list_voices.py --language Portuguese
  ```
- `--background "#RRGGBB"` — cor de fundo (padrão `#FFFFFF`)
- `--aspect-ratio` — `9:16` (Reels/Stories, padrão), `16:9` (YouTube/anúncio horizontal), `1:1` (feed)

O script submete o vídeo, faz poll do status a cada 10s (timeout padrão 600s) e baixa
o MP4 final automaticamente.

**Pré-requisito:** `HEYGEN_API_KEY` configurada em `.env` na raiz do repo (ver
Segurança de Credenciais no `CLAUDE.md` raiz — nunca commitar a chave real).
Se a variável não existir, avise o usuário e pare antes de tentar gerar.

---

## PASSO 4 — Registrar em Marketing/Social

Crie `Marketing/Social/_video-gerados/avatar-simples/<AAAA-MM>/<slug>/registro.md`
(mesma pasta do `raw.mp4` gerado no PASSO 3):

```markdown
---
type: video-avatar
skill: skolen-video-generator
tags: [skolen, video, heygen, avatar]
status: teste
data_postagem:
metricas:
---

# <tema/ângulo>

**Skill:** skolen-video-generator
**Avatar:** <avatar_id>

---

## Roteiro

<roteiro completo>

## Vídeo

Raw (HeyGen): raw.mp4
```

---

## PASSO 5 — Confirmar

Informe:
- Caminho do vídeo gerado
- Roteiro usado
- Duração aproximada
- Próximo passo sugerido (ex: revisar antes de postar, usar como matéria-prima de
  anúncio, publicar via skill de Instagram)

---

# Fluxo `--news` — Template de Notícia

Gera um Reel de avatar a partir de um achado do `skolen-news-radar`
(`Marketing/Social/_news-radar/radar-noticias.md`): CTA (manchete traduzida) fixo no
topo, cards de citação da matéria (com fonte e marca-texto nas palavras-chave) no
meio — trocando em sincronia com o roteiro — e o avatar HeyGen no rodapé.

Renderizado via Remotion, composição `Avatar-News-Template`, em
`Marketing/Anuncios/logo-animation/`.

Ative este fluxo quando o usuário pedir para transformar uma notícia/achado do radar
em vídeo/reel, ou passar a flag `--news`.

---

## NEWS PASSO 1 — Escolher o achado

Se o usuário não apontou uma notícia específica, use a de maior `Score` com
`Status: novo` em `Marketing/Social/_news-radar/radar-noticias.md`. Confirme com o
usuário qual achado antes de prosseguir se houver ambiguidade.

Extraia da entrada do radar:
- **Manchete original** (título do achado)
- **Número-âncora**
- **Fonte** (nome + ano, ex: "EdWeek, 2026")
- **Tradução pra dor da secretaria/gestor**

Achados marcados como "uso interno/estratégico" (lente Concorrência que cita
concorrente nominalmente) **não** viram vídeo público — avise o usuário e pare.

---

## NEWS PASSO 2 — Gerar CTA (título)

O CTA é a manchete da matéria **traduzida para PT-BR e resumida** — não é um hook de
copy novo, é o título da notícia em si, direto.

Regras:
- Máx. ~12 palavras / 2-3 linhas no template (fonte grande, `textWrap: balance`)
- Tradução natural, não literal — mantenha o número-âncora quando ele for o cerne da
  manchete (ex: "Ferramenta prevê quem vai faltar demais — com até 92% de precisão")
- PT-BR com acentuação completa e correta

Apresente **2 opções de CTA** e aguarde o usuário escolher.

---

## NEWS PASSO 3 — Selecionar 2-3 trechos (quotes) com fonte

Extraia da matéria (ou da entrada do radar) 2 a 3 trechos curtos que sirvam como
citação visual — frases que caberiam em um card, não parágrafos. Cada trecho leva:

- `text` — o trecho, com as palavras-chave (número, dado, termo-chave) marcadas
  entre `==...==` para virar marca-texto (highlight) no vídeo.
  Ex: `"precisão de ==88% a 92%==, meses antes dos dados fecharem"`
- `source` — nome da fonte + ano, ex: `"EdWeek, 2026"` ou `"Sponte/TOTVS, 2026"`.
  Use `"Skolen"` como fonte só para a frase final de CTA/fechamento, se houver uma
  que não é citação direta da matéria.

Regra de highlight: marque só o **dado ou termo que sustenta a afirmação** (número,
percentual, nome de estudo) — no máximo 1-2 marcações por trecho. Não marque a frase
inteira.

---

## NEWS PASSO 4 — Escrever roteiro do avatar sincronizado aos trechos

Escreva o roteiro do avatar dividido em **blocos que se alinham 1:1 com os trechos**
do PASSO 3 — cada bloco de fala corresponde ao período em que aquele card de citação
fica em tela. Mesmas regras de copy do PASSO 2 do fluxo padrão (tom direto, gestor
para gestor, acentuação completa).

Duração alvo: 20-30s total (~45-65 palavras, ritmo TTS HeyGen ~150 palavras/min).

Apresente o roteiro completo dividido por bloco, com a duração estimada de cada
bloco (proporcional à contagem de palavras), e aguarde aprovação:

```
[BLOCO 1 — ~Xs] <fala referente ao trecho 1>
[BLOCO 2 — ~Xs] <fala referente ao trecho 2>
[BLOCO 3 — ~Xs] <fala referente ao trecho 3, se houver>
```

---

## NEWS PASSO 5 — Gerar o avatar (HeyGen)

Mesmo script do fluxo padrão, salvando o raw na pasta definitiva do caso
(`Marketing/Social/_video-gerados/news/<AAAA-MM>/<slug>/`, ver "Organização das
pastas de vídeo" no fim deste arquivo):

```bash
cd "c:/Users/felipe.fadel/skolen-management"

python .claude/skills/skolen-video-generator/scripts/heygen_generate.py \
  --avatar-id "87289bc673fd4be2a0a275b5d11c1598" \
  --text "<roteiro completo aprovado, todos os blocos concatenados>" \
  --aspect-ratio "9:16" \
  --out "Marketing/Social/_video-gerados/news/<AAAA-MM>/<slug>/raw.mp4"
```

Depois de baixado, confira a duração real com `ffprobe` — ela define o `start`/`end`
de cada quote no PASSO 6 (os tempos estimados do roteiro podem divergir um pouco do
áudio final gerado):

```bash
ffprobe -v error -show_entries format=duration -of csv=p=0 \
  "Marketing/Social/_video-gerados/news/<AAAA-MM>/<slug>/raw.mp4"
```

---

## NEWS PASSO 6 — Montar as props e renderizar com Remotion

O fundo "branco" do HeyGen sai levemente acinzentado — isso é uma característica do
próprio vídeo do avatar, não do template. O slot do avatar (`AvatarNewsTemplate.tsx`)
usa branco puro (`#FFFFFF`), igual ao resto do frame; não tentar mascarar essa
diferença de tom via colorkey/matting — um teste anterior com colorkey removeu
partes da camiseta branca do avatar junto com o fundo. Não é necessário nenhum
pré-processamento do MP4 do avatar antes deste passo.

O Remotion só resolve `avatarVideoSrc` via `staticFile` dentro de `public/` — copie
o raw pra lá **temporariamente**, só para o render (o arquivo definitivo continua
sendo o `raw.mp4` na pasta do caso; a cópia em `public/avatars/` é descartável):

```bash
cp "Marketing/Social/_video-gerados/news/<AAAA-MM>/<slug>/raw.mp4" \
   "Marketing/Anuncios/logo-animation/public/avatars/<slug>.mp4"
```

Crie um JSON de props (ex: `Marketing/Anuncios/logo-animation/props-<slug>.json`):

```json
{
  "title": "<CTA escolhido>",
  "avatarVideoSrc": "avatars/<slug>.mp4",
  "durationInSeconds": <duração real do MP4, via ffprobe>,
  "quotes": [
    { "start": 0.0, "end": 9.0, "text": "<trecho 1 com ==highlight==>", "source": "<fonte 1>" },
    { "start": 9.0, "end": 18.0, "text": "<trecho 2 com ==highlight==>", "source": "<fonte 2>" },
    { "start": 18.0, "end": <duração total>, "text": "<trecho 3 com ==highlight==>", "source": "<fonte 3>" }
  ]
}
```

Os `start`/`end` de cada quote devem corresponder ao tempo em que o bloco de fala
correspondente (PASSO 4) ocorre no áudio real — ajuste proporcionalmente à contagem
de palavras de cada bloco sobre a duração total.

Renderize direto para a pasta definitiva do caso:

```bash
cd "Marketing/Anuncios/logo-animation"
npx remotion render Avatar-News-Template \
  --props="props-<slug>.json" \
  --output="../../Social/_video-gerados/news/<AAAA-MM>/<slug>/final.mp4"
```

**Pré-requisito:** dependências do projeto instaladas (`npm i` em
`Marketing/Anuncios/logo-animation/`, uma vez só).

Depois de renderizar, limpe os arquivos temporários — nenhum dos dois precisa ficar
versionado, o `final.mp4` já está salvo na pasta definitiva:

```bash
rm "Marketing/Anuncios/logo-animation/props-<slug>.json"
rm "Marketing/Anuncios/logo-animation/public/avatars/<slug>.mp4"
```

---

## NEWS PASSO 7 — Registrar em Marketing/Social

Crie `Marketing/Social/_video-gerados/news/<AAAA-MM>/<slug>/registro.md` (mesma
pasta do `raw.mp4`/`final.mp4`):

```markdown
---
type: video-avatar-news
skill: skolen-video-generator (--news)
tags: [skolen, video, heygen, avatar, news-radar]
status: teste
data_postagem:
metricas:
---

# <CTA>

**Skill:** skolen-video-generator (--news)
**Fonte do achado:** Marketing/Social/_news-radar/radar-noticias.md
**Avatar:** <avatar_id>

---

## Roteiro

<roteiro completo por blocos>

## Citações usadas

1. "<trecho 1>" — <fonte 1>
2. "<trecho 2>" — <fonte 2>
3. "<trecho 3>" — <fonte 3>

## Vídeo

Raw (HeyGen): raw.mp4
Final (renderizado, Avatar-News-Template): final.mp4
```

Depois, atualize o `Status` do achado correspondente em
`Marketing/Social/_news-radar/radar-noticias.md` para `em produção`, referenciando
o caminho do `registro.md`.

---

## NEWS PASSO 8 — Confirmar

Informe: caminho do vídeo final, CTA usado, os 3 trechos/fontes, e próximo passo
sugerido (revisar antes de postar, mover MP4 para pasta de publicação).

---

## Regras críticas

- **Nunca** escrever a `HEYGEN_API_KEY` real em arquivos versionados — sempre via
  `.env` (checar `.gitignore` antes, conforme protocolo de credenciais do `CLAUDE.md`
  raiz).
- Roteiro sempre com acentuação completa em pt-BR.
- Aguardar aprovação do roteiro antes de chamar a API (gerar vídeo tem custo).
- Se `HEYGEN_API_KEY` não estiver configurada, parar e pedir para o usuário
  configurá-la — não inventar/mockar resultado.
- No fluxo `--news`: nunca inventar ou arredondar o número-âncora — usar exatamente
  o valor verificado no radar/fonte primária. Nunca gerar vídeo público sobre achado
  marcado como uso interno/estratégico (lente Concorrência).

---

# Método CDP/Avatar IV (alternativo, em validação)

Portado do projeto vivavr-claude, onde o resultado do Avatar IV rende
visivelmente melhor que a API v3 oficial. Ainda **não validado** com o avatar
da Skolen — usar só quando o usuário pedir explicitamente para testar/usar
este método, não como padrão automático.

## Pré-requisito único (rodar uma vez)

```bash
cd "c:/Users/felipe.fadel/skolen-management"
python .claude/skills/skolen-video-generator/scripts/heygen_save_session.py
```

Abre um Chrome num profile isolado (`Temp\skolen-heygen-playwright-profile`,
não interfere no Chrome normal do usuário). O usuário loga manualmente na
conta HeyGen da Skolen e confirma no terminal. A sessão fica salva no profile
e é reaproveitada automaticamente nas próximas gerações — não precisa logar de
novo, a menos que o cookie expire.

## Gerar vídeo

```bash
cd "c:/Users/felipe.fadel/skolen-management"

python .claude/skills/skolen-video-generator/scripts/heygen_gen_video_cdp.py \
  --avatar-id "87289bc673fd4be2a0a275b5d11c1598" \
  --voice-id "<voice_id>" \
  --input-text "<roteiro, com acentos, ... para pausas>" \
  --title "<slug>" \
  --orientation "portrait" \
  --out "Marketing/Social/_video-gerados/<tipo>/<AAAA-MM>/<slug>/raw.mp4"
```

Onde `<tipo>` é `news` ou `avatar-simples`, conforme o fluxo em uso — ver
"Organização das pastas de vídeo" no fim deste arquivo.

Diferenças em relação ao `heygen_generate.py`:
- Não usa `HEYGEN_API_KEY` — autentica via sessão de Chrome logada (CDP).
- `--voice-id` é obrigatório (não há voz padrão do avatar nesse endpoint).
- `--orientation` (`portrait`/`landscape`) em vez de `--aspect-ratio`.
- Usa `cross_ref_avatar_id` internamente (Avatar IV) — valor herdado do
  vivavr-claude, **não confirmado** para o avatar da Skolen. Se o rosto/corpo
  no vídeo final vier errado ou estranho, é o primeiro parâmetro a suspeitar;
  reportar ao usuário antes de reusar em produção.
- Abre uma janela do Chrome durante a geração (necessária para a chamada via
  CDP) — normal, não é erro. Some sozinha ao final (cleanup em `finally`, para
  não acumular processos Chrome órfãos).

## Antes de usar em produção

Progresso da validação:
1. ✅ `heygen_save_session.py` rodado, login confirmado (2026-07-28).
2. ✅ Primeiro vídeo de teste gerado — ver
   `Marketing/Social/_video-gerados/news/2026-07/absenteismo-matematica-recuperacao/`
   (status: teste). Confirmação visual da qualidade/rosto ainda pendente do usuário.
3. ⏳ `cross_ref_avatar_id` padrão (herdado do vivavr-claude) ainda não confirmado
   como correto para o avatar da Skolen — não deu erro na geração, mas isso não
   confirma que é o valor ideal.
Só considerar trocar o PASSO 3 do fluxo padrão para este método depois que o
usuário validar visualmente o resultado.

---

# Organização das pastas de vídeo

Todo vídeo gerado por esta skill mora em:

```
Marketing/Social/_video-gerados/<tipo>/<AAAA-MM>/<slug>/
  raw.mp4        — MP4 cru do HeyGen (a fala do avatar). Sempre existe. É a fonte:
                   se algo no template/copy precisar mudar, re-renderiza a partir
                   dele em vez de gerar vídeo novo no HeyGen (que tem custo).
  final.mp4      — só existe quando o fluxo usa template Remotion (--news, ou
                   Avatar-Template com captions). No fluxo padrão sem template,
                   não há final.mp4 — o raw.mp4 já é o vídeo pronto pra publicar.
  registro.md    — roteiro, fontes, avatar/voice_id, status, métricas.
```

`<tipo>`:
- `news/` — fluxo `--news` (template `Avatar-News-Template`, achado do radar).
- `avatar-simples/` — fluxo padrão (avatar falando, com ou sem overlay de
  captions simples via `Avatar-Template`).

`<AAAA-MM>` é o ano-mês em que o vídeo foi gerado (ex: `2026-07`).

Diferenciação teste vs. produção é só o campo `status:` no front-matter do
`registro.md` (`teste`, `em produção`, `publicado`) — não há pasta nem prefixo
de nome separado para isso.

`Marketing/Anuncios/logo-animation/public/avatars/` e
`Marketing/Anuncios/logo-animation/out/` são **apenas working directories do
Remotion** durante o render (PASSO NEWS 6) — nunca o destino final de um vídeo.
Sempre limpar os arquivos temporários criados ali depois de renderizar.
