// Campo de direções interativo para EDOs de primeira ordem  y' = f(t, y).
//
// Uso numa página .qmd (célula OJS):
//
//   ```{ojs}
//   //| echo: false
//   import { campoDirecoes } from "../../../assets/js/campo-direcoes.js"
//   viewof k = Inputs.range([-2, 2], { value: 0.5, step: 0.1, label: "k" })
//   campoDirecoes({ f: (t, y) => k * y, t: [-3, 3], y: [-3, 3], largura: width, chave: "aula02-k" })
//   ```
//
// Opções principais:
//   f            função (t, y) => y'
//   t, y         intervalos [mín, máx] da janela
//   largura      largura inicial em pixels (o gráfico se ajusta sozinho ao espaço disponível)
//   solucoes     pontos iniciais já desenhados: [[t0, y0], ...]
//   interativo   true: o leitor toca no campo e a solução pelo ponto aparece
//   chave        nome único; mantém as soluções desenhadas quando um controle deslizante muda
//   cores        lista de cores CSS para as curvas
//   rotulos      { t: "t", y: "y" }
//   descricao    texto para leitores de tela

const SVG = "http://www.w3.org/2000/svg";
const memoria = new Map();
const observadores = new Map();
let contador = 0;

function no(nome, atributos = {}, pai = null) {
  const e = document.createElementNS(SVG, nome);
  for (const [k, v] of Object.entries(atributos)) e.setAttribute(k, v);
  if (pai) pai.appendChild(e);
  return e;
}

function passoRK4(f, t, y, h) {
  const k1 = f(t, y);
  const k2 = f(t + h / 2, y + (h * k1) / 2);
  const k3 = f(t + h / 2, y + (h * k2) / 2);
  const k4 = f(t + h, y + h * k3);
  return y + (h * (k1 + 2 * k2 + 2 * k3 + k4)) / 6;
}

// Solução aproximada (Runge-Kutta 4) pelo ponto (t0, y0), para a frente e para trás.
export function integrar(f, t0, y0, { t: [tMin, tMax], y: [yMin, yMax], passos = 800 }) {
  const h = (tMax - tMin) / passos;
  const folga = yMax - yMin;
  const fora = (y) => y < yMin - folga || y > yMax + folga;

  const percorrer = (sentido) => {
    const pontos = [];
    let t = t0;
    let y = y0;
    const limite = sentido > 0 ? tMax : tMin;
    while (sentido > 0 ? t < limite : t > limite) {
      const passo = Math.min(h, Math.abs(limite - t));
      y = passoRK4(f, t, y, sentido * passo);
      t += sentido * passo;
      if (!Number.isFinite(y)) break;
      pontos.push([t, y]);
      if (fora(y)) break;
    }
    return pontos;
  };

  return percorrer(-1).reverse().concat([[t0, y0]], percorrer(1));
}

function passoBonito(amplitude, maxMarcas = 8) {
  const bruto = amplitude / maxMarcas;
  const potencia = Math.pow(10, Math.floor(Math.log10(bruto)));
  for (const m of [1, 2, 2.5, 5, 10]) {
    if (m * potencia >= bruto) return m * potencia;
  }
  return 10 * potencia;
}

function formatar(v) {
  const r = Math.round(v * 100) / 100;
  return String(r).replace(".", ",").replace("-", "−");
}

