---
name: spec-cadeia-valor
description: Use quando o usuário quer a visão geral de como as features se encaixam — o Anexo B (Cadeia de valor) do `spec.md`, que agrupa as features por etapa do processo de negócio.
---

# spec-cadeia-valor

Dona do **Anexo B — Cadeia de valor** do `spec.md`.

Responde: *como as features se encaixam na solução?* É a única visão product-level da
spec — uma tabela, não um documento.

## Quando usar
Quando o usuário pede a visão geral da solução, o encadeamento das features, ou como o
produto cobre o processo de negócio.

## Entrada
As features da seção 7 e o contexto da seção 1 (problema, objetivo, personas).

## Processo
1. Ler as features da seção 7 e o contexto.
2. Escrever a tabela `Etapa | Features`, uma linha por etapa do processo de negócio, na
   sequência em que o valor é entregue. Cada feature aparece na etapa em que entrega
   valor, citada pelo número da seção (`7.1`, `7.3`).
3. Feature que não cabe em nenhuma etapa é sinal de escopo solto: ou a etapa falta, ou a
   feature está fora do problema declarado em §1.1. Registrar como lacuna na seção 8, não
   inventar etapa.
4. Manter no anexo. Cadeia de valor é orientação de leitura, não requisito — não pode
   competir com a seção 7 pela atenção do leitor.

## Saída
Anexo B preenchido: etapas na ordem da cadeia de valor, com as features de cada uma
citadas por número de seção.
