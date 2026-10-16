# Plano do projeto

Fases combinadas com o Wanderson. Ao terminar cada fase: mostrar o resultado, resumir e esperar aprovação.

## Já feito (16/10/2026, antes de ter acesso aos arquivos .tex)

- [x] Projeto Quarto com navegação completa: Início, Disciplinas, Semestre, Projetos (Ensino, Pesquisa, Extensão), Publicações, Orientações, Recursos, Currículo, Contato.
- [x] Temas claro e escuro com as cores por área; tipografia Literata (texto) e Fira Sans (títulos e interface); responsivo e testado em 390 px e 1280 px.
- [x] Componentes: dicas numeradas, resposta, solução, rascunhos ocultos (perfil `revisao`), referência da questão, conferência automática, objetivos/pré-requisitos, botão de PDF, macros LaTeX.
- [x] Applet de campo de direções (toque para traçar soluções, controle deslizante, redimensiona sozinho).
- [x] Página-modelo `disciplinas/edo/aulas/aula-00-modelo.qmd` com todos os componentes.
- [x] Páginas-base das disciplinas em construção: Lógica, Cálculo N1, Otimização Combinatória.
- [x] Conversor TikZ → SVG (`ferramentas/tikz_para_svg.py`), testado com TikZ e pgfplots.
- [x] Publicação automática (GitHub Actions → GitHub Pages).
- [x] `CLAUDE.md`, comandos do Claude Code, `COMO-USAR.md`, `PENDENCIAS.md`.

## Próximas fases

### Fase 0: reconhecimento
- [ ] Perguntar ao Wanderson os itens de `PENDENCIAS.md` (pelo menos: caminho dos .tex de EDO e usuário do GitHub).
- [ ] Verificar o computador dele: git, Quarto, TeX Live, um conversor PDF→SVG (`pdftocairo` vem no pacote `poppler-utils`). Ver `COMO-USAR.md`.
- [ ] Analisar os .tex de EDO: preâmbulo, macros, ambientes, como os exercícios estão marcados, quantas figuras TikZ e de que tipo. Entregar relatório curto e plano de conversão.

### Fase 1: revisão do visual
- [ ] Mostrar o site com `quarto preview` e ajustar cores, fontes e navegação ao gosto dele.

### Fase 2: aula piloto
- [ ] Converter só a Aula 01 de EDO com `/nova-aula` e parar para revisão. Ajustar o padrão de conversão até ele aprovar.

### Fase 3: restante de EDO
- [ ] Converter as demais aulas em lotes, com resumo por lote do que não converteu bem.
- [ ] Apagar `aula-00-modelo.qmd`.

### Fase 4: interatividade
- [ ] Trocar figuras de famílias de soluções e campos de direções por applets (ver `candidata_a_applet` nos manifestos).
- [ ] Criar conferências automáticas para revisões conceituais (identificação e classificação de EDOs).

### Fase 5: dicas sugeridas
- [ ] Escrever `GUIA-DE-ESTILO-DIDATICO.md` a partir das notas e mostrar para ele ajustar.
- [ ] `/sugerir-dicas` aula por aula; `/revisar-dicas` com ele.

### Fase 6: portfólio
- [ ] Preencher Início, Projetos, Publicações, Orientações, Recursos, Currículo e Contato com o que ele fornecer.
- [ ] Ativar o espaço de dúvidas (Giscus) nas aulas, explicando que é preciso conta no GitHub para comentar.

### Fase 7: publicação
- [ ] Criar o repositório, enviar, ativar o Pages (Source: GitHub Actions) e conferir o site no ar.
- [ ] Se a UFRPE ceder um subdomínio, configurar o domínio próprio.

### Fase 8: manutenção
- [ ] Revisar os comandos em `.claude/commands/` depois do uso real e ajustar.
