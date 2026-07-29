---
name: feature-dados
description: Use quando o usuário quer escrever ou revisar os dados de uma feature — subseção 7.N.5 do `spec.md`, que referencia as entidades canônicas da seção 4 e descreve só o que é próprio da feature.
---

# feature-dados

Dona da subseção **7.N.5 (Dados)** de uma feature.

Responde: *que informação a feature manipula?* O modelo é **derivado**, não paralelo:
nasce do fluxo e das telas já escritos, não é artefato independente.

## Quando usar
Quando o usuário pede o modelo de dados, as entidades, os campos ou as relações de uma
feature.

## Entrada
Seção 4 (modelo de dados canônico), seção 2 (Glossário) e as subseções 7.N.1 a 7.N.4 já
escritas.

## Processo

1. Abrir com a linha de referência canônica:
   `Entidades canônicas usadas (§4): <Entidade>, <Entidade>.`
   Referenciar por nome, sem re-modelar. **Entidade canônica não se redescreve aqui.**
2. Descrever **só o que é próprio** da feature — configuração, log, instância de execução
   (`*_log`, `*_execucao`) e os campos que a feature acrescenta. Uma subseção por entidade
   própria, com tabela `Campo | Tipo | Descrição`.
3. Derivar conforme o eixo declarado nos metadados da feature:
   - `eixo=classe` — cada formulário/objeto da 7.N.2 **é** uma entidade. Já existe em §4?
     referenciar e listar apenas os campos próprios.
   - `eixo=processo` — derivar das **atividades** do fluxo (7.N.1): cada informação
     processada ou produzida referencia uma entidade canônica ou vira entidade própria.
4. **Tipo agnóstico e obrigatório** em todo campo: `texto`, `número`, `data`, `booleano`,
   `referência`. Campo sem tipo é achado do gate.
5. Para campo que também existe numa entidade canônica, declarar se a feature é **dona**
   do campo ou apenas o **referencia**. É o que evita divergência entre features.
6. Verificar que o modelo **sustenta** os RF da 7.N.3: cada estado, contagem, carimbo ou
   vínculo que um RF exige tem campo aqui.
7. Entidade própria que aparece em ≥2 features deve subir para §4 — acionar
   `spec-transversais`, não duplicar.
8. Relações com cardinalidade (`1:N`, `N:N`, `1:1`) entre entidades próprias e canônicas.

## Proibido nesta subseção
Endpoint, contrato de API, método HTTP, DDL/SQL, tipo de banco, nome de índice. É modelo
**conceitual**: entidade, campo, relação. Terminologia vem do Glossário (§2).

## Saída
Subseção 7.N.5 preenchida: canônicas referenciadas por nome, entidades próprias com campos
tipados e fonte da verdade declarada, relações com cardinalidade.
