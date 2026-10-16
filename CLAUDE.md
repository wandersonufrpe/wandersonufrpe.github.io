# Site-portfólio do prof. Wanderson Aleksander Oliveira

Site em Quarto que é ao mesmo tempo o portfólio de professor universitário (UFRPE, desde 2013) e o lugar das notas de aula, convertidas dos arquivos LaTeX dele. Publicado no GitHub Pages por GitHub Actions. O plano completo e o que já foi feito estão em `PLANO.md`; o que falta ele informar está em `PENDENCIAS.md`.

O Wanderson está aprendendo Quarto e Git agora: explique em português, sem jargão, e mostre o resultado (`quarto preview`) antes de seguir para a próxima etapa. O computador dele é Windows.

Repositório: `wandersonufrpe/wanderson.github.io` (a cópia oficial). Os .tex de EDO ficam em `D:\Coisas no Drive\Aula a aula (1)\Notas de aula\Introdução às equações ordinárias\txt` (um arquivo por aula, `Aula NN.tex`; preâmbulo em `Notas de aula - EDO.tex` e `config.tex`).

## Regras que não mudam

- **Nunca invente conteúdo factual**: ementas, bibliografias, datas, publicações, orientações, projetos, dados biográficos, contatos. Onde faltar, escreva `[A PREENCHER: o que falta]{.a-preencher}` e registre em `PENDENCIAS.md`.
- **Os .tex originais ficam fora deste repositório e nunca são alterados.** Leia-os de onde estão. Compile PDFs numa pasta temporária (`-output-directory`), nunca ao lado do original.
- Não publique dados de alunos (nomes, notas, matrículas) nem provas antigas.
- Não inclua artigos ou trabalhos em preparação (nem em Projetos, nem em Publicações).
- Questões tiradas de livros ou de outros lugares levam a referência no atributo `fonte`.
- Tudo que você sugerir de conteúdo didático (dicas, respostas, soluções) entra como **rascunho** (classe `.rascunho`) até ele aprovar.
- Antes de afirmar que uma resposta ou solução está certa, confira a conta (de preferência com Python/SymPy).

## Estrutura

```
_quarto.yml               navegação, temas, filtros
_quarto-revisao.yml       perfil que mostra rascunhos (nunca publicado)
macros.tex                \newcommand de matemática usados em todas as páginas (MathJax)
filtros/componentes.lua   dicas, resposta, solução, rascunho, fonte, quiz, objetivos, PDF
assets/js/                campo-direcoes.js (applet) e quiz.js
estilos/                  claro.scss, escuro.scss (cores) e comum.scss (regras)
ferramentas/              tex_para_qmd.py (conversor de aulas), conversao.lua, tikz_para_svg.py
_modelo-de-aula.qmd       todos os componentes funcionando (não é publicado: começa com _)
disciplinas/<sigla>/      index.qmd (apresentação) e aulas/aula-NN-assunto.qmd
semestre/                 semestre atual e semestres anteriores
projetos/                 visão geral, ensino, pesquisa, extensão
.claude/commands/         comandos /nova-aula, /sugerir-dicas etc.
```

Pastas das disciplinas: `edo` (Introdução às EDOs, a única completa por enquanto), `logica`, `calculo-n1`, `otimizacao-combinatoria`.

## Cores por área

Cada página declara a área em `body-classes` (no cabeçalho YAML ou num `_metadata.yml` da pasta):

| Classe | Uso | Cor |
|---|---|---|
| `area-ensino` | Disciplinas, aulas, Recursos | verde-bandeira |
| `area-projetos` | Projetos e subpáginas | azul-bebê |
| `area-pesquisa` | Publicações, Orientações, Currículo | vinho |
| `area-admin` | Semestre, Contato | amarelo |
| `area-inicio` | só a página inicial | as quatro |

As cores estão em `estilos/claro.scss` e `estilos/escuro.scss`. Mantenha contraste WCAG AA.

## Modelo de aula

Arquivo `disciplinas/<sigla>/aulas/aula-NN-assunto.qmd` (NN com dois dígitos, para a ordem ficar certa):

```markdown
---
title: "Aula 3: Equações separáveis"
description: "Separação de variáveis e problemas de valor inicial"
objetivos:
  - Reconhecer uma equação separável.
pre-requisitos:
  - Integração por substituição.
pdf-aula: pdf/aula-03.pdf
---
```

`_modelo-de-aula.qmd` mostra todos os componentes funcionando (dicas, rascunhos, quiz, applet). Arquivos que começam com `_` não viram páginas.

### Conversão LaTeX → Quarto

Use o conversor, feito para o formato das notas dele:

```
python3 ferramentas/tex_para_qmd.py "CAMINHO/Aula 03.tex" --disciplina edo
```

Ele gera a página, as figuras TikZ em SVG e um relatório (contagem .tex × página e o que não converteu). Rodar de novo **sobrescreve** a página: se ela já foi editada à mão (applet, dicas), use `--saida /tmp/nova.qmd --sem-figuras` e copie só o que mudou.

