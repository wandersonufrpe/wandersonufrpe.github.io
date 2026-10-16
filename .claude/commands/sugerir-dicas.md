---
description: Sugere dicas, respostas e soluções (como rascunho) para os exercícios de uma aula
argument-hint: <arquivo da aula .qmd ou número da aula>
---

Sugira ajuda graduada para os exercícios de `$ARGUMENTS`.

1. Leia `CLAUDE.md` e `GUIA-DE-ESTILO-DIDATICO.md`. Se o guia ainda não existir, pare e proponha criá-lo primeiro a partir das notas de aula (ele precisa aprovar o guia antes).
2. Para cada exercício da aula, complete o que falta, nesta ordem: Dica 1, Dica 2, Resposta, Solução.
   - Dica 1: um empurrão (qual ideia ou resultado da aula usar), sem fazer contas.
   - Dica 2: o primeiro passo concreto.
   - Resposta: só o resultado final.
   - Solução: a resolução completa, no estilo e na notação das notas.
   - Use resultados e nomes que aparecem na própria aula ou em aulas anteriores.
3. Tudo o que você escrever leva a classe `.rascunho`: `::: {.dica .rascunho}`, `::: {.resposta .rascunho}`, `::: {.solucao .rascunho}`. Não mexa no que já existe sem `.rascunho`.
4. Confira cada resposta e solução com Python/SymPy quando der (derivar, substituir, resolver). Se não conseguir confirmar, escreva isso no relatório em vez de arriscar.
5. `quarto render` sem erros. Relatório: quantas sugestões por exercício e quais você não conseguiu verificar.
6. Lembre que ele pode ver os rascunhos com `quarto preview --profile revisao` e aprová-los com `/revisar-dicas`.
