#!/usr/bin/env python3
"""
Converte uma aula das notas de EDO (formato do prof. Wanderson) numa página do site.

Uso:
    python3 ferramentas/tex_para_qmd.py "CAMINHO/Aula 02.tex" --disciplina edo

Gera disciplinas/<disciplina>/aulas/aula-NN-assunto.qmd e as figuras TikZ em
disciplinas/<disciplina>/aulas/figuras/aula-NN/. O .tex original não é alterado.

O que é tratado (ver também ferramentas/conversao.lua):
  \\chapter[curto]{longo}    -> título "Aula N: curto" e subtítulo com o título longo
  \\section, \\subsection     -> ##, ###
  tcolorbox "Exemplo NN"     -> exemplo numerado automaticamente (a numeração manual é descartada)
  question                   -> exercício (sem dicas: elas entram depois, como rascunho)
  definition, theorem...     -> blocos numerados do Quarto
  tikzpicture                -> SVG (via tikz_para_svg.py)
  \\vspace, \\pagebreak etc.  -> removidos (só fazem sentido no PDF)

Ao final, imprime um relatório com contagens (.tex x página) e o que não foi convertido.
"""
import argparse
import json
import pathlib
import re
import subprocess
import sys
import unicodedata

RAIZ = pathlib.Path(__file__).resolve().parent.parent
FILTRO = RAIZ / "ferramentas" / "conversao.lua"
TIKZ = RAIZ / "ferramentas" / "tikz_para_svg.py"

REMOVER = [
    r"\\vspace\*?\{[^}]*\}", r"\\hspace\*?\{[^}]*\}", r"\\pagebreak", r"\\newpage", r"\\clearpage",
    r"\\linebreak", r"\\vfill", r"\\hfill", r"\\noindent", r"\\medskip", r"\\bigskip", r"\\smallskip",
    r"\\begingroup", r"\\endgroup", r"\\mdfapptodefinestyle\{[^}]*\}\{[^}]*\}", r"\\centering",
]
TEOREMAS = "definition|theorem|proposicao|corolario|lema|axiom|question|problem|example|demonstration|note|discussion"


def sem_comentarios(texto: str) -> str:
    linhas = []
    for linha in texto.splitlines():
        m = re.search(r"(?<!\\)%", linha)
        linhas.append(linha[: m.start()] if m else linha)
    return "\n".join(linhas)


VAZIAS = {"a", "as", "o", "os", "e", "de", "da", "do", "das", "dos", "em", "na", "no", "ao", "aos", "para", "por", "um", "uma"}


def lugar(texto: str, palavras: int = 5) -> str:
    s = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    s = re.sub(r"[^a-zA-Z0-9]+", "-", s.lower()).strip("-")
    partes = [p for p in s.split("-") if p and p not in VAZIAS]
    return "-".join(partes[:palavras])


def ler_grupo(texto: str, inicio: int):
    """Lê {...} balanceado começando em texto[inicio] == '{'. Devolve (conteúdo, fim)."""
    assert texto[inicio] == "{"
    nivel = 0
    for i in range(inicio, len(texto)):
        if texto[i] == "{" and texto[i - 1] != "\\":
            nivel += 1
        elif texto[i] == "}" and texto[i - 1] != "\\":
            nivel -= 1
            if nivel == 0:
                return texto[inicio + 1 : i], i + 1
    raise ValueError("chave sem fechamento")


PREFIXOS = {"definition": "def", "theorem": "thm", "proposicao": "prp", "corolario": "cor", "lema": "lem",
            "axiom": "def", "question": "exr", "problem": "exr", "example": "exm", "caixa": "exm"}
NOMES_REF = r"(?:Teorema|Definição|Definicão|Proposição|Corolário|Lema|Exemplo|Exercício|Questão)"


def trocar_systeme(texto: str) -> str:
    """\\systeme{a=b, c=d} (pacote systeme, sem equivalente no MathJax) -> chave + aligned."""
    while True:
        m = re.search(r"\\systeme\*?\{", texto)
        if not m:
            return texto
        corpo, fim = ler_grupo(texto, m.end() - 1)
        partes, nivel, atual = [], 0, ""
        for ch in corpo:
            if ch in "{(":
                nivel += 1
            elif ch in "})":
                nivel -= 1
            if ch == "," and nivel == 0:
                partes.append(atual)
                atual = ""
            else:
                atual += ch
        partes.append(atual)
        linhas = [p.strip().replace("=", "&=", 1) for p in partes if p.strip()]
        novo = "\\left\\{\\begin{aligned}" + " \\\\ ".join(linhas) + "\\end{aligned}\\right."
        texto = texto[: m.start()] + novo + texto[fim:]


