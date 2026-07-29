---
name: spec-audit
description: Use quando o usuário quer auditar a clareza do começo da spec (seções 1 a 3) pelo método CSD — Certezas, Suposições e Dúvidas — antes de escrever as features. Complementa o loop crítico, que cobre a seção 7.
---

# spec-audit

Audita as **seções 1 a 3** do `spec.md` (contexto, glossário, regras) pelo método
**CSD — Certezas, Suposições e Dúvidas**: separa o que está firmado do que é inferência e
do que falta, e converte suposição e dúvida em pergunta acionável.

Serve para **validar o alicerce antes de escrever feature**. A crítica da seção 7 é do
loop `spec-critico`; esta skill cobre o que vem antes dele.

> **Grade de cobertura.** Ao auditar levantamento de demanda negocial (contexto, regras e
> fluxos, sem solução técnica), usar o
> [Checklist de Levantamento Negocial](../../docs/checklist-levantamento-negocial.md).
> O item *Integrações e sistemas envolvidos* alimenta a §5.3 (catálogo de integrações).

## Quando usar
Quando o usuário pede para auditar ou revisar a spec, checar se o contexto está sólido o
bastante para avançar, gerar perguntas de refino, ou levantar o que está em aberto.

## Entrada
As seções 1 a 3 do `spec.md`. Pode auditar uma seção isolada ou as três.

## Processo
1. Ler as seções 1 a 3.
2. Classificar cada afirmação relevante:
   - **Certeza** — afirmada com fonte citada, sem `*(inferência)*`, sem `⚠`. Listar para
     o usuário confirmar.
   - **Suposição** — marcada `*(inferência)*` ou apoiada em fonte indireta. Vira pergunta
     de confirmação.
   - **Dúvida** — marcada `⚠ NÃO IDENTIFICADO` ou lacuna evidente. Vira pergunta aberta.
3. Cada suposição e dúvida vira **pergunta acionável**: específica, respondível, citando a
   seção e o ID afetados (`§3, RN-07`).
4. Verificações próprias destas seções:
   - Objetivo (§1.2) é verificável? dá para saber quando o negócio considera atendido?
   - Todo termo usado da §4 em diante está no Glossário (§2)?
   - Toda `RN-NN` tem fonte (documento + seção, ou interlocutor + data)?
   - Alguma `RN` descreve *como implementar* (tela, classe, método) em vez do *o quê*?
   - `RN-AI-NN` é de fato não-determinística, ou é regra determinística disfarçada?
5. Apresentar a matriz CSD, priorizando as perguntas que mais travam o avanço.
6. Registrar as dúvidas que sobrarem na **seção 8** (Questões em aberto) do `spec.md`, com
   o marcador `⚠ NÃO IDENTIFICADO — definir: <pergunta>`.

## Saída
Matriz CSD com as certezas listadas e as suposições/dúvidas convertidas em perguntas
acionáveis priorizadas, mais a seção 8 do `spec.md` atualizada. Relatório longo vai em
arquivo (`criticas/csd-<data>.md`), não no chat.
