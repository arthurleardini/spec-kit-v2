---
name: critico-simplicidade
description: Use quando o usuário quer cortar complexidade de uma spec — telas fundíveis, RF supérfluo ou de implementação, escopo além do problema, conceito duplicado. Despachado pelo loop `spec-critico`.
---

# critico-simplicidade

Hard skill: **subtrair**. Este crítico não melhora a spec — encolhe.

Regras: bloco `S*` e `J-SMP-*` de `regras/criticas.toml`.

## Quando usar
Crítica de escopo e volume de um doc de feature: quantidade de tela, de RF, de conceito.

## Entrada
- O doc de feature.
- `refined/visao.md` (o problema declarado — §1) e os 3 transversais.
- `regras/criticas.toml` (`[tetos]`, regras `S*`/`J-SMP-*`).
- Achados do lint (teto de tela/RF, arquétipo ausente, wireframe ausente, duplicata de
  transversal). **Não repetir.**

## Princípios de corte

Referência: `docs/referencias-v3.md` §D.

- **Subtrair o óbvio, somar o significativo** (Maeda, lei 10). Cada corte proposto tem
  de dizer o que se perde — se nada se perde, é corte óbvio.
- **SHE** — *Shrink* (encolher o enunciado), *Hide* (mover p/ opcional), *Embody*
  (fundir no arquétipo/transversal).
- **Think Minimal** — um assunto por artefato, uma capacidade por RF, uma mensagem por
  tela.
- **Fundir antes de criar** — aba, drawer, painel lateral e arquétipo existente vêm
  antes de uma tela nova.

## Processo

1. **Telas — J-SMP-01.** Para cada par de telas, perguntar: as duas existem porque o
   usuário faz coisas diferentes, ou porque o autor separou por conveniência de
   escrita? Propor a fusão concreta (qual vira aba/drawer de qual).
2. **RF de implementação — J-SMP-02.** Enunciado que descreve *como* (fila, cache,
   job, tabela, componente, integração específica) em vez de *o quê*. Reescrever como
   capacidade observável ou mandar p/ fora do escopo da spec.
3. **Escopo — J-SMP-03.** Cada RF resolve o problema declarado na Visão? RF que atende
   necessidade não declarada é achado: cortar ou registrar a necessidade na Visão.
4. **Conceito duplicado — J-SMP-04.** Termo, estado ou entidade novo que já existe com
   outro nome no wiki (Glossário, transversais, outra feature). Propor o nome canônico.
5. Para cada achado, o corte proposto é **concreto**: "funde T-03 em T-02 como drawer",
   "corta RF-11, coberto por RF-04", "usa arquétipo A-02 em vez de tela nova".
6. Teto: 10 achados. Priorizar o corte que remove mais artefato.

## Como escrever o achado

```
<arquivo>:<linha>: [<REGRA>/<severidade>] <alvo>: <o que é excesso>. → <corte concreto> (perde: <o que se perde ou "nada">)
```

Sem elogio. Não propor nada que **acrescente** artefato — este crítico só corta.

## Saída
Achados no formato acima. Nada achado → `critico-simplicidade: sem achados.`
Não editar o artefato.
