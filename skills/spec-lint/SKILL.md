---
name: spec-lint
description: Use quando o usuário quer um health-check do wiki — detectar links quebrados, páginas órfãs, lacunas acumuladas e páginas sem seção Relacionado.
---

# spec-lint

Roda um **health-check** do wiki: varre `refined/` em busca de problemas estruturais e reporta o resultado. Mantém o wiki navegável e consistente conforme ele cresce.

## Quando usar
Quando o usuário pede para verificar a saúde do wiki, checar links quebrados, encontrar páginas órfãs, listar as lacunas ainda em aberto, ou fazer uma faxina/auditoria estrutural da spec.

## Entrada
O diretório `<wiki>` que contém `refined/`. Sem outra fonte — o lint só lê o que já está no wiki.

## Processo
1. Varrer todas as páginas `.md` sob `refined/`.
2. Detectar:
   - **Links relativos quebrados** — links `[texto](caminho)` cujo arquivo-alvo não existe.
   - **Páginas órfãs** — páginas `.md` que nenhuma outra página linka (sem link de entrada); ignorar `index.md` e `overview.md`, que são portas de entrada.
   - **Lacunas acumuladas** — ocorrências de `⚠ NÃO IDENTIFICADO` e `⚠ CONTRADIÇÃO`, contadas por página.
   - **Páginas sem `## Relacionado`** — toda página do wiki deve terminar com essa seção.
3. Montar o relatório agrupado por tipo de problema, com caminho do arquivo e, quando aplicável, linha/contexto.
4. Reportar no `refined/log.md` — anexar entrada `## [YYYY-MM-DD] lint | <resumo>` com a contagem por categoria.
5. Se o relatório for grande (muitos itens), criar uma página detalhada em `refined/analyses/` e referenciá-la na entrada do `log.md`.

## Saída
- Relatório de health-check com links quebrados, páginas órfãs, lacunas `⚠` por página e páginas sem `## Relacionado`.
- Entrada de `lint` no `log.md`; página em `refined/analyses/` quando o relatório for substancial.
