# Como usar o site no dia a dia

Guia curto para Windows. Na prática, você pode pedir quase tudo isto ao Claude ("converte a Aula 03", "publica o site"); o guia serve para entender o que acontece.

## Onde fica cada coisa

- **Seus .tex** continuam em `D:\Coisas no Drive\Aula a aula (1)\Notas de aula`. Nada é alterado lá.
- **O site** está em https://wandersonufrpe.github.io e o código fica no GitHub, em `wandersonufrpe/wandersonufrpe.github.io`. Essa é a cópia oficial.
- **No seu computador**, uma cópia do site serve para você abrir, mexer e ver a prévia (passo 2).

## 1. Publicar (ativar uma vez)

No repositório do GitHub, em **Settings → Pages → Build and deployment → Source**, deve estar marcado **GitHub Actions**. Com isso, cada alteração enviada ao GitHub é publicada sozinha em um ou dois minutos.

Para acompanhar: aba **Actions** do repositório. Cada envio aparece como "Publicar site", com um sinal verde quando termina.


## 2. Ter o site no seu computador (opcional)

1. Instale o **GitHub Desktop** (<https://desktop.github.com>) e entre com sua conta.
2. **File → Clone repository**, escolha `wandersonufrpe.github.io` e uma pasta **fora** do Google Drive (por exemplo `C:\Users\SeuNome\Documents\GitHub`). Pastas do Git dentro do Drive podem gerar conflitos de sincronização.
3. Para receber o que o Claude enviou: botão **Fetch origin**, depois **Pull origin**.
4. Para enviar o que você mudou: escreva um resumo no canto inferior esquerdo, **Commit to main**, depois **Push origin**.

A pasta `D:\Coisas no Drive\SiteGithub\site-portfolio` foi só o pacote inicial. Depois de clonar, pode apagá-la.

## 3. Ver o site antes de publicar (opcional)

1. Instale o **Quarto** para Windows: <https://quarto.org/docs/get-started/>.
2. No GitHub Desktop: **Repository → Open in Command Prompt** (ou Terminal).
3. Digite `quarto preview`. O navegador abre o site; cada arquivo salvo atualiza a página. Para parar: `Ctrl+C`.
4. Para ver também as dicas em rascunho: `quarto preview --profile revisao`.

## 4. Onde editar cada coisa

| Quero mudar... | Arquivo |
|---|---|
| Texto da página inicial | `index.qmd` |
| Uma aula | `disciplinas/edo/aulas/aula-NN-....qmd` |
| PDF de uma aula | `disciplinas/edo/aulas/pdf/aula-NN.pdf` (troque pelo seu, mesmo nome) |
| Ementa, bibliografia, cronograma de EDO | `disciplinas/edo/index.qmd` |
| Turmas, horários, avisos | `semestre/index.qmd` |
| Projetos, publicações etc. | `projetos/`, `publicacoes.qmd`, `orientacoes.qmd`... |
| Itens do menu | `_quarto.yml` |
| Cores | `estilos/claro.scss` e `estilos/escuro.scss` |
| Macros de matemática | `macros.tex` |

Os `.qmd` são texto com matemática em LaTeX (`$...$` e `$$...$$`). Abra com qualquer editor (o Bloco de Notas serve; o VS Code é mais confortável). O formato dos exercícios está em `CLAUDE.md`.

## 5. Desfazer um erro

No GitHub Desktop, aba **History**: clique com o botão direito numa alteração e escolha **Revert changes in commit**. Depois **Push origin**. Nada se perde de vez: o Git guarda todas as versões.

## 6. Domínio próprio (opcional)

Endereços `.edu` e `.edu.br` são só para instituições. Se a TI da UFRPE aceitar criar um subdomínio para você:

1. Peça que criem um registro **CNAME** do subdomínio apontando para `wandersonufrpe.github.io`.
2. No repositório: **Settings → Pages → Custom domain**, digite o subdomínio e salve.
3. Quando o GitHub confirmar, marque **Enforce HTTPS**.

## 7. Espaço de dúvidas nas aulas (opcional)

Usa as Discussions do GitHub, pelo Giscus. Quem quiser comentar precisa de conta no GitHub.

1. No repositório: **Settings → General → Features**, marque **Discussions** e crie uma categoria "Dúvidas".
2. Instale o app em <https://github.com/apps/giscus> só para este repositório.
3. Em `disciplinas/edo/aulas/_metadata.yml`, tire os `#` do bloco `comments`.
