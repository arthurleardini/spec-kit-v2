---
titulo: Visão
tipo: intencao
atualizado_em: <data>
status: ativo
fontes: []
---
# Visão
> Camada de Intenção · Spec-Driven Development
> Pergunta-mãe: *Quem somos, para quem, com que vocabulário e sob quais leis?*

Documento canônico da Camada de Intenção. Consolida em três capítulos a descrição do produto-alvo: **Produto** (quem somos e para quem), **Glossário** (qual é o vocabulário) e **Regras & Métricas** (quais são as leis e como nos medimos). As fontes que sustentam cada afirmação estão agrupadas na seção "Fontes", ao final.

> **Convenção de marcadores.** Marcar inferências (algo deduzido, não afirmado pela fonte) com `*(inferência)*` e lacunas com `⚠ NÃO IDENTIFICADO — definir: <pergunta>`. IDs (`JTBD-NN`, `RN-NN`, `RN-AI-NN`, `IM-NN`) são estáveis e referenciados pela Camada de Requisitos — não renumerar; ao remover um item, manter o número vago.

<!--
SEÇÕES OPCIONAIS (não geradas por padrão — incluir só quando explicitamente pedido):
  · Princípios de Produto (PR-NN) — como decidir quando há tensão entre alternativas.
  · Capacidades de IA como catálogo dedicado (CAI-NN) — o essencial já vive em "Regras dependentes de IA".
  · Roadmap de evolução (horizontes H1/H2/H3) e trajetória da IA.
  · Métricas detalhadas (Input Metrics, Métricas de Saúde além do guard-rail mínimo).
-->

---

## 1. Produto

> *Quem somos e para quem?*

### Visão

<O que é o produto, em 1–2 parágrafos. Que problema resolve, para quem, e qual a transformação que promove.>

### Proposta de Valor

<Frase de posicionamento: "Para <público> que <necessidade>, o <produto> é um(a) <categoria> que <benefício central>. Diferente de <alternativas>, <diferencial>." Seguir com a lista de diferenciais.>

Diferenciais:

- **<diferencial>** — <descrição>.
- <... um marcador por diferencial>

### Personas

<Para cada persona, uma subseção. Ordenar por relevância: primária, secundária, terciária...>

#### Persona <ordem> — <nome do papel>

**Quem é.** <Perfil: cargo, contexto organizacional, responsabilidades.>

**Contexto de uso.** <Como e quando usa o produto; que tarefas executa.>

**Dores.**
- <dor atual que o produto endereça>
- <... um marcador por dor>

<!-- O ganho desejado de cada dor é o JTBD/RF correspondente — não duplicar aqui. -->

#### <Papel fora do escopo> — fora do escopo

<Quando houver um papel relevante que NÃO é usuário do produto, explicitar aqui por que está fora e onde ele é atendido.>

### Jobs / Necessidades

<Um marcador JTBD-NN por job. Formato: "Quando <situação>, quero <motivação>, para <resultado esperado>.">

- **JTBD-01** — Quando <situação>, quero <motivação>, para <resultado esperado>.
- **JTBD-02** — <...>

### Não-objetivos

<O que o produto explicitamente NÃO faz. Um marcador por não-objetivo, com a justificativa.>

- **<Não-objetivo>.** <Por que está fora do escopo.>
- <...>

---

## 2. Glossário

> *Qual é o vocabulário?*

Definições precisas dos termos do negócio. Cada termo deve ser usado de forma consistente em todos os documentos da spec — é o guard-rail de linguagem.

### Termos do domínio

<Um termo por subseção, em ordem alfabética. Para cada termo: Definição (precisa, sem circularidade), Sinônimos a evitar (termos vagos ou ambíguos que NÃO devem ser usados como sinônimo) e Exemplo concreto. Termos fora do escopo podem usar a forma curta "→ Ver <outro termo>" ou "→ Fora do escopo — <onde é tratado>".>

#### <Termo>
**Definição**: <definição precisa do termo no domínio do produto>
**Sinônimos a evitar**: <termos a não usar — com o motivo entre parênteses>
**Exemplo**: <exemplo concreto de uso do termo>

#### <Termo>
**Definição**: <...>
**Sinônimos a evitar**: <...>
**Exemplo**: <...>

### Convenções de nomenclatura

<Regras numeradas que resolvem ambiguidades recorrentes do vocabulário — distinções entre termos próximos, grafias canônicas, abreviações aceitas.>

1. **<convenção>**: <regra>.
2. <...>

---

## 3. Regras & Métricas

> *Quais são as leis do produto, e como saber se ele cumpre a missão?*

Invariantes e políticas do domínio independem de interface — valem em qualquer stack ou tela. As métricas dizem se o produto está cumprindo sua missão.

<Convenções transversais que valem para todas as regras — opcional. Ex.: tratamento de valores numéricos, precedência entre regras.>

### Regras de Negócio

<Agrupar as regras por tema quando forem muitas. Uma subseção por regra, com ID estável RN-NN.>

#### RN-01 — <título curto da regra>
**Enunciado**: <o que a regra determina — invariante ou política, de forma precisa e testável>
**Justificativa**: <por que a regra existe>
**Exceções**: <condições em que a regra não se aplica — opcional>
**Impacta**: <que partes do produto a regra afeta>

#### RN-02 — <título curto da regra>
**Enunciado**: <...>
**Justificativa**: <...>
**Impacta**: <...>

### Regras dependentes de IA

<Incluir esta seção SÓ se houver regras que dependem de inferência algorítmica (ML, NLP, embeddings, IA generativa) para serem aplicadas. Lógica determinística — máquinas de estado, regras compostas, contagem — NÃO entra aqui; é regra de negócio comum (RN-NN). Princípio orientador: quando uma capability puder ser implementada como regra determinística com qualidade equivalente, prefere-se a regra. Os parâmetros técnicos — modelo, prompt, threshold — vivem nos Contratos, não aqui.>

#### RN-AI-01 — <título curto da regra>
**Enunciado**: <o que o componente infere/classifica/gera/ranqueia e quando é acionado>
**Justificativa**: <por que a regra existe>
**Fallback**: <comportamento quando o componente está indisponível ou faltam dados>
**Impacta**: <que partes do produto a regra afeta>

### Métricas de sucesso

**North Star Metric (NSM): <nome da métrica>.**

```
<fórmula da NSM, com as desagregações entre parênteses>
```

<Definição dos termos da fórmula — o que conta no numerador e no denominador, modelo de atribuição.>

**Cadência.** <Periodicidade de apuração.>

**Por que esta métrica.** <Como traduz a missão e distingue esforço de resultado.>

**Baseline de referência.** <Valor de partida observado; não meta imposta pelo produto.>

**Guard-rails** — <1 a 2 métricas que não devem piorar enquanto a NSM é otimizada.>

- **IM-01 — <nome>.** <Definição e o que a deterioração indica.>
- **IM-02 — <nome>.** <...>

---

## Questões em aberto

<Decisões de produto, vocabulário, regras ou métricas ainda não fechadas. Um marcador por questão.>

- <questão em aberto>

---

## Fontes

<Evidência que sustenta este documento, agrupada por capítulo/seção. Citar as fontes em trusted/ ou refined/.>

---

## Relacionado
- [Blueprint](blueprint.md)
- [Índice do wiki](index.md)

---

*Camada de Intenção. Documento canônico — descreve o produto-alvo: quem é, com que vocabulário e sob quais leis.*
