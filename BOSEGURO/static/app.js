// =====================================================
// ANIMAÇÃO DE REVELAR (tela do boletim legível)
// O texto aparece embaralhado e vai se revelando da esquerda para a direita.
// É só um efeito visual: a descriptografia de verdade acontece no app.py.
// =====================================================

// Se a pessoa pediu "reduzir movimento" no sistema, não faz animação
if (!window.matchMedia("(prefers-reduced-motion: reduce)").matches) {

    var simbolos = "▓▒░#@$%&*+=?";

    // pega todos os textos que têm a classe "decode"
    var textos = document.querySelectorAll(".decode");

    for (var n = 0; n < textos.length; n++) {
        animar(textos[n]);
    }
}

function animar(elemento) {
    var textoFinal = elemento.textContent;   // o texto verdadeiro
    var quadro = 0;                          // quantas vezes a animação já atualizou
    var totalDeQuadros = 24;

    // setInterval repete a função a cada 35 milissegundos
    var timer = setInterval(function () {
        quadro = quadro + 1;

        // quantas letras já podem aparecer certas
        var reveladas = Math.floor(textoFinal.length * quadro / totalDeQuadros);

        var textoNaTela = "";
        for (var i = 0; i < textoFinal.length; i++) {
            var letra = textoFinal[i];
            if (i < reveladas || letra === " " || letra === "\n") {
                textoNaTela = textoNaTela + letra;                  // letra certa
            } else {
                var sorteio = Math.floor(Math.random() * simbolos.length);
                textoNaTela = textoNaTela + simbolos[sorteio];      // símbolo aleatório
            }
        }
        elemento.textContent = textoNaTela;

        // terminou: mostra o texto verdadeiro e para o timer
        if (quadro >= totalDeQuadros) {
            clearInterval(timer);
            elemento.textContent = textoFinal;
        }
    }, 35);
}
