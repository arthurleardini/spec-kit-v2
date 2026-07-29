---
name: spec-transversais
description: Use quando o usuário quer gerar ou manter o que é comum a várias features — modelo de dados canônico, requisitos não-funcionais e funcionais transversais, catálogo de integrações e arquétipos de tela (seções 4 a 6 do `spec.md`).
---

# spec-transversais

Dona das **seções 4 a 6** do `spec.md`. É a skill que impede a spec de duplicar.

Princípio: **o que é comum a duas features vive uma vez**, aqui, e a feature cita por ID.

## Quando usar
Quando o usuário pede o modelo de dados do produto, os requisitos não-funcionais, o
catálogo de integrações ou os arquétipos de tela — e sempre que uma feature nova entra na
seção 7 (para varrer o que subiu de comum).

## Entrada
As seções 1 a 3 (vocabulário e regras) e todas as features já escritas na seção 7.

## Processo

1. **§4 Modelo de dados** — entidades canônicas do produto, uma vez.
   - `4.1 Entidades` — nome, definição, campos-chave. Nome vem do Glossário (§2).
   - `4.2 Relações` — `erDiagram` em Mermaid.
   - Varrer a seção 7: entidade que aparece em ≥2 features **sobe** para cá; a feature
     passa a referenciá-la.
   - Para cada entidade, declarar a **fonte da verdade** (quem é dona do dado). É o que
     evita divergência entre features do mesmo programa.

2. **§5 Requisitos transversais** — o **único** lugar onde requisito não-funcional existe.
   - `5.1 Não-funcionais` — `RNF-T-<categoria>-NN` com **mecanismo** declarado, não prosa
     genérica. Categorias: SEG, AUD, LGPD, DISP, PERF, OBS, CONF, ESC.
     - Segurança/LGPD exige concreto: matriz perfil × ação, base legal por dado, retenção.
     - Imutabilidade exige o *como* (ex.: PDF/A + SHA-256 + ICP-Brasil + WORM).
     - Observabilidade é obrigatória: métrica de negócio, métrica técnica, alerta, log.
   - `5.2 Funcionais transversais` — `RF-T-NN` em EARS-PT, para o RF que vale em ≥2 features.
   - `5.3 Integrações` — matriz sistema × papel × direção × criticidade × features.
     Cada integração tem ficha (endpoint, payload, idempotência, mapa de erro, SLA) **ou**
     o marcador `⚠ NÃO IDENTIFICADO — depende de: <origem>`.

3. **§6 Arquétipos de tela** — `A-NN` com bloco ` ```wireframe ` e "Quando usar".
   Padrão de tela que aparece em ≥2 features vira arquétipo aqui; a tela da feature só
   descreve o que muda.

4. **Emagrecer a seção 7.** Depois de promover algo para cá, voltar em cada feature e
   trocar o texto duplicado pela citação do ID. Promover sem emagrecer piora a spec.

5. Respeitar os tetos de `[tetos.secoes]` (`modelo_dados`, `transversais`, `arquetipos`).
   Estourou? o excesso é detalhe de implementação ou repetição — cortar.

## Saída
Seções 4, 5 e 6 do `spec.md` preenchidas, e as features da seção 7 emagrecidas para apenas
citar os IDs promovidos.
