---
name: contrato-blueprint
description: Use quando o usuário quer gerar ou revisar o blueprint do produto — a visão geral da solução como cadeia de valor — na Camada de Contrato do modelo wikiLLM.
---

# contrato-blueprint

Gera o documento `blueprint.md` da Camada de Contrato no wiki, em `refined/blueprint.md`.

Responde à pergunta-mãe *Como as features se encaixam na solução?* — apresenta a visão geral do produto organizada como cadeia de valor: cada etapa agrupa as features que a compõem. É um documento **product-level** — um por produto, não por feature.

## Quando usar
Quando o usuário pede para criar, escrever ou revisar o blueprint do produto — ou pede para mostrar a visão geral da solução, organizar as features em cadeia de valor, ou montar o mapa navegável das features.

## Entrada
As entidades de feature em `refined/entities/features/` e a Camada de Intenção em `refined/intencao/` (produto, jobs, personas). Se a fonte for documento binário (PDF/DOCX/PPTX), converter com `markitdown` antes de ler.

## Processo
1. Ler as entidades de feature e a Camada de Intenção para entender o produto e suas features.
2. Preencher o template `templates/contrato/blueprint.md` do spec-kit:
   - Cada etapa da cadeia de valor é um heading `## `.
   - Sob cada etapa, um bullet por feature no formato:
     `- [<feature legível>](entities/features/<slug>.md) — <resumo>  [ator:<ator>] [ia]`
   - O marcador `[ator:<ator>]` indica a persona principal; `[ia]` marca features com componente de IA (omitir quando não houver).
3. Ordenar as etapas conforme a sequência da cadeia de valor; cada feature aparece na etapa onde entrega valor.
4. Salvar em `refined/blueprint.md`, com frontmatter `tipo: blueprint`.
5. **Após gerar ou atualizar o `blueprint.md`, rodar** `python3 <spec-kit>/scripts/build-navigator.py <wiki>` (ou a skill `spec-navigator`) para que o blueprint apareça como tela de cadeia de valor dentro do `refined-navigator.html`. (`<wiki>` é o diretório que contém `refined/`.)
6. Atualizar `refined/index.md` e anexar entrada em `refined/log.md`.

## Saída
- `refined/blueprint.md` preenchido conforme o template, com frontmatter `tipo: blueprint` — features organizadas em etapas de cadeia de valor.
- O blueprint renderizado como tela navegável dentro do `refined-navigator.html` (gerado pelo `build-navigator.py`).
