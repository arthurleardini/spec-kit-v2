---
name: critico-dados
description: Use quando o usuário quer criticar o capítulo de Dados de uma feature — entidade que deveria ser canônica, campo sem fonte da verdade, modelo que não sustenta os RF. Despachado pelo loop `spec-critico`.
---

# critico-dados

Hard skill: **um fato, um dono**. Entidade duplicada entre features é a dívida mais
cara de um wiki de produto.

Regras: bloco `D*` e `J-DAD-*` de `regras/criticas.toml`.

## Quando usar
Crítica do §3 (Dados) de um doc de feature, contra o `modelo-dados.md` transversal e os
RF do §2.2.

## Entrada
- O doc de feature.
- `refined/modelo-dados.md` (entidades canônicas) e as outras features de
  `refined/Requisitos/` (para achar entidade repetida).
- `regras/criticas.toml` (regras `D*`/`J-DAD-*`).
- Achados do lint (entidade canônica remodelada, cap. 3 sem referência canônica, campo
  sem tipo, detalhe técnico). **Não repetir.**

## Processo

1. **Promoção — J-DAD-01.** Para cada entidade própria da feature, procurar entidade
   equivalente (mesmo nome, sinônimo, ou mesmo conjunto de campos) nas outras features.
   Apareceu em ≥2 → deve ser canônica. Propor o nome e os campos da entidade canônica.
2. **Fonte da verdade — J-DAD-02.** Para cada campo de entidade própria que também
   existe numa entidade canônica: declarar se a feature é **dona** do campo ou apenas
   **referencia**. Campo sem essa declaração é achado — é o que gera divergência entre
   produtos do mesmo programa.
3. **Suporte aos RF — J-DAD-03.** Percorrer os RF do §2.2 e verificar se o modelo do
   §3 guarda a informação que cada um exige (estado, contagem, carimbo, vínculo). RF
   sem lastro no modelo é achado, citando o campo que falta.
4. Conferir que o §3 fica no nível conceitual — entidade, campo, relação. Detalhe
   técnico já é pego pelo lint (`D04`); aqui só o que o script não vê, como campo que
   é claramente coluna de implementação.
5. Teto: 10 achados.

## Como escrever o achado

```
<arquivo>:<linha>: [<REGRA>/<severidade>] <entidade ou campo>: <problema>. → <ajuste no modelo>
```

## Saída
Achados no formato acima. Nada achado → `critico-dados: sem achados.`
Não editar o artefato — nem o de feature, nem o `modelo-dados.md`.
