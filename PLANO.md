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

### Fase 0: reconhecimento (feita em 16/10)
- [x] Caminho dos .tex e repositório (`wandersonufrpe/wanderson.github.io`) informados.
- [x] Computador dele é Windows; guia ajustado em `COMO-USAR.md`.
- [x] Análise dos .tex: 22 aulas (01–13, 16–24; não existem 14 e 15), exercícios no ambiente `question` sem soluções, exemplos em `tcolorbox`, 18 figuras TikZ (quase todas candidatas a applet). Conversor `ferramentas/tex_para_qmd.py` testado em todas: contagens batem.

### Fase 1: revisão do visual
- [ ] Mostrar o site com `quarto preview` e ajustar cores, fontes e navegação ao gosto dele.

### Fase 2: aula piloto
- [x] Aulas 01 e 02 convertidas (a 01 não tem teoria nem figuras; a 02 mostra todos os tipos de bloco). Campo de direções da Aula 02 virou applet.
- [x] Formato aprovado pelo Wanderson.

### Fase 3: restante de EDO
- [x] Aulas 03 a 13 e 16 a 18 convertidas (16/10), com PDFs. Aulas 14 e 15 foram revisão e prova (aviso na página da disciplina).
- [ ] Aulas 19 a 24: esperar o Wanderson organizar as notas.
- [ ] Anexos da disciplina (futuro): começar pela demonstração de Abel-Liouville ("Aula 17 - demonstração de Abel-Liouville.tex").
- [x] Página-modelo movida para `_modelo-de-aula.qmd` (não é publicada).

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
- [x] Repositório criado e site enviado.
- [x] Site no ar em https://wandersonufrpe.github.io/wanderson.github.io/
- [ ] Decidir se renomeia o repositório para `wandersonufrpe.github.io` (endereço curto).
- [ ] Se a UFRPE ceder um subdomínio, configurar o domínio próprio.

### Fase 8: manutenção
- [ ] Revisar os comandos em `.claude/commands/` depois do uso real e ajustar.
