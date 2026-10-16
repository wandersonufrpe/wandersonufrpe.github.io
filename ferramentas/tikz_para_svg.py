#!/usr/bin/env python3
"""
Converte as figuras TikZ de uma aula (.tex) em arquivos SVG para o site.

Uso:
    python3 ferramentas/tikz_para_svg.py CAMINHO/aula01.tex disciplinas/edo/aulas/figuras/aula01

O que faz:
  1. Lê o preâmbulo da aula (pacotes, bibliotecas TikZ, cores, macros).
  2. Encontra cada ambiente tikzpicture, na ordem em que aparece.
  3. Compila cada figura sozinha (classe standalone) com pdflatex e converte para SVG
     (dvisvgm, pdf2svg ou pdftocairo, o que estiver instalado).
  4. Grava fig-01.svg, fig-02.svg... e um manifesto.json com a linha de origem de cada
     figura, se a conversão deu certo e se ela parece um bom candidato a applet
     (família de soluções, campo de direções).

Figuras que não mudaram desde a última execução não são recompiladas.
O arquivo .tex original nunca é alterado.
"""
import argparse
import hashlib
import json
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

LINHAS_MINIMAS = re.compile(
    r"^\s*\\(usepackage|RequirePackage|usetikzlibrary|usepgfplotslibrary|pgfplotsset|tikzset|"
    r"definecolor|colorlet|newcommand|renewcommand|providecommand|DeclareMathOperator|def)\b"
)
EVITAR = re.compile(r"\\usepackage(\[[^\]]*\])?\{(geometry|fancyhdr|titlesec|hyperref|tocloft|enumitem)\}")
PISTAS_APPLET = [
    (r"\\foreach", "laço \\foreach (várias curvas)"),
    (r"exp\s*\(|e\^", "exponencial"),
    (r"quiver", "campo vetorial (quiver)"),
    (r"slope|direç|direc", "menção a direções/inclinações"),
    (r"\\addplot.*\\addplot", "várias curvas pgfplots"),
]


def preambulo(texto: str, minimo: bool) -> str:
    inicio = texto.find("\\begin{document}")
    if inicio < 0:
        return ""
    linhas = texto[:inicio].splitlines()
    saida = []
    for linha in linhas:
        if linha.lstrip().startswith("\\documentclass"):
            continue
        if EVITAR.search(linha):
            continue
        if minimo and not LINHAS_MINIMAS.match(linha):
            continue
        saida.append(linha)
    return "\n".join(saida)


def figuras(texto: str):
    padrao = re.compile(r"\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}", re.S)
    for m in padrao.finditer(texto):
        linha = texto.count("\n", 0, m.start()) + 1
        yield linha, m.group(0)


def conversor():
    if shutil.which("dvisvgm"):
        return "dvisvgm"
    if shutil.which("pdf2svg"):
        return "pdf2svg"
    if shutil.which("pdftocairo"):
        return "pdftocairo"
    return None


def converter(pdf: pathlib.Path, svg: pathlib.Path, ferramenta: str) -> bool:
    if ferramenta == "dvisvgm":
        cmd = ["dvisvgm", "--pdf", "--no-fonts", "--exact-bbox", "-o", str(svg), str(pdf)]
    elif ferramenta == "pdf2svg":
        cmd = ["pdf2svg", str(pdf), str(svg)]
    else:
        cmd = ["pdftocairo", "-svg", str(pdf), str(svg)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    return r.returncode == 0 and svg.exists()


def compilar(codigo: str, pre: str, destino: pathlib.Path, ferramenta: str):
    doc = "\\documentclass[tikz,border=3pt]{standalone}\n" + pre + "\n\\begin{document}\n" + codigo + "\n\\end{document}\n"
    with tempfile.TemporaryDirectory() as tmp:
        tex = pathlib.Path(tmp) / "figura.tex"
        tex.write_text(doc, encoding="utf-8")
        r = subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "figura.tex"],
            cwd=tmp, capture_output=True, text=True,
        )
        pdf = pathlib.Path(tmp) / "figura.pdf"
        if r.returncode != 0 or not pdf.exists():
            erros = [l for l in r.stdout.splitlines() if l.startswith("!")]
            return False, (erros[0] if erros else "pdflatex falhou")
        if not converter(pdf, destino, ferramenta):
            return False, f"conversão para SVG falhou ({ferramenta})"
    return True, "ok"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("tex", type=pathlib.Path, help="arquivo .tex da aula (não é modificado)")
    ap.add_argument("saida", type=pathlib.Path, help="pasta onde os SVG serão gravados")
    ap.add_argument("--forcar", action="store_true", help="recompila mesmo as figuras que não mudaram")
    args = ap.parse_args()

    ferramenta = conversor()
    if not shutil.which("pdflatex") or not ferramenta:
        sys.exit("Preciso de pdflatex e de um conversor (dvisvgm, pdf2svg ou pdftocairo). Veja COMO-USAR.md.")

    texto = args.tex.read_text(encoding="utf-8", errors="replace")
    pre_completo = preambulo(texto, minimo=False)
    pre_minimo = preambulo(texto, minimo=True)
    args.saida.mkdir(parents=True, exist_ok=True)
    arq_manifesto = args.saida / "manifesto.json"
    anterior = {}
    if arq_manifesto.exists():
        anterior = {f["arquivo"]: f for f in json.loads(arq_manifesto.read_text(encoding="utf-8")).get("figuras", [])}

    registros = []
    for i, (linha, codigo) in enumerate(figuras(texto), start=1):
        nome = f"fig-{i:02d}.svg"
        destino = args.saida / nome
        assinatura = hashlib.sha1((pre_completo + codigo).encode()).hexdigest()[:12]
        antigo = anterior.get(nome)
        if not args.forcar and antigo and antigo.get("assinatura") == assinatura and antigo.get("ok") and destino.exists():
            registros.append(antigo)
            continue
        ok, msg = compilar(codigo, pre_completo, destino, ferramenta)
        if not ok:
            ok, msg = compilar(codigo, pre_minimo, destino, ferramenta)
            if ok:
                msg = "ok (com preâmbulo reduzido)"
        pistas = [desc for padrao, desc in PISTAS_APPLET if re.search(padrao, codigo, re.I | re.S)]
        registros.append({
            "arquivo": nome,
            "linha_no_tex": linha,
            "ok": ok,
            "mensagem": msg,
            "assinatura": assinatura,
            "candidata_a_applet": bool(pistas),
            "pistas": pistas,
            "inicio_do_codigo": " ".join(codigo.split())[:160],
        })
        print(f"{nome}  linha {linha:>5}  {'OK ' if ok else 'ERRO'}  {msg}" + ("  [candidata a applet]" if pistas else ""))

    arq_manifesto.write_text(
        json.dumps({"origem": str(args.tex), "figuras": registros}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    falhas = sum(1 for r in registros if not r["ok"])
    print(f"\n{len(registros)} figura(s); {falhas} com erro. Detalhes em {arq_manifesto}")


if __name__ == "__main__":
    main()
