---
name: critico-testabilidade
description: Use quando o usuário quer criticar a verificabilidade dos requisitos — se cada RF tem cenário que realmente o prova, se o cenário é key example e se o resultado esperado é observável. Despachado pelo loop `spec-critico`.
---

# critico-testabilidade

Hard skill: **provar que o requisito foi cumprido sem depender de opinião**.

Regras: bloco `T*` e `J-TST-*` de `regras/criticas.toml`.

## Quando usar
Crítica do §2.4 (Cenários de Teste) contra o §2.2 (RF) de um doc de feature.

## Entrada
- O doc de feature.
- `regras/criticas.toml` (regras `T*`/`J-TST-*`, `[tetos]`, `[vocabulario].sinais_excecao`).
- Achados do lint — o script já cobre RF sem cenário, cenário sem RF-pai, ausência de
  Dado/Quando/Então, teto de palavras e cenário que só reescreve o RF. **Não repetir.**

## Princípio

O cenário é a **verificação** do RF, não a repetição narrativa dele
(Specification by Example — `docs/referencias-v3.md` §C). Dois testes rápidos:

- **Teste do caso de teste** — dá para escrever um cenário objetivo a partir deste RF?
  Não dá → o RF está furado, não o cenário.
- **Teste do dado concreto** — o cenário cita valor, estado ou identificador concreto?
  Se descreve só a regra em abstrato, não é key example.

## Processo

1. Montar a matriz RF × cenário. O lint já reporta os vazios; aqui interessa o
   **cenário que existe mas não prova**.
2. Para cada par:
   - **J-TST-01 — não prova.** O `Então` não decide se o RF foi cumprido, ou verifica
     outra coisa. Achado citando o que o `Então` deveria afirmar.
   - **J-TST-03 — não observável.** O resultado esperado não é visível numa tela, num
     registro, num log ou num retorno. "Fica consistente", "processa corretamente" são
     achados.
3. Cobertura de fronteira — **J-TST-02**: para cada RF `Must` com limite numérico,
   temporal ou de estado (teto, prazo, contagem, transição), exigir um key example
   **no limite** (o valor que passa e o que não passa). Falta → achado.
4. Conferir se cada RF de comportamento indesejado (padrão #5 EARS-PT) tem cenário
   próprio. Desvio declarado como RF e não verificado é achado `J-TST-01`.
5. Teto: 10 achados.

## Como escrever o achado

```
<arquivo>:<linha>: [<REGRA>/<severidade>] <CT-NN ou RF-NN>: <problema>. → <cenário ou passo proposto>
```

A proposta vem pronta: `Dado <estado concreto> / Quando <ação> / Então <resultado observável>`.

## Saída
Achados no formato acima, `bloqueia` primeiro. Nada achado → `critico-testabilidade:
sem achados.` Não editar o artefato.
