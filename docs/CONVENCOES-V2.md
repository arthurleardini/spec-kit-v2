# Convenções spec-kit v2 — Rodada 1

Fonte única de verdade para a Rodada 1. Decisões vêm de `../../spec-kit/docs/2026-06-14-backlog-v2.md` (cópia em `docs/` do repo original). Tudo aqui se aplica a `spec-kit-v2/`.

## Princípio geral

Padronizar o **mínimo comum**; o resto é opcional por projeto. Menos conceitos, mais robustos. Agentes mais **especialistas** gerando **menos artefatos**. Linguagem de produto **agnóstica** mantida.

## Mudança 1 — Camada de Intenção vira "Visão" (1 doc, 3 capítulos)

Os 5 documentos viram **um único** `refined/visao.md` (na raiz de `refined/`; H1 + 3 capítulos H2):

- `## 1. Produto` — Visão, Proposta de Valor, Personas, Jobs/Necessidades (`JTBD-NN`), Não-objetivos.
- `## 2. Glossário` — Termos do domínio, Convenções de nomenclatura. (guard-rail de linguagem; mantido inteiro)
- `## 3. Regras & Métricas` — Regras de Negócio (`RN-NN`), Regras dependentes de IA (`RN-AI-NN`, só se houver), Métricas de sucesso (NSM + 1-2 guard-rails, `IM-NN`).

Final do doc: `## Questões em aberto`, `## Fontes`, `## Relacionado`.

**IDs preservados:** `JTBD-NN`, `RN-NN`, `RN-AI-NN`, `IM-NN`.
**Saem do mínimo (viram OPCIONAIS, não gerados por padrão):** Princípios (`PR-NN`), Capacidades de IA como doc dedicado (`CAI-NN` — o essencial vira `RN-AI`), Roadmap de evolução, Input/Health metrics detalhadas.

**Skill:** os 5 `intencao-*` viram **um** `skills/intencao-visao/` — o "agente gerador de visão", especialista, que produz/mantém o `visao.md` inteiro. Pode adicionar seções opcionais **só quando pedido**.

## Mudança 2 — Camada de Requisitos: 1 doc por feature, com eixo de granularidade

A antiga "Camada de Contrato" passa a se chamar **Camada de Requisitos**. Por feature, os 4 docs viram **um** `refined/Requisitos/<feature>.md`. Frontmatter inclui `eixo: processo | classe`. Capítulos H2:

- `## 1. Telas & Fluxos` — telas + **diagrama Mermaid** de navegação entre telas.
- `## 2. Histórias` — `US-NN`.
- `## 3. Requisitos & Cenários de Teste` — `RF-NN`, `RNF-*` + cenários de teste (Gherkin-like).
- `## 4. Dados` — modelo **derivado** (não paralelo): se `eixo=classe`, a própria classe é o modelo; se `eixo=processo`, deriva das atividades.

**Eixo:**
- `processo` — fluxo/atividades; o Mermaid do Cap. 1 e/ou um Mermaid de processo (flowchart estilo BPMN leve); dados derivam das atividades.
- `classe` — formulários/objetos; cada formulário ≈ uma classe; a classe já é o modelo de dados.

**Skills:** mantêm-se especialistas, mas **escrevem capítulos** no `Requisitos/<feature>.md` (não arquivos soltos), cientes do `eixo`:
- `contrato-telas-fluxos` → Cap. 1 (com Mermaid).
- `contrato-historias` → Cap. 2.
- `contrato-requisitos` → Cap. 3 (agora inclui cenários de teste).
- `contrato-dados` → Cap. 4 (derivado).
- `contrato-blueprint` → inalterado (product-level PRD).

## Mudança 3 — Mermaid (BL-21)

Blocos ` ```mermaid ` embutidos no markdown:
- Contrato Cap. 1 (navegação entre telas) — sempre.
- Contrato `eixo=processo` (fluxo de processo) — quando aplicável.
- Visão Cap. 1 (jornada macro) — opcional.
O `scripts/build-navigator.py` deve **renderizar Mermaid** no HTML (incluir mermaid.js, inicializar nos blocos ` ```mermaid `).

## Mudança 4 — Mínimo vs Opcional (BL-01)

Marcar explicitamente em README, `spec-scaffold` e `templates/wiki/CLAUDE.md`:
- **Mínimo comum:** `visao.md` (3 caps) + `Requisitos/<feature>.md` por feature (4 caps) + `blueprint.md`.
- **Opcional:** princípios, capacidades-IA dedicada, roadmap, input/health metrics, auditoria extra.

## Estrutura final do `refined/` gerado

```
refined/
  index.md  log.md  overview.md  blueprint.md   (4 mds da wiki)
  visao.md                                        (a Visão — Camada de Intenção, na raiz)
  componentes.md                                  (catálogo de componentes de UI, na raiz)
  Requisitos/
    <feature>.md                                  (1 doc por feature = Camada de Requisitos)
```

## Regra de não-regressão

Não apagar o `spec-kit/` original. Trabalhar só em `spec-kit-v2/`. Preservar conteúdo bom dos templates antigos ao consolidar (copiar as boas instruções, não reinventar).
