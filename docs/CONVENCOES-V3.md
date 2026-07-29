---
titulo: Convenções spec-kit v3 — spec única
tipo: convencoes
criado_em: 2026-07-29
status: ativo
---

# Convenções v3 — uma spec, não um wiki

O v2 entregava um **wiki**: `visao.md`, três transversais, um doc por feature,
`index.md`, `log.md`, `overview.md`, `blueprint.md`, `componentes.md`, links relativos
entre páginas. O v3 entrega uma **spec**: um arquivo, seções numeradas, leitura de cima
para baixo.

Motivo medido: no wiki `knowledge_cob`, `visao.md` tinha **15.086 palavras** — o maior
artefato do conjunto, sem teto nenhum. O bloco comum (visão + 3 transversais +
componentes) somava **23.100 palavras** contra **36.500** das 14 features. Espalhar em
arquivos escondia o tamanho; concentrar num arquivo expõe e obriga a cortar.

## Estrutura

```
<dir>/
  spec.md          # a especificação — arquivo único
  CLAUDE.md        # regras de escrita do projeto
  criticas/        # ledgers do loop crítico
  refined-navigator.html   # derivado, gerado pelo build-navigator.py
```

Seções do `spec.md` (esqueleto em `templates/spec.md`):

| Seção | Conteúdo | Skill dona | Registro |
|---|---|---|---|
| 1 | Contexto: problema, objetivo, personas, não-objetivos | `spec-contexto` | narrativa |
| 2 | Glossário | `spec-contexto` | tabela |
| 3 | Regras de negócio (`RN-NN`, `RN-AI-NN`) | `spec-contexto` | tabela |
| 4 | Modelo de dados canônico (`erDiagram`) | `spec-transversais` | tabela + Mermaid |
| 5 | Requisitos transversais (`RNF-T-*`, `RF-T-NN`, integrações) | `spec-transversais` | tabela |
| 6 | Arquétipos de tela (`A-NN` + wireframe) | `spec-transversais` | wireframe |
| 7 | Features — uma subseção `7.N` por feature | `feature-*` | estruturado |
| 8 | Questões em aberto | todas | lista |
| 9 | Fontes | `spec-fontes` | tabela |
| Anexo A | Vocabulário de componentes | — | lista |
| Anexo B | Cadeia de valor | `spec-cadeia-valor` | tabela |

Cada feature `7.N` tem cinco subseções fixas:

```
### 7.N <Nome da feature>
**Eixo:** processo | classe · **Apetite:** <2 semanas | 6 semanas> · **Fora desta feature:** <no-gos>
#### 7.N.1 Fluxo e navegação      (2 Mermaid: fluxo + navegação entre telas)
#### 7.N.2 Telas                  (##### T-NN, com **Arquétipo:** e ```wireframe)
#### 7.N.3 Requisitos funcionais  (tabela, EARS-PT)
#### 7.N.4 Cenários de teste      (##### CT-NN — título (verifica RF-NN))
#### 7.N.5 Dados                  (canônicas por referência + entidades próprias)
```

## O que morreu

| Morreu | Onde foi | Por quê |
|---|---|---|
| `index.md` | numeração das seções | sumário em arquivo separado desatualiza |
| `log.md` | git | histórico de edição é trabalho do versionador |
| `overview.md` | §1 Contexto | duplicava o começo da Visão |
| `blueprint.md` | Anexo B | orientação de leitura, não requisito |
| `componentes.md` | Anexo A | ponteiro de 400 palavras não é documento |
| `visao.md` | §1 a §3 | virou seção, com teto |
| 3 transversais | §4 a §6 | viraram seção, com teto |
| `Requisitos/<feature>.md` | §7.N | virou subseção |
| `## Relacionado` | referência por §número e ID | link relativo é mobília de wiki |
| skill `spec-lint` | `scripts/lint_critico.py` + `spec-critico` | link quebrado e página órfã não existem num arquivo |

## O que mudou de convenção

- **IDs contínuos no documento.** `RF-01`…`RF-40`, `T-01`…, `CT-01`… numerados no spec
  inteiro, não reiniciando por feature. Num arquivo único, `RF-03` tem de ser único.
- **RNF só na §5.** Nenhuma feature define requisito não-funcional; cita `RNF-T-*` por ID.
  O lint bloqueia definição local (regra `N01`).
- **RF em EARS-PT** — 6 padrões, verificados pelo lint (`R01`).
- **Apetite e no-gos** na linha de metadados da feature (Shape Up).
- **Teto por seção** — `[tetos.secoes]` em `regras/criticas.toml` — mais teto global do
  documento. Estourou, corta.
- **Registro por camada** — §1 é narrativa; da §4 em diante é tabela e frase-padrão. Não
  misturar no mesmo bloco.

## Skills renomeadas

| v2 | v3 | Escreve |
|---|---|---|
| `intencao-visao` | `spec-contexto` | §1, §2, §3 |
| `spec-transversais` | `spec-transversais` | §4, §5, §6 |
| `contrato-telas-fluxos` | `feature-telas-fluxos` | §7.N.1, §7.N.2 |
| `contrato-requisitos` | `feature-requisitos` | §7.N.3, §7.N.4 |
| `contrato-dados` | `feature-dados` | §7.N.5 |
| `contrato-blueprint` | `spec-cadeia-valor` | Anexo B |
| `spec-wiki` | `spec-fontes` | roteia fonte nova; consulta |
| `spec-lint` | — | absorvida pelo lint crítico |

O nome `contrato-*` saiu junto com o modelo mental: não existe "camada de contrato", existe
a seção 7.

## Compatibilidade com o wiki v2

`scripts/lint_critico.py` e `scripts/build-navigator.py` aceitam os **dois** formatos. Sem
`spec.md`, procuram `refined/` com `visao.md` e `Requisitos/`. Wiki existente
(`knowledge_cob`, `knowledge-mt`) continua funcionando sem migração.

Migrar um wiki para spec única, quando valer a pena:

1. Concatenar na ordem: `visao.md` → §1-3, `modelo-dados.md` → §4,
   `requisitos-transversais.md` → §5, `telas-comuns.md` → §6, cada
   `Requisitos/<feature>.md` → uma `7.N`, `blueprint.md` → Anexo B,
   `componentes.md` → Anexo A.
2. Renumerar IDs de `RF`/`T`/`CT` para serem contínuos.
3. Trocar link relativo por referência a §número/ID; apagar `## Relacionado`.
4. Promover todo `RNF-<cat>-NN` local para `RNF-T-*` na §5.
5. Rodar `python3 scripts/lint_critico.py spec.md` e tratar o que aparecer — em especial
   `R08` (seção comum acima do teto), que é onde o wiki costuma estar gordo.

## Referências

- Formato e origem das regras: [`referencias-v3.md`](referencias-v3.md).
- Gate e loop de crítica: [`LOOP-CRITICO.md`](LOOP-CRITICO.md).
- Convenções do v2 (histórico): [`CONVENCOES-V2.md`](CONVENCOES-V2.md).