def rotulos_e_referencias(texto: str, numero: int) -> str:
    """\\label dentro de teoremas/exemplos vira id estável; \\ref vira referência cruzada do Quarto."""
    nn = f"{numero:02d}"
    pilha, mapa, trocas = [], {}, []
    for m in re.finditer(r"\\begin\{([a-zA-Z*]+)\}|\\end\{([a-zA-Z*]+)\}|\\label\{([^}]*)\}", texto):
        if m.group(1):
            pilha.append(m.group(1))
        elif m.group(2):
            if pilha and pilha[-1] == m.group(2):
                pilha.pop()
        else:
            rotulo = m.group(3)
            amb = next((a for a in reversed(pilha) if a in PREFIXOS), None)
            if amb:
                slug = lugar(rotulo) or "r"
                mapa[rotulo] = f"{PREFIXOS[amb]}-a{nn}-{slug}"
                trocas.append((m.start(), m.end(), f"\n\nROTULO⟦{slug}⟧\n\n"))
            else:
                trocas.append((m.start(), m.end(), ""))
    for ini, fim, novo in reversed(trocas):
        texto = texto[:ini] + novo + texto[fim:]

    def ref(m):
        alvo = mapa.get(m.group(2))
        return f"REFX⟦{alvo}⟧" if alvo else (m.group(1) or "")

    texto = re.sub(r"(" + NOMES_REF + r"(?:~|\s)+)?\\ref\{([^}]*)\}", ref, texto)
    return texto


def preprocessar(texto: str):
    texto = sem_comentarios(texto)
    info = {}

    m = re.search(r"\\setcounter\{chapter\}\{(\d+)\}", texto)
    if m:
        info["numero"] = int(m.group(1)) + 1
        texto = texto.replace(m.group(0), "")

    m = re.search(r"\\chapter\*?(\[([^\]]*)\])?\{", texto)
    if m:
        longo, fim = ler_grupo(texto, m.end() - 1)
        info["curto"] = (m.group(2) or longo).strip()
        info["longo"] = longo.strip()
        texto = texto[: m.start()] + texto[fim:]

    # Figuras TikZ -> marcador numerado (mesma ordem que tikz_para_svg.py usa).
    contador = {"n": 0}

    def figura(_):
        contador["n"] += 1
        return f"\n\\begin{{figuratikz}}FIGURA {contador['n']}\\end{{figuratikz}}\n"

    texto = re.sub(r"\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}", figura, texto, flags=re.S)
    info["figuras"] = contador["n"]

    # tcolorbox com ou sem título.
    def caixa(m):
        opcoes = m.group(1) or ""
        t = re.search(r"title=\{([^}]*)\}", opcoes) or re.search(r"title=([^,\]]*)", opcoes)
        marcador = f"\nTITULO⟦{t.group(1).strip()}⟧\n\n" if t else "\n"
        return "\\begin{caixa}" + marcador

    texto = re.sub(r"\\begin\{tcolorbox\}(\[[^\]]*\])?", caixa, texto)
    texto = texto.replace("\\end{tcolorbox}", "\\end{caixa}")

    # Título de teorema passado como {..} ou [..] logo após \begin{theorem}.
    def titulo_teorema(m):
        return f"\\begin{{{m.group(1)}}}\nTITULO⟦{m.group(3) or m.group(4)}⟧\n\n"

    texto = re.sub(r"\\begin\{(" + TEOREMAS + r")\}\s*(\{([^{}]*)\}|\[([^\]]*)\])", titulo_teorema, texto)

    # Listas com rótulos manuais \item[a)] -> enumerate no estilo a), sem rótulo em cada item.
    def estilo_lista(m):
        rotulo = m.group(2)
        if re.fullmatch(r"[a-z]\)", rotulo):
            return m.group(1) + "[a)]" + m.group(3) + "\\item"
        if re.fullmatch(r"\([a-z]\)", rotulo):
            return m.group(1) + "[(a)]" + m.group(3) + "\\item"
        if re.fullmatch(r"[ivx]+\)", rotulo):
            return m.group(1) + "[i)]" + m.group(3) + "\\item"
        return m.group(0)

    texto = re.sub(r"(\\begin\{enumerate\})(?:\s*)\\item\[([^\]]*)\]()", lambda m: estilo_lista(m), texto)
    texto = re.sub(r"(\\begin\{enumerate\}\[[^\]]*\])\s*\\item", lambda m: m.group(1) + "\n\\item", texto)
    texto = re.sub(r"\\item\[(?:[a-z]|\([a-z]\)|[ivx]+)\)\]", r"\\item", texto)
    texto = re.sub(r"\\item\[\([a-z]\)\]", r"\\item", texto)

    texto = trocar_systeme(texto)
    texto = rotulos_e_referencias(texto, info.get("numero", 0))

    for padrao in REMOVER:
        texto = re.sub(padrao, "", texto)
    # "\ " solto (espaço forçado) no fim de linhas e depois de ambientes
    texto = re.sub(r"\\ (?=\s*\n)", "", texto)
    texto = re.sub(r"(\\end\{[a-z]+\})\s*\\\s", r"\1", texto)
    return texto, info


