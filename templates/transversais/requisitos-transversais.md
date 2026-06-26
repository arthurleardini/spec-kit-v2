---
titulo: Requisitos Transversais
tipo: contract
atualizado_em: <data>
status: ativo
---
# Requisitos Transversais

> Camada de Requisitos · Requisitos cross-cutting · Spec-Driven Development
> Pergunta-mãe: *Quais requisitos valem para todas (ou quase todas) as features, de modo
> que não precisem ser repetidos em cada uma?*

Este documento consolida os requisitos não-funcionais e funcionais que se repetem — quase
sempre de forma idêntica — ao longo das features de `<produto>`. O princípio é
**minimizar complexidade e duplicação**: um requisito cross-cutting vive aqui uma única
vez, com ID estável, e cada feature apenas o **referencia** no seu Cap. 2 (ex.: "aplica-se
`RNF-T-<categoria>-01`"), reservando o capítulo para o que é genuinamente próprio da
feature. Os IDs aqui (`RNF-T-<categoria>-NN`, `RF-T-NN`) são estáveis e não devem ser
renumerados; ao remover um item, manter o número vago. Valores numéricos (limites, prazos,
percentuais) são **parâmetros configuráveis por instância**, sem default imposto pelo
produto. Marcadores: `*(inferência)*` para deduções não afirmadas explicitamente pelas
fontes e `⚠ NÃO IDENTIFICADO` para lacunas.

---

## RNF transversais

<!-- Agrupe por categoria; inclua só as categorias com requisitos reais. Para cada item,
um enunciado claro e, opcionalmente, uma linha *Subsume:* listando os requisitos de feature
que ele substitui (rastreabilidade de onde o requisito foi consolidado). -->

### Segurança

#### RNF-T-SEG-01 — <título do requisito de segurança>
<Enunciado do requisito cross-cutting de segurança/controle de acesso.>
*Subsume:* <features e IDs locais que este transversal substitui — opcional>.

### Auditoria

#### RNF-T-AUD-01 — <título do requisito de auditoria>
<Enunciado — ex.: trilha de auditoria em toda ação relevante: ator, timestamp, payload,
resultado, fundamentação.>
*Subsume:* <...>.

### Performance

#### RNF-T-PERF-01 — <título do piso de performance comum>
<Enunciado — ex.: latência padrão de telas/consultas; valores específicos por feature
prevalecem quando declarados.>
*Subsume:* <...>.

### Disponibilidade

#### RNF-T-DISP-01 — <título — ex.: degradação segura e isolamento de falhas>
<Enunciado.>
*Subsume:* <...>.

### Observabilidade

#### RNF-T-OBS-01 — <título — ex.: publicação contínua de métricas / eventos versionados>
<Enunciado.>
*Subsume:* <...>.

### Conformidade

#### RNF-T-CONF-01 — <título — ex.: fundamentação obrigatória em alteração sensível>
<Enunciado.>
*Subsume:* <...>.

<!-- Outras categorias conforme o domínio: Escalabilidade, LGPD/Privacidade, etc. -->

---

## RF transversais

<!-- Requisitos FUNCIONAIS comuns a várias features (ex.: exportação, idempotência,
versionamento de configuração). -->

#### RF-T-01 — <título do requisito funcional comum>
<Enunciado — ex.: exportação CSV/PDF com checksum e registro em trilha, respeitando o
field-level access.>
*Subsume:* <features e IDs locais — opcional>.

#### RF-T-02 — <título>
<Enunciado.>
*Subsume:* <...>.

---

## Integrações

<!-- Catálogo CONSOLIDADO de integrações do produto. NÃO é RF-T nem RNF-T: é uma matriz
sistema × feature. Cada sistema externo/fonte aparece UMA vez (dedupe por sistema); a coluna
"Features que usam" lista todas as features que o tocam. Cada contrato de feature apenas
**referencia** este catálogo (linha única na Cap. 2.3), sem replicar a tabela. Origem
conceitual: item "Integrações e sistemas envolvidos" do Checklist de Levantamento Negocial
(§11). Regras:
- Nomear os sistemas com o **vocabulário canônico** do Glossário (Cap. 2 de visao.md).
- "Papel (consolidado)" descreve a função do sistema no produto, somando os papéis vistos nas features.
- "Direção": consome / produz / bidirecional (a do conjunto de usos).
- "Criticidade / fallback": crítica ou degradável + fallback **coerente** com o RNF-T de
  degradação (ex.: `RNF-T-DISP-01`), citado por ID.
- Marcar `*(inferência)*` para sistemas/papéis deduzidos e `⚠ NÃO IDENTIFICADO — definir:
  <pergunta>` quando faltar confirmação. -->

| Sistema / fonte | Papel (consolidado) | Direção | Criticidade / fallback | Features que usam |
|---|---|---|---|---|
| <sistema, do Glossário> | <para que serve no produto, somando os usos das features> | consome / produz / bidirecional | <crítica / degradável> + <fallback coerente com `RNF-T-DISP-01`> | <feature-a>, <feature-b> |

---

## Notas de uso

- Cada feature deve, no seu Cap. 2, **referenciar os IDs acima** (ex.: "Segurança:
  aplica-se `RNF-T-SEG-01`") e listar apenas os requisitos **específicos** (thresholds
  próprios, regras exclusivas, CTs particulares).
- Quando um valor numérico da feature **diverge** do piso transversal, o valor da feature
  **prevalece** e fica documentado na feature.
- As features **provedoras** dos cross-cuttings (a feature-lar de cada capability comum —
  ex.: controle de acesso, auditoria, métricas, integração) têm parte destes "transversais"
  como requisito **próprio**, não apenas referenciado.

## Relacionado
- [Índice do wiki](index.md)
- [Visão do produto](visao.md)
- [Modelo de dados (transversal)](modelo-dados.md)
- [Telas comuns (arquétipos)](telas-comuns.md)
