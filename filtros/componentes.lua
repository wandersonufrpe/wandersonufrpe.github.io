--[[
Componentes didáticos do site.

Sintaxe nas páginas (.qmd):

  ::: {#exr-aula01-separaveis fonte="Autor, Obra, seção 2.1, exercício 5"}
  Enunciado do exercício.

  ::: dica
  Primeiro empurrão.
  :::

  ::: dica
  Uma ajuda mais direta.
  :::

  ::: resposta
  Só o resultado final.
  :::

  ::: solucao
  A resolução completa.
  :::
  :::

  - Cada dica/resposta/solução vira uma caixa recolhível; as dicas são numeradas sozinhas.
  - Acrescente a classe .rascunho ({.dica .rascunho}) para algo ainda não revisado:
    some do site publicado e só aparece com `quarto preview --profile revisao`.
  - Qualquer bloco ::: rascunho (sem outro componente) segue a mesma regra.
  - O atributo fonte="..." no exercício mostra a referência da questão.

  Conferência automática:

  ::: quiz
  A EDO $y' = t\,y^2$ é:

  - [ ] linear
  - [x] não linear

  ::: explicacao
  O termo $y^2$ torna a equação não linear.
  :::
  :::

Metadados de aula (no cabeçalho YAML):
  objetivos: [lista]      pre-requisitos: [lista]      pdf-aula: caminho/para/aula.pdf

Macros: o conteúdo de macros.tex (raiz do projeto) é injetado em todas as páginas.
]]

local revisao = false
for _, perfil in ipairs(quarto.project.profile or {}) do
  if perfil == "revisao" then revisao = true end
end

local usa_quiz = false

local COMPONENTES = {
  dica = { tipo = "tip" },
  resposta = { tipo = "note", titulo = "Resposta final" },
  solucao = { tipo = "important", titulo = "Solução completa" },
}
local ORDEM = { "dica", "resposta", "solucao" }

local function tem_classe(el, classe)
  return el.classes ~= nil and el.classes:includes(classe)
end

local function componente_de(div)
  for _, nome in ipairs(ORDEM) do
    if tem_classe(div, nome) then return nome end
  end
  return nil
end

-- Converte dicas/resposta/solução filhas diretas de uma lista de blocos.
local function processar_blocos(blocos)
  local alterou = false
  local n_dica = 0
  local novos = pandoc.List()
  for _, bloco in ipairs(blocos) do
    if bloco.t == "Div" then
      local nome = componente_de(bloco)
      local rascunho = tem_classe(bloco, "rascunho")
      if nome then
        alterou = true
        if (not rascunho) or revisao then
          local titulo
          if nome == "dica" then
            n_dica = n_dica + 1
            titulo = "Dica " .. n_dica
          else
            titulo = COMPONENTES[nome].titulo
          end
          if rascunho then titulo = titulo .. " (rascunho, aguardando revisão)" end
          local caixa = quarto.Callout({
            type = rascunho and "warning" or COMPONENTES[nome].tipo,
            title = titulo,
            collapse = true,
            content = bloco.content,
          })
          novos:insert(caixa)
        end
      elseif rascunho then
        alterou = true
        if revisao then
          -- mantém o bloco inteiro (um quiz em rascunho continua sendo quiz)
          bloco.classes:insert("rascunho-visivel")
          novos:insert(bloco)
        end
      else
        novos:insert(bloco)
      end
    else
      novos:insert(bloco)
    end
  end
  return novos, alterou
end

-- Referência (fonte) de um exercício, inserida antes da primeira caixa.
local function inserir_fonte(div)
  local fonte = div.attributes["fonte"]
  if not fonte or fonte == "" then return end
  div.attributes["fonte"] = nil
  local nota = pandoc.Div(
    { pandoc.Para({ pandoc.Emph({ pandoc.Str("Fonte:") }), pandoc.Space(), pandoc.Str(fonte) }) },
    pandoc.Attr("", { "fonte-questao" })
  )
  local pos = #div.content + 1
  for i, bloco in ipairs(div.content) do
    if bloco.t == "Div" and (componente_de(bloco) or tem_classe(bloco, "rascunho")) then
      pos = i
      break
    end
  end
  div.content:insert(pos, nota)
end

local function eh_lista_de_tarefas(lista)
  local primeiro = lista.content[1] and lista.content[1][1]
  if not primeiro or not primeiro.content or not primeiro.content[1] then return false end
  local s = primeiro.content[1]
  return s.t == "Str" and (s.text == "☐" or s.text == "☒")
end

local function processar_quiz(div)
  usa_quiz = true
  local novos = pandoc.List()
  for _, bloco in ipairs(div.content) do
    if bloco.t == "BulletList" and eh_lista_de_tarefas(bloco) then
      local opcoes = pandoc.List()
      for _, item in ipairs(bloco.content) do
        local correta = false
        local inicio = item[1] and item[1].content
        if inicio and inicio[1] and inicio[1].t == "Str" then
          correta = inicio[1].text == "☒"
          inicio:remove(1)
          if inicio[1] and inicio[1].t == "Space" then inicio:remove(1) end
        end
        opcoes:insert(pandoc.Div(item, pandoc.Attr("", { "quiz-opcao" }, { ["data-correta"] = correta and "sim" or "nao" })))
      end
      novos:insert(pandoc.Div(opcoes, pandoc.Attr("", { "quiz-opcoes" })))
    elseif bloco.t == "Div" and tem_classe(bloco, "explicacao") then
      novos:insert(pandoc.Div(bloco.content, pandoc.Attr("", { "quiz-explicacao" })))
    else
      novos:insert(bloco)
    end
  end
  div.content = novos
  return div
end

local function Div(div)
  local mudou = false
  if tem_classe(div, "quiz") then
    div = processar_quiz(div)
    mudou = true
  end
  -- (o Quarto já tirou o id "exr-..." deste bloco quando o filtro roda; basta o atributo)
  if div.attributes["fonte"] then
    inserir_fonte(div)
    mudou = true
  end
  local novos, alterou = processar_blocos(div.content)
  if alterou then
    div.content = novos
    mudou = true
  end
  -- Em filtros Lua, alterações só valem se o elemento for devolvido.
  if mudou then return div end
  return nil
end

-- Lista do YAML (objetivos, pré-requisitos) para blocos.
local function lista_meta(valor)
  local itens = pandoc.List()
  if valor == nil then return itens end
  local tipo = pandoc.utils.type(valor)
  if tipo ~= "List" then valor = { valor } end
  for _, item in ipairs(valor) do
    local t = pandoc.utils.type(item)
    if t == "Blocks" then
      itens:insert(item)
    elseif t == "Inlines" then
      itens:insert({ pandoc.Plain(item) })
    else
      itens:insert({ pandoc.Plain({ pandoc.Str(pandoc.utils.stringify(item)) }) })
    end
  end
  return itens
end

local function ler_macros()
  local base = quarto.project.directory or "."
  local arq = io.open(pandoc.path.join({ base, "macros.tex" }), "r")
  if not arq then return nil end
  local linhas = {}
  for linha in arq:lines() do
    local sem_comentario = linha:gsub("^%s*%%.*$", "")
    if sem_comentario:match("%S") then table.insert(linhas, sem_comentario) end
  end
  arq:close()
  if #linhas == 0 then return nil end
  return table.concat(linhas, "\n")
end

-- Converte as linhas \\newcommand/\\renewcommand de macros.tex para o formato do MathJax.
local function configuracao_mathjax(macros)
  local itens = {}
  for linha in (macros or ""):gmatch("[^\n]+") do
    local nome, args, corpo = linha:match("^%s*\\r?e?n?e?w?command%*?%s*{\\(%a+)}%s*%[?(%d*)%]?%s*{(.*)}%s*$")
    if nome then
      local valor = string.format("%q", corpo):gsub("\\\n", "\\n")
      if args ~= "" then
        table.insert(itens, string.format("%s: [%s, %s]", nome, valor, args))
      else
        table.insert(itens, string.format("%s: %s", nome, valor))
      end
    end
  end
  return "<script>\nwindow.MathJax = {\n"
    .. "  tex: { macros: { " .. table.concat(itens, ", ") .. " } },\n"
    .. '  output: { displayOverflow: "linebreak", linebreaks: { inline: true } },\n'
    .. '  chtml: { displayOverflow: "linebreak" }\n'
    .. "};\n</script>"
end

local function Pandoc(doc)
  local novos, _ = processar_blocos(doc.blocks)
  doc.blocks = novos

  local topo = pandoc.List()

  -- Macros LaTeX (bloco oculto lido pelo MathJax).
  local macros = ler_macros()
  if quarto.doc.is_format("html") then
    -- Configuração do MathJax no <head>: macros de macros.tex e quebra de linha automática
    -- de equações longas no celular. Fica fora do conteúdo da página (busca e listagens não veem).
    quarto.doc.include_text("in-header", configuracao_mathjax(macros))
  end

  -- Ações da aula (PDF).
  local pdf = doc.meta["pdf-aula"]
  if pdf then
    local link = pandoc.Link({ pandoc.Str("Baixar o PDF desta aula") }, pandoc.utils.stringify(pdf), "", pandoc.Attr("", { "botao-pdf" }))
    topo:insert(pandoc.Div({ pandoc.Para({ link }) }, pandoc.Attr("", { "aula-acoes" })))
  end

  -- Objetivos e pré-requisitos.
  local objetivos = lista_meta(doc.meta["objetivos"])
  local prereq = lista_meta(doc.meta["pre-requisitos"])
  if #objetivos > 0 or #prereq > 0 then
    local caixa = pandoc.List()
    if #objetivos > 0 then
      caixa:insert(pandoc.Para({ pandoc.Strong({ pandoc.Str("Ao final desta aula você deve saber:") }) }))
      caixa:insert(pandoc.BulletList(objetivos))
    end
    if #prereq > 0 then
      caixa:insert(pandoc.Para({ pandoc.Strong({ pandoc.Str("Antes de começar, revise:") }) }))
      caixa:insert(pandoc.BulletList(prereq))
    end
    topo:insert(pandoc.Div(caixa, pandoc.Attr("", { "aula-objetivos" })))
  end

  for i = #topo, 1, -1 do doc.blocks:insert(1, topo[i]) end

  if usa_quiz then
    quarto.doc.add_html_dependency({
      name = "quiz",
      version = "1.0.0",
      scripts = { "../assets/js/quiz.js" },
    })
  end
  return doc
end

return {
  { Div = Div },
  { Pandoc = Pandoc },
}
