
import json
import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, session, flash

app = Flask(__name__)
app.secret_key = "chave-secreta-do-flask"    # o Flask usa para proteger o login (session)

PASTA = os.path.dirname(os.path.abspath(__file__))   # pasta onde está este arquivo
ARQUIVO = os.path.join(PASTA, "boletins.json")       # onde os boletins são guardados

CHAVE = "DELEGACIA"    # chave de segurança do sistema (usada para criptografar)

# Usuários do sistema (login, senha, perfil e nome para mostrar na tela)
USUARIOS = {
    "vitima":   {"senha": "1234", "perfil": "vitima",    "nome": "Vítima"},
    "atendente": {"senha": "1234", "perfil": "atendente", "nome": "Atendente / Escrivão"},
    "delegado":  {"senha": "abcd", "perfil": "delegado",  "nome": "Delegado / Policial"},
}

# Campos do boletim: nome interno -> texto que aparece na tela
ROTULOS = {
    "nome": "Nome",
    "cpf": "CPF",
    "telefone": "Telefone",
    "endereco": "Endereço",
    "tipo": "Tipo de ocorrência",
    "data_hora": "Data e hora",
    "local": "Local da ocorrência",
    "descricao": "Descrição",
    "pessoas": "Pessoas envolvidas",
    "objetos": "Objetos envolvidos",
}
CAMPOS = list(ROTULOS.keys())    # só os nomes internos: ["nome", "cpf", ...]

NOMES_PERFIL = {"vitima": "Vítima", "atendente": "Atendente", "delegado": "Delegado"}


# O Flask chama esta função e deixa as variáveis disponíveis em TODOS os arquivos HTML
@app.context_processor
def variaveis_para_os_html():
    return {"ROTULOS": ROTULOS, "NOMES_PERFIL": NOMES_PERFIL}

# Função para mostrar o número identificador do boletim
@app.template_filter("numero_bo")
def numero_bo(boletim):
    return f"{boletim['id']:03d}"


# CRIPTOGRAFIA (Transposição Colunar)

def ordem_das_colunas(chave):
    # Devolve a ordem alfabética das letras da chave.
    # Exemplo: "BCA" -> [2, 0, 1]  (A é a 3ª letra, B é a 1ª, C é a 2ª)
    return sorted(range(len(chave)), key=lambda i: chave[i])


def criptografar(texto, chave):
    tamanho_original = len(texto)
    n = len(chave)

    # completa o texto com "#" até caber certinho na tabela
    while len(texto) % n != 0:
        texto = texto + "#"

    # lê a tabela coluna por coluna, na ordem da chave
    resultado = ""
    for coluna in ordem_das_colunas(chave):
        for posicao in range(coluna, len(texto), n):
            resultado = resultado + texto[posicao]

    # guarda o tamanho original no começo, para saber quantos "#" cortar depois
    return str(tamanho_original) + "|" + resultado


def descriptografar(texto_cifrado, chave):
    tamanho, cifrado = texto_cifrado.split("|", 1)
    n = len(chave)

    # faz o caminho inverso: devolve cada letra para a posição de origem
    texto = [""] * len(cifrado)
    i = 0
    for coluna in ordem_das_colunas(chave):
        for posicao in range(coluna, len(cifrado), n):
            texto[posicao] = cifrado[i]
            i = i + 1

    texto_completo = "".join(texto)
    return texto_completo[:int(tamanho)]    # corta os "#" do final

# PARTE 2: FUNÇÕES AUXILIARES


def ler_boletins():
    # Lê o arquivo boletins.json e devolve a lista de boletins
    if not os.path.exists(ARQUIVO):
        return []
    with open(ARQUIVO, "r", encoding="utf-8") as f:
        return json.load(f)


def salvar_boletins(lista):
    # Grava a lista de boletins no arquivo boletins.json
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(lista, f, ensure_ascii=False, indent=2)


def agora():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")


def achar_boletim(lista, numero):
    # Procura o boletim pelo número. Se não achar, devolve None.
    for boletim in lista:
        if boletim["id"] == numero:
            return boletim
    return None


def proximo_numero(lista):
    # O número do boletim nunca se repete: é o maior número que existe + 1
    maior = 0
    for boletim in lista:
        if boletim["id"] > maior:
            maior = boletim["id"]
    return maior + 1


def ler_formulario():
    # Pega do formulário o que foi digitado em cada campo
    digitado = {}
    for campo in CAMPOS:
        digitado[campo] = request.form[campo].strip()
    return digitado


def criptografar_dados(digitado):
    # Criptografa cada campo e devolve um dicionário só com os textos cifrados
    cifrado = {}
    for campo in CAMPOS:
        cifrado[campo] = criptografar(digitado[campo], CHAVE)
    return cifrado


def descriptografar_dados(boletim):
    # Descriptografa cada campo. O resultado fica só na memória, nunca é salvo.
    legivel = {}
    for campo in CAMPOS:
        legivel[campo] = descriptografar(boletim["dados"][campo], CHAVE)
    return legivel


# PARTE 3: REGRAS DE PERMISSÃO (quem pode fazer o quê)

