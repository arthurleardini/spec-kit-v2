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
   - **Catálogo de Integrações ausente** — `requisitos-transversais.md` deve ter a seção `## Integrações` com a **matriz** (`| Sistema / fonte | Papel (consolidado) | Direção | Criticidade / fallback | Features que usam |`). Reportar se a seção ou a tabela faltar.
   - **Linha de referência a Integrações ausente** — todo `Requisitos/<feature>.md` (Cap. 2.3 RNF) deve conter a **linha** `**Integrações:** ver [catálogo transversal](../requisitos-transversais.md) (§ Integrações) — esta feature usa: …` (ou "nenhuma integração externa"), **não** a tabela completa. Reportar features que não têm a linha — e features que ainda trazem uma tabela `Interoperabilidade / Integrações` própria (regressão a corrigir).
   - **Sistema citado fora do catálogo** — cada sistema nomeado na linha de referência de uma feature deve existir na matriz `## Integrações` do transversal. Reportar sistemas citados que não constam do catálogo.
   - **Arquivo fora-de-escopo malformado** — todo `_archive/*.md` que seja feature arquivada deve ter, no frontmatter (1ª linha, YAML válido), `status: fora-escopo`, e um banner `> **FORA DE ESCOPO** — …` logo após o frontmatter. Reportar os que faltam um ou outro.
   - **`index.md` sem seção fora-de-escopo** — se existir ao menos um `_archive/*.md` com `status: fora-escopo`, o `index.md` deve ter a seção `## Fora de escopo (arquivado — não priorizado)` listando-os. Reportar se a seção faltar ou estiver incompleta.
3. Montar o relatório agrupado por tipo de problema, com caminho do arquivo e, quando aplicável, linha/contexto.
4. Reportar no `refined/log.md` — anexar entrada `## [YYYY-MM-DD] lint | <resumo>` com a contagem por categoria.
5. Se o relatório for grande (muitos itens), criar uma página detalhada em `refined/_archive/` e referenciá-la na entrada do `log.md`.

## Saída
- Relatório de health-check com links quebrados, páginas órfãs, lacunas `⚠` por página, páginas sem `## Relacionado`, `requisitos-transversais.md` sem a seção `## Integrações`/matriz, features sem a linha de referência ao catálogo de integrações (ou que ainda trazem a tabela por feature), sistemas citados fora do catálogo, arquivos `_archive/` fora-de-escopo malformados (sem `status: fora-escopo` ou sem banner) e `index.md` sem a seção fora-de-escopo quando há arquivados.
- Entrada de `lint` no `log.md`; página em `refined/_archive/` quando o relatório for substancial.
