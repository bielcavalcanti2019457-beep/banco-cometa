"""contas.py - CRUD de contas bancárias (o ID da conta é o número da conta)."""

import dados
import utilidades as u
import clientes

TIPOS_CONTA = ["Corrente", "Poupança"]
LIMITE_PADRAO = 500.00  # cheque especial da conta corrente


def exibir_conta(conta):
    cliente = u.buscar_por_id(dados.CLIENTES, conta["cliente_id"])
    print(f"\nConta {conta['id']:04d}  |  {conta['tipo']}  |  Titular: {cliente['nome']}")
    print(f"  Saldo: {u.formatar_moeda(conta['saldo'])}", end="")
    if conta["tipo"] == "Corrente":
        print(f"  |  Limite: {u.formatar_moeda(conta['limite'])}", end="")
    print(f"  |  Aberta em: {conta['abertura']}")


def listar_contas(contas=None):
    contas = dados.CONTAS if contas is None else contas
    if not contas:
        print("\nNenhuma conta encontrada.")
        return
    print(f"\n{'Conta':<8}{'Tipo':<11}{'Titular':<24}{'Saldo':>16}")
    print("-" * 59)
    for conta in contas:
        titular = u.buscar_por_id(dados.CLIENTES, conta["cliente_id"])["nome"]
        print(f"{conta['id']:04d}    {conta['tipo']:<11}{u.cortar(titular, 22):<24}"
              f"{u.formatar_moeda(conta['saldo']):>16}")


def abrir_conta():
    u.exibir_titulo("ABRIR CONTA")
    if not dados.CLIENTES:
        print("Cadastre um cliente antes de abrir uma conta.")
        return
    clientes.listar_clientes()
    cliente = u.selecionar_por_id(dados.CLIENTES, "\nID do titular", "Cliente")
    if cliente is None:
        return
    tipo = u.escolher_da_lista("Tipo de conta:", TIPOS_CONTA)
    # Regra de negócio: cada cliente pode ter só uma conta de cada tipo.
    for conta in clientes.contas_do_cliente(cliente["id"]):
        if conta["tipo"] == tipo:
            print(f"\n{cliente['nome']} já possui uma conta {tipo}.")
            return
    conta = {
        "id": u.proximo_id("conta"),
        "cliente_id": cliente["id"],
        "tipo": tipo,
        "saldo": 0.0,
        "limite": LIMITE_PADRAO if tipo == "Corrente" else 0.0,
        "abertura": u.hoje(),
    }
    dados.CONTAS.append(conta)
    print(f"\nConta aberta com sucesso! Número: {conta['id']:04d}")


def consultar_conta():
    u.exibir_titulo("CONSULTAR CONTA")
    opcao = u.escolher_da_lista("Consultar por:", ["Número da conta", "Cliente (ID)"])
    if opcao == "Número da conta":
        conta = u.selecionar_por_id(dados.CONTAS, "Número da conta", "Conta")
        if conta:
            exibir_conta(conta)
    else:
        cliente = u.selecionar_por_id(dados.CLIENTES, "ID do cliente", "Cliente")
        if cliente:
            contas = clientes.contas_do_cliente(cliente["id"])
            if not contas:
                print("Este cliente não possui contas.")
            for conta in contas:
                exibir_conta(conta)


def alterar_limite():
    u.exibir_titulo("ALTERAR LIMITE (CONTA CORRENTE)")
    conta = u.selecionar_por_id(dados.CONTAS, "Número da conta", "Conta")
    if conta is None:
        return
    if conta["tipo"] != "Corrente":
        print("Somente contas correntes possuem limite.")
        return
    exibir_conta(conta)
    conta["limite"] = u.ler_campo("Novo limite", u.validar_limite(conta["saldo"]),
                                  conta["limite"], u.formatar_moeda(conta["limite"]))
    print("\nLimite alterado com sucesso!")


def encerrar_conta():
    u.exibir_titulo("ENCERRAR CONTA")
    conta = u.selecionar_por_id(dados.CONTAS, "Número da conta", "Conta")
    if conta is None:
        return
    exibir_conta(conta)
    # Regra de negócio: só encerra conta com saldo exatamente zero.
    if conta["saldo"] != 0:
        print("\nNão é possível encerrar: o saldo da conta deve ser R$ 0,00.")
        return
    if u.confirmar("Encerrar esta conta?"):
        dados.CONTAS.remove(conta)
        print("Conta encerrada com sucesso!")
    else:
        print("Operação cancelada.")


def menu_contas():
    u.executar_menu("GERENCIAR CONTAS", [
        ("Abrir conta", abrir_conta),
        ("Listar contas", lambda: (u.exibir_titulo("CONTAS"), listar_contas())),
        ("Consultar conta", consultar_conta),
        ("Alterar limite", alterar_limite),
        ("Encerrar conta", encerrar_conta),
    ])
