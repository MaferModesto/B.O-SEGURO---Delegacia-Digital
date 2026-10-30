# =====================================================
# Cria boletins de exemplo (fictícios) para a apresentação.
#
# Como usar:   python popular.py
# ATENÇÃO: isso APAGA os boletins que já estão no boletins.json!
# =====================================================

from app import criptografar, CHAVE, CAMPOS, salvar_boletins

# Dados pessoais repetidos (cada vítima registra vários boletins)
ANA = {"nome": "Ana Beatriz Souza", "cpf": "111.222.333-44", "telefone": "(19) 99811-2201",
       "endereco": "Rua das Acácias, 120 - Taquaral, Campinas/SP"}
MARCOS = {"nome": "Marcos Vinícius Lima", "cpf": "555.666.777-88", "telefone": "(19) 99722-3310",
          "endereco": "Av. Brasil, 845 - Cambuí, Campinas/SP"}

# Cada boletim: (quem registrou, quando registrou, quando editou ou None, dados)
# A lista está em ordem de data, então o número do boletim (1, 2, 3...) segue essa ordem.
# dict(ANA, tipo=...) copia os dados da Ana e acrescenta os dados da ocorrência.
BOLETINS = [
    ("vitima1", "20/10/2026 19:12:05", None, dict(ANA,
        tipo="Furto de celular", data_hora="2026-10-20T18:40", local="Terminal Central de Ônibus, Campinas",
        descricao="Eu estava no ponto de ônibus quando percebi que o celular havia sumido da bolsa. O local estava lotado no horário de pico.",
        pessoas="Nenhuma identificada", objetos="Celular Samsung Galaxy A54 preto")),

    ("vitima2", "21/10/2026 08:20:11", None, dict(MARCOS,
        tipo="Furto de bicicleta", data_hora="2026-10-21T07:30", local="Bicicletário do campus da Unicamp, Barão Geraldo",
        descricao="Deixei a bicicleta presa com cadeado às 7h30. Ao voltar, às 12h, encontrei só o cadeado cortado no chão.",
        pessoas="Nenhuma identificada", objetos="Bicicleta Caloi aro 29 azul, cadeado de aço")),

    ("atendente", "22/10/2026 21:15:30", None, {
        "nome": "Juliana Prado Ferreira", "cpf": "222.333.444-55", "telefone": "(19) 99633-4412",
        "endereco": "Rua Dr. Quirino, 310 - Centro, Campinas/SP",
        "tipo": "Roubo", "data_hora": "2026-10-22T20:30", "local": "Praça Carlos Gomes, Campinas",
        "descricao": "A vítima foi abordada por dois homens que anunciaram o assalto e levaram a bolsa. Ela não ficou ferida e os homens fugiram a pé.",
        "pessoas": "Dois homens: um de camiseta preta e outro de boné vermelho",
        "objetos": "Bolsa de couro marrom, carteira, R$ 120 em dinheiro"}),

    ("vitima2", "23/10/2026 22:03:47", None, dict(MARCOS,
        tipo="Ameaça", data_hora="2026-10-23T21:10", local="Aplicativo de mensagens (ocorreu online)",
        descricao="Recebi várias mensagens ameaçadoras de um ex-colega de trabalho depois de uma discussão sobre uma demissão. Guardei todas as capturas de tela.",
        pessoas="Roberto Alves (ex-colega de trabalho)", objetos="Capturas de tela das mensagens, celular")),

    ("vitima1", "24/10/2026 13:02:41", None, dict(ANA,
        tipo="Perda de documentos", data_hora="2026-10-24T12:15", local="Shopping Iguatemi, Campinas",
        descricao="Perdi a carteira na praça de alimentação. Dentro estavam RG, CNH e dois cartões de crédito. Os cartões já foram bloqueados.",
        pessoas="Nenhuma", objetos="Carteira preta, RG, CNH, dois cartões de crédito")),

    ("atendente", "26/10/2026 08:40:20", None, {
        "nome": "Roberto Nascimento", "cpf": "333.444.555-66", "telefone": "(19) 99544-5523",
        "endereco": "Rua Culto à Ciência, 98 - Botafogo, Campinas/SP",
        "tipo": "Furto de veículo", "data_hora": "2026-10-25T23:00", "local": "Rua Regente Feijó, em frente ao nº 450",
        "descricao": "A moto foi estacionada às 23h e, às 7h da manhã seguinte, não estava mais no local. Não havia câmeras visíveis na rua.",
        "pessoas": "Nenhuma identificada", "objetos": "Moto Honda CG 160 vermelha, placa FGH2J45"}),

    ("vitima2", "26/10/2026 16:11:09", "26/10/2026 16:25:33", dict(MARCOS,
        tipo="Estelionato (golpe do Pix)", data_hora="2026-10-26T15:20", local="Internet, site de vendas falso",
        descricao="Comprei um notebook em um site e fiz um Pix de R$ 450,00 de entrada. Depois do pagamento, o vendedor sumiu e o site saiu do ar.",
        pessoas="Vendedor desconhecido (usava o nome Tech Express)", objetos="Comprovante do Pix, capturas de tela do anúncio")),

    ("vitima1", "27/10/2026 09:30:18", "27/10/2026 09:41:50", dict(ANA,
        tipo="Acidente de trânsito", data_hora="2026-10-27T08:05", local="Av. Norte-Sul com Rua Barão de Itapura, Campinas",
        descricao="Meu carro parou no semáforo e foi atingido na traseira por outro veículo. Ninguém se feriu, mas o para-choque ficou danificado.",
        pessoas="Carlos Menezes (motorista do outro veículo)", objetos="Honda Fit prata placa ABC1D23, Fiat Argo branco")),

    ("atendente", "27/10/2026 10:12:44", None, {
        "nome": "Patrícia Gomes Duarte", "cpf": "444.555.666-77", "telefone": "(19) 99455-6634",
        "endereco": "Av. Francisco Glicério, 1020 - Centro, Campinas/SP",
        "tipo": "Perturbação do sossego", "data_hora": "2026-10-27T01:30", "local": "Rua Ferreira Penteado, 77 (apartamento vizinho)",
        "descricao": "Festa com som muito alto até as 4h da manhã, mesmo depois de pedidos do síndico para baixar o volume. Não é a primeira vez.",
        "pessoas": "Morador do apartamento 52 (nome não informado)", "objetos": "Caixas de som"}),

    ("vitima2", "28/10/2026 07:30:55", None, dict(MARCOS,
        tipo="Dano ao patrimônio", data_hora="2026-10-28T06:50", local="Rua Barreto Leme, em frente ao nº 230",
        descricao="Ao sair para o trabalho, encontrei o vidro traseiro do carro quebrado. Nada foi levado de dentro do veículo.",
        pessoas="Nenhuma identificada", objetos="Vidro traseiro do VW Gol prata")),

    ("atendente", "28/10/2026 15:20:03", None, {
        "nome": "Eduardo Martins", "cpf": "666.777.888-99", "telefone": "(19) 99366-7745",
        "endereco": "Rua José Paulino, 515 - Centro, Campinas/SP",
        "tipo": "Extravio de bagagem", "data_hora": "2026-10-28T14:00", "local": "Rodoviária de Campinas, plataforma 7",
        "descricao": "O declarante deixou a mala ao lado do banco para comprar passagem e, quando voltou, ela não estava mais lá.",
        "pessoas": "Nenhuma identificada", "objetos": "Mala azul média com roupas e um notebook"}),

    ("vitima1", "28/10/2026 20:01:14", None, dict(ANA,
        tipo="Furto de objetos no veículo", data_hora="2026-10-28T19:00", local="Estacionamento do Parque Portugal (Lagoa do Taquaral)",
        descricao="Deixei o carro estacionado por uma hora. Ao voltar, o vidro da porta estava quebrado e a mochila no banco de trás havia sumido.",
        pessoas="Nenhuma identificada", objetos="Mochila preta com um tablet e fones de ouvido")),

    ("atendente", "29/10/2026 08:05:37", None, {
        "nome": "Luciana Teixeira Rocha", "cpf": "777.888.999-00", "telefone": "(19) 99277-8856",
        "endereco": "Rua Conceição, 205 - Sousas, Campinas/SP",
        "tipo": "Invasão de propriedade", "data_hora": "2026-10-29T05:40", "local": "Chácara no distrito de Sousas",
        "descricao": "A declarante viu pela câmera que duas pessoas pularam o muro e entraram no terreno. Elas saíram quando o alarme tocou.",
        "pessoas": "Duas pessoas não identificadas", "objetos": "Portão lateral danificado"}),
]

# Monta a lista final: criptografa cada campo e dá um número para cada boletim
lista = []
numero = 1
for autor, criado_em, editado_em, dados in BOLETINS:
    cifrado = {}
    for campo in CAMPOS:
        cifrado[campo] = criptografar(dados[campo], CHAVE)

    boletim = {
        "id": numero,
        "ano": 2026,
        "autor": autor,
        "criado_em": criado_em,
        "dados": cifrado,
    }
    if editado_em is not None:
        boletim["editado_em"] = editado_em

    lista.append(boletim)
    numero = numero + 1

salvar_boletins(lista)
print("Pronto:", len(lista), "boletins de exemplo criados.")
