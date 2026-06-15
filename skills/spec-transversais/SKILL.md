---
name: spec-transversais
description: Use quando o usuário quer gerar ou manter os documentos transversais de uma spec wikiLLM — o modelo de dados canônico, os requisitos transversais (RNF-T/RF-T) e o catálogo de telas comuns (arquétipos) — e emagrecer as features para que apenas os referenciem.
---

# spec-transversais

Gera e mantém os **três documentos transversais** na raiz de `refined/`, que concentram o
que é comum a várias features para que **nenhuma feature precise duplicá-lo**:

- `refined/modelo-dados.md` — **modelo de dados canônico**: as entidades do domínio num
  único modelo compartilhado (`## Entidades` + `## Relações` + `erDiagram` em Mermaid).
- `refined/requisitos-transversais.md` — **requisitos cross-cutting**: não-funcionais
  `RNF-T-<categoria>-NN` por categoria + funcionais `RF-T-NN`.
- `refined/telas-comuns.md` — **arquétipos de tela** `A-NN`, cada um com um wireframe e a
  linha "Quando usar".

Responde à pergunta-mãe *O que se repete entre as features — e deve viver num só lugar?*

## Princípio: transversal-first

Pensar **transversalmente, não por feature**. Um único modelo de dados, um conjunto de
`RNF-T-*`/`RF-T-*`, um catálogo de arquétipos de tela — e features que **referenciam** esses
transversais e descrevem só o que é específico. Isso **minimiza o número de telas e a
complexidade**, elimina a duplicação (a mesma entidade/requisito/tela remodelada em cada
feature) e dá IDs estáveis para cross-reference.

## Quando usar
Quando o usuário pede para criar ou atualizar o modelo de dados canônico, consolidar os
requisitos transversais (RNF-T/RF-T), montar o catálogo de telas comuns / arquétipos, ou
"emagrecer"/"deduplicar" as features para que apontem para os transversais. Roda depois que
a Visão existe e há ≥ 2 features (ou para consolidar uma spec já escrita por feature).

## Entrada
- `refined/visao.md` — Glossário (§2) e Regras (§3) ancoram a terminologia e os `RN-NN`.
- `refined/Requisitos/<feature>.md` — todas as features existentes (fonte do scan).
- `refined/componentes.md` — vocabulário genérico de componentes (citado por `telas-comuns`).
- Templates: `templates/transversais/{modelo-dados,requisitos-transversais,telas-comuns}.md`.

## Workflow transversal-first

### 1. Modelo de dados (`modelo-dados.md`)
1. Varrer o **Cap. 3 (Dados)** de cada `Requisitos/<feature>.md` (e, em specs antigas, o
   antigo Cap. 4) e o Glossário da Visão.
2. **Extrair as entidades canônicas:** as que aparecem em ≥ 2 features (ou são entidades de
   domínio centrais). Para cada uma, definir a **feature-lar** (a que a define/alimenta) e
   consolidar campos, citando a `RN-NN` que governa cada campo quando houver.
3. Escrever `## Entidades` (uma subseção por entidade), `## Relações` (cardinalidades em
   prosa) e o bloco ` ```mermaid ` `erDiagram`. Tabelas de execução/log de uma única
   feature **não** entram aqui (ficam no Cap. 3 da feature, referenciando a entidade).

### 2. Requisitos transversais (`requisitos-transversais.md`)
1. Varrer o **Cap. 2 (Requisitos & Cenários)** de cada feature (RFs, RNFs, CTs).
2. **Detectar os requisitos comuns:** os que se repetem quase idênticos em ≥ 2 features.
   Promovê-los a `RNF-T-<categoria>-NN` (por categoria: Segurança, Auditoria, Performance,
   Disponibilidade, Observabilidade, Conformidade, …) ou `RF-T-NN`. Registrar em
   `*Subsume:*` quais requisitos de feature cada transversal substitui (rastreabilidade).
3. IDs estáveis; ao remover, manter o número vago. Valores numéricos são parâmetros de
   instância.

### 3. Telas comuns (`telas-comuns.md`)
1. Varrer o **Cap. 1 (Telas & Fluxos)** de cada feature — os `#### T-NN` e seus wireframes.
2. **Identificar os arquétipos:** padrões de layout/comportamento que se repetem (dashboard,
   lista/fila, formulário de configuração, detalhe, linha do tempo, fila de aprovação,
   editor/canvas, comparação, visão 360, construtor de consulta, …). Atribuir IDs `A-NN`.
3. Para cada arquétipo: descrição, um wireframe na DSL `wireframe`, a linha **Quando usar**,
   os **Componentes** genéricos e (opcional) as **Instâncias** por feature.

### 4. Emagrecer as features (slim-down)
Depois de consolidar os três docs, **revisar cada `Requisitos/<feature>.md`** para que
apenas referencie os transversais:
- **Cap. 1:** cada `T-NN` declara `**Arquétipo:** A-NN` e descreve só o que muda; fundir
  telas redundantes em abas/drawers quando o arquétipo permitir (minimizar telas).
- **Cap. 2:** trocar requisitos comuns por citações de `RNF-T-*`/`RF-T-*` no bloco
  "Transversais aplicáveis"; manter só o que é próprio da feature.
- **Cap. 3:** trocar a re-modelagem de entidades canônicas por referência a
  `modelo-dados.md`; manter só entidades/campos próprios (configs, logs, execução).
Nunca apagar conteúdo em silêncio que diverge do transversal — quando uma feature diverge
(ex.: threshold próprio), o valor da feature **prevalece** e fica documentado nela.

## Manutenção
Ao surgir uma feature nova ou um requisito/entidade/tela recorrente, **promover ao
transversal** em vez de duplicar. Manter os IDs estáveis. Ao concluir, atualizar
`refined/index.md` (entradas dos 3 docs sob "Transversais") e anexar entrada em
`refined/log.md`. Rodar `spec-navigator` para regenerar o navegador (os 3 docs aparecem no
submenu **Transversais**).

## Saída
- `refined/modelo-dados.md`, `refined/requisitos-transversais.md` e `refined/telas-comuns.md`
  na raiz de `refined/`, com frontmatter `tipo: contract`.
- As `Requisitos/<feature>.md` emagrecidas, referenciando os transversais por ID/nome.
- `index.md` e `log.md` atualizados.
