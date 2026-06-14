---
name: spec-audit
description: Use quando o usuário quer auditar a clareza de um documento da spec via CSD — levantar Certezas, Suposições e Dúvidas como perguntas acionáveis antes de avançar de camada.
---

# spec-audit

Lê um documento da spec (tipicamente da Camada de Intenção) e o audita pelo método **CSD — Certezas, Suposições e Dúvidas** — separando o que está firmado do que é inferência e do que falta, e transformando suposições e dúvidas em perguntas acionáveis para o usuário.

Serve para **validar a clareza antes de avançar de camada** — por exemplo, conferir a Camada de Intenção antes de gerar a Camada de Requisitos.

## Quando usar
Quando o usuário pede para auditar/revisar a spec, checar se a Camada de Intenção está sólida o bastante para seguir, gerar perguntas de refino, ou levantar o que ainda está em aberto.

## Entrada
- O(s) documento(s) da spec a auditar — em geral a Visão em `refined/visao.md`, mas vale qualquer página do wiki.
- Pode auditar um documento isolado ou a camada inteira.

## Processo
1. Ler o(s) documento(s) alvo no `refined/`.
2. Classificar cada afirmação relevante em três baldes:
   - **Certezas** — afirmado com base na fonte, sem `*(inferência)*`, sem `⚠`. Listar para confirmar que o usuário concorda.
   - **Suposições** — marcado `*(inferência)*` ou apoiado em fonte fraca/indireta. Cada uma vira uma pergunta de confirmação.
   - **Dúvidas** — marcado `⚠ NÃO IDENTIFICADO` ou lacuna evidente. Cada uma vira uma pergunta aberta.
3. Para cada Suposição e Dúvida, escrever uma **pergunta acionável** — específica, respondível, e que indique o documento/ID afetado.
4. Apresentar o resultado como matriz CSD (Certezas / Suposições / Dúvidas), priorizando as perguntas que mais bloqueiam o avanço de camada.
5. Anexar entrada em `refined/log.md` (`## [YYYY-MM-DD] audit | CSD de <documento>`). Se a matriz for extensa, salvar também uma página em `refined/_archive/`.

## Saída
- Uma matriz CSD com Certezas listadas e Suposições/Dúvidas convertidas em perguntas acionáveis priorizadas.
- Entrada de `audit` no `log.md`; opcionalmente uma página em `refined/_archive/` quando o relatório for grande.
