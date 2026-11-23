"""transacoes.py - Depósito, saque, transferência e extrato."""

import dados
import utilidades as u
import contas

TIPO_DEPOSITO = "Depósito"
TIPO_SAQUE = "Saque"
TIPO_TRANSF_ENVIADA = "Transferência enviada"
TIPO_TRANSF_RECEBIDA = "Transferência recebida"


def registrar_transacao(conta, tipo, valor):
    """Atualiza o saldo da conta e guarda a movimentação no histórico."""
    if tipo in (TIPO_SAQUE, TIPO_TRANSF_ENVIADA):
        conta["saldo"] = round(conta["saldo"] - valor, 2)
    else:
        conta["saldo"] = round(conta["saldo"] + valor, 2)
    dados.TRANSACOES.append({
        "id": u.proximo_id("transacao"),
        "conta_id": conta["id"],
        "tipo": tipo,
        "valor": valor,
        "saldo_apos": conta["saldo"],
        "data": u.agora(),
    })


def saldo_disponivel(conta):
    """Saldo + limite de cheque especial."""
    return conta["saldo"] + conta["limite"]


def depositar():
    u.exibir_titulo("DEPÓSITO")
    conta = u.selecionar_por_id(dados.CONTAS, "Número da conta", "Conta")
    if conta is None:
        return
    valor = u.ler_campo("Valor do depósito", u.validar_valor)
    registrar_transacao(conta, TIPO_DEPOSITO, valor)
    print(f"\nDepósito realizado! Novo saldo: {u.formatar_moeda(conta['saldo'])}")


def sacar():
    u.exibir_titulo("SAQUE")
    conta = u.selecionar_por_id(dados.CONTAS, "Número da conta", "Conta")
    if conta is None:
        return
    print(f"Disponível para saque: {u.formatar_moeda(saldo_disponivel(conta))}")
    valor = u.ler_campo("Valor do saque", u.validar_valor)
    if valor > saldo_disponivel(conta):
        print("\nSaldo insuficiente. Operação não realizada.")
        return
    registrar_transacao(conta, TIPO_SAQUE, valor)
    print(f"\nSaque realizado! Novo saldo: {u.formatar_moeda(conta['saldo'])}")


def transferir():
    u.exibir_titulo("TRANSFERÊNCIA")
    origem = u.selecionar_por_id(dados.CONTAS, "Conta de origem", "Conta")
    if origem is None:
        return
    destino = u.selecionar_por_id(dados.CONTAS, "Conta de destino", "Conta")
    if destino is None:
        return
    if origem["id"] == destino["id"]:
        print("\nA conta de origem e a de destino devem ser diferentes.")
        return
    print(f"Disponível para transferir: {u.formatar_moeda(saldo_disponivel(origem))}")
    valor = u.ler_campo("Valor da transferência", u.validar_valor)
    if valor > saldo_disponivel(origem):
        print("\nSaldo insuficiente. Operação não realizada.")
        return
    registrar_transacao(origem, TIPO_TRANSF_ENVIADA, valor)
    registrar_transacao(destino, TIPO_TRANSF_RECEBIDA, valor)
    print(f"\nTransferência realizada! Saldo da origem: {u.formatar_moeda(origem['saldo'])}")


def extrato():
    u.exibir_titulo("EXTRATO")
    conta = u.selecionar_por_id(dados.CONTAS, "Número da conta", "Conta")
    if conta is None:
        return
    contas.exibir_conta(conta)
    movimentos = [t for t in dados.TRANSACOES if t["conta_id"] == conta["id"]]
    if not movimentos:
        print("\nNenhuma movimentação nesta conta.")
        return
    print(f"\n{'Data':<18}{'Tipo':<24}{'Valor':>14}{'Saldo':>16}")
    print("-" * 72)
    for t in movimentos:
        print(f"{t['data']:<18}{t['tipo']:<24}{u.formatar_moeda(t['valor']):>14}"
              f"{u.formatar_moeda(t['saldo_apos']):>16}")


def menu_transacoes():
    u.executar_menu("OPERAÇÕES BANCÁRIAS", [
        ("Depósito", depositar),
        ("Saque", sacar),
        ("Transferência", transferir),
        ("Extrato", extrato),
    ])
