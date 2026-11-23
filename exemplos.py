"""exemplos.py - Carrega dados de demonstração (útil para o vídeo e testes)."""

import dados
import utilidades as u
import contas
import transacoes


def carregar_exemplos():
    if dados.CLIENTES or dados.CONTAS:
        print("\nJá existem dados cadastrados. Os exemplos só carregam com o sistema vazio.")
        return
    pessoas = [
        ("Maria Souza", "529.982.247-25", "15/03/1990", "(83) 98888-1111", "maria@email.com"),
        ("João Pereira", "111.444.777-35", "02/11/1985", "(83) 97777-2222", ""),
        ("Ana Lima", "390.533.447-05", "21/07/2000", "(83) 3222-3333", "ana@email.com"),
    ]
    for nome, cpf, nascimento, telefone, email in pessoas:
        dados.CLIENTES.append({"id": u.proximo_id("cliente"), "nome": nome, "cpf": cpf,
                               "nascimento": nascimento, "telefone": telefone, "email": email})
    for cliente_id, tipo in [(1, "Corrente"), (1, "Poupança"), (2, "Corrente"), (3, "Corrente")]:
        dados.CONTAS.append({"id": u.proximo_id("conta"), "cliente_id": cliente_id,
                             "tipo": tipo, "saldo": 0.0,
                             "limite": contas.LIMITE_PADRAO if tipo == "Corrente" else 0.0,
                             "abertura": u.hoje()})
    for conta_id, valor in [(1, 2500.00), (2, 1000.00), (3, 800.00), (4, 150.00)]:
        transacoes.registrar_transacao(dados.CONTAS[conta_id - 1], transacoes.TIPO_DEPOSITO, valor)
    transacoes.registrar_transacao(dados.CONTAS[0], transacoes.TIPO_SAQUE, 300.00)
    print("\nDados de exemplo carregados: 3 clientes, 4 contas e movimentações.")
