---
titulo: Telas Comuns (arquétipos transversais)
tipo: contract
atualizado_em: <data>
status: ativo
---

# Telas Comuns (arquétipos transversais)

Estes são os **arquétipos de tela reutilizáveis** de `<produto>`: padrões de layout e de
comportamento que se repetem em quase todas as features. Uma tela de feature que segue um
arquétipo **deve referenciá-lo e descrever só o que muda** (colunas, filtros, ações,
estados específicos), em vez de re-desenhar o wireframe do zero. O objetivo é **minimizar
o número de telas distintas a desenhar e manter** — pensar telas transversalmente, não por
feature, e **fundir** vistas (abas, drawers, painéis laterais) sempre que possível. Cada
`#### T-NN` de feature declara seu `**Arquétipo:** A?` e descreve só o que diverge. Os
componentes citados são o vocabulário genérico de [componentes.md](componentes.md).

> **Como nomear:** arquétipos recebem IDs estáveis `A1`, `A2`, … `A-NN`. Ao descobrir um
> novo padrão recorrente (≥ 2 features o usam), adicione um arquétipo aqui em vez de
> deixá-lo nascer duplicado nas features.

## Arquétipos

<!-- Um bloco por arquétipo. Inclua: descrição curta do padrão, um wireframe na DSL
`wireframe`, a linha "Quando usar", os Componentes genéricos e (opcional) as Instâncias
nas features. -->

### A1 — <nome do arquétipo, ex.: Painel de Indicadores (Dashboard)>
<Descrição do padrão em 1–3 frases: o que ele resolve e como se comporta.>

```wireframe
# <Título do padrão>
[Filtro v] [Filtro v]
[[ KPI 1 | KPI 2 | KPI 3 ]]
(!) alerta opcional
[~ visualização principal ~]
card "Bloco de detalhe":
  | Col A | Col B |
  | linha | valor |
[Ação primária] [Ação secundária]
```
- **Quando usar:** <em que situação este arquétipo é a escolha certa; quando NÃO usá-lo>.
- **Componentes:** <nomes genéricos de componentes.md — ex.: toolbar, card, chart, table, button>.
- **Instâncias:** <opcional — feature · T-NN (nome da tela) · …>.

### A2 — <nome do arquétipo, ex.: Lista / Fila com Filtros>
<Descrição.>

```wireframe
# <Coleção>
[Buscar____] [Filtro v] [Ordenar por X v]
| Col A | Col B | Status | Ação |
| reg | reg | ... | ... |
[Abrir] [Ação 1]
```
- **Quando usar:** <...>.
- **Componentes:** <...>.
- **Instâncias:** <...>.

### A3 — <nome do arquétipo, ex.: Formulário de Configuração>
<Descrição.>

```wireframe
# Configurar <Parâmetro>
card "Bloco de parâmetros":
  [Campo____] [Campo v]
(!) regra/validação
[Fundamentação____]
[Validar] [Salvar]
```
- **Quando usar:** <...>.
- **Componentes:** <...>.
- **Instâncias:** <...>.

### A4 — <nome do arquétipo, ex.: Painel de Detalhe do Registro>
<Descrição. Acrescente quantos arquétipos `A-NN` o produto realmente exibir — detalhe,
linha do tempo/histórico, fila de aprovação, editor visual/canvas, comparação, visão 360,
construtor de consulta/exportação, etc.>

```wireframe
# Detalhe de <Registro>
card "Resumo / metadados":
  [[ Atributo | Atributo | Atributo ]]
card "Bloco de contexto":
  - linhas / tabela
[Ação contextual] [Editar]
```
- **Quando usar:** <...>.
- **Componentes:** <...>.
- **Instâncias:** <...>.

## Relacionado
- [Índice do wiki](index.md)
- [Visão do produto](visao.md)
- [Modelo de dados (transversal)](modelo-dados.md)
- [Requisitos transversais](requisitos-transversais.md)
- [Vocabulário de componentes](componentes.md)