def pode_abrir(boletim):
    # Delegado abre qualquer boletim.
    # Vítima e atendente só abrem os que elas mesmas registraram.
    if session["perfil"] == "delegado":
        return True
    return boletim["autor"] == session["usuario"]


def pode_ler(boletim):
    # Delegado lê qualquer boletim.
    # Vítima lê só o dela.
    # Atendente nunca lê: vê só o texto criptografado.
    if session["perfil"] == "delegado":
        return True
    if session["perfil"] == "vitima":
        return boletim["autor"] == session["usuario"]
    return False


def pode_editar(boletim):
    # Só a vítima edita, e só o boletim que ela mesma escreveu.
    # O atendente não edita depois de registrar, e o delegado só consulta.
    return session["perfil"] == "vitima" and boletim["autor"] == session["usuario"]

# PARTE 4: PÁGINAS DO SITE

@app.route("/")
def inicio():
    if "usuario" in session:
        return redirect("/lista")
    return redirect("/login")


@app.route("/login", methods=["GET", "POST"])
def login():
    erro = None
    if request.method == "POST":
        usuario = request.form["usuario"].strip()
        senha = request.form["senha"]
        if usuario in USUARIOS and USUARIOS[usuario]["senha"] == senha:
            session["usuario"] = usuario
            session["perfil"] = USUARIOS[usuario]["perfil"]
            session["nome"] = USUARIOS[usuario]["nome"]
            return redirect("/lista")
        erro = "Usuário ou senha incorretos."
    return render_template("login.html", erro=erro)


@app.route("/sair")
def sair():
    session.clear()
    return redirect("/login")


@app.route("/lista")
def lista():
    if "usuario" not in session:
        return redirect("/login")

    todos = ler_boletins()

    if session["perfil"] == "delegado":
        boletins = todos          # delegado vê todos
    else:
        # vítima e atendente veem só os que elas registraram
        boletins = []
        for b in todos:
            if b["autor"] == session["usuario"]:
                boletins.append(b)

    boletins.reverse()            # o mais novo aparece primeiro
    return render_template("lista.html", boletins=boletins)


@app.route("/solicitar")
def solicitar():
    # Pedir um B.O. pelo número. Aceita "7".
    if "usuario" not in session:
        return redirect("/login")

    texto = request.args.get("numero", "").split("/")[0].strip()
    if not texto.isdigit():
        flash("Digite o número do boletim", "erro")
        return redirect("/lista")
    return redirect("/boletim/" + str(int(texto)))


@app.route("/cadastrar", methods=["GET", "POST"])
def cadastrar():
    if "usuario" not in session:
        return redirect("/login")

    if session["perfil"] == "delegado":
        flash("O perfil Delegado consulta boletins, mas não registra.", "erro")
        return redirect("/lista")

    if request.method == "POST":
        digitado = ler_formulario()       # o que a pessoa digitou (texto normal)
        boletins = ler_boletins()

        novo = {
            "id": proximo_numero(boletins),
            "ano": datetime.now().year,
            "autor": session["usuario"],
            "criado_em": agora(),
            "dados": criptografar_dados(digitado),    # só o texto criptografado é salvo
        }
        boletins.append(novo)
        salvar_boletins(boletins)

        # A tela de confirmação mostra a animação: o texto digitado (planos)
        # se transforma no texto criptografado que foi salvo (dados).
        return render_template("confirmacao.html", dados=novo["dados"], planos=digitado,
                               classe="cifrado", b=novo)

    return render_template("form.html", modo="novo", dados={}, b=None)


@app.route("/boletim/<int:numero>")
def ver_boletim(numero):
    if "usuario" not in session:
        return redirect("/login")

    b = achar_boletim(ler_boletins(), numero)

    # Mesma mensagem para "não existe" e "sem permissão" (não revela quais números existem)
    if b is None or not pode_abrir(b):
        flash("Boletim não encontrado ou sem permissão de acesso.", "erro")
        return redirect("/lista")

    if pode_ler(b):
        dados = descriptografar_dados(b)    # descriptografa só para mostrar nesta tela
        legivel = True
    else:
        dados = b["dados"]                  # continua criptografado
        legivel = False

    return render_template("ver.html", dados=dados, b=b, legivel=legivel,
                           pode_editar=pode_editar(b))


@app.route("/boletim/<int:numero>/editar", methods=["GET", "POST"])
def editar(numero):
    if "usuario" not in session:
        return redirect("/login")

    boletins = ler_boletins()
    b = achar_boletim(boletins, numero)

    if b is None or not pode_editar(b):
        flash("Este boletim não pode ser editado. Apenas a vítima corrige o boletim que ela mesma registrou.", "erro")
        return redirect("/lista")

    if request.method == "POST":
        novos = ler_formulario()
        b["dados"] = criptografar_dados(novos)    # criptografa de novo com os dados corrigidos
        b["editado_em"] = agora()
        salvar_boletins(boletins)
        flash("Boletim atualizado e criptografado novamente.", "ok")
        return redirect("/boletim/" + str(numero))

    # O formulário abre com os dados da vítima (descriptografados só na memória)
    return render_template("form.html", modo="editar", dados=descriptografar_dados(b), b=b)


if __name__ == "__main__":
    app.run(debug=True)
