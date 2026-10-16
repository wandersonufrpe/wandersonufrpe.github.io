// Conferência automática dos blocos ::: quiz (ver filtros/componentes.lua).
(function () {
  function iniciar() {
    document.querySelectorAll(".quiz").forEach(function (quiz) {
      if (quiz.dataset.pronto) return;
      quiz.dataset.pronto = "sim";

      var retorno = document.createElement("p");
      retorno.className = "quiz-retorno";
      retorno.setAttribute("aria-live", "polite");
      var explicacao = quiz.querySelector(".quiz-explicacao");
      if (explicacao) quiz.insertBefore(retorno, explicacao);
      else quiz.appendChild(retorno);

      quiz.querySelectorAll(".quiz-opcao").forEach(function (opcao) {
        opcao.setAttribute("role", "button");
        opcao.setAttribute("tabindex", "0");

        function escolher() {
          if (quiz.classList.contains("acertou")) return;
          if (opcao.dataset.correta === "sim") {
            opcao.classList.add("correta");
            quiz.classList.add("acertou");
            retorno.textContent = "Isso mesmo.";
            quiz.querySelectorAll(".quiz-opcao").forEach(function (o) {
              o.setAttribute("aria-disabled", "true");
            });
          } else {
            opcao.classList.add("errada");
            opcao.setAttribute("aria-disabled", "true");
            retorno.textContent = "Ainda não. Tente outra opção.";
          }
        }

        opcao.addEventListener("click", escolher);
        opcao.addEventListener("keydown", function (ev) {
          if (ev.key === "Enter" || ev.key === " ") {
            ev.preventDefault();
            escolher();
          }
        });
      });
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", iniciar);
  } else {
    iniciar();
  }
})();
