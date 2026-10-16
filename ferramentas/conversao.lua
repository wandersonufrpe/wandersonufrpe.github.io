--[[
Filtro usado por ferramentas/tex_para_qmd.py (não pelo site).
Transforma o que o Pandoc leu dos .tex do professor em blocos do Quarto:

  definition            -> ::: {#def-aNN-k}
  theorem               -> ::: {#thm-aNN-k name="..."}
  proposicao            -> #prp-     corolario -> #cor-     lema -> #lem-
  question / problem    -> ::: {#exr-aNN-k}
  tcolorbox "Exemplo .."-> ::: {#exm-aNN-k}   (a caixa sem título logo depois é a continuação)
  tcolorbox outro título-> callout com o título
  tcolorbox sem título  -> continuação da caixa anterior ou ::: caixa
  demonstration / proof -> ::: proof
  note                  -> callout-note simples
  discussion            -> callout "Texto complementar"
  figuratikz            -> imagem SVG da pasta figuras/aula-NN
  comandos LaTeX que o Pandoc não entendeu -> [...]{.nao-convertido} e aviso no terminal
]]

local AULA = "00"
local avisos = {}
local contadores = {}

local function proximo(prefixo)
  contadores[prefixo] = (contadores[prefixo] or 0) + 1
  return string.format("%s-a%s-%d", prefixo, AULA, contadores[prefixo])
end

local function tem(el, classe)
  return el.classes and el.classes:includes(classe)
end

-- Marcadores de título inseridos pelo pré-processamento em Python: TITULO⟦...⟧
local function extrair_titulo(div)
  local primeiro = div.content[1]
  if not primeiro or (primeiro.t ~= "Para" and primeiro.t ~= "Plain") then return nil end
  local texto = pandoc.utils.stringify(primeiro)
  local titulo = texto:match("^TITULO⟦(.-)⟧%s*$")
  if titulo then
    div.content:remove(1)
    return titulo
  end
  -- marcador no começo de um parágrafo com mais texto
  local inl = primeiro.content
  if inl[1] and inl[1].t == "Str" and inl[1].text:match("^TITULO⟦") then
    local partes, fim = {}, nil
    for i, x in ipairs(inl) do
      local s = pandoc.utils.stringify(x)
      if x.t == "Space" then s = " " end
      table.insert(partes, s)
      if s:find("⟧") then fim = i break end
    end
    if fim then
      local junto = table.concat(partes)
      titulo = junto:match("^TITULO⟦(.-)⟧")
      for _ = 1, fim do inl:remove(1) end
      while inl[1] and (inl[1].t == "Space" or inl[1].t == "SoftBreak") do inl:remove(1) end
      return titulo
    end
  end
  return nil
end

local function extrair_rotulo(div)
  for i = 1, math.min(3, #div.content) do
    local b = div.content[i]
    if b.t == "Para" or b.t == "Plain" then
      local r = pandoc.utils.stringify(b):match("^ROTULO⟦(.-)⟧%s*$")
      if r then
        div.content:remove(i)
        return r
      end
    end
  end
  return nil
end

local function limpar_nome(titulo, palavras)
  if not titulo then return nil end
  for _, p in ipairs(palavras) do
    local resto = titulo:match("^" .. p .. "%s+de%s+(.+)$") or titulo:match("^" .. p .. "%s+(.+)$")
    if resto then return resto end
  end
  return titulo
end

local TEOREMAS = {
  definition = { "def", { "Definição" } },
  theorem = { "thm", { "Teorema" } },
  proposicao = { "prp", { "Proposição" } },
  corolario = { "cor", { "Corolário" } },
  lema = { "lem", { "Lema" } },
  axiom = { "def", { "Axioma" } },
  question = { "exr", { "Questão", "Exercício" } },
  problem = { "exr", { "Problema" } },
  example = { "exm", { "Exemplo" } },
}

local function vazio(bloco)
  if bloco.t ~= "Para" and bloco.t ~= "Plain" then return false end
  for _, x in ipairs(bloco.content) do
    if x.t == "Image" or x.t == "Math" or x.t == "Cite" then return false end
  end
  local s = pandoc.utils.stringify(bloco):gsub("[%s\194\160]", "")
  return s == ""
end

local function converter_div(div)
  for env, info in pairs(TEOREMAS) do
    if tem(div, env) then
      local titulo = extrair_titulo(div)
      local rotulo = extrair_rotulo(div)
      local attrs = {}
      local nome = limpar_nome(titulo, info[2])
      if nome and nome ~= "" then attrs.name = nome end
      local id = proximo(info[1])
      if rotulo then id = string.format("%s-a%s-%s", info[1], AULA, rotulo) end
      return pandoc.Div(div.content, pandoc.Attr(id, {}, attrs))
    end
  end
  if tem(div, "demonstration") or tem(div, "proof") then
    extrair_titulo(div)
    return pandoc.Div(div.content, pandoc.Attr("", { "proof" }))
  end
  if tem(div, "note") then
    extrair_titulo(div)
    return pandoc.Div(div.content, pandoc.Attr("", { "callout-note" }, { appearance = "simple", icon = "false" }))
  end
  if tem(div, "discussion") then
    extrair_titulo(div)
    return pandoc.Div(div.content, pandoc.Attr("", { "callout-note" }, { title = "Texto complementar" }))
  end
  if tem(div, "center") or tem(div, "minipage") or tem(div, "frame") then
    return div.content
  end
  if tem(div, "figuratikz") then
    local n = pandoc.utils.stringify(div):match("(%d+)")
    local caminho = string.format("figuras/aula-%s/fig-%02d.svg", AULA, tonumber(n))
    local img = pandoc.Image({}, caminho, "", pandoc.Attr("", { "tikz" }, { ["fig-alt"] = "DESCREVER: figura " .. n }))
    table.insert(avisos, "figura " .. n .. ": confira a imagem e escreva a descrição (texto alternativo)")
    return pandoc.Para({ img })
  end
  return nil
end

-- Caixas (tcolorbox): título "Exemplo ..." vira exemplo; caixa sem título continua a anterior.
local function converter_caixas(blocos)
  local saida = pandoc.List()
  local ultimo_exemplo, ultimo_titulo = nil, nil
  for _, b in ipairs(blocos) do
    if b.t == "Div" and tem(b, "caixa") then
      local titulo = extrair_titulo(b)
      local rotulo = extrair_rotulo(b)
      if titulo and ultimo_exemplo and titulo == ultimo_titulo then
        -- mesma caixa repetida logo em seguida (quebra de página no PDF): é continuação
        ultimo_exemplo.content:extend(b.content)
      elseif titulo and titulo:match("^Exemplo") then
        ultimo_titulo = titulo
        local id = proximo("exm")
        if rotulo then id = string.format("exm-a%s-%s", AULA, rotulo) end
        local ex = pandoc.Div(b.content, pandoc.Attr(id, {}))
        saida:insert(ex)
        ultimo_exemplo = ex
      elseif titulo then
        saida:insert(pandoc.Div(b.content, pandoc.Attr("", { "callout-note" }, { title = titulo })))
        ultimo_exemplo = nil
      elseif ultimo_exemplo then
        ultimo_exemplo.content:extend(b.content)
      else
        saida:insert(pandoc.Div(b.content, pandoc.Attr("", { "caixa" })))
      end
    else
      local ignoravel = vazio(b)
      if not ignoravel then
        saida:insert(b)
        ultimo_exemplo = nil
      end
    end
  end
  return saida
end

local function bruto(el)
  if el.format == "latex" or el.format == "tex" then
    local codigo = el.text
    table.insert(avisos, "comando não convertido: " .. codigo:sub(1, 80))
    if el.t == "RawInline" then
      return pandoc.Span({ pandoc.Code(codigo) }, pandoc.Attr("", { "nao-convertido" }))
    else
      return pandoc.Div({ pandoc.Para({ pandoc.Code(codigo) }) }, pandoc.Attr("", { "nao-convertido" }))
    end
  end
end

return {
  {
    Meta = function(m)
      if m.aula then AULA = pandoc.utils.stringify(m.aula) end
    end,
  },
  { RawInline = bruto, RawBlock = bruto },
  {
    Str = function(el)
      local antes, id, depois = el.text:match("^(.-)REFX⟦(.-)⟧(.*)$")
      if not id then return nil end
      local saida = pandoc.List()
      if antes ~= "" then saida:insert(pandoc.Str(antes)) end
      saida:insert(pandoc.Cite({ pandoc.Str("@" .. id) }, { pandoc.Citation(id, "AuthorInText") }))
      if depois ~= "" then saida:insert(pandoc.Str(depois)) end
      return saida
    end,
  },
  {
    Header = function(h)
      h.level = h.level + 1
      return h
    end,
  },
  { Blocks = converter_caixas },
  { Div = converter_div },
  {
    -- Listas compactas (como no PDF): itens de um parágrafo só viram Plain.
    BulletList = function(l)
      for _, item in ipairs(l.content) do
        if #item == 1 and item[1].t == "Para" then item[1] = pandoc.Plain(item[1].content) end
      end
      return l
    end,
    OrderedList = function(l)
      for _, item in ipairs(l.content) do
        if #item == 1 and item[1].t == "Para" then item[1] = pandoc.Plain(item[1].content) end
      end
      return l
    end,
  },
  {
    Blocks = function(blocos)
      local saida = pandoc.List()
      for _, b in ipairs(blocos) do
        if not vazio(b) then saida:insert(b) end
      end
      return saida
    end,
    Pandoc = function(doc)
      for _, a in ipairs(avisos) do io.stderr:write("AVISO ", a, "\n") end
      return doc
    end,
  },
}
