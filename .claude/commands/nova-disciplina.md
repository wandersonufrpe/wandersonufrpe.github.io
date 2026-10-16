---
description: Cria a estrutura de uma disciplina nova ou ativa uma que estava em construção
argument-hint: <nome da disciplina>
---

Crie ou ative a disciplina `$ARGUMENTS`.

1. Escolha uma sigla curta para a pasta (minúsculas, hífens). Se já existir em `disciplinas/`, use a existente.
2. `disciplinas/<sigla>/index.qmd` no mesmo formato de `disciplinas/edo/index.qmd`: Sobre a disciplina, Ementa, Bibliografia, Cronograma, Aulas (listagem automática). O que não souber fica como `[A PREENCHER]{.a-preencher}` e vai para `PENDENCIAS.md`.
3. Crie `disciplinas/<sigla>/aulas/` e, em `_quarto.yml`, uma barra lateral com `id: <sigla>` no mesmo formato da de EDO.
4. Atualize o item da disciplina em `disciplinas/index.qmd` (status e descrição).
5. `quarto render` sem erros e relatório do que ficou pendente.
