"""clientes.py - CRUD de clientes do banco."""

import dados
import utilidades as u


def buscar_por_cpf(cpf):
    for cliente in dados.CLIENTES:
        if cliente["cpf"] == cpf:
            return cliente
    return None


def _validar_cpf_unico(ignorar_id=None):
    """CPF válido e que ainda não pertence a outro cliente."""

    def validar(texto):
        ok, resultado = u.validar_cpf(texto)
        if not ok:
            return ok, resultado
        existente = buscar_por_cpf(resultado)
        if existente and existente["id"] != ignorar_id:
            return False, f"CPF já cadastrado para {existente['nome']}."
        return True, resultado

    return validar


def exibir_cliente(cliente):
    print(f"\nID: {cliente['id']}  |  {cliente['nome']}")
    print(f"  CPF: {cliente['cpf']}  |  Nascimento: {cliente['nascimento']}")
    print(f"  Telefone: {cliente['telefone']}  |  E-mail: {cliente['email'] or '-'}")
    quantidade = len(contas_do_cliente(cliente["id"]))
    print(f"  Contas abertas: {quantidade}")


def contas_do_cliente(cliente_id):
    return [conta for conta in dados.CONTAS if conta["cliente_id"] == cliente_id]


def _ler_dados(cliente=None):
    """Lê os campos do cliente. Na alteração, ENTER mantém o valor atual."""
    atual = cliente or {}
    return {
        "nome": u.ler_campo("Nome completo", u.validar_nome, atual.get("nome")),
        "cpf": u.ler_campo("CPF", _validar_cpf_unico(atual.get("id")), atual.get("cpf")),
        "nascimento": u.ler_campo("Data de nascimento (dd/mm/aaaa)",
                                  u.validar_nascimento, atual.get("nascimento")),
        "telefone": u.ler_campo("Telefone com DDD", u.validar_telefone, atual.get("telefone")),
        "email": u.ler_campo("E-mail (opcional)", u.validar_email, atual.get("email", "")),
    }


def cadastrar_cliente():
    u.exibir_titulo("CADASTRAR CLIENTE")
    cliente = _ler_dados()
    cliente["id"] = u.proximo_id("cliente")
    dados.CLIENTES.append(cliente)
    print(f"\nCliente cadastrado com sucesso! ID: {cliente['id']}")


def listar_clientes():
    if not dados.CLIENTES:
        print("\nNenhum cliente cadastrado.")
        return
    print(f"\n{'ID':<5}{'Nome':<28}{'CPF':<16}{'Telefone':<16}")
    print("-" * 65)
    for c in dados.CLIENTES:
        print(f"{c['id']:<5}{u.cortar(c['nome'], 26):<28}{c['cpf']:<16}{c['telefone']:<16}")


def consultar_cliente():
    u.exibir_titulo("CONSULTAR CLIENTE")
    termo = input("Digite o ID, o CPF ou parte do nome: ").strip()
    if termo == "":
        print("Nenhum termo informado.")
        return
    if termo.isdigit() and len(termo) < 6:
        encontrados = [c for c in dados.CLIENTES if c["id"] == int(termo)]
    elif u.somente_digitos(termo) and len(u.somente_digitos(termo)) == 11:
        encontrados = [c for c in dados.CLIENTES if c["cpf"] == u.validar_cpf(termo)[1]]
    else:
        encontrados = [c for c in dados.CLIENTES if termo.lower() in c["nome"].lower()]
    if not encontrados:
        print("Nenhum cliente encontrado.")
    for cliente in encontrados:
        exibir_cliente(cliente)


def alterar_cliente():
    u.exibir_titulo("ALTERAR CLIENTE")
    listar_clientes()
    cliente = u.selecionar_por_id(dados.CLIENTES, "\nID do cliente", "Cliente")
    if cliente is None:
        return
    print("Pressione ENTER para manter o valor atual.")
    cliente.update(_ler_dados(cliente))
    print("\nCliente alterado com sucesso!")


def excluir_cliente():
    u.exibir_titulo("EXCLUIR CLIENTE")
    listar_clientes()
    cliente = u.selecionar_por_id(dados.CLIENTES, "\nID do cliente", "Cliente")
    if cliente is None:
        return
    quantidade = len(contas_do_cliente(cliente["id"]))
    if quantidade > 0:
        print(f"\nNão é possível excluir: {cliente['nome']} possui {quantidade} conta(s) aberta(s).")
        print("Encerre as contas antes de excluir o cliente.")
        return
    if u.confirmar(f"Excluir o cliente {cliente['nome']}?"):
        dados.CLIENTES.remove(cliente)
        print("Cliente excluído com sucesso!")
    else:
        print("Exclusão cancelada.")


def menu_clientes():
    u.executar_menu("GERENCIAR CLIENTES", [
        ("Cadastrar cliente", cadastrar_cliente),
        ("Listar clientes", lambda: (u.exibir_titulo("CLIENTES"), listar_clientes())),
        ("Consultar cliente", consultar_cliente),
        ("Alterar cliente", alterar_cliente),
        ("Excluir cliente", excluir_cliente),
    ])