export function campoDirecoes(opcoes = {}) {
  const {
    f,
    t: [tMin, tMax] = [-4, 4],
    y: [yMin, yMax] = [-3, 3],
    solucoes = [],
    cores = ["var(--cor-solucao-1)", "var(--cor-solucao-2)", "var(--cor-solucao-3)", "var(--cor-solucao-4)"],
    interativo = true,
    rotulos = { t: "t", y: "y" },
    descricao = "Campo de direções de uma equação diferencial",
    chave = null,
    eixos = true,
  } = opcoes;

  if (typeof f !== "function") throw new Error("campoDirecoes: informe f(t, y).");

  const figura = document.createElement("figure");
  figura.className = "campo-direcoes";

  // Pontos tocados pelo leitor (sobrevivem a mudanças do controle deslizante quando há `chave`).
  const pontosLeitor = chave ? memoria.get(chave) ?? [] : [];
  if (chave) memoria.set(chave, pontosLeitor);

  let atual = null;

  // Desenha (ou redesenha) o gráfico na largura real disponível, para o texto não encolher no celular.
  function montar(largura) {
    const altura = opcoes.altura ?? Math.max(240, Math.round(largura * (largura < 520 ? 0.78 : 0.6)));
    const malha = opcoes.malha ?? Math.min(24, Math.max(11, Math.round(largura / 30)));
    const m = { esq: eixos ? 40 : 4, dir: 10, topo: 10, base: eixos ? 30 : 4 };
    const pw = largura - m.esq - m.dir;
    const ph = altura - m.topo - m.base;
    const sx = pw / (tMax - tMin);
    const sy = ph / (yMax - yMin);
    const X = (t) => m.esq + (t - tMin) * sx;
    const Y = (y) => m.topo + (yMax - y) * sy;
    const id = `campo-${++contador}`;

    const svg = no("svg", {
      viewBox: `0 0 ${largura} ${altura}`,
      width: largura,
      height: altura,
      role: "img",
      "aria-label": descricao,
      class: "campo-svg" + (interativo ? " interativo" : ""),
    });

    const defs = no("defs", {}, svg);
    const clip = no("clipPath", { id: `${id}-recorte` }, defs);
    no("rect", { x: m.esq, y: m.topo, width: pw, height: ph }, clip);
    no("rect", { x: m.esq, y: m.topo, width: pw, height: ph, class: "campo-fundo" }, svg);

    if (eixos) {
      const g = no("g", { class: "campo-eixos" }, svg);
      if (yMin < 0 && yMax > 0) no("line", { x1: m.esq, x2: m.esq + pw, y1: Y(0), y2: Y(0), class: "campo-eixo" }, g);
      if (tMin < 0 && tMax > 0) no("line", { x1: X(0), x2: X(0), y1: m.topo, y2: m.topo + ph, class: "campo-eixo" }, g);
      const passoT = passoBonito(tMax - tMin, Math.max(3, Math.floor(pw / 60)));
      for (let v = Math.ceil(tMin / passoT) * passoT; v <= tMax + 1e-9; v += passoT) {
        const txt = no("text", { x: X(v), y: altura - 10, class: "campo-marca", "text-anchor": "middle" }, g);
        txt.textContent = formatar(v);
      }
      const passoY = passoBonito(yMax - yMin, Math.max(3, Math.floor(ph / 40)));
      for (let v = Math.ceil(yMin / passoY) * passoY; v <= yMax + 1e-9; v += passoY) {
        const txt = no("text", { x: m.esq - 6, y: Y(v) + 4, class: "campo-marca", "text-anchor": "end" }, g);
        txt.textContent = formatar(v);
      }
      const rt = no("text", { x: m.esq + pw - 4, y: Y(yMin < 0 && yMax > 0 ? 0 : yMin) - 6, class: "campo-rotulo", "text-anchor": "end" }, g);
      rt.textContent = rotulos.t;
      const ry = no("text", { x: (tMin < 0 && tMax > 0 ? X(0) : m.esq) + 6, y: m.topo + 14, class: "campo-rotulo" }, g);
      ry.textContent = rotulos.y;
    }

    // Segmentos do campo.
    const nT = malha;
    const nY = Math.max(6, Math.round((malha * ph) / pw));
    const cw = pw / nT;
    const ch = ph / nY;
    const L = 0.38 * Math.min(cw, ch);
    let d = "";
    for (let i = 0; i < nT; i++) {
      for (let j = 0; j < nY; j++) {
        const px = m.esq + (i + 0.5) * cw;
        const py = m.topo + (j + 0.5) * ch;
        const inclinacao = f(tMin + (px - m.esq) / sx, yMax - (py - m.topo) / sy);
        if (!Number.isFinite(inclinacao)) continue;
        let dx = sx;
        let dy = -inclinacao * sy;
        const n = Math.hypot(dx, dy);
        dx = (dx / n) * L;
        dy = (dy / n) * L;
        d += `M${(px - dx).toFixed(1)},${(py - dy).toFixed(1)}L${(px + dx).toFixed(1)},${(py + dy).toFixed(1)}`;
      }
    }
    no("path", { d, class: "campo-setas" }, svg);

    // Curvas-solução.
    const gSol = no("g", { "clip-path": `url(#${id}-recorte)` }, svg);
    let n = 0;
    const desenhar = (t0, y0) => {
      const cor = cores[n++ % cores.length];
      const pts = integrar(f, t0, y0, { t: [tMin, tMax], y: [yMin, yMax] });
      const caminho = pts.map(([t, y], k) => `${k ? "L" : "M"}${X(t).toFixed(1)},${Y(y).toFixed(1)}`).join("");
      no("path", { d: caminho, class: "campo-solucao", style: `stroke:${cor}` }, gSol);
      no("circle", { cx: X(t0), cy: Y(y0), r: 4.5, class: "campo-ponto", style: `fill:${cor}` }, gSol);
    };
    const redesenhar = () => {
      gSol.replaceChildren();
      n = 0;
      solucoes.forEach(([t0, y0]) => desenhar(t0, y0));
      pontosLeitor.forEach(([t0, y0]) => desenhar(t0, y0));
    };
    redesenhar();

    if (interativo) {
      svg.addEventListener("click", (ev) => {
        const p = svg.createSVGPoint();
        p.x = ev.clientX;
        p.y = ev.clientY;
        const q = p.matrixTransform(svg.getScreenCTM().inverse());
        if (q.x < m.esq || q.x > m.esq + pw || q.y < m.topo || q.y > m.topo + ph) return;
        const t0 = tMin + (q.x - m.esq) / sx;
        const y0 = yMax - (q.y - m.topo) / sy;
        pontosLeitor.push([t0, y0]);
        desenhar(t0, y0);
      });
    }

    if (atual) figura.replaceChild(svg, atual.svg);
    else figura.prepend(svg);
    atual = { svg, largura, redesenhar };
  }

  montar(Math.round(opcoes.largura ?? 640));

  if (interativo) {
    const legenda = document.createElement("figcaption");
    const texto = document.createElement("span");
    texto.textContent = opcoes.legenda ?? "Toque no campo para desenhar a solução que passa pelo ponto.";
    const botao = document.createElement("button");
    botao.type = "button";
    botao.className = "campo-apagar";
    botao.textContent = "Apagar curvas";
    botao.addEventListener("click", () => {
      pontosLeitor.length = 0;
      atual.redesenhar();
    });
    legenda.append(texto, botao);
    figura.appendChild(legenda);
  } else if (opcoes.legenda) {
    const legenda = document.createElement("figcaption");
    legenda.textContent = opcoes.legenda;
    figura.appendChild(legenda);
  }

  // Acompanha a largura real (rotação do celular, colunas da página inicial etc.).
  if (typeof ResizeObserver !== "undefined") {
    if (chave && observadores.has(chave)) observadores.get(chave).disconnect();
    let quadro = 0;
    const observador = new ResizeObserver((entradas) => {
      const w = Math.round(entradas[0].contentRect.width);
      if (w > 120 && Math.abs(w - atual.largura) > 8) {
        cancelAnimationFrame(quadro);
        quadro = requestAnimationFrame(() => montar(w));
      }
    });
    observador.observe(figura);
    if (chave) observadores.set(chave, observador);
  }

  return figura;
}
