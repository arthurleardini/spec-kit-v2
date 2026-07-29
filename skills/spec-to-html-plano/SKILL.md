---
name: spec-to-html-plano
description: Use quando o usuário quer iniciar um protótipo HTML navegável de um produto a partir da seção 7 (Features) — fase de plano: cria o repo do protótipo e seleciona o conjunto 80/20 de telas.
---

# spec-to-html-plano

Primeira fase da geração de um protótipo HTML navegável a partir da Camada de
seção 7 do `spec.md`. Cria o repositório do protótipo e decide **quais telas
prototipar** — o recorte 80/20 da jornada — emitindo a tabela de telas que as fases
seguintes consomem.

Faz parte da família `spec-to-html` (ver a skill `spec-to-html` para o fluxo
completo). É a fase que abre o primeiro checkpoint: a tabela de telas deve ser
validada pelo usuário antes de construir qualquer coisa.

## Quando usar
Quando o usuário pede um protótipo navegável de um produto e a seção 7 já
existe no wiki. Sempre a primeira das skills `spec-to-html-*` a rodar.

## Entrada
- A seção 7 (Features) do wiki: o 7.N.1 e 7.N.2 (fluxo e telas) de cada
  `spec.md` (seção 7.N) e o catálogo o Anexo A (componentes).
- A seções 1 a 3 (as seções 1 a 3 do `spec.md`) para conhecer as personas e priorizar.

## Processo
1. Criar o repositório do protótipo num diretório separado do wiki —
   `<produto>-prototipo/`. Rodar `git init`, criar `.gitignore` e um `README.md`
   stub de uma linha (o `spec-to-html-build` finaliza o README depois).
   Opcionalmente registrar `docs/spec-prototipo-v0.md` com escopo e decisões fixadas.
2. Ler as subseções 7.N.1 e 7.N.2 (fluxo e telas) das features e as personas de §1.3.
3. Selecionar o conjunto 80/20 de telas — ~10-12 telas que cobrem a maior parte do
   valor. Priorizar a jornada da persona primária de ponta a ponta; incluir telas de
   setup e pontes entre personas só quando necessárias para a jornada fazer sentido.
4. **Organizar o fluxo de informação (ver Princípios transversais em `spec-to-html`):**
   - Agrupar as telas em **poucas áreas de menu** (não um item por tela). Nomear os grupos
     pela cadeia de valor / por modo de uso (ex.: Carteira · Operação · Analytics ·
     Configurações).
   - **Separar configuração de operação:** toda tela de parâmetro vai para um grupo
     **Configurações**; telas operacionais não carregam blocos de config.
   - Marcar quais telas são **navegação interna** (detalhe que abre em drawer lateral,
     editor que abre por clique/modal) em vez de item de menu próprio — essas não entram
     na sidebar, são alcançadas de dentro de outra tela.
5. Emitir a tabela de telas: uma linha por tela, colunas `id` · tela · **área (grupo de menu)** ·
   **acesso (menu | interna: drawer/modal/clique)** · persona · feature-fonte. O `id` segue o padrão `tela-<slug>`.
6. **Checkpoint:** apresentar a tabela (com áreas e acesso) ao usuário e aguardar validação antes de
   passar para `spec-to-html-scaffold`.

## Saída
- O repositório `<produto>-prototipo/` inicializado (git, `.gitignore`, README stub,
  `docs/` opcional).
- A tabela de telas validada — entrada das fases `scaffold` e `telas`.
