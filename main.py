"""
main.py - Ponto de entrada do sistema Banco Cometa.

Execute com:  python main.py
"""

import utilidades as u
import clientes
import contas
import transacoes
import relatorios
import exemplos

NOME_BANCO = "BANCO COMETA"


def main():
    try:
        u.executar_menu(
            NOME_BANCO,
            [
                ("Gerenciar Clientes", clientes.menu_clientes),
                ("Gerenciar Contas", contas.menu_contas),
                ("Operações Bancárias", transacoes.menu_transacoes),
                ("Relatórios", relatorios.menu_relatorios),
                ("Carregar dados de exemplo", exemplos.carregar_exemplos),
            ],
            subtitulo="Sistema de Gerenciamento",
            texto_voltar="Sair do Sistema",
            pausar_apos=False,
        )
    except (KeyboardInterrupt, EOFError):
        print("\n\nEntrada interrompida.")
    print("\nSistema encerrado. Os dados em memória foram descartados.")


if __name__ == "__main__":
    main()
