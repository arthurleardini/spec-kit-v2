---
name: contrato-dados
description: Use quando o usuário quer gerar ou revisar o modelo de Dados (Cap. 3) do doc de Requisitos de uma feature no modelo wikiLLM — referencia o modelo de dados transversal e descreve só o que é próprio da feature.
---

# contrato-dados

Escreve e mantém o **Capítulo 3 — Dados** do documento único `refined/Requisitos/<feature>.md` da Camada de Requisitos. Não cria arquivo solto: o doc de requisitos de cada feature é **um só** (3 capítulos — Telas & Fluxos, Requisitos & Cenários, Dados); esta skill é dona do Cap. 3.

Responde à pergunta-mãe *Que informação a feature manipula?* — descreve o modelo de dados conceitual: entidades, campos e relações. O modelo é **derivado, não paralelo**: nasce do eixo da feature, não é um artefato independente.

**Pense transversalmente.** As entidades canônicas do produto vivem em `refined/modelo-dados.md` (modelo de dados transversal). Este capítulo **referencia** essas entidades por nome e descreve **apenas o que é próprio** da feature: configurações, logs e instâncias de execução (ex.: `*_log`, `*_execucao`) e campos específicos. **Não re-modelar** aqui uma entidade canônica — se ela já existe em `modelo-dados.md`, apenas apontar para ela. Se a feature usa uma entidade que ainda não é canônica e ela se repete em outra feature, promovê-la ao transversal (skill `spec-transversais`).

**Regra de não-sobreposição** (ver bloco-intro do `Requisitos/<feature>.md`): cada fato mora em UM lugar. Este capítulo é o modelo conceitual próprio da feature; entidades canônicas são de `modelo-dados.md` (citadas por nome); invariantes de domínio permanecem como `RN-NN` na Visão (citados por ID); o que o sistema deve fazer fica na tabela RF do Cap. 2.2.

## Quando usar
Quando o usuário pede para criar, escrever ou revisar o modelo de dados de uma feature — ou pede para listar as entidades, os campos ou as relações de informação que a feature acrescenta ao modelo canônico.

## Eixo (`processo` | `classe`) — como derivar
Ler `eixo` no frontmatter do `Requisitos/<feature>.md`. O Cap. 3 **deriva** do que já foi escrito nos capítulos anteriores:
- **`eixo=classe`** — cada formulário/objeto do Cap. 1 **é** uma entidade; se já existe em `modelo-dados.md`, referenciá-la e listar só os campos próprios. Não inventar entidades paralelas às telas.
- **`eixo=processo`** — derivar as entidades das **atividades** do fluxo (Cap. 1.1): cada informação processada/produzida referencia uma entidade canônica ou vira entidade própria da feature.
Anotar a origem de cada entidade própria (ex.: `<!-- deriva de: formulário X | atividade Y; referencia <Entidade canônica> de ../modelo-dados.md -->`).

## Entrada
`refined/modelo-dados.md` (modelo de dados transversal — fonte das entidades canônicas), a Camada de Intenção em `refined/visao.md` (Glossário §2 para o vocabulário; Regras §3), a fonte da feature e os **Caps. 1 e 2** já preenchidos no `Requisitos/<feature>.md`. Se a fonte for documento binário (PDF/DOCX/PPTX), converter com `markitdown` antes de ler.

## Processo
1. Ler `refined/modelo-dados.md`, `refined/visao.md` e a fonte da feature. Conferir o `eixo` e reler os Caps. 1–2 do `Requisitos/<feature>.md` (deles vem o modelo).
2. No mesmo `refined/Requisitos/<feature>.md`, preencher o **Cap. 3 — Dados**, sem tocar nos Caps. 1 e 2, **derivando** conforme o `eixo`:
   - **3.1 Entidades canônicas usadas:** listar, por nome, as entidades de `../modelo-dados.md` que a feature consome — sem re-modelá-las — e como a feature as usa.
   - **3.2 Entidades próprias da feature:** uma subseção por entidade específica (config/log/execução), com tabela de campos. O tipo de cada campo é **simples e agnóstico** — `texto`, `número`, `data`, `booleano`, `referência`.
   - **3.3 Relações:** cardinalidade (`1:N` / `N:N` / `1:1`) entre entidades próprias e/ou canônicas referenciadas.
3. **Proibido** neste capítulo: endpoints, contratos de API, métodos HTTP, DDL/SQL, tipos de banco específicos e diagramas. Apenas o modelo conceitual — entidades, campos e relações.
4. Usar a terminologia do Glossário (Cap. 2 de `visao.md`). Marcar lacunas com `⚠ NÃO IDENTIFICADO — definir: <pergunta>` e inferências com `*(inferência)*`.
5. Salvar o `Requisitos/<feature>.md`. Atualizar `refined/index.md` (linha da feature) e anexar entrada em `refined/log.md`.

## Saída
**Cap. 3** do `refined/Requisitos/<feature>.md` preenchido, com frontmatter `tipo: contract` — as entidades canônicas referenciadas de `../modelo-dados.md`, somente as entidades/campos **próprios** da feature (tipos agnósticos) e as relações, **derivados** do eixo da feature.
