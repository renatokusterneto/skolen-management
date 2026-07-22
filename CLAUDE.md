# Skolen — Instruções Gerais

> **PROTOCOLO OBRIGATÓRIO — leia antes de qualquer ação:**
> 1. Leia este arquivo (`CLAUDE.md` raiz) **sempre**, independente da tarefa.
> 2. Identifique a pasta em que está trabalhando e leia o `CLAUDE.md` dela.
> 3. Se estiver em uma subpasta, leia também o `CLAUDE.md` dessa subpasta.
> 4. Use **ambos** (raiz + pasta) como contexto combinado para executar a tarefa.
> 5. Leia os arquivos existentes na pasta antes de criar qualquer conteúdo novo.

---

## Identidade do Projeto

**Skolen** é uma empresa de educação. Este repositório centraliza os materiais, estratégias e execução das áreas de Marketing e Vendas.

## Regra Principal

Sempre que iniciar uma tarefa neste projeto:

1. Leia este arquivo (`CLAUDE.md` na raiz) antes de qualquer ação.
2. Se estiver trabalhando dentro de uma subpasta, leia também o `CLAUDE.md` daquela pasta.
3. Use o conteúdo dos arquivos presentes na pasta de trabalho como contexto principal para a tarefa.

## Estrutura do Projeto

```
Skolen/
├── Marketing/
│   ├── Social Media/     → Conteúdo orgânico, redes sociais
│   └── Tráfego Pago/     → Campanhas de anúncios pagos
└── Vendas/               → Scripts, propostas, CRM e estratégias comerciais
```

## Comportamento Esperado

- Sempre adapte o tom e o formato ao contexto da pasta em que está trabalhando.
- Antes de criar qualquer conteúdo, verifique os arquivos existentes na pasta para manter coerência.
- Respeite o contexto de cada área: Marketing não é Vendas, Social Media não é Tráfego Pago.
- Quando houver dúvida sobre o escopo de uma tarefa, pergunte antes de agir.

## Idioma

Português brasileiro, exceto quando explicitamente solicitado em outro idioma.

## Segurança de Credenciais

Sempre que uma tarefa envolver chaves de API, tokens, secrets ou qualquer credencial:

1. Nunca escreva o valor real da credencial em arquivos versionados (código, documentação, configs de exemplo).
2. Antes de criar ou editar qualquer arquivo que vá conter uma credencial real, verifique se ele (ou o padrão dele, ex. `.env`) já está no `.gitignore`. Se não estiver, adicione a entrada ao `.gitignore` **antes** de escrever a credencial.
3. Use `.env.example` (ou equivalente) como template público, apenas com placeholders — nunca com valores reais.
4. Antes de qualquer `git add`/commit, revise os arquivos staged em busca de segredos, mesmo em arquivos com nome inofensivo.
