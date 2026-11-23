"""relatorios.py - Relatórios gerenciais do banco."""

import dados
import utilidades as u
import contas
import transacoes


def relatorio_saldos():
    u.exibir_titulo("RELATÓRIO DE SALDOS")
    if not dados.CONTAS:
        print("Nenhuma conta aberta.")
        return
    for tipo in contas.TIPOS_CONTA:
        do_tipo = [c for c in dados.CONTAS if c["tipo"] == tipo]
        total = sum(c["saldo"] for c in do_tipo)
        print(f"Contas {tipo:<9}: {len(do_tipo):>3}  |  Saldo: {u.formatar_moeda(total)}")
    print("-" * u.LARGURA)
    print(f"Total de clientes : {len(dados.CLIENTES)}")
    print(f"Total de contas   : {len(dados.CONTAS)}")
    print(f"Saldo total       : {u.formatar_moeda(sum(c['saldo'] for c in dados.CONTAS))}")
    negativas = [c for c in dados.CONTAS if c["saldo"] < 0]
    print(f"Contas no negativo: {len(negativas)}")


def ranking_clientes():
    u.exibir_titulo("RANKING DE CLIENTES POR SALDO")
    if not dados.CLIENTES:
        print("Nenhum cliente cadastrado.")
        return
    totais = []
    for cliente in dados.CLIENTES:
        total = sum(c["saldo"] for c in dados.CONTAS if c["cliente_id"] == cliente["id"])
        totais.append((total, cliente["nome"]))
    totais.sort(reverse=True)
    for posicao, (total, nome) in enumerate(totais, start=1):
        print(f"{posicao:>2}. {u.cortar(nome, 28):<30}{u.formatar_moeda(total):>16}")


def relatorio_movimentacoes():
    u.exibir_titulo("RELATÓRIO DE MOVIMENTAÇÕES")
    if not dados.TRANSACOES:
        print("Nenhuma movimentação registrada.")
        return
    tipos = [transacoes.TIPO_DEPOSITO, transacoes.TIPO_SAQUE,
             transacoes.TIPO_TRANSF_ENVIADA]
    for tipo in tipos:
        do_tipo = [t for t in dados.TRANSACOES if t["tipo"] == tipo]
        total = sum(t["valor"] for t in do_tipo)
        print(f"{tipo:<24}: {len(do_tipo):>3} operação(ões)  |  {u.formatar_moeda(total)}")


def menu_relatorios():
    u.executar_menu("RELATÓRIOS", [
        ("Saldos do banco", relatorio_saldos),
        ("Ranking de clientes por saldo", ranking_clientes),
        ("Movimentações por tipo", relatorio_movimentacoes),
    ])
