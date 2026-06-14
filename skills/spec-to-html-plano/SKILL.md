---
name: spec-to-html-plano
description: Use quando o usuário quer iniciar um protótipo HTML navegável de um produto a partir da Camada de Requisitos — fase de plano: cria o repo do protótipo e seleciona o conjunto 80/20 de telas.
---

# spec-to-html-plano

Primeira fase da geração de um protótipo HTML navegável a partir da Camada de
Requisitos de um wiki wikiLLM. Cria o repositório do protótipo e decide **quais telas
prototipar** — o recorte 80/20 da jornada — emitindo a tabela de telas que as fases
seguintes consomem.

Faz parte da família `spec-to-html` (ver a skill `spec-to-html` para o fluxo
completo). É a fase que abre o primeiro checkpoint: a tabela de telas deve ser
validada pelo usuário antes de construir qualquer coisa.

## Quando usar
Quando o usuário pede um protótipo navegável de um produto e a Camada de Requisitos já
existe no wiki. Sempre a primeira das skills `spec-to-html-*` a rodar.

## Entrada
- A Camada de Requisitos do wiki: o Cap. 1 (Telas & Fluxos) de cada
  `refined/Requisitos/<feature>.md` e o catálogo `refined/componentes.md`.
- A Camada de Intenção (`refined/visao.md`) para conhecer as personas e priorizar.

## Processo
1. Criar o repositório do protótipo num diretório separado do wiki —
   `<produto>-prototipo/`. Rodar `git init`, criar `.gitignore` e um `README.md`
   stub de uma linha (o `spec-to-html-build` finaliza o README depois).
   Opcionalmente registrar `docs/spec-prototipo-v0.md` com escopo e decisões fixadas.
2. Ler o Cap. 1 (Telas & Fluxos) dos `Requisitos/<feature>.md` das features e as personas da Camada de Intenção.
3. Selecionar o conjunto 80/20 de telas — ~10-12 telas que cobrem a maior parte do
   valor. Priorizar a jornada da persona primária de ponta a ponta; incluir telas de
   setup e pontes entre personas só quando necessárias para a jornada fazer sentido.
4. Emitir a tabela de telas: uma linha por tela, colunas `id` · tela · persona ·
   feature-fonte. O `id` segue o padrão `tela-<slug>`.
5. **Checkpoint:** apresentar a tabela ao usuário e aguardar validação antes de
   passar para `spec-to-html-scaffold`.

## Saída
- O repositório `<produto>-prototipo/` inicializado (git, `.gitignore`, README stub,
  `docs/` opcional).
- A tabela de telas validada — entrada das fases `scaffold` e `telas`.
