---
name: spec-wiki
description: Use quando o usuário quer manter o wiki em uso — integrar uma fonte nova (ingest) ou consultar o wiki (query). Manutenção contínua da spec depois de criada.
---

# spec-wiki

Ações de **manutenção contínua** do wiki wikiLLM, depois que a spec já existe. Duas ações:
- **`ingest`** — integrar uma fonte nova ao wiki.
- **`query`** — consultar o wiki e responder com citações.

## Quando usar
Quando o usuário traz uma informação/documento novo para incorporar à spec (`ingest`), ou faz uma pergunta a ser respondida a partir do wiki (`query`).

## Entrada
- **ingest:** a fonte nova — conversa, documento ou arquivo. Se for binário (PDF/DOCX/PPTX), converter com `markitdown` antes de ler.
- **query:** a pergunta do usuário.

## Processo

### ingest
1. Ler a fonte nova (converter para Markdown antes, se preciso).
2. Discutir os takeaways com o usuário e registrar um resumo em `trusted/` (se o wiki usa pipeline trusted).
3. Propagar o conteúdo para os documentos afetados — `visao.md` (na raiz) e os docs em `Requisitos/`.
4. Onde a fonte nova contradiz o que já está escrito, **marcar `⚠ CONTRADIÇÃO — ver <página>`** — nunca sobrescrever em silêncio.
5. Atualizar `refined/index.md` (novas páginas / descrições) e anexar entrada em `refined/log.md` (`## [YYYY-MM-DD] ingest | <título>`).
6. Recomendar rodar `spec-navigator` para regenerar os HTMLs.

### query
1. Ler `refined/index.md` **primeiro** — é o catálogo de tudo.
2. Identificar as páginas relevantes pelo índice e lê-las.
3. Responder com **citações** — links relativos para as páginas e IDs que sustentam a resposta.
4. Se a resposta for valiosa/reutilizável, arquivá-la em `refined/_archive/` — isso dispara um mini-ingest: atualizar `index.md` e anexar entrada em `log.md` (`## [YYYY-MM-DD] query | <título>`).

## Saída
- **ingest:** documentos do wiki atualizados, conflitos marcados com `⚠ CONTRADIÇÃO`, `index.md` e `log.md` atualizados.
- **query:** resposta com citações; opcionalmente uma página nova em `refined/_archive/` com `index.md`/`log.md` atualizados.
