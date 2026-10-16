---
description: Converte uma aula em LaTeX numa página do site
argument-hint: <caminho/da/aula.tex> [sigla-da-disciplina]
---

Converta a aula `$ARGUMENTS` para o site, seguindo `CLAUDE.md` (leia antes, se ainda não leu nesta sessão) e, se existir, `GUIA-DE-ESTILO-DIDATICO.md`.

1. **Identificar**: descubra a disciplina (pasta em `disciplinas/`; padrão `edo`), o número e o assunto da aula. Nome do arquivo: `disciplinas/<sigla>/aulas/aula-NN-assunto.qmd`. Se o número ou a disciplina não estiverem claros, pergunte.
2. **Figuras**: rode `python3 ferramentas/tikz_para_svg.py <tex> disciplinas/<sigla>/aulas/figuras/aula-NN` e leia o `manifesto.json`. Figuras com erro: tente corrigir o preâmbulo; se não der, anote. Figuras marcadas como `candidata_a_applet`: liste-as no relatório com uma proposta de applet, mas use o SVG por enquanto.
3. **Macros**: leve para `macros.tex` os `\newcommand` de matemática que ainda não estão lá.
4. **Texto**: converta seguindo a tabela de `CLAUDE.md`. Preserve toda a matemática e a ordem do texto. Não reescreva as explicações do professor; só adapte a marcação.
5. **Exercícios**: use o formato de `CLAUDE.md`. Dicas, respostas ou soluções que já estão nas notas entram normalmente. Não crie dicas novas aqui (isso é com `/sugerir-dicas`).
6. **Cabeçalho**: `title`, `description`, `objetivos` e `pre-requisitos` (se as notas trazem; se não, registre em `PENDENCIAS.md`), `pdf-aula`.
7. **PDF**: compile o .tex original numa pasta temporária (`pdflatex -output-directory=<tmp>`), nunca ao lado do original, e copie para `disciplinas/<sigla>/aulas/pdf/aula-NN.pdf`.
8. **Conferir**: `quarto render` sem erros; compare a contagem de definições, teoremas, exemplos, exercícios e figuras entre o .tex e a página.
9. **Relatório** curto: o que foi convertido, o que não converteu bem, figuras candidatas a applet, pendências. Sugira `quarto preview` para ele ver.

Não altere o arquivo .tex original. Não faça commit nem push sem pedir.
