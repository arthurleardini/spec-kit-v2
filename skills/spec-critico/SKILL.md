---
name: spec-critico
description: Use quando o usuário quer criticar, auditar ou "fechar o gate" de um documento da Camada de Requisitos antes de entregar — roda o lint determinístico, despacha os críticos especialistas em paralelo, consolida o ledger de achados e reabre o loop até o gate abrir ou acabarem as rodadas.
---

# spec-critico — orquestrador do loop crítico

Fecha o gate de um `refined/Requisitos/<feature>.md`. Duas camadas de crítica:

1. **Determinística** — `scripts/lint_critico.py`. Forma, teto, ID, link, RF↔cenário.
   Barato, repetível, exit code. Roda sempre primeiro.
2. **Julgamento** — 6 críticos especialistas, um por hard skill. Cada um lê **só a
   sua parte** de `regras/criticas.toml` e devolve achados no mesmo formato.

Fonte única das regras: **`regras/criticas.toml`**. Regra que não está lá não existe —
nem o script nem o crítico inventam exigência.

## Quando usar
Antes de entregar uma feature, antes de avançar de camada, ou quando o usuário pede
para criticar/auditar/revisar requisitos. Para auditar a **Visão** (Camada de Intenção)
pelo método CSD, use `spec-audit` — este loop é da Camada de Requisitos.

## Entrada
- Um ou mais `refined/Requisitos/<feature>.md`.
- O `refined/` do wiki (o lint precisa dele p/ resolver `RN-*`, `RNF-T-*`, `A-*`, entidades).

## Processo

### Rodada (repetir até `rodadas_max` do TOML — padrão 2)

1. **Lint.** `python3 scripts/lint_critico.py <refined> --json --ledger criticas/`
   Exit 0 = limpo · 1 = só «corrige» · 2 = há «bloqueia».
2. **Despacho paralelo.** Um subagente por crítico, numa só mensagem. Só os críticos
   relevantes ao artefato — não despache `critico-dados` num doc sem capítulo 3.

   | Crítico | Mandato |
   |---|---|
   | `critico-redacao` | forma EARS-PT, ambiguidade, vocabulário, brevidade |
   | `critico-testabilidade` | RF↔cenário, key example, observabilidade do resultado |
   | `critico-simplicidade` | redução de tela/RF/conceito, escopo, implementação disfarçada |
   | `critico-fluxos` | desvio, exceção, contradição fluxo↔RF, estado órfão |
   | `critico-dados` | entidade canônica, fonte da verdade, suporte aos RF |
   | `critico-rastreabilidade` | ID, fonte, rastreio falso, fato duplicado |

   No prompt de cada subagente, repassar: caminho do artefato, caminho do
   `regras/criticas.toml`, o bloco de regras que é dele, os achados do lint (para não
   repetir) **e as regras de resposta do `CLAUDE.md` do workspace** (falar pouco, zero
   juízo de valor, texto longo em arquivo).
3. **Consolidar.** Juntar achados do lint + dos críticos no ledger
   `criticas/<feature>-<AAAA-MM-DD>.md`. Deduplicar por `(regra, alvo)`. Ordenar
   `bloqueia` antes de `corrige`.
4. **Corrigir.** Aplicar as correções no artefato. Cada edição referencia o **ID do
   achado** no ledger (`✅`). Recusa é legítima, mas exige justificativa escrita na
   linha do ledger (`🚫` + motivo). Achado sem tratamento (`⬜`) mantém o gate fechado.
5. **Re-lint.** Voltar ao passo 1.

### Critério de saída
- **Gate abre** quando: lint exit 0 **e** nenhum achado `bloqueia` em aberto.
- **Gate fecha** e escala ao humano quando as `rodadas_max` acabam. Entregar o ledger
  com o que sobrou — não rodar rodada extra "até ficar bom".

## Regras do loop

- **Crítico não edita.** Ele acha e assina; a correção é do autor. Separar achado de
  correção é o que torna o ledger auditável.
- **Teto de 10 achados por crítico.** Estourou? o crítico prioriza e diz que priorizou.
  Lista de 40 achados não é crítica, é despejo.
- **Sem elogio.** Nenhum crítico abre com o que está bom. Achado ou silêncio.
- **Teto estourado corta conteúdo**, não sobe o teto. Mudar teto no TOML é decisão do
  usuário, não do loop.

## Formato do achado (lint e crítico usam o mesmo)

```
<arquivo>:<linha>: [<REGRA>/<severidade>] <alvo>: <problema>. → <correção proposta>
```

Exemplo:

```
Requisitos/regua.md:168: [J-RED-01/bloqueia] RF-03: "respeitar aceite vigente" admite duas
  leituras — bloquear o disparo ou registrar a exceção. → escolher uma e escrever em EARS-PT.
```

## Saída
- Ledger `criticas/<feature>-<data>.md` com todos os achados e o tratamento de cada um.
- Artefato corrigido.
- Uma linha em `refined/log.md`: `## [AAAA-MM-DD] critico | <feature> — <N> achados, gate <aberto|fechado>`.
- Resposta no chat: 3 linhas no máximo — gate aberto/fechado, quantos achados por
  severidade, caminho do ledger.
