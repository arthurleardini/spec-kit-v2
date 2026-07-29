#!/usr/bin/env python3
"""Teste de regressão do lint crítico.

Cinco asserções, cobrindo os dois formatos de entrada:

  spec único (v3)
  1. `spec-boa.md` sai limpa — prova que o ruleset é satisfazível no formato novo.
  2. `spec-ruim.md` dispara cada regra de `examples/lint/esperado-spec-ruim.txt`.
  3. Com tetos apertados, `spec-boa.md` dispara os tetos de seção e o global (R08, R09).

  wiki legado (v2)
  4. `feature-boa.md` sai limpa.
  5. `feature-ruim.md` dispara cada regra de `examples/lint/esperado-ruim.txt`;
     com tetos apertados, dispara também as regras de tamanho.

Uso: python3 scripts/testa_lint.py
"""

from __future__ import annotations

import re
import subprocess
import sys
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
LINT = RAIZ / "scripts" / "lint_critico.py"
EX = RAIZ / "examples" / "lint"
SPEC_BOA = EX / "spec-boa.md"
SPEC_RUIM = EX / "spec-ruim.md"
BOA = EX / "refined" / "Requisitos" / "feature-boa.md"
RUIM = EX / "refined" / "Requisitos" / "feature-ruim.md"
REGRAS = RAIZ / "regras" / "criticas.toml"

TETOS_TAMANHO = {"palavras_por_rf": 5, "telas_por_feature": 2, "rf_por_feature": 3,
                 "palavras_por_cenario": 10, "feature": 50}
TETOS_SECAO = {"contexto": 20, "modelo_dados": 20, "transversais": 20,
               "arquetipos": 20, "palavras_por_spec": 100}


def roda(alvo: Path, regras: Path = REGRAS) -> tuple[int, str]:
    p = subprocess.run([sys.executable, str(LINT), str(alvo), "--regras", str(regras)],
                       capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr


def disparadas(saida: str) -> set[str]:
    return set(re.findall(r"\[([A-Z]\d{2})/", saida))


def esperadas(arq: Path) -> set[str]:
    return {ln.split()[0] for ln in arq.read_text(encoding="utf-8").splitlines()
            if ln.strip() and not ln.startswith("#")}


def toml_com(novos: dict) -> Path:
    texto = REGRAS.read_text(encoding="utf-8")
    for chave, valor in novos.items():
        texto = re.sub(rf"^{chave}\s*=.*$", f"{chave} = {valor}", texto,
                       count=1, flags=re.MULTILINE)
    tmp = Path(tempfile.mkdtemp()) / "criticas.toml"
    tmp.write_text(texto, encoding="utf-8")
    return tmp


def main() -> int:
    falhas: list[str] = []

    def checa_limpo(alvo: Path) -> None:
        codigo, saida = roda(alvo)
        if codigo != 0:
            falhas.append(f"{alvo.name} deveria sair limpa; exit={codigo}\n{saida}")

    def checa_dispara(alvo: Path, mapa: Path) -> None:
        codigo, saida = roda(alvo)
        if codigo != 2:
            falhas.append(f"{alvo.name} deveria bloquear (exit 2); exit={codigo}")
        if faltando := esperadas(mapa) - disparadas(saida):
            falhas.append(f"{alvo.name}: regras esperadas que não dispararam: {sorted(faltando)}")

    def checa_tetos(alvo: Path, tetos: dict, regras_esperadas: set[str]) -> None:
        _, saida = roda(alvo, toml_com(tetos))
        if faltando := regras_esperadas - disparadas(saida):
            falhas.append(f"{alvo.name}: tetos não dispararam: {sorted(faltando)}")

    # --- spec único --------------------------------------------------------
    checa_limpo(SPEC_BOA)
    checa_dispara(SPEC_RUIM, EX / "esperado-spec-ruim.txt")
    checa_tetos(SPEC_BOA, TETOS_SECAO, {"R08", "R09"})

    # --- wiki legado ------------------------------------------------------
    checa_limpo(BOA)
    checa_dispara(RUIM, EX / "esperado-ruim.txt")
    checa_tetos(BOA, TETOS_TAMANHO, {"R05", "R06", "S01", "S03", "T06"})

    if falhas:
        for f in falhas:
            print("FALHA:", f)
        return 1
    print("testa_lint: ok — 5 asserções passaram (spec único + wiki legado).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