def comandos_perdidos(texto: str):
    """Comandos LaTeX fora da matemática que o Pandoc não entende (somem na conversão)."""
    r = subprocess.run(["quarto", "pandoc", "-f", "latex+raw_tex", "-t", "json"],
                       input=texto, capture_output=True, text=True, encoding="utf-8", errors="replace")
    achados = []

    def andar(no):
        if isinstance(no, dict):
            if no.get("t") == "RawInline" and no["c"][0] in ("latex", "tex"):
                achados.append(no["c"][1])
            for v in no.values():
                andar(v)
        elif isinstance(no, list):
            for v in no:
                andar(v)

    try:
        andar(json.loads(r.stdout))
    except json.JSONDecodeError:
        return []
    vistos = []
    for a in achados:
        cmd = re.match(r"\\[a-zA-Z]+", a)
        chave = cmd.group(0) if cmd else a[:30]
        if chave not in vistos:
            vistos.append(chave)
    return [f"comando sem equivalente no site (some na conversão): {c}" for c in vistos]


def achar_principal(tex: pathlib.Path):
    """O arquivo com \\documentclass que inclui as aulas (na pasta da aula ou na de cima)."""
    for pasta in (tex.parent, tex.parent.parent):
        for candidato in sorted(pasta.glob("*.tex")):
            if candidato == tex:
                continue
            try:
                inicio = candidato.read_text(encoding="utf-8", errors="replace")[:4000]
            except OSError:
                continue
            if "\\documentclass" in inicio:
                return candidato
    return None


def contar(texto: str):
    c = {}
    for env, nome in [("question", "exercícios"), ("definition", "definições"), ("theorem", "teoremas"),
                      ("proposicao", "proposições"), ("corolario", "corolários"), ("tikzpicture", "figuras")]:
        c[nome] = len(re.findall(r"\\begin\{" + env + r"\}", texto))
    c["exemplos"] = len(re.findall(r"title=\{?Exemplo", texto))
    return c


def contar_qmd(md: str):
    return {
        "exercícios": len(re.findall(r"\{#exr-", md)),
        "definições": len(re.findall(r"\{#def-", md)),
        "teoremas": len(re.findall(r"\{#thm-", md)),
        "proposições": len(re.findall(r"\{#prp-", md)),
        "corolários": len(re.findall(r"\{#cor-", md)),
        "figuras": len(re.findall(r"\.svg\)", md)),
        "exemplos": len(re.findall(r"\{#exm-", md)),
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("tex", type=pathlib.Path)
    ap.add_argument("--disciplina", default="edo")
    ap.add_argument("--sem-figuras", action="store_true", help="não compila as figuras TikZ")
    ap.add_argument("--saida", type=pathlib.Path, help="grava a página neste arquivo (para comparar sem sobrescrever)")
    args = ap.parse_args()

    original = args.tex.read_text(encoding="utf-8", errors="replace")
    texto, info = preprocessar(original)
    numero = info.get("numero")
    if numero is None:
        m = re.search(r"(\d+)", args.tex.stem)
        numero = int(m.group(1)) if m else 0
    nn = f"{numero:02d}"
    pasta = RAIZ / "disciplinas" / args.disciplina / "aulas"
    pasta.mkdir(parents=True, exist_ok=True)
    nome = f"aula-{nn}-{lugar(info.get('curto', 'aula'))}.qmd"

    r = subprocess.run(
        ["quarto", "pandoc", "-f", "latex", "-t", "markdown", "--wrap=none",
         "--lua-filter", str(FILTRO), "-M", f"aula={nn}"],
        input=texto, capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    if r.returncode != 0:
        sys.exit("Pandoc falhou:\n" + r.stderr)
    corpo = r.stdout
    avisos = [l[6:] for l in r.stderr.splitlines() if l.startswith("AVISO ")]
    avisos += comandos_perdidos(texto)

    titulo = f"Aula {numero}: {info.get('curto', '')}".strip()
    cab = ["---", f'title: "{titulo}"']
    if info.get("longo") and info["longo"] != info.get("curto"):
        cab.append(f'subtitle: "{info["longo"]}"')
    if info.get("longo") and info["longo"] != info.get("curto"):
        cab.append(f'description: "{info["longo"]}"')
    pdf = pasta / "pdf" / f"aula-{nn}.pdf"
    if pdf.exists():
        cab.append(f"pdf-aula: pdf/aula-{nn}.pdf")
    cab.append("---")
    destino = args.saida.resolve() if args.saida else pasta / nome
    destino.write_text("\n".join(cab) + "\n\n" + corpo, encoding="utf-8")

    if info["figuras"] and not args.sem_figuras:
        cmd = [sys.executable, str(TIKZ), str(args.tex), str(pasta / "figuras" / f"aula-{nn}")]
        principal = achar_principal(args.tex)
        if principal:
            cmd += ["--preambulo", str(principal)]
        subprocess.run(cmd)

    antes, depois = contar(sem_comentarios(original)), contar_qmd(corpo)
    print(f"\nGerado: {destino}")
    print(f"{'':14}{'.tex':>6}{'página':>8}")
    for k in antes:
        marca = "" if antes[k] == depois.get(k, 0) else "  <- confira"
        print(f"{k:14}{antes[k]:>6}{depois.get(k, 0):>8}{marca}")
    if avisos:
        print("\nPara revisar:")
        for a in avisos:
            print("  -", a)


if __name__ == "__main__":
    main()
