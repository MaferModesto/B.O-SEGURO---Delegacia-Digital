// =====================================================
// ANIMAÇÃO DE CRIPTOGRAFIA (tela de confirmação do cadastro)
// O texto digitado se embaralha e vira o texto criptografado que foi salvo.
//
// IMPORTANTE: a criptografia de verdade já aconteceu no app.py, antes da página abrir.
// Aqui só mostramos isso na tela. Sem JavaScript, a página já mostra o resultado final.
// =====================================================

// Se a pessoa pediu "reduzir movimento" no sistema, não faz animação
if (!window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    iniciar();
}

function iniciar() {
    var campos = document.querySelectorAll(".valor[data-plano]");   // os 10 campos da ficha
    if (campos.length === 0) {
        return;
    }

    var simbolos = "▓▒░#@$%&*+=?";

    // elementos da tela que vamos mexer
    var carimbo = document.getElementById("carimbo");
    var processo = document.getElementById("processo");
    var textoProcesso = document.getElementById("processoTexto");
    var barra = document.getElementById("barraFill");
    var botoes = document.getElementById("acoesFinais");

    // 1) Guarda o texto criptografado de cada campo e coloca o texto digitado no lugar
    var cifras = [];
    for (var i = 0; i < campos.length; i++) {
        cifras[i] = campos[i].textContent;                              // texto criptografado (final)
        campos[i].textContent = campos[i].getAttribute("data-plano");   // texto digitado (começo)
        campos[i].classList.remove("cifrado");
    }

    // 2) Mostra a barra de progresso, esconde os botões e muda o carimbo
    processo.hidden = false;
    botoes.classList.add("oculto");
    carimbo.classList.add("processando");
    carimbo.innerHTML = "CRIPTOGRAFANDO<small>aguarde</small>";

    // 3) Começa a animar um campo de cada vez
    var prontos = 0;    // quantos campos já terminaram
    for (var j = 0; j < campos.length; j++) {
        comecarCampo(campos[j], cifras[j], j);
    }

    // espera um pouco (para dar tempo de ler) e começa a animar este campo
    function comecarCampo(campo, cifra, posicao) {
        setTimeout(function () {
            criptografarCampo(campo, cifra);
        }, 1200 + posicao * 250);
    }

    function criptografarCampo(campo, cifra) {
        var plano = campo.textContent;
        var quadro = 0;
        var fase1 = 10;    // até o quadro 10: o texto original vai se embaralhando
        var fase2 = 26;    // até o quadro 26: os símbolos viram o texto criptografado

        var timer = setInterval(function () {
            quadro = quadro + 1;
            var textoNaTela = "";

            if (quadro <= fase1) {
                // FASE 1: cada vez mais letras viram símbolos
                var chance = quadro / fase1;
                for (var a = 0; a < plano.length; a++) {
                    var letra = plano[a];
                    if (letra === " " || letra === "\n" || Math.random() > chance) {
                        textoNaTela = textoNaTela + letra;
                    } else {
                        textoNaTela = textoNaTela + sortearSimbolo();
                    }
                }
            } else {
                // FASE 2: da esquerda para a direita, aparecem as letras do texto criptografado
                campo.classList.add("cifrado");
                var reveladas = Math.floor(cifra.length * (quadro - fase1) / (fase2 - fase1));
                for (var b = 0; b < cifra.length; b++) {
                    if (b < reveladas) {
                        textoNaTela = textoNaTela + cifra[b];
                    } else {
                        textoNaTela = textoNaTela + sortearSimbolo();
                    }
                }
            }

            campo.textContent = textoNaTela;

            // terminou este campo
            if (quadro >= fase2) {
                clearInterval(timer);
                campo.textContent = cifra;
                campoTerminou();
            }
        }, 40);
    }

    function sortearSimbolo() {
        return simbolos[Math.floor(Math.random() * simbolos.length)];
    }

    // chamado toda vez que um campo termina: atualiza a barra e, no último, finaliza
    function campoTerminou() {
        prontos = prontos + 1;
        barra.style.width = Math.round(prontos / campos.length * 100) + "%";
        textoProcesso.textContent = "Criptografando... " + prontos + " de " + campos.length + " campos";

        if (prontos === campos.length) {
            textoProcesso.textContent = "Pronto: boletim criptografado e salvo.";
            carimbo.classList.remove("processando");
            carimbo.innerHTML = "CRIPTOGRAFADO<small>boletim protegido</small>";
            botoes.classList.remove("oculto");
        }
    }
}
