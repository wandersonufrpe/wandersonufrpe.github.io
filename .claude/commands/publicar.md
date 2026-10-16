---
description: Confere o site e publica no GitHub Pages
argument-hint: [mensagem do commit, opcional]
---

Publique as alterações do site.

1. `git status`: resuma em português o que mudou desde a última publicação.
2. `quarto render` (sem perfil). Pare se houver erro ou aviso de link quebrado e explique como resolver.
3. Confira que nenhum rascunho foi para o HTML: `grep -rl "aguardando revisão\|rascunho-visivel" _site --include=*.html` não deve listar nada.
4. Conte quantos `[A PREENCHER` ainda existem nas páginas e avise (não impede a publicação).
5. Mostre a mensagem de commit proposta (use `$ARGUMENTS` se ele deu uma) e **peça confirmação** antes de `git commit` e `git push`.
6. Depois do push, diga onde acompanhar a publicação (aba Actions do repositório) e o endereço do site.
