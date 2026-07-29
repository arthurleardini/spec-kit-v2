#!/usr/bin/env python3
"""
build-navigator.py — Gera um navegador HTML single-file do refined/.

Varre a Camada de Intenção (refined/intencao/visao.md) e a Camada de Contrato
(refined/contracts/<feature>/contrato.md) e embute todo o conteúdo num único
arquivo refined-navigator.html, que abre com duplo-clique (sem servidor).
Blocos ```mermaid embutidos no markdown são renderizados como diagramas.

Uso:
    python3 build-navigator.py [diretorio-do-wiki]

Rode novamente sempre que os .md mudarem.
"""
import json
import re
import sys
from pathlib import Path

BASE = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
REFINED = BASE / "refined"
CONTRACTS = REFINED / "contracts"
OUT = BASE / "refined-navigator.html"

DOC_LABELS = {
    "contrato": "Contrato",
    # compatibilidade com docs antigos (caso existam):
    "06-telas-fluxos": "06 · Telas e Fluxos",
    "07-historias": "07 · Histórias",
    "08-requisitos": "08 · Requisitos",
    "09-dados": "09 · Dados",
}


def read(p: Path) -> str:
    txt = p.read_text(encoding="utf-8")
    return strip_frontmatter(txt)


def strip_frontmatter(txt: str) -> str:
    """Remove o bloco YAML frontmatter inicial (--- ... ---) para não vazar no render."""
    if txt.startswith("---"):
        end = txt.find("\n---", 3)
        if end != -1:
            nl = txt.find("\n", end + 1)
            return txt[nl + 1:].lstrip("\n") if nl != -1 else ""
    return txt


def md_title(p: Path) -> str:
    """Primeiro heading '# ' do arquivo, ou o stem."""
    if not p.stat().st_size:
        return p.stem
    for line in read(p).splitlines():
        s = line.strip()
        if s.startswith("# "):
            return s[2:].strip()
    return p.stem


def parse_blueprint(text):
    """Parseia blueprint.md em [{'etapa': str, 'features': [{nome,href,resumo,ator,ia}]}]."""
    etapas = []
    atual = None
    for line in text.splitlines():
        h2 = re.match(r"^##\s+(.+)$", line)
        if h2:
            atual = {"etapa": h2.group(1).strip(), "features": []}
            etapas.append(atual)
            continue
        if atual is None:
            continue
        b = re.match(r"^\s*-\s+\[([^\]]+)\]\(([^)]+)\)\s*(.*)$", line)
        if b:
            nome, href, resto = b.group(1), b.group(2), b.group(3)
            am = re.search(r"\[ator:([^\]]+)\]", resto)
            ator = am.group(1).strip() if am else None
            ia = "[ia]" in resto
            resumo = re.sub(r"\[ator:[^\]]+\]|\[ia\]", "", resto).lstrip("-— ").strip()
            atual["features"].append({"nome": nome, "href": href, "resumo": resumo,
                                      "ator": ator, "ia": ia})
    return [e for e in etapas if e["features"]]


