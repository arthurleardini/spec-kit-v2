---
name: spec-scaffold
description: Use quando o usuário quer iniciar uma spec nova — cria o `spec.md` único do produto a partir do template, mais o `CLAUDE.md` do repositório. Primeiro passo de uso do spec-kit.
---

# spec-scaffold

Cria a spec de um produto: **um arquivo**, `spec.md`, a partir de `templates/spec.md`.

Roda uma vez por produto, antes de qualquer skill geradora.

## Quando usar
Quando o usuário pede para começar uma spec nova, montar o esqueleto de uma
especificação ou inicializar um repositório de spec.

## Entrada
- Diretório onde a spec vai viver.
- Nome do produto.

## Processo
1. Confirmar diretório e nome do produto.
2. Copiar `templates/spec.md` → `<dir>/spec.md`, substituindo `<Produto>` e `<AAAA-MM-DD>`.
3. Copiar `templates/CLAUDE.md` → `<dir>/CLAUDE.md` (regras de escrita que o agente lê
   antes de tocar na spec).
4. Criar `<dir>/criticas/` (vazio) — é onde o loop crítico grava os ledgers.
5. Não preencher conteúdo. Cada seção é preenchida pela skill dona dela:

   | Seção | Skill |
   |---|---|
   | 1 Contexto · 2 Glossário · 3 Regras de negócio | `spec-contexto` |
   | 4 Modelo de dados · 5 Requisitos transversais · 6 Arquétipos de tela | `spec-transversais` |
   | 7.N.1 Fluxo e navegação · 7.N.2 Telas | `feature-telas-fluxos` |
   | 7.N.3 Requisitos funcionais · 7.N.4 Cenários de teste | `feature-requisitos` |
   | 7.N.5 Dados | `feature-dados` |
   | Anexo B Cadeia de valor | `spec-cadeia-valor` |

## Estrutura criada

```
<dir>/
  spec.md          # a especificação — arquivo único
  CLAUDE.md        # regras de escrita do projeto
  criticas/        # ledgers do loop crítico
```

Não existem `index.md`, `log.md`, `overview.md`, `blueprint.md`, `componentes.md`, nem
pasta `Requisitos/`. Uma spec não é um wiki: sumário é a numeração das seções, histórico
é o git, e o que era documento transversal virou seção.

## Saída
`spec.md` e `CLAUDE.md` criados a partir dos templates, com produto e data preenchidos, e
`criticas/` pronto para o loop crítico.
