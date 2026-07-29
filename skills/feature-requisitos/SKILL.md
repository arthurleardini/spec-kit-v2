---
name: feature-requisitos
description: Use quando o usuário quer escrever ou revisar os requisitos funcionais e os cenários de teste de uma feature — subseções 7.N.3 (RF em EARS-PT) e 7.N.4 (cenários) do `spec.md`.
---

# feature-requisitos

Dona das subseções **7.N.3 (Requisitos funcionais)** e **7.N.4 (Cenários de teste)**.

Responde: *o que o produto deve fazer — e como se prova?*

## Quando usar
Quando o usuário pede requisitos, RF, critérios de aceite, cenários ou casos de teste de
uma feature.

## Entrada
Seções 1 a 6 do `spec.md` (personas, `RN-NN`, `RNF-T-*`, `RF-T-*`), a 7.N.1/7.N.2 já
escritas (fluxo e telas) e a fonte da feature.

## Requisito funcional — EARS-PT, sempre

| # | Padrão | Template |
|---|---|---|
| 1 | Ubíquo | `O <sistema> deve <resposta>` |
| 2 | Estado | `Enquanto <precondição>, o <sistema> deve <resposta>` |
| 3 | Evento | `Quando <gatilho>, o <sistema> deve <resposta>` |
| 4 | Opcional | `Onde <feature existe>, o <sistema> deve <resposta>` |
| 5 | Indesejado | `Se <gatilho>, então o <sistema> deve <resposta>` |
| 6 | Composto | `Enquanto <precondição>, quando <gatilho>, o <sistema> deve <resposta>` |

Ruleset: 0..n precondições · 0..1 gatilho · 1 sistema · 1..n respostas.

Regras duras:

- **Uma capacidade por RF.** `e` / `e/ou` ligando duas ações = dois RF.
- **Vocabulário fechado.** Nada de subjetivo (amigável, adequado), brecha (se possível,
  quando aplicável), não-verificável (eficiente, otimizado), verbo oco (suportar,
  gerenciar, prover). Lista completa em `regras/criticas.toml`, `[vocabulario]`.
- **Voz ativa.** Quem faz o que a quem.
- **Positivo.** Em vez de "não deve X", escrever o padrão #5: `Se <X>, então o sistema
  deve <resposta>`.
- **Desvio é RF.** Toda exceção do fluxo (7.N.1) vira RF padrão #5. Feature sem nenhum
  padrão #5 não passa no gate. Checklist mínimo: timeout, processamento parcial,
  concorrência, retomada idempotente.
- **Lacuna é honesta.** Sem informação para especificar? escrever
  `⚠ NÃO IDENTIFICADO — definir: <pergunta>` em vez de RF vago.
- Teto de palavras por RF e de RF por feature em `[tetos]`.

**Não escrever requisito não-funcional aqui.** RNF vive só em §5 e a feature cita por ID,
na linha `**Transversais aplicáveis:**`. RF que fala de latência, throughput,
disponibilidade ou segurança é RNF disfarçado: promover a `RNF-T-*` em §5.

Cada RF traz a `RN-NN` (ou `JTBD-NN`) de origem. Sem origem, o requisito não é auditável.

## Cenário de teste — key example, não paráfrase

O cenário **prova** o RF; não o reescreve em Gherkin. Formato `Dado / Quando / Então`,
com id `CT-NN` contínuo no spec, declarando `(verifica RF-NN)`.

- **Dado** = estado concreto (valor, identificador, data), não a regra em abstrato.
- **Então** = resultado **observável** — visível em tela, registro, log ou retorno.
  "Fica consistente" e "processa corretamente" não são resultado.
- Cobrir: caminho feliz, cada RF padrão #5, e a **fronteira** de todo RF com limite
  numérico, temporal ou de estado (o valor que passa e o que não passa).
- Teto de palavras por cenário em `[tetos]`.

## Processo
1. Ler as seções 1 a 6 e a 7.N.1/7.N.2. Conferir o eixo declarado nos metadados.
2. Escrever a tabela 7.N.3 em EARS-PT, com prioridade e `RN` de origem, e a linha
   `**Transversais aplicáveis:**` citando os `RNF-T-*` / `RF-T-*` que valem.
3. Escrever os cenários 7.N.4, um por RF no mínimo, com os desvios cobertos.
4. Rodar o gate: `python3 scripts/lint_critico.py <spec.md>`. Corrigir antes de entregar.

## Saída
Subseções 7.N.3 e 7.N.4 preenchidas: RF em EARS-PT rastreáveis a `RN`, transversais citados
por ID, e cenários que provam cada RF.
