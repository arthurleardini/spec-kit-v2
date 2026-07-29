---
name: critico-dados
description: Use quando o usuário quer criticar o capítulo de Dados de uma feature — entidade que deveria ser canônica, campo sem fonte da verdade, modelo que não sustenta os RF. Despachado pelo loop `spec-critico`.
---

# critico-dados

Hard skill: **um fato, um dono**. Entidade duplicada entre features é a dívida mais
cara de uma spec de produto.

Regras: bloco `D*` e `J-DAD-*` de `regras/criticas.toml`.

## Quando usar
Crítica da subseção 7.N.5 (Dados) de uma feature, contra a seção 4 (Modelo de dados) e
os RF da 7.N.3.

## Entrada
- A feature (7.N) do `spec.md`.
- A seção 4 (entidades canônicas) e as demais features da seção 7, para achar entidade
  repetida.
- `regras/criticas.toml` (regras `D*`/`J-DAD-*`).
- Achados do lint (entidade canônica remodelada, Dados sem referência canônica, campo
  sem tipo, detalhe técnico). **Não repetir.**

## Processo

1. **Promoção — J-DAD-01.** Para cada entidade própria da feature, procurar entidade
   equivalente (mesmo nome, sinônimo, ou mesmo conjunto de campos) nas outras features.
   Apareceu em ≥2 → deve ser canônica. Propor o nome e os campos da entidade canônica.
2. **Fonte da verdade — J-DAD-02.** Para cada campo de entidade própria que também
   existe numa entidade canônica: declarar se a feature é **dona** do campo ou apenas
   **referencia**. Campo sem essa declaração é achado — é o que gera divergência entre
   produtos do mesmo programa.
3. **Suporte aos RF — J-DAD-03.** Percorrer os RF da 7.N.3 e verificar se o modelo da
   7.N.5 guarda a informação que cada um exige (estado, contagem, carimbo, vínculo). RF
   sem lastro no modelo é achado, citando o campo que falta.
4. Conferir que a 7.N.5 fica no nível conceitual — entidade, campo, relação. Detalhe
   técnico já é pego pelo lint (`D04`); aqui só o que o script não vê, como campo que
   é claramente coluna de implementação.
5. Teto: 10 achados.

## Como escrever o achado

```
<arquivo>:<linha>: [<REGRA>/<severidade>] <entidade ou campo>: <problema>. → <ajuste no modelo>
```

## Saída
Achados no formato acima. Nada achado → `critico-dados: sem achados.`
Não editar a spec — nem a feature, nem a seção 4.
