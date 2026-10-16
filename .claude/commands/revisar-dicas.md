---
description: Mostra os rascunhos pendentes e aplica a decisão do professor (aprovar, editar, descartar)
argument-hint: [aula ou disciplina, opcional]
---

Revise com o Wanderson os rascunhos pendentes em `$ARGUMENTS` (se vazio, em todo o site).

1. Encontre todos os blocos com a classe `.rascunho` nos `.qmd` (limite ao escopo pedido).
2. Mostre um exercício por vez: o enunciado e os rascunhos dele, com a matemática legível.
3. Para cada rascunho, pergunte: aprovar, editar (ele diz o que mudar) ou descartar.
   - Aprovar: tire só a classe `.rascunho` (ex.: `::: {.dica .rascunho}` vira `::: dica`).
   - Editar: aplique a mudança e mostre de novo antes de aprovar.
   - Descartar: apague o bloco.
4. Se ele corrigir o jeito de explicar, proponha registrar a lição em `GUIA-DE-ESTILO-DIDATICO.md`.
5. No fim: `quarto render` e um resumo (aprovados, editados, descartados, ainda pendentes).
