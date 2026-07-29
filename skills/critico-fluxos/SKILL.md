---
name: critico-fluxos
description: Use quando o usuário quer criticar fluxo e cobertura de desvio de uma feature — exceção não modelada, contradição entre fluxo e RF, tela ou estado inalcançável. Despachado pelo loop `spec-critico`.
---

# critico-fluxos

Hard skill: **enumerar o que dá errado**. O furo mais comum de spec é o caminho feliz
completo e o desvio ausente.

Regras: bloco `F*` e `J-FLX-*` de `regras/criticas.toml`.

## Quando usar
Crítica da 7.N.1 (fluxo e navegação) contra a 7.N.3 (RF) de uma feature.

## Entrada
- A feature (7.N): os dois Mermaid da 7.N.1, as telas da 7.N.2 e os RF da 7.N.3.
- `regras/criticas.toml` (regras `F*`/`J-FLX-*`, `[vocabulario].desvios_canonicos`).
- Achados do lint (ausência de RF padrão #5, fluxo sem decisão, navegação ausente,
  desvio canônico não citado). **Não repetir.**

## Checklist de desvio

Cada item vira `J-FLX-01` quando o fluxo e os RF não o resolvem. O desvio se declara
como **RF padrão #5** — `Se <gatilho>, então o <sistema> deve <resposta>` — não como
parágrafo solto.

| Desvio | Pergunta |
|---|---|
| Timeout / sem resposta | A fonte externa não responde. O que o usuário vê? |
| Processamento parcial | O lote conclui metade. Qual o estado dos dois grupos? |
| Concorrência | Dois atores agem no mesmo registro. Quem ganha? |
| Retomada idempotente | O passo repete. Duplica ou reaproveita? |
| Falha de autorização | O ator perde o perfil no meio do fluxo. |
| Dado ausente | O campo obrigatório não veio da origem. |
| Reversão | O usuário desfaz depois de um efeito externo já emitido. |

## Processo

1. Ler o flowchart de fluxo (7.N.1) e listar cada nó de decisão e cada ramo. Ramo que termina sem
   saída declarada é `J-FLX-03`.
2. Rodar o checklist acima contra os RF. Falta → `J-FLX-01`, com o RF padrão #5 já
   redigido no campo `→`.
3. **Contradição — J-FLX-02.** Comparar cada aresta do fluxo com os RF: fluxo que
   permite um caminho que um RF proíbe (ou vice-versa). Citar os dois lados.
4. **Alcançabilidade — J-FLX-03.** Cruzar as telas da 7.N.2 com o diagrama de navegação:
   tela sem aresta de entrada, ou estado descrito na tela que nenhum fluxo produz.
5. Teto: 10 achados. Priorizar o desvio que hoje deixaria o usuário travado sem saída.

## Como escrever o achado

```
<arquivo>:<linha>: [<REGRA>/<severidade>] <alvo>: <desvio ou contradição>. → <RF padrão #5 ou ajuste de fluxo>
```

## Saída
Achados no formato acima. Nada achado → `critico-fluxos: sem achados.`
Não editar o artefato.
