---
titulo: Backlog de Ajustes da Metodologia (spec-kit-v2)
tipo: backlog
origem: análise transversal P2.1–P2.7 (Knowledge-MT), 2026-07-01
status: aberto
---

# Backlog de Ajustes da Metodologia

> **Nota v3.** Os caminhos citados abaixo são do v2 (`skills/contrato-*`,
> `templates/transversais/*`). No v3 eles correspondem a: `skills/feature-requisitos`
> (M1, M3), `skills/feature-telas-fluxos` (M2), `skills/spec-transversais` + §5 do
> `spec.md` (M4, M5). **M1 a M5 viraram regra do loop crítico** — ver
> [`LOOP-CRITICO.md`](LOOP-CRITICO.md). M6 e M7 seguem abertos.

Os 7 padrões achados na análise dos produtos Knowledge-MT
(`knowledge-mt/criticas/Backlog_Ajustes_TRANSVERSAL_P2.1-2.7.md`) não são erro de quem
escreveu — são **lacunas do próprio kit**. Se o template/skill não pede, o agente não
gera. Cada item abaixo corrige a metodologia para que a próxima spec já nasça sem a lacuna.

Convenção: `M-N` = ajuste metodológico; mapeia 1:1 ao `A-N` do backlog de produto.

---

## M1 — Regra de testabilidade de RF → skill `contrato-requisitos`

**Onde.** `skills/contrato-requisitos/` + `templates/contrato/contrato.md` (§2.2 RF).

**Mudança.** Gate obrigatório: ao emitir um RF, o agente aplica o teste *"1 CT objetivo
valida isto?"*. Se não → grava `⚠ NÃO IDENTIFICADO — definir: <X>` em vez de RF vago.
Adicionar à skill a lista de verbos proibidos sem parâmetro (relevante, adequado, rápido,
tempo real, marcos) → exigem `RN-NN` ou lacuna.

**Aceite.** `spec-lint` falha se existe RF sem CT associado e sem marcador de lacuna.

---

## M2 — Mínimo de desvios por fluxo → skill `contrato-telas-fluxos`

**Onde.** `skills/contrato-telas-fluxos/` (§1.1 Fluxo Mermaid).

**Mudança.** Template de fluxo exige **≥3 ramos de exceção**. Checklist de desvios
canônicos: timeout/falha de fonte, processamento parcial, concorrência/lock, retomada
idempotente. Cada ramo referencia `RNF-T-DISP-01` ou RF de tratamento.

**Aceite.** `spec-lint` conta ramos de exceção por `mermaid` de fluxo; <3 → warning.

---

## M3 — Cobertura mínima de CT → skill `contrato-requisitos`

**Onde.** `skills/contrato-requisitos/` (§2.4 Cenários de Teste).

**Mudança.** Regra: ≥1 CT por RNF crítico (SEG/AUD/PERF/DISP) + ≥1 CT de borda por RF
`Must`. Template de CT ganha campo `tipo: feliz | borda | rnf`.

**Aceite.** `spec-audit` reporta RF Must sem CT de borda e RNF crítico sem CT.

---

## M4 — Segurança/LGPD concreta → template `requisitos-transversais` + skill `spec-transversais`

**Onde.** `templates/transversais/requisitos-transversais.md`, `skills/spec-transversais/`.

**Mudança.** Template passa a exigir 4 blocos concretos, não prosa genérica:
1. **Matriz perfil × ação** (tabela).
2. **Tabela base legal por dado** (dado → base LGPD → retenção).
3. **RNF de imutabilidade com mecanismo**: pilha de referência **PDF/A + SHA-256 +
   ICP-Brasil + WORM** (o kit hoje só diz "trilha imutável" sem o *como*).
4. **Gancho de sigilo setorial** — placeholder para regra de domínio (ex.: CTN art. 198
   fiscal) acionável quando o produto tem canal externo.

**Aceite.** `spec-lint` exige as 4 seções em `requisitos-transversais.md`.

---

## M5 — Observabilidade obrigatória → template `requisitos-transversais`

**Onde.** `templates/transversais/requisitos-transversais.md` (§Observabilidade).

**Mudança.** `RNF-T-OBS-*` deixa de ser opcional. Template exige nomear métricas
(negócio+técnica), alertas e política de log de auditoria. Reforça o hoje-fraco
"status rastreável".

**Aceite.** `spec-lint` trata ausência de bloco Observabilidade como erro, não omissão.

---

## M6 — Contrato detalhado de integração → **novo** template + skill

**Onde.** Novo `templates/contrato/integracao.md`; estender `skills/contrato-blueprint`
(catálogo de integrações).

**Mudança.** O kit hoje só tem catálogo conceitual (papel/direção/criticidade). Adicionar
ficha de contrato por integração: endpoint/método, schema payload in/out, chave de
idempotência, mapa de erros, SLA. Quando o sistema-fonte não é conhecido →
`⚠ NÃO IDENTIFICADO — depende de: <origem>`.

**Aceite.** Toda integração no catálogo tem ficha OU marcador de dependência.

---

## M7 — ER canônico de programa → **novo** artefato acima do produto

**Onde.** Novo `templates/programa/modelo-canonico.md`; nova skill `spec-programa`
(ou extensão de `spec-transversais` para escopo multi-produto).

**Mudança.** O kit modela dados **por produto** (`modelo-dados.md`), sem camada de
**programa**. Adicionar modelo canônico do programa: entidades globais + **fonte da
verdade (home)** por entidade + estratégia de propagação (referência vs. enriquecimento).
Cada `modelo-dados.md` de produto passa a apontar a entidade-lar e marcar campos
próprios × referenciados.

**Aceite.** Programa multi-produto exige `modelo-canonico.md`; `spec-audit` cruza
entidades homônimas entre produtos e sinaliza divergência de campo sem fonte declarada.

---

## Resumo

| M | Corrige A | Artefato do kit | Tipo |
|---|-----------|-----------------|------|
| M1 | A1 | skill contrato-requisitos + template contrato | ajuste |
| M2 | A2 | skill contrato-telas-fluxos | ajuste |
| M3 | A3 | skill contrato-requisitos | ajuste |
| M4 | A4 | template requisitos-transversais + spec-transversais | ajuste |
| M5 | A5 | template requisitos-transversais | ajuste |
| M6 | A6 | **novo** templates/contrato/integracao.md | criação |
| M7 | A7 | **novo** templates/programa/modelo-canonico.md + skill | criação |

Boa parte vira regra de **`spec-lint`/`spec-audit`** — assim a lacuna falha o build em vez
de passar despercebida. M6 e M7 são criação de artefato novo; o resto é reforço de
template/skill existente.