Ambientes das notas dele e o que viram: `question` → exercício (`#exr-`), `tcolorbox` com título "Exemplo NN" → exemplo numerado automaticamente (a caixa sem título logo depois é continuação), `definition`, `theorem`, `proposicao`, `corolario`, `lema` → blocos numerados, `demonstration`/`proof` → `.proof`, `note` → nota, `discussion` → "Texto complementar". `\sin`, `\tan`, `\arctan`, `\arcsin` aparecem como sen, tg, arctg, arcsen (em `macros.tex`).

Notas não têm soluções nem objetivos: dicas e respostas entram depois como rascunho (`/sugerir-dicas`); objetivos ficam pendentes até ele escrever.

Tabela geral, para outros formatos:

| LaTeX | Quarto |
|---|---|
| `\section{...}` | `## ...` |
| `\begin{definition}[Nome]` | `::: {#def-rotulo}` + `## Nome` na primeira linha |
| `\begin{theorem}`, `lemma`, `corollary`, `proposition` | `#thm-`, `#lem-`, `#cor-`, `#prp-` |
| `\begin{example}` | `#exm-` |
| `\begin{proof}` | `::: {.proof}` |
| `\begin{remark}`/observação | `::: {.callout-note appearance="simple"}` |
| `\label{x}` + `\ref{x}` | id do bloco + `@def-rotulo` |
| `equation`, `align` | `$$ ... $$` (align vira `\begin{aligned}` dentro de `$$`) |
| figura TikZ | SVG (`ferramentas/tikz_para_svg.py`) ou applet |
| `\newcommand` do preâmbulo | `macros.tex` |

Ids de blocos precisam ser únicos no site inteiro: use o número da aula (`#thm-a03-existencia`).

### Exercícios

```markdown
::: {#exr-a03-1 fonte="Boyce e DiPrima, 9. ed., seção 2.2, exercício 4"}
Enunciado.

::: dica
Primeiro empurrão.
:::

::: dica
Ajuda mais direta.
:::

::: resposta
Só o resultado.
:::

::: solucao
Resolução completa.
:::
:::
```

- Dicas são numeradas sozinhas. Ordem sempre: dicas → resposta → solução.
- Sugestão ainda não aprovada: `::: {.dica .rascunho}` (vale para `resposta` e `solucao`). Ela some do site e só aparece em `quarto preview --profile revisao`.
- `fonte` é opcional; use só quando a questão vem de outro lugar.

### Conferência automática (revisões conceituais curtas)

```markdown
::: quiz
A EDO $y' = t\,y^2$ é:

- [ ] linear
- [x] não linear

::: explicacao
Por que a resposta certa é a certa.
:::
:::
```

Uma única opção marcada com `[x]`. Bom para classificar EDOs (ordem, linearidade, autonomia, separabilidade, homogeneidade).

### Applets (campo de direções)

~~~markdown
```{ojs}
//| echo: false
import { campoDirecoes } from "../../../assets/js/campo-direcoes.js"
viewof k = Inputs.range([-2, 2], { value: 0.5, step: 0.1, label: "k" })
campoDirecoes({ f: (t, y) => k * y, t: [-3, 3], y: [-3, 3], largura: width,
                solucoes: [[0, 1]], chave: "a03-k", descricao: "Campo de direções de y' = k y" })
```
~~~

- `chave` única por applet (mantém as curvas tocadas quando o controle muda).
- O caminho do `import` é relativo à página (de uma aula: `../../../assets/js/`).
- Prefira applet quando a figura original mostra uma família de soluções ou um campo de direções. Para outras figuras, SVG.

### Figuras TikZ

```
python3 ferramentas/tikz_para_svg.py CAMINHO/aula03.tex disciplinas/edo/aulas/figuras/aula-03
```

Gera `fig-01.svg`… e `manifesto.json` (linha de origem, erros, candidatas a applet). Use na página como `![Descrição da figura para leitores de tela](figuras/aula-03/fig-01.svg){.tikz}`. A classe `.tikz` dá fundo branco no modo escuro.

## Comandos

- `quarto preview`: ver o site enquanto edita.
- `quarto preview --profile revisao`: ver também os rascunhos.
- `quarto render`: gerar tudo; leia os avisos (links quebrados aparecem aqui).
- Comandos do Claude Code em `.claude/commands/`: `/nova-aula`, `/nova-disciplina`, `/sugerir-dicas`, `/revisar-dicas`, `/novo-semestre`, `/publicar`.

## Antes de publicar

1. `quarto render` sem erros nem avisos novos.
2. Nenhum `.rascunho` virou conteúdo publicado sem aprovação.
3. Se as Actions do GitHub avisarem de versões antigas (`actions/checkout@v4` etc.), atualize em `.github/workflows/publicar.yml`.
4. Commit com mensagem em português descrevendo a mudança; só faça `git push` com a confirmação do Wanderson.