def _slug(txt: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", txt.lower()).strip("-")
    return s or "secao"


def acha_spec() -> Path | None:
    """Formato v3: um `spec.md` por produto. Preferido sobre o wiki de vários arquivos."""
    for cand in (BASE / "spec.md", REFINED / "spec.md"):
        if cand.is_file():
            return cand
    return None


def collect_spec(spec: Path):
    """Fatia o spec.md por seção `##`. Cada seção vira um doc do navegador; as features
    (subseções `###` da seção Features) viram um grupo. Mesmo formato de saída do modo
    wiki, então o render de Mermaid e wireframe continua igual."""
    linhas = read(spec).splitlines()
    caminho = str(spec.relative_to(BASE))
    docs, tree = {}, []

    h2 = [(i, m.group(1).strip()) for i, ln in enumerate(linhas)
          if (m := re.match(r"^##\s+(.+)$", ln))]

    if h2 and h2[0][0] > 0:                       # título + preâmbulo antes da 1ª seção
        docs["spec/capa"] = {"title": "Capa", "path": caminho,
                             "content": "\n".join(linhas[:h2[0][0]])}
        tree.append({"label": "capa", "type": "doc", "id": "spec/capa"})

    for idx, (ini, titulo) in enumerate(h2):
        fim = h2[idx + 1][0] if idx + 1 < len(h2) else len(linhas)
        bloco = linhas[ini:fim]
        doc_id = f"spec/{_slug(titulo)}"
        e_features = "feature" in titulo.lower()

        if e_features:
            kids = []
            sub = [(j, m.group(1).strip()) for j, ln in enumerate(bloco)
                   if (m := re.match(r"^###\s+(.+)$", ln))]
            intro = "\n".join(bloco[1:sub[0][0]]).strip() if sub else ""
            if intro:                             # texto introdutório da seção
                docs[doc_id] = {"title": titulo, "path": caminho,
                                "content": "\n".join(bloco[:sub[0][0]])}
                kids.append({"label": "visão geral", "type": "doc", "id": doc_id})
            for k, (sj, stitulo) in enumerate(sub):
                sfim = sub[k + 1][0] if k + 1 < len(sub) else len(bloco)
                sid = f"spec/{_slug(stitulo)}"
                docs[sid] = {"title": stitulo, "path": caminho,
                             "content": "\n".join(bloco[sj:sfim])}
                kids.append({"label": stitulo, "type": "doc", "id": sid})
            tree.append({"label": f"{titulo} ({len(sub)})", "type": "group",
                         "children": kids})
        else:
            docs[doc_id] = {"title": titulo, "path": caminho,
                            "content": "\n".join(bloco)}
            tree.append({"label": titulo, "type": "doc", "id": doc_id})

    return docs, tree


def collect():
    if (spec := acha_spec()) is not None:
        return collect_spec(spec)
    if not REFINED.is_dir():
        sys.exit(f"ERRO: nem {BASE / 'spec.md'} nem {REFINED} encontrados.")

    docs = {}
    tree = []

    def add_doc(doc_id, path, label, group_children):
        docs[doc_id] = {"title": md_title(path), "path": str(path.relative_to(BASE)),
                        "content": read(path)}
        group_children.append({"label": label, "type": "doc", "id": doc_id})

    # ---- Páginas-raiz do wiki (4 mds + Visão + Componentes) ----
    raiz = []
    for name in ("overview.md", "index.md", "log.md", "visao.md"):
        f = REFINED / name
        if f.is_file():
            add_doc(f"wiki/{f.stem}", f, f.stem, raiz)
    bp = REFINED / "blueprint.md"
    if bp.is_file():
        bp_text = read(bp)
        docs["wiki/blueprint"] = {"title": md_title(bp), "path": str(bp.relative_to(BASE)),
                                  "content": bp_text, "kind": "blueprint",
                                  "etapas": parse_blueprint(bp_text)}
        raiz.append({"label": "blueprint", "type": "doc", "id": "wiki/blueprint"})
    if raiz:
        tree.append({"label": "Wiki", "type": "group", "children": raiz})

    # ---- Camada de Requisitos (1 .md por feature) ----
    # Varre SOMENTE Requisitos/*.md — features arquivadas (fora de escopo) vivem em
    # refined/_archive/ e são deliberadamente ignoradas aqui, somindo do navegador.
    req = REFINED / "Requisitos"
    if req.is_dir():
        kids = []
        for f in sorted(req.glob("*.md")):
            add_doc(f"requisitos/{f.stem}", f, f.stem, kids)
        if kids:
            tree.append({"label": f"Requisitos ({len(kids)})",
                         "type": "group", "children": kids})

    # ---- Transversais (modelo de dados, requisitos, telas comuns, componentes) ----
    trans = []
    for name in ("modelo-dados.md", "requisitos-transversais.md", "telas-comuns.md", "componentes.md"):
        f = REFINED / name
        if f.is_file():
            add_doc(f"wiki/{f.stem}", f, f.stem, trans)
    if trans:
        tree.append({"label": "Transversais", "type": "group", "children": trans})

    return docs, tree


HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Navegador — __WIKINAME__/refined</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=Roboto+Mono:wght@400;500&display=swap" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/marked@12/marked.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/roughjs@4.6.6/bundled/rough.js"></script>
<style>
  :root {
    --bg: #F9F9F9; --panel: #FFFFFF; --ink: #272727; --muted: #6B6E7A;
    --line: #D8DAE0; --accent: #0C1BA8; --accent-soft: #EEF2FE;
    --sidebar-w: 312px; --toc-w: 224px;
    --code-bg: #F0F2F7; --hl: #FFF3CD;
  }
  body.dark {
    --bg: #16161c; --panel: #20202b; --ink: #e8e8ee; --muted: #9a9aa8;
    --line: #34343f; --accent: #9DB0F5; --accent-soft: #262b46;
    --code-bg: #26262f; --hl: #3a3420;
  }
  * { box-sizing: border-box; }
  html, body { margin: 0; height: 100%; }
  body {
    font: 15px/1.6 'Outfit', system-ui, -apple-system, sans-serif;
    background: var(--bg); color: var(--ink);
    display: grid; grid-template-columns: var(--sidebar-w) 1fr;
    grid-template-rows: 54px 1fr; height: 100vh; overflow: hidden;
  }
  header {
    grid-column: 1 / -1; display: flex; align-items: center; gap: 14px;
    padding: 0 18px; border-bottom: 1px solid var(--line); background: var(--panel);
  }
  header .brand small { color: var(--muted); font-weight: 400; margin-left: 6px; }
  header .spacer { flex: 1; }
  #search {
    width: 320px; max-width: 40vw; padding: 7px 11px; border-radius: 8px;
    border: 1px solid var(--line); background: var(--bg); color: var(--ink); font-size: 14px;
  }
  #search:focus { outline: 2px solid var(--accent-soft); }
  .btn {
    padding: 6px 11px; border-radius: 8px; border: 1px solid var(--line);
    background: var(--bg); color: var(--ink); cursor: pointer; font-size: 13px;
  }
  .btn:hover { border-color: var(--accent); }

  aside {
    border-right: 1px solid var(--line); background: var(--panel);
    overflow-y: auto; padding: 10px 8px 40px;
  }
  .node-group > .row {
    font-weight: 600; cursor: pointer; user-select: none;
    padding: 5px 8px; border-radius: 6px; display: flex; gap: 6px; align-items: center;
  }
  .node-group > .row:hover { background: var(--accent-soft); }
  .node-group .caret { color: var(--muted); transition: transform .15s; font-size: 11px; }
  .node-group.collapsed .caret { transform: rotate(-90deg); }
  .node-group.collapsed > .children { display: none; }
  .children { margin-left: 13px; border-left: 1px solid var(--line); padding-left: 6px; }
  .doc {
    cursor: pointer; padding: 4px 8px; border-radius: 6px; color: var(--ink);
    font-size: 13.5px; display: block; white-space: nowrap; overflow: hidden;
    text-overflow: ellipsis;
  }
  .doc:hover { background: var(--accent-soft); }
  .doc.active { background: var(--accent); color: #fff; }
  .doc.hit { box-shadow: inset 2px 0 0 var(--accent); }
  .hidden { display: none !important; }

  main { overflow-y: auto; position: relative; }
  .layout { display: grid; grid-template-columns: 1fr var(--toc-w);
            max-width: 1180px; margin: 0 auto; }
  article { padding: 30px 38px 120px; min-width: 0; }
  .crumb { color: var(--muted); font-size: 13px; margin-bottom: 4px; }
  .docpath { color: var(--muted); font-size: 12px; font-family: 'Roboto Mono', ui-monospace, monospace; }

  nav.toc {
    padding: 30px 16px; font-size: 12.5px; position: sticky; top: 0;
    align-self: start; max-height: 100vh; overflow-y: auto;
  }
  nav.toc h4 { margin: 0 0 8px; color: var(--muted); text-transform: uppercase;
               letter-spacing: .6px; font-size: 11px; }
  nav.toc a { display: block; color: var(--muted); text-decoration: none;
              padding: 2px 0; border-left: 2px solid transparent; padding-left: 8px; }
  nav.toc a:hover { color: var(--accent); }
  nav.toc a.lvl3 { padding-left: 18px; font-size: 12px; }
  nav.toc a.active { color: var(--accent); border-left-color: var(--accent); }

  article h1 { font-size: 26px; letter-spacing: -.4px; margin: .2em 0 .5em; }
  article h2 { font-size: 20px; margin-top: 1.6em; padding-bottom: 4px;
               border-bottom: 1px solid var(--line); }
  article h3 { font-size: 16px; margin-top: 1.4em; }
  article h4 { font-size: 14px; color: var(--muted); }
  article code { background: var(--code-bg); padding: 1px 5px; border-radius: 4px;
                 font-family: 'Roboto Mono', ui-monospace, monospace; font-size: 13px; }
  article pre { background: var(--code-bg); padding: 13px 15px; border-radius: 9px;
                overflow-x: auto; border: 1px solid var(--line); }
  article pre code { background: none; padding: 0; font-size: 12.5px; line-height: 1.5; }
  article table { border-collapse: collapse; width: 100%; margin: 1em 0; font-size: 13px; }
  article th, article td { border: 1px solid var(--line); padding: 6px 9px;
                           text-align: left; vertical-align: top; }
  article th { background: var(--accent-soft); }
  article tr:nth-child(even) td { background: var(--code-bg); }
  article blockquote { margin: 1em 0; padding: 6px 14px; border-left: 3px solid var(--accent);
                       background: var(--code-bg); border-radius: 0 8px 8px 0; color: var(--muted); }
  article a { color: var(--accent); }
  article hr { border: none; border-top: 1px solid var(--line); margin: 1.8em 0; }
  .mermaid { background: var(--panel); border: 1px solid var(--line); border-radius: 9px;
             padding: 14px; margin: 1em 0; text-align: center; overflow-x: auto; }
  .mermaid-err { color: #b04a3a; font-size: 12px; }
  .wireframe { background: #fff; border: 1px solid var(--line); border-radius: 9px;
               padding: 10px; margin: 1em 0; overflow-x: auto; }
  .wireframe svg { display: block; }
  body.dark .wireframe { background: #f7f7fa; }
  mark { background: var(--hl); color: inherit; padding: 0 2px; border-radius: 3px; }

  .empty { color: var(--muted); padding: 60px 38px; text-align: center; }
  .badge { display: inline-block; font-size: 10.5px; padding: 1px 7px; border-radius: 20px;
           background: var(--accent-soft); color: var(--accent); margin-left: 6px;
           vertical-align: middle; }
  .searchcount { font-size: 12px; color: var(--muted); padding: 4px 10px; }
  .bp-hint { color: var(--muted); font-size: 13px; margin: 0 0 14px; }
  .bp-chain { display: flex; overflow-x: auto; padding: 4px 0 24px; align-items: stretch; }
  .bp-stage { min-width: 230px; flex: 1; background: var(--panel);
    border: 1px solid var(--line); border-radius: 10px; }
  .bp-stage-h { background: var(--accent-soft); color: var(--accent); font-weight: 700;
    padding: 9px 12px; border-radius: 10px 10px 0 0; border-bottom: 1px solid var(--line); }
  .bp-arrow { display: flex; align-items: center; color: var(--muted); font-size: 20px; padding: 0 3px; }
  .bp-feat { display: block; padding: 9px 12px; border-bottom: 1px solid var(--line);
    color: var(--ink); text-decoration: none; cursor: pointer; }
  .bp-feat:last-child { border-bottom: none; }
  .bp-feat:hover { background: var(--accent-soft); }
  .bp-nome { font-weight: 600; }
  .bp-resumo { display: block; color: var(--muted); font-size: 12.5px; }
  .bp-badge { display: inline-block; font-size: 10px; padding: 1px 6px; border-radius: 20px; margin-left: 6px; }
  .bp-badge.ator { background: var(--accent-soft); color: var(--accent); }
  .bp-badge.ia { background: var(--accent); color: #fff; }
  a.deadlink { color: var(--muted) !important; text-decoration: line-through; cursor: default; }
  .brand { display: flex; align-items: center; gap: 10px; }
  .brand-logo svg { height: 22px; width: auto; display: block; }
  .brand-txt { font-weight: 700; letter-spacing: -.2px; }
  body.dark .brand-logo svg { filter: invert(1) brightness(1.7); }
</style>
</head>
<body>
<header>
  <div class="brand"><span class="brand-logo"><svg id="Layer_1" data-name="Layer 1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 595.28 175.54"><defs><style>.cls-1{fill:#272727;}</style></defs><rect class="cls-1" x="54.02" y="94.52" width="13.5" height="13.5"/><path class="cls-1" d="M87.78,121.53a13.5,13.5,0,0,0,13.5-13.5H67.53v13.5Z"/><path class="cls-1" d="M81,81a13.5,13.5,0,0,0-13.5,13.5h54A13.49,13.49,0,0,0,135,81H81Z"/><path class="cls-1" d="M114.79,54a13.51,13.51,0,0,0-13.51,13.51H135V54Z"/><rect class="cls-1" x="135.04" y="67.52" width="13.5" height="13.5"/><path class="cls-1" d="M202.64,103V72.64H234.9v6.75H211v4.75h19.7v6.75H211v5.34H234.9V103Z"/><path class="cls-1" d="M244.35,103V72.64h8.38V95.85h20V103Z"/><path class="cls-1" d="M284.08,99.26a14.07,14.07,0,0,1-5.25-11.45,14.08,14.08,0,0,1,5.25-11.45c3.55-2.87,8.25-4.32,14.19-4.32s10.64,1.45,14.15,4.32a14,14,0,0,1,5.29,11.45,14,14,0,0,1-5.29,11.45c-3.51,2.87-8.21,4.32-14.15,4.32S287.63,102.13,284.08,99.26Zm22.1-4.87a8.21,8.21,0,0,0,2.94-6.58,8,8,0,0,0-2.94-6.54,13.85,13.85,0,0,0-15.82,0,8.05,8.05,0,0,0-2.95,6.54,8.21,8.21,0,0,0,2.95,6.58,14,14,0,0,0,15.82,0Z"/><path class="cls-1" d="M330,99.35A14.53,14.53,0,0,1,325,87.81a13.9,13.9,0,0,1,5.3-11.41c3.54-2.91,8.25-4.36,14-4.36,7.52,0,13.59,2.82,16.7,7.74l-6.11,4a13,13,0,0,0-10.64-5,11.5,11.5,0,0,0-7.78,2.48,8.13,8.13,0,0,0-2.9,6.54c0,5.51,4.1,9.06,10.64,9.06a13.36,13.36,0,0,0,9.87-4.27h-8.76v-6.2h17V103h-6.54v-4.1c-2.69,3.08-6.92,4.7-12.44,4.7S333.33,102.17,330,99.35Z"/><path class="cls-1" d="M372.19,103V72.64h24a11.16,11.16,0,0,1,7.86,2.78,9.25,9.25,0,0,1,3,7.13,8.72,8.72,0,0,1-3,6.88,11.14,11.14,0,0,1-7.61,2.65L408.22,103H396.85l-10.47-10.6h-5.81V103Zm8.38-23.59v6.33h13.67c2.69,0,4.28-1.16,4.28-3.17s-1.59-3.16-4.28-3.16Z"/><path class="cls-1" d="M419.47,99.26a14.07,14.07,0,0,1-5.26-11.45,14.09,14.09,0,0,1,5.26-11.45C423,73.49,427.72,72,433.66,72s10.64,1.45,14.15,4.32a14,14,0,0,1,5.29,11.45,14,14,0,0,1-5.29,11.45c-3.51,2.87-8.21,4.32-14.15,4.32S423,102.13,419.47,99.26Zm22.1-4.87a8.21,8.21,0,0,0,2.94-6.58,8,8,0,0,0-2.94-6.54,13.85,13.85,0,0,0-15.82,0,8.05,8.05,0,0,0-2.95,6.54,8.21,8.21,0,0,0,2.95,6.58,14,14,0,0,0,15.82,0Z"/><path class="cls-1" d="M496.46,72.64v17c0,9.1-6.11,14-17.52,14s-17.52-4.87-17.52-14v-17h8.37V88.79c0,5.13,3.21,7.87,9.15,7.87s9.14-2.74,9.14-7.87V72.64Z"/><path class="cls-1" d="M514.84,94.18V103h-8.38V72.64H529c7.73,0,12.3,4,12.3,10.73A10,10,0,0,1,538,91.23a12.37,12.37,0,0,1-8.64,3Zm0-14.79v8h12.61c3.38,0,5.21-1.46,5.21-4.06s-1.83-4-5.21-4Z"/></svg></span><span class="brand-txt">__WIKINAME__ <small>· navegador</small></span></div>
  <div class="spacer"></div>
  <input id="search" type="search" placeholder="Buscar na árvore e no conteúdo…" autocomplete="off">
  <button class="btn" id="expand">Expandir tudo</button>
  <button class="btn" id="theme">◐ Tema</button>
</header>
<aside id="sidebar"></aside>
<main>
  <div class="layout">
    <article id="article"><div class="empty">Selecione um documento na barra lateral.</div></article>
    <nav class="toc" id="toc"></nav>
  </div>
</main>

<script>
const DOCS = __DOCS__;
const TREE = __TREE__;

const PATH_TO_ID = {};
for (const [id, d] of Object.entries(DOCS)) { if (d.path) PATH_TO_ID[d.path] = id; }

function resolvePath(fromPath, href) {
  href = (href || '').split('#')[0].split('?')[0];
  if (!href || !fromPath) return null;
  const stack = fromPath.split('/').slice(0, -1);
  for (const p of href.split('/')) {
    if (p === '..') stack.pop();
    else if (p === '.' || p === '') continue;
    else stack.push(p);
  }
  return stack.join('/');
}

function rewireLinks(scope, doc) {
  scope.querySelectorAll('a[href]').forEach(a => {
    const href = a.getAttribute('href') || '';
    if (/^https?:/i.test(href)) return;
    if (!/\.md($|#|\?)/.test(href)) return;
    const tid = PATH_TO_ID[resolvePath(doc.path, href)];
    if (tid) {
      a.addEventListener('click', e => { e.preventDefault(); renderDoc(tid); });
    } else {
      a.classList.add('deadlink');
    }
  });
}

function renderBlueprint(id, doc) {
  const art = document.getElementById('article');
  document.getElementById('toc').innerHTML = '';
  let head = '<div class="crumb">Wiki</div><div class="docpath">' + doc.path + '</div>'
    + '<h1>' + (doc.title || 'Blueprint') + '</h1>'
    + '<p class="bp-hint">Cadeia de valor — clique numa feature para abrir a página.</p>';
  let chain = '';
  const etapas = doc.etapas || [];
  etapas.forEach((e, i) => {
    let feats = '';
    e.features.forEach(f => {
      let badges = '';
      if (f.ator) badges += '<span class="bp-badge ator">' + f.ator + '</span>';
      if (f.ia) badges += '<span class="bp-badge ia">IA</span>';
      const tid = PATH_TO_ID[resolvePath(doc.path, f.href)];
      feats += '<a class="bp-feat' + (tid ? '' : ' deadlink') + '"'
        + (tid ? ' data-bpid="' + tid + '"' : '') + '>'
        + '<span class="bp-nome">' + f.nome + '</span>' + badges
        + '<span class="bp-resumo">' + f.resumo + '</span></a>';
    });
    chain += '<div class="bp-stage"><div class="bp-stage-h">' + e.etapa + '</div>' + feats + '</div>';
    if (i < etapas.length - 1) chain += '<div class="bp-arrow">&rarr;</div>';
  });
  art.innerHTML = head + '<div class="bp-chain">' + chain + '</div>';
  art.querySelectorAll('.bp-feat[data-bpid]').forEach(a =>
    a.addEventListener('click', () => renderDoc(a.dataset.bpid)));
  document.querySelector('main').scrollTop = 0;
  location.hash = encodeURIComponent(id);
}

mermaid.initialize({ startOnLoad: false, theme: 'neutral', securityLevel: 'loose' });

/* ---------- DBML → Mermaid erDiagram ---------- */
function dbmlToMermaid(dbml) {
  const lines = dbml.split('\n');
  const tables = []; const refs = [];
  let cur = null; let depth = 0; let inIndexes = false;
  const clean = t => (t || '').split('(')[0].replace(/[^A-Za-z0-9_]/g, '') || 'x';
  for (let raw of lines) {
    const line = raw.replace(/\/\/.*$/, '').trim();
    if (!line) continue;
    const mt = line.match(/^Table\s+"?([A-Za-z0-9_]+)"?/);
    if (mt && !cur) { cur = { name: mt[1], cols: [] }; depth = 0; inIndexes = false;
                      if (line.includes('{')) depth = 1; continue; }
    if (!cur) continue;
    if (/^indexes\s*\{/.test(line)) { inIndexes = true; depth += 1; continue; }
    const opens = (line.match(/\{/g) || []).length;
    const closes = (line.match(/\}/g) || []).length;
    if (inIndexes) { depth += opens - closes; if (depth <= 1) inIndexes = false; continue; }
    depth += opens - closes;
    if (depth <= 0) { tables.push(cur); cur = null; continue; }
    const cm = line.match(/^"?([A-Za-z0-9_]+)"?\s+([A-Za-z0-9_]+(?:\([^)]*\))?)(.*)$/);
    if (cm) {
      const cname = cm[1], ctype = clean(cm[2]), rest = cm[3] || '';
      let key = '';
      if (/\[pk\]|primary key|\bpk\b/i.test(rest)) key = 'PK';
      const rf = rest.match(/ref:\s*[<>-]\s*"?([A-Za-z0-9_]+)"?\.\s*"?([A-Za-z0-9_]+)"?/);
      if (rf) { key = key ? 'PK' : 'FK'; refs.push([cur.name, rf[1], cname]); }
      cur.cols.push({ name: cname, type: ctype, key });
    }
  }
  if (cur) tables.push(cur);
  if (!tables.length) return null;
  let out = 'erDiagram\n';
  for (const t of tables) {
    out += '  ' + t.name + ' {\n';
    for (const c of t.cols.slice(0, 30))
      out += '    ' + c.type + ' ' + c.name + (c.key ? ' ' + c.key : '') + '\n';
    out += '  }\n';
  }
  const seen = new Set();
  for (const [from, to, col] of refs) {
    const k = from + '>' + to;
    if (seen.has(k) || from === to) continue;
    seen.add(k);
    if (tables.find(t => t.name === to))
      out += '  ' + from + ' }o--|| ' + to + ' : "' + col + '"\n';
  }
  return out;
}

/* ---------- Render ---------- */
/* ---------- Wireframe fat-marker (parser + render, layout + texto) ---------- */
function parseInline(text) {
  const re = /\[~[^\]]*~\]|\[[^\]]*?_{2,}\]|\[[^\]]+\]|[^\[]+/g;
  const out = []; let m;
  while ((m = re.exec(text)) !== null) {
    const t = m[0].trim(); if (!t) continue;
    if (/^\[~.*~\]$/.test(t)) out.push({t:'chart', s:t.replace(/^\[~|~\]$/g,'').trim()});
    else if (/^\[.*_{2,}\]$/.test(t)) out.push({t:'input', s:t.replace(/[\[\]]/g,'').replace(/_+/g,'').trim()});
    else if (/^\[.+\]$/.test(t)) out.push({t:'button', s:t.slice(1,-1).trim()});
    else out.push({t:'label', s:t});
  }
  return out;
}
function parseWireframe(src) {
  const lines = src.replace(/\t/g,'  ').split('\n');
  let i = 0;
  function indentOf(s){ return s.match(/^ */)[0].length; }
  function block(minIndent) {
    const nodes = [];
    while (i < lines.length) {
      const raw = lines[i];
      if (raw.trim() === '') { i++; continue; }
      const ind = indentOf(raw);
      if (ind < minIndent) break;
      const s = raw.trim();
      let mm;
      if ((mm = s.match(/^card\s+"?(.*?)"?:$/))) { i++; const kids = block(ind+1); nodes.push({t:'card', s:mm[1], kids}); continue; }
      if (s[0] === '|') {
        const rows = [];
        while (i < lines.length && lines[i].trim()[0] === '|') {
          const cells = lines[i].trim().replace(/^\||\|$/g,'').split('|').map(c=>c.trim());
          if (!cells.every(c=>/^[-:]+$/.test(c))) rows.push(cells);
          i++;
        }
        nodes.push({t:'table', rows}); continue;
      }
      if (s.startsWith('- ')) {
        const items = [];
        while (i < lines.length && lines[i].trim().startsWith('- ')) { items.push(lines[i].trim().slice(2)); i++; }
        nodes.push({t:'list', items}); continue;
      }
      i++;
      if (s.startsWith('# ')) nodes.push({t:'title', s:s.slice(2)});
      else if (s.startsWith('## ')) nodes.push({t:'sub', s:s.slice(3)});
      else if ((mm = s.match(/^\[\[(.+)\]\]$/))) nodes.push({t:'row', cells: mm[1].split('|').map(c=>parseInline(c.trim()))});
      else if (s.startsWith('(!)')) nodes.push({t:'alert', s:s.slice(3).trim()});
      else nodes.push({t:'line', items: parseInline(s)});
    }
    return nodes;
  }
  return block(0);
}
const WF = {W:560, PAD:12, GAP:8, TITLE:34, SUB:22, ROW:54, LINE:34, CHART:88, ALERT:32, LI:22, TR:28, CH:26, CPAD:9};
function wfMeasure(nodes) { let h=0; for (const n of nodes) h += wfH(n) + WF.GAP; return h; }
function wfH(n) {
  switch(n.t){
    case 'title': return WF.TITLE; case 'sub': return WF.SUB; case 'row': return WF.ROW;
    case 'alert': return WF.ALERT; case 'list': return Math.max(1,n.items.length)*WF.LI;
    case 'table': return Math.max(1,n.rows.length)*WF.TR;
    case 'line': return n.items.some(x=>x.t==='chart') ? WF.CHART : WF.LINE;
    case 'card': return WF.CH + WF.CPAD*2 + wfMeasure(n.kids);
    default: return WF.LINE;
  }
}
function renderWireframe(src) {
  const SVG='http://www.w3.org/2000/svg';
  const nodes = parseWireframe(src);
  const W = WF.W, total = wfMeasure(nodes) + WF.PAD*2;
  const svg = document.createElementNS(SVG,'svg');
  svg.setAttribute('viewBox','0 0 '+W+' '+total);
  svg.setAttribute('width','100%'); svg.setAttribute('style','max-width:'+W+'px;height:auto');
  const rc = rough.svg(svg);
  const FM = {roughness:2.1, strokeWidth:2.2, stroke:'#2a2a2a'};
  const g = el => svg.appendChild(el);
  const FONT = '"Comic Sans MS","Segoe Print","Bradley Hand",Chalkboard,cursive';
  function txt(x,y,s,maxw,size,anchor,weight){
    if(!s) return;
    const fs = size||13.5;
    const cap = Math.max(1, Math.floor(maxw/(fs*0.52)));
    let str = String(s); if (str.length>cap) str = str.slice(0,Math.max(1,cap-1))+'…';
    const t = document.createElementNS(SVG,'text');
    t.setAttribute('x',x); t.setAttribute('y',y); t.setAttribute('font-family',FONT);
    t.setAttribute('font-size',fs); t.setAttribute('fill','#222');
    t.setAttribute('dominant-baseline','middle');
    if (anchor) t.setAttribute('text-anchor',anchor);
    if (weight) t.setAttribute('font-weight','700');
    t.textContent = str; g(t);
  }
  function drawNodes(nodes, x, w, y) { for (const n of nodes) { y = drawNode(n,x,w,y) + WF.GAP; } return y; }
  function drawNode(n,x,w,y){
    const h = wfH(n);
    if (n.t==='title'){ g(rc.rectangle(x,y,w,WF.TITLE-4,{...FM,fill:'#dadaea',fillStyle:'hachure',hachureGap:6})); txt(x+12,y+(WF.TITLE-4)/2,n.s,w-24,15,null,true); }
    else if (n.t==='sub'){ txt(x+2,y+WF.SUB/2,n.s,w,13,null,true); }
    else if (n.t==='alert'){ g(rc.rectangle(x,y,w,WF.ALERT-4,{...FM,fill:'#f6dada',fillStyle:'hachure',hachureGap:7})); g(rc.line(x+3,y+3,x+3,y+WF.ALERT-7,{stroke:'#b03030',strokeWidth:5,roughness:1})); txt(x+14,y+(WF.ALERT-4)/2,'⚠ '+(n.s||''),w-22,12.5); }
    else if (n.t==='list'){ let yy=y; for(const it of n.items){ g(rc.circle(x+6,yy+WF.LI/2,5,FM)); txt(x+16,yy+WF.LI/2,it,w-22,13); yy+=WF.LI; } }
    else if (n.t==='table'){ const R=n.rows.length||1, C=(n.rows[0]||['','']).length||2, cw=w/C; g(rc.rectangle(x,y,w,R*WF.TR,FM)); for(let r=1;r<R;r++) g(rc.line(x,y+r*WF.TR,x+w,y+r*WF.TR,{roughness:1.6,strokeWidth:1.4,stroke:'#666'})); for(let c=1;c<C;c++) g(rc.line(x+c*cw,y,x+c*cw,y+R*WF.TR,{roughness:1.6,strokeWidth:1.4,stroke:'#666'})); for(let r=0;r<R;r++) for(let c=0;c<(n.rows[r]||[]).length;c++) txt(x+c*cw+7,y+r*WF.TR+WF.TR/2,n.rows[r][c],cw-12,12.5,null,r===0); }
    else if (n.t==='row'){ const N=n.cells.length, cw=(w-(N-1)*WF.GAP)/N; for(let c=0;c<N;c++){ const cx=x+c*(cw+WF.GAP); g(rc.rectangle(cx,y,cw,WF.ROW-4,{...FM,strokeWidth:2})); drawInline(n.cells[c],cx+8,cw-16,y+(WF.ROW-4)/2,true); } }
    else if (n.t==='line'){ if(n.items.some(it=>it.t==='chart')) drawChart(x,y,w,n.items.find(it=>it.t==='chart').s); else drawInline(n.items,x,w,y+WF.LINE/2,false); }
    else if (n.t==='card'){ g(rc.rectangle(x,y,w,h,{...FM,strokeWidth:2})); txt(x+12,y+WF.CH/2,n.s,w-24,13.5,null,true); drawNodes(n.kids,x+WF.CPAD,w-WF.CPAD*2,y+WF.CH+WF.CPAD); }
    return y+h;
  }
  function drawChart(x,y,w,cap){ const hh=WF.CHART-22; g(rc.rectangle(x,y,w,hh,FM)); g(rc.line(x+12,y+hh-10,x+w-10,y+hh-10,{roughness:1.4,strokeWidth:2,stroke:'#666'})); g(rc.line(x+12,y+8,x+12,y+hh-10,{roughness:1.4,strokeWidth:2,stroke:'#666'})); const bw=(w-44)/4; for(let b=0;b<4;b++){ const bh=12+((b*37)%(hh-26)); g(rc.rectangle(x+20+b*bw,y+hh-10-bh,bw*0.6,bh,{...FM,strokeWidth:1.6,fill:'#cfcfe6',fillStyle:'hachure',hachureGap:4})); } txt(x+w/2,y+hh+10,cap||'gráfico',w-16,12,'middle'); }
  function drawInline(items,x,w,cy,center){
    const onlyLabels = items.every(it=>it.t==='label');
    if (center && onlyLabels){ txt(x+w/2,cy,items.map(it=>it.s).join(' '),w,13.5,'middle'); return; }
    let cur=x;
    for (const it of items){
      const avail = x+w-cur;
      if (it.t==='button'){ const bw=Math.min(it.s.length*8+22,Math.max(40,avail)); g(rc.rectangle(cur,cy-13,bw,26,{...FM,strokeWidth:2,fill:'#eef0f6',fillStyle:'solid'})); txt(cur+bw/2,cy,it.s,bw-12,12.5,'middle'); cur+=bw+8; }
      else if (it.t==='input'){ const iw=Math.min(Math.max(it.s.length*8+30,90),avail); g(rc.rectangle(cur,cy-13,iw,26,{roughness:1.5,strokeWidth:2,stroke:'#444'})); txt(cur+7,cy,it.s,iw-12,12.5); cur+=iw+8; }
      else if (it.t==='chart'){ /* tratado em drawChart */ }
      else { txt(cur,cy,it.s,avail,13); cur += Math.min(it.s.length*7+8, avail); }
      if (cur > x+w-6) break;
    }
  }
  drawNodes(nodes, WF.PAD, W-WF.PAD*2, WF.PAD);
  return svg;
}
let mermaidSeq = 0;
function renderDoc(id) {
  const doc = DOCS[id];
  const art = document.getElementById('article');
  if (!doc) { art.innerHTML = '<div class="empty">Documento não encontrado.</div>'; return; }
  document.querySelectorAll('.doc').forEach(d =>
    d.classList.toggle('active', d.dataset.id === id));

  if (doc.kind === 'blueprint') { renderBlueprint(id, doc); return; }

  let html = marked.parse(doc.content);
  const wrap = document.createElement('div');
  wrap.innerHTML = html;

  // converter blocos de código mermaid / dbml / wireframe
  wrap.querySelectorAll('pre > code').forEach(code => {
    const cls = code.className || '';
    const txt = code.textContent;
    if (/language-wireframe/.test(cls)) {
      const div = document.createElement('div');
      div.className = 'wireframe';
      div.dataset.src = txt;
      code.parentElement.replaceWith(div);
      return;
    }
    let diagram = null;
    if (/language-mermaid/.test(cls)) diagram = txt;
    else if (/language-dbml/.test(cls)) diagram = dbmlToMermaid(txt);
    if (diagram) {
      const div = document.createElement('div');
      div.className = 'mermaid';
      div.dataset.src = diagram;
      code.parentElement.replaceWith(div);
    }
  });

  const head = '<div class="crumb">' + (id.split('/').slice(0, -1).join(' / ') || '') +
    '</div><div class="docpath">' + doc.path + '</div>';
  art.innerHTML = head;
  art.appendChild(wrap);

  rewireLinks(wrap, doc);

  // renderizar mermaid
  wrap.querySelectorAll('.mermaid').forEach(async div => {
    const src = div.dataset.src;
    const gid = 'mmd' + (mermaidSeq++);
    try {
      const { svg } = await mermaid.render(gid, src);
      div.innerHTML = svg;
    } catch (e) {
      div.innerHTML = '<div class="mermaid-err">⚠ Não foi possível renderizar o diagrama</div>' +
        '<pre><code>' + src.replace(/</g, '&lt;') + '</code></pre>';
    }
  });

  // renderizar wireframes (fat marker, só layout, sem texto)
  wrap.querySelectorAll('.wireframe').forEach(div => {
    try { div.replaceChildren(renderWireframe(div.dataset.src)); }
    catch (e) { div.innerHTML = '<div class="mermaid-err">⚠ wireframe inválido</div>'; }
  });

  buildToc(wrap);
  highlightSearch();
  document.querySelector('main').scrollTop = 0;
  location.hash = encodeURIComponent(id);
}

/* ---------- TOC ---------- */
function buildToc(scope) {
  const toc = document.getElementById('toc');
  const heads = [...scope.querySelectorAll('h1, h2, h3')];
  if (heads.length < 2) { toc.innerHTML = ''; return; }
  let html = '<h4>Neste documento</h4>';
  heads.forEach((h, i) => {
    const slug = 'h_' + i;
    h.id = slug;
    const lvl = h.tagName === 'H3' ? ' lvl3' : '';
    if (h.tagName === 'H1') return;
    html += '<a class="toclink' + lvl + '" href="#" data-slug="' + slug + '">' +
      h.textContent + '</a>';
  });
  toc.innerHTML = html;
  toc.querySelectorAll('a').forEach(a => a.onclick = e => {
    e.preventDefault();
    document.getElementById(a.dataset.slug)
      .scrollIntoView({ behavior: 'smooth', block: 'start' });
  });
}

/* ---------- Sidebar ---------- */
function buildTree(nodes, container) {
  for (const n of nodes) {
    if (n.type === 'group') {
      const g = document.createElement('div');
      g.className = 'node-group';
      const row = document.createElement('div');
      row.className = 'row';
      row.innerHTML = '<span class="caret">▼</span><span>' + n.label + '</span>';
      const kids = document.createElement('div');
      kids.className = 'children';
      row.onclick = () => g.classList.toggle('collapsed');
      g.appendChild(row); g.appendChild(kids);
      container.appendChild(g);
      buildTree(n.children || [], kids);
    } else {
      const d = document.createElement('a');
      d.className = 'doc';
      d.dataset.id = n.id;
      d.textContent = n.label;
      d.title = (DOCS[n.id] && DOCS[n.id].title) || n.label;
      d.onclick = () => renderDoc(n.id);
      container.appendChild(d);
    }
  }
}

/* ---------- Busca ---------- */
let searchTerm = '';
function applySearch() {
  const q = searchTerm.toLowerCase().trim();
  const docEls = [...document.querySelectorAll('.doc')];
  if (!q) {
    docEls.forEach(d => { d.classList.remove('hidden', 'hit'); });
    document.querySelectorAll('.node-group').forEach(g => g.classList.remove('hidden'));
    return;
  }
  let hits = 0;
  docEls.forEach(d => {
    const id = d.dataset.id;
    const doc = DOCS[id];
    const inName = d.textContent.toLowerCase().includes(q) ||
      (doc && doc.title.toLowerCase().includes(q));
    const inBody = doc && doc.content.toLowerCase().includes(q);
    const match = inName || inBody;
    d.classList.toggle('hidden', !match);
    d.classList.toggle('hit', !!(inBody && match));
    if (match) hits++;
  });
  // esconder grupos sem filhos visíveis
  document.querySelectorAll('.node-group').forEach(g => {
    const anyVisible = g.querySelector('.doc:not(.hidden)');
    g.classList.toggle('hidden', !anyVisible);
    if (anyVisible) g.classList.remove('collapsed');
  });
}
function highlightSearch() {
  const q = searchTerm.trim();
  if (q.length < 2) return;
  const art = document.getElementById('article');
  const needle = q.toLowerCase();
  const esc = q.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const escapeHtml = s => s.replace(/&/g, '&amp;').replace(/</g, '&lt;')
                            .replace(/>/g, '&gt;');
  const walk = node => {
    if (node.nodeType === 3) {
      if (node.nodeValue.toLowerCase().includes(needle)) {
        const rx = new RegExp('(' + esc + ')', 'gi');
        const span = document.createElement('span');
        span.innerHTML = escapeHtml(node.nodeValue).replace(rx, '<mark>$1</mark>');
        node.replaceWith(span);
      }
    } else if (node.nodeType === 1 &&
               !['PRE', 'CODE', 'SCRIPT', 'STYLE'].includes(node.tagName) &&
               !node.classList.contains('mermaid')) {
      [...node.childNodes].forEach(walk);
    }
  };
  [...art.childNodes].forEach(walk);
}

/* ---------- Init ---------- */
buildTree(TREE, document.getElementById('sidebar'));

document.getElementById('search').addEventListener('input', e => {
  searchTerm = e.target.value;
  applySearch();
});
document.getElementById('theme').onclick = () => {
  document.body.classList.toggle('dark');
  const dark = document.body.classList.contains('dark');
  mermaid.initialize({ startOnLoad: false, theme: dark ? 'dark' : 'neutral',
                       securityLevel: 'loose' });
  try { localStorage.setItem('nav-theme', dark ? 'dark' : 'light'); } catch (e) {}
  const cur = location.hash.slice(1);
  if (cur) renderDoc(decodeURIComponent(cur));
};
let allExpanded = true;
document.getElementById('expand').onclick = () => {
  allExpanded = !allExpanded;
  document.querySelectorAll('.node-group').forEach(g =>
    g.classList.toggle('collapsed', !allExpanded));
  document.getElementById('expand').textContent =
    allExpanded ? 'Recolher tudo' : 'Expandir tudo';
};
try {
  if (localStorage.getItem('nav-theme') === 'dark') {
    document.body.classList.add('dark');
    mermaid.initialize({ startOnLoad: false, theme: 'dark', securityLevel: 'loose' });
  }
} catch (e) {}

// abrir doc do hash, ou o primeiro
const initial = location.hash.slice(1);
if (initial && DOCS[decodeURIComponent(initial)]) renderDoc(decodeURIComponent(initial));
else { const first = Object.keys(DOCS)[0]; if (first) renderDoc(first); }
</script>
</body>
</html>
"""


def main():
    docs, tree = collect()
    docs_json = json.dumps(docs, ensure_ascii=False).replace("</", "<\\/")
    tree_json = json.dumps(tree, ensure_ascii=False).replace("</", "<\\/")
    html = (HTML_TEMPLATE
            .replace("__DOCS__", docs_json)
            .replace("__TREE__", tree_json)
            .replace("__WIKINAME__", BASE.name or "wiki"))
    OUT.write_text(html, encoding="utf-8")
    total_kb = OUT.stat().st_size / 1024
    print(f"OK: {OUT.relative_to(BASE)} gerado — {len(docs)} documentos, {total_kb:.0f} KB")


if __name__ == "__main__":
    main()
