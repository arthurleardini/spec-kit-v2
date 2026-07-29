---
name: spec-contexto
description: Use quando o usuário quer escrever ou revisar o começo da spec — contexto, problema, objetivo, personas, não-objetivos, glossário e regras de negócio (seções 1 a 3 do `spec.md`).
---

# spec-contexto

Dona das **seções 1 a 3** do `spec.md`: o *por que e para quem*, o vocabulário e as leis
do domínio.

Responde: *que problema, para quem, com que vocabulário e sob quais regras?*

## Quando usar
Quando o usuário pede para descrever o produto, o problema, personas, jobs, não-objetivos;
padronizar o vocabulário do domínio; ou consolidar as regras de negócio.

## Entrada
Qualquer fonte: conversa, acervo de documentos, ou pipeline `trusted/`. Fonte binária
(PDF/DOCX/PPTX) passa por `markitdown` antes.

## Registro

Seções 1 a 3 são o **único lugar narrativo** da spec. Prosa curta, densa, sem bullet
decorativo. Da seção 7 em diante o registro é estruturado (tabela + EARS-PT); não misturar.

## Processo

1. Ler a fonte, ou conduzir a conversa se a fonte é brainstorm.
2. Escrever no `spec.md`:
   - **1.1 Problema** — situação atual e a dor concreta. Não descrever solução.
   - **1.2 Objetivo** — resultado verificável em linguagem de negócio.
   - **1.3 Personas e necessidades** — tabela persona → necessidade → `JTBD-NN`.
   - **1.4 Não-objetivos** — o que a spec deliberadamente não resolve.
   - **2. Glossário** — termo → definição → fonte. É o guard-rail de linguagem: todo termo
     usado da seção 4 em diante tem de estar aqui.
   - **3. Regras de negócio** — `RN-NN` (determinístico) e `RN-AI-NN` (depende de
     inferência de IA), cada um com **fonte** citada.
3. **Fronteira IA × determinístico:** só é `RN-AI-NN` o comportamento não-determinístico
   (ML, NLP, embeddings, IA generativa). Máquina de estados, contagem e regra composta
   são `RN-NN`.
4. IDs (`JTBD-NN`, `RN-NN`, `RN-AI-NN`) são estáveis — a seção 7 os cita. Não renumerar;
   ao remover um item, deixar o número vago.
5. Marcar inferência com `*(inferência)*` e lacuna com
   `⚠ NÃO IDENTIFICADO — definir: <pergunta>`, e listar a lacuna na seção 8. Não inventar
   conteúdo para tapar buraco.
6. Respeitar o teto de palavras da seção 1 (`regras/criticas.toml`, `[tetos.secoes]`).
   Glossário e Regras não têm teto — são tabela de domínio, onde volume é conteúdo.
   Estourou o teto da seção 1? cortar prosa, não subir o teto.

## Opcional (só quando pedido)
Princípios de produto (`PR-NN`), catálogo de capacidades de IA (`CAI-NN`), roadmap por
horizonte, métricas de input/health. Não gerar por iniciativa própria — o essencial de IA
já vive em `RN-AI-NN`.

## Saída
Seções 1, 2 e 3 do `spec.md` preenchidas, com IDs estáveis e fonte por regra.
