# Como usar o site no dia a dia

Guia curto para o Linux Mint. Na prática, você pode pedir quase tudo isto ao Claude Code ("publica o site", "mostra a prévia"); o guia serve para entender o que acontece.

## 1. Instalar (uma vez)

Abra o Terminal e rode:

```bash
sudo apt install git poppler-utils
```

- **Quarto**: baixe o arquivo `.deb` para Linux em <https://quarto.org/docs/get-started/> e instale com
  `sudo apt install ./quarto-*-linux-amd64.deb` (na pasta de Downloads).
- **LaTeX**: você já usa. O conversor de figuras precisa de `pdflatex` e do `pdftocairo` (vem no `poppler-utils`).

Confira com `quarto check`.

## 2. Ver o site no seu computador

Dentro da pasta do projeto:

```bash
quarto preview
```

O navegador abre com o site. Cada vez que você salva um arquivo, a página atualiza sozinha. Para parar, `Ctrl+C` no terminal.

Para ver também as dicas em rascunho (sugeridas pelo Claude Code e ainda não aprovadas):

```bash
quarto preview --profile revisao
```

## 3. Onde editar cada coisa

| Quero mudar... | Arquivo |
|---|---|
| Texto da página inicial | `index.qmd` |
| Uma aula | `disciplinas/edo/aulas/aula-NN-....qmd` |
| Ementa, bibliografia, cronograma de EDO | `disciplinas/edo/index.qmd` |
| Turmas, horários, avisos | `semestre/index.qmd` |
| Projetos, publicações etc. | `projetos/`, `publicacoes.qmd`, `orientacoes.qmd`... |
| Itens do menu | `_quarto.yml` |
| Cores | `estilos/claro.scss` e `estilos/escuro.scss` |
| Macros de matemática | `macros.tex` |

Os arquivos `.qmd` são Markdown com matemática em LaTeX (`$...$` e `$$...$$`). O formato dos exercícios está em `CLAUDE.md`.

## 4. Publicar pela primeira vez

1. No GitHub, crie um repositório vazio (botão **New**). Se o nome for `SEU-USUARIO.github.io`, o endereço do site fica mais curto.
2. Na pasta do projeto:
   ```bash
   git remote add origin https://github.com/SEU-USUARIO/NOME-DO-REPOSITORIO.git
   git push -u origin main
   ```
3. No repositório, vá em **Settings → Pages → Build and deployment → Source** e escolha **GitHub Actions**.
4. Em **Actions** aparece "Publicar site" rodando. Quando ficar verde (um ou dois minutos), o site está no ar.

## 5. Publicar alterações

```bash
git add -A
git commit -m "Aula 03 publicada"
git push
```

Ou peça ao Claude Code: `/publicar`.

## 6. Desfazer um erro

- Antes de publicar, para voltar um arquivo à última versão salva no Git: `git restore caminho/do/arquivo.qmd`
- Depois de publicar, para desfazer o último envio: `git revert HEAD` e depois `git push`

Nada se perde de vez: o Git guarda todas as versões.

## 7. Domínio próprio (opcional)

Endereços `.edu` e `.edu.br` são só para instituições. Se a TI da UFRPE aceitar criar um subdomínio para você:

1. Peça que criem um registro **CNAME** do subdomínio apontando para `SEU-USUARIO.github.io`.
2. No repositório: **Settings → Pages → Custom domain**, digite o subdomínio e salve.
3. Quando o GitHub confirmar, marque **Enforce HTTPS**.

## 8. Espaço de dúvidas nas aulas (opcional)

Usa as Discussions do GitHub, pelo Giscus. Quem quiser comentar precisa de conta no GitHub.

1. No repositório: **Settings → General → Features**, marque **Discussions** e crie uma categoria "Dúvidas".
2. Instale o app em <https://github.com/apps/giscus> só para este repositório.
3. Em `disciplinas/edo/aulas/_metadata.yml`, tire os `#` do bloco `comments` e troque `SEU-USUARIO/SEU-REPOSITORIO`.
