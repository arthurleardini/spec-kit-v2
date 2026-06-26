# Checklist — Especificação de Demanda Negocial

Modelo de validação para **um único documento** de levantamento de demanda: contexto, regras e fluxos — **sem proposta de solução técnica**.

Artefato de referência do **spec-kit**: serve para auditar uma spec de demanda negocial (o *o quê* e o *por quê* do negócio) **antes** de avançar para a Camada de Requisitos / modelagem técnica. O item "Integrações e sistemas envolvidos" (seção 11) é a origem conceitual do **catálogo de Integrações** (seção `## Integrações`) do `requisitos-transversais.md` — cada feature apenas o referencia por uma linha na Cap. 2.3 do contrato.

> **Escopo deste checklist:** o documento descreve *o quê* o negócio precisa e *por quê*. Modelagem técnica, gap de plataforma e plano de implementação ficam para etapas posteriores.

---

## Como usar

1. **Validação** — percorra a seção [Checklist de validação](#checklist-de-validação) e marque cada item.
2. **Redação** — use a seção [Estrutura do documento](#estrutura-do-documento) como índice obrigatório ao criar ou revisar uma spec.
3. **Estados** — para cada item:
   - `[ ]` **Ausente** — seção não existe ou está vazia
   - `[~]` **Parcial** — existe, mas sem fonte, ID ou cobertura incompleta
   - `[x]` **Atende** — preenchido conforme mínimo

**Regra geral:** o bloco inicial do documento declara **propósito** e **limitações** do levantamento.

---

## Metadados obrigatórios (frontmatter)

Todo documento consolidado deve iniciar com YAML contendo, no mínimo:

```yaml
---
tipo: especificacao-demanda-negocial
projeto: "nome-do-projeto"
versao: "0.1.0"
criado_em: "AAAA-MM-DD"
atualizado_em: "AAAA-MM-DD"
autor: "nome ou agente"
origem: "artefato(s) de entrada"
---
```

### Checklist — metadados

- [ ] `tipo`, `projeto`, `versao`, `criado_em` presentes
- [ ] `origem` aponta para insumo(s) rastreáveis (transcrição, ata, apresentação, etc.)
- [ ] Bloco inicial declara **propósito** e **limitações** (ex.: escopo do levantamento, premissas assumidas)
- [ ] Documento **não contém** proposta técnica, classes/modelagem de plataforma ou plano de implementação

---

## Estrutura do documento

Ordem recomendada das seções. Numeração flexível; **nomes e conteúdo mínimo são obrigatórios**.

| # | Seção | O que deve conter |
|---|--------|-------------------|
| 1 | **Contexto** | Situação atual, processo/sistema afetado, evolução pretendida |
| 2 | **Glossário** | Termos de domínio, siglas, sistemas externos |
| 3 | **Problema / dor** | Lacunas de hoje; impacto operacional |
| 4 | **Objetivo** | Resultado verificável em linguagem de negócio |
| 5 | **Escopo** | Dentro / fora; fases futuras explicitamente excluídas |
| 6 | **Atores** | Tabela papel × responsabilidade no fluxo |
| 7 | **Restrições e premissas** | Regras fixas, dependências, limitações, calendário |
| 8 | **Riscos** | Ameaças ao levantamento ou ao processo; impacto e mitigação |
| 9 | **Regras de negócio** | RN-xxx com fonte e flag obrigatória/opcional |
| 10 | **Fluxos de negócio** | Sequências passo a passo + tabela passo × descrição × fonte |
| 11 | **Integrações e sistemas envolvidos** | Sistemas externos, documentos, dependências de negócio (não modelagem) |
| 12 | **Critérios de aceite** | Condições para considerar o levantamento negocial completo |
| 13 | **Referências** | Documentos, transcrições, atas citadas |

---

## Convenções de identificação

| Prefixo | Uso | Exemplo |
|---------|-----|---------|
| `RN-xxx` | Requisito / regra de negócio | RN-007: soma por fundo ≤ teto |

**Rastreabilidade mínima:** toda RN obrigatória deve apontar para **fonte** (documento + seção ou interlocutor + data).

**Separação obrigatória:**

| Natureza | Onde documentar | Marcador |
|----------|-----------------|----------|
| Fato documentado | Seções 9–10 | Fonte citada |
| Proposta de solução | **Fora deste documento** | Etapa posterior (modelagem técnica / plataforma) |

---

## Checklist de validação

### 1. Contexto e motivação

- [ ] **1.1** Contexto descreve processo/sistema e situação atual
- [ ] **1.2** Glossário (seção 2) define termos, siglas e sistemas usados no documento
- [ ] **1.3** Problema/dor lista lacunas concretas (não genéricas)
- [ ] **1.4** Objetivo é verificável — dá para saber quando o negócio considera atendido
- [ ] **1.5** Escopo **dentro** listado explicitamente
- [ ] **1.6** Escopo **fora** listado (integrações, migração, fases futuras, solução técnica)
- [ ] **1.7** Atores cobrem todos os papéis do fluxo principal
- [ ] **1.8** Restrições incluem premissas e limitações conhecidas do negócio
- [ ] **1.9** Riscos (seção 8) listam ameaças relevantes com impacto e mitigação

### 2. Regras e fluxos de negócio

- [ ] **2.1** Regras numeradas (RN-xxx) — mínimo cobrindo fluxo principal
- [ ] **2.2** Cada RN obrigatória tem **fonte** citada
- [ ] **2.3** Fluxo principal documentado passo a passo (texto ou diagrama)
- [ ] **2.4** Tabela passo × descrição × fonte (ou RN) para fluxo principal
- [ ] **2.5** Fluxos secundários ou exceções relevantes documentados (ex.: devolução, ciclo anual)
- [ ] **2.6** Nenhuma RN descreve *como implementar* (classe, método, tela) — apenas *o quê* o negócio exige

### 3. Integrações e aceite

- [ ] **3.1** Sistemas externos e dependências de negócio listados (se houver)
- [ ] **3.2** Nenhuma RN **obrigatória** sem cobertura em fluxo ou regra explícita
- [ ] **3.3** Critérios de aceite descrevem o levantamento negocial (não implementação)
- [ ] **3.4** Referências completas (seção 13)

### 4. Governança do documento

- [ ] **4.1** Versão presente (identifica a entrega ao cliente)
- [ ] **4.2** Documento livre de proposta técnica, classes/modelagem de plataforma e plano de implementação
- [ ] **4.3** Handoff ou próximo passo definido (validação cliente, análise técnica, protótipo)

---

## Template mínimo (copiar e preencher)

```markdown
---
tipo: especificacao-demanda-negocial
projeto: "nome-do-projeto"
versao: "0.1.0"
criado_em: "AAAA-MM-DD"
origem: "caminho/do/insumo.md"
---

# [Título da demanda]

> [Uma frase: propósito do documento e limitações — ex.: escopo do levantamento e premissas assumidas. Sem proposta de solução técnica.]

## 1. Contexto

## 2. Glossário

| Termo | Definição | Fonte |
|-------|-----------|-------|
| | | |

## 3. Problema / dor

## 4. Objetivo

## 5. Escopo

### Dentro do escopo
-

### Fora do escopo
-

## 6. Atores

| Ator | Papel |
|------|-------|
| | |

## 7. Restrições e premissas

| Restrição | Detalhe |
|-----------|---------|
| | |

## 8. Riscos

| Risco | Impacto | Mitigação |
|-------|---------|-----------|
| | | |

## 9. Regras de negócio

| ID | Regra | Fonte | Obrigatória |
|----|-------|-------|-------------|
| RN-001 | | | sim |

## 10. Fluxos de negócio

### Fluxo principal

\`\`\`text
[Ator] → passo → passo → [resultado]
\`\`\`

| Passo | Descrição | Fonte / RN |
|-------|-----------|------------|
| 1 | | |

## 11. Integrações e sistemas envolvidos

| Sistema / artefato | Papel no processo | Observação |
|--------------------|-------------------|------------|
| | | |

## 12. Critérios de aceite

- [ ] Objetivo e escopo validados com stakeholders
- [ ] Fluxo principal acordado
- [ ] RNs obrigatórias com fonte citada

## 13. Referências

| Referência | Tipo | Observação |
|------------|------|------------|
| | | |
```
