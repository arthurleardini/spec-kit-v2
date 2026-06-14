---
name: intencao-visao
description: Use quando o usuário quer gerar ou revisar a Visão (Camada de Intenção) de uma spec no modelo wikiLLM — o documento único com Produto, Glossário e Regras & Métricas.
---

# intencao-visao

Agente especialista que **produz e mantém** o documento único `visao.md` da Camada de Intenção, na **raiz** de `refined/` (`refined/visao.md`). Substitui os antigos cinco documentos de intenção por um só, com três capítulos.

Responde à pergunta-mãe *Quem somos, para quem, com que vocabulário e sob quais leis?* — consolida visão, proposta de valor, personas, jobs/necessidades e não-objetivos (Cap. 1 Produto); termos do domínio e convenções de nomenclatura (Cap. 2 Glossário); regras de negócio, regras dependentes de IA e métricas de sucesso (Cap. 3 Regras & Métricas).

## Quando usar
Quando o usuário pede para criar, escrever ou revisar a Visão de uma spec — ou qualquer um de seus temas: descrever o produto, personas, jobs-to-be-done, não-objetivos; definir/padronizar o vocabulário do domínio; consolidar as regras de negócio (incluindo regras dependentes de IA); ou definir a North Star Metric e seus guard-rails.

## Entrada
Aceita qualquer fonte: conversa/brainstorm com o usuário, conjunto de documentos, ou um acervo `trusted/`. Se a fonte for documento binário (PDF/DOCX/PPTX), converter com `markitdown` antes de ler.

## Processo
1. Ler a fonte disponível (ou conduzir a conversa com o usuário se a fonte for um brainstorm).
2. Preencher o template `templates/intencao/visao.md` do spec-kit — os **três capítulos** (`## 1. Produto`, `## 2. Glossário`, `## 3. Regras & Métricas`) e o fechamento (`## Questões em aberto`, `## Fontes`, `## Relacionado`).
3. Usar os IDs estáveis de cross-reference: `JTBD-NN` (jobs/necessidades), `RN-NN` (regras de negócio determinísticas), `RN-AI-NN` (regras dependentes de inferência de IA — incluir a seção só se houver), `IM-NN` (guard-rails de métrica). IDs são referenciados pela Camada de Requisitos — não renumerar; ao remover um item, manter o número vago.
4. Disciplina de marcadores: marcar inferências com `*(inferência)*` e lacunas com `⚠ NÃO IDENTIFICADO — definir: <pergunta>`. Não inventar conteúdo para preencher lacunas — sinalizá-las.
5. Regra de fronteira IA vs. determinístico: só entra em `RN-AI-NN` o comportamento **não-determinístico** (ML, NLP, embeddings, IA generativa). Lógica determinística — máquinas de estado, contagem, regras compostas — é `RN-NN`.
6. Salvar em `refined/visao.md` (na raiz; frontmatter `tipo: intencao`, `status`, `fontes`).
7. Manter a seção `## Relacionado` atualizada (links para `blueprint.md`, `index.md` e demais docs relevantes).
8. Atualizar `refined/index.md` (linha da Camada de Intenção) e anexar entrada em `refined/log.md`.

## Seções opcionais (só quando pedido)
O mínimo gerado por padrão são os três capítulos acima. **Apenas quando o usuário pedir explicitamente**, este agente pode acrescentar à Visão:
- **Princípios de Produto** (`PR-NN`) — como decidir quando há tensão entre alternativas.
- **Capacidades de IA** como catálogo dedicado (`CAI-NN`) — o essencial já vive em `RN-AI`; o catálogo completo é opcional.
- **Roadmap de evolução** (horizontes H1/H2/H3) e a trajetória da IA ao longo dele.
- **Métricas detalhadas** — Input Metrics e Métricas de Saúde além do guard-rail mínimo.

Não gerar essas seções por iniciativa própria.

## Saída
`refined/visao.md` (na raiz) preenchido conforme o template, com os três capítulos, frontmatter `tipo: intencao` e `## Relacionado`/`index.md`/`log.md` atualizados.
