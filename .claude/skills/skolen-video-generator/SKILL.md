---
name: skolen-video-generator
description: >
  Gera um vídeo de avatar falando (HeyGen) para a Skolen a partir de um roteiro em
  PT-BR. Usa TTS nativo do HeyGen — sem dependências externas de áudio. Use quando o
  usuário pedir para gerar um vídeo com avatar, um vídeo de porta-voz, ou um reel
  falado pela Skolen.
---

# skolen-video-generator

Gera um vídeo de avatar HeyGen falando um roteiro em português, pronto para publicar
como Reel/Story ou usar como matéria-prima de um anúncio.

Avatar padrão da Skolen: `09dae41419364c3599c1f1ca346d00e8`
(se o usuário não especificar outro `avatar_id`, use este).

---

## PASSO 1 — Coletar o tema

Se não informado, pergunte:
1. **Tema/ângulo** — sobre o que o avatar vai falar? (ex: inadimplência, retenção de
   alunos, rotina da secretaria, um dado ou insight de gestão escolar)
2. **Objetivo** — awareness, consideração ou conversão?
3. **Avatar** — usar o padrão (`09dae41419364c3599c1f1ca346d00e8`) ou outro `avatar_id`?

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
  --avatar-id "09dae41419364c3599c1f1ca346d00e8" \
  --text "<roteiro escolhido, com acentos>" \
  --aspect-ratio "9:16" \
  --out "Marketing/Social/_video-gerados/<slug>.mp4"
```

Onde `<slug>` é um nome descritivo em kebab-case (ex: `inadimplencia-gancho-01`).

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

Crie `Marketing/Social/_video-gerados/<slug>.md`:

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

Arquivo: <slug>.mp4
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

## Regras críticas

- **Nunca** escrever a `HEYGEN_API_KEY` real em arquivos versionados — sempre via
  `.env` (checar `.gitignore` antes, conforme protocolo de credenciais do `CLAUDE.md`
  raiz).
- Roteiro sempre com acentuação completa em pt-BR.
- Aguardar aprovação do roteiro antes de chamar a API (gerar vídeo tem custo).
- Se `HEYGEN_API_KEY` não estiver configurada, parar e pedir para o usuário
  configurá-la — não inventar/mockar resultado.
