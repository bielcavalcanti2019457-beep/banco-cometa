"""
testes.py - Testes automáticos do Banco Cometa.

Execute com:  python testes.py
Os testes simulam o que o usuário digita (input) e conferem o resultado.
"""

import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

import clientes
import contas
import dados
import exemplos
import relatorios
import transacoes
import utilidades as u


def executar(funcao, *digitado):
    """Roda uma função simulando as entradas digitadas; devolve o texto impresso."""
    saida = io.StringIO()
    with patch("builtins.input", side_effect=list(digitado)), redirect_stdout(saida):
        funcao()
    return saida.getvalue()


class BaseTeste(unittest.TestCase):
    def setUp(self):
        dados.CLIENTES.clear()
        dados.CONTAS.clear()
        dados.TRANSACOES.clear()
        for chave in dados.CONTADORES:
            dados.CONTADORES[chave] = 0
        self.cadastrar_maria()

    def cadastrar_maria(self, cpf="529.982.247-25"):
        executar(clientes.cadastrar_cliente, "Maria Souza", cpf, "15/03/1990",
                 "83988881111", "maria@email.com")


class TestValidacoes(unittest.TestCase):
    def test_cpf(self):
        self.assertTrue(u.validar_cpf("52998224725")[0])
        self.assertFalse(u.validar_cpf("52998224724")[0])   # dígito errado
        self.assertFalse(u.validar_cpf("11111111111")[0])   # todos iguais
        self.assertFalse(u.validar_cpf("123")[0])           # curto

    def test_valor(self):
        self.assertEqual(u.validar_valor("1.500,50"), (True, 1500.50))
        self.assertEqual(u.validar_valor("150.5"), (True, 150.5))
        self.assertFalse(u.validar_valor("abc")[0])
        self.assertFalse(u.validar_valor("-10")[0])
        self.assertFalse(u.validar_valor("0")[0])

    def test_nascimento_menor_de_idade_e_futuro(self):
        self.assertFalse(u.validar_nascimento(u.hoje())[0])
        self.assertFalse(u.validar_nascimento("31/02/1990")[0])
        self.assertFalse(u.validar_nascimento("01/01/2999")[0])
        self.assertTrue(u.validar_nascimento("01/01/1990")[0])

    def test_telefone_e_email(self):
        self.assertEqual(u.validar_telefone("83988881111"), (True, "(83) 98888-1111"))
        self.assertFalse(u.validar_telefone("123")[0])
        self.assertTrue(u.validar_email("")[0])
        self.assertFalse(u.validar_email("sem-arroba")[0])
        self.assertFalse(u.validar_email("a@b")[0])

    def test_moeda(self):
        self.assertEqual(u.formatar_moeda(1234.5), "R$ 1.234,50")


class TestClientes(BaseTeste):
    def test_cadastro(self):
        self.assertEqual(len(dados.CLIENTES), 1)
        self.assertEqual(dados.CLIENTES[0]["telefone"], "(83) 98888-1111")

    def test_entradas_invalidas_sao_repetidas(self):
        saida = executar(clientes.cadastrar_cliente,
                         "Jo", "João Pereira",               # nome curto, depois válido
                         "123", "11144477735",               # CPF inválido, depois válido
                         "10/10/2020", "02/11/1985",         # menor de idade, depois válido
                         "999", "83977772222", "", )         # telefone inválido, depois válido
        self.assertEqual(saida.count("Erro:"), 4)  # nome, CPF, nascimento e telefone
        self.assertEqual(len(dados.CLIENTES), 2)

    def test_cpf_duplicado_bloqueado(self):
        saida = executar(clientes.cadastrar_cliente, "Outra Pessoa", "529.982.247-25",
                         "39053344705", "01/01/1990", "83999990000", "")
        self.assertIn("já cadastrado", saida)
        self.assertEqual(len(dados.CLIENTES), 2)

    def test_consultar(self):
        self.assertIn("Maria Souza", executar(clientes.consultar_cliente, "mar"))
        self.assertIn("Maria Souza", executar(clientes.consultar_cliente, "1"))
        self.assertIn("Maria Souza", executar(clientes.consultar_cliente, "52998224725"))
        self.assertIn("Nenhum cliente encontrado", executar(clientes.consultar_cliente, "zzz"))

    def test_alterar_mantem_valores_com_enter(self):
        executar(clientes.alterar_cliente, "1", "Maria S. Lima", "", "", "", "")
        self.assertEqual(dados.CLIENTES[0]["nome"], "Maria S. Lima")
        self.assertEqual(dados.CLIENTES[0]["cpf"], "529.982.247-25")

    def test_excluir(self):
        executar(clientes.excluir_cliente, "1", "n")
        self.assertEqual(len(dados.CLIENTES), 1)
        executar(clientes.excluir_cliente, "1", "x", "s")  # 'x' é inválido, repete
        self.assertEqual(len(dados.CLIENTES), 0)

    def test_excluir_cliente_com_conta_bloqueado(self):
        executar(contas.abrir_conta, "1", "1")
        saida = executar(clientes.excluir_cliente, "1")
        self.assertIn("possui 1 conta", saida)
        self.assertEqual(len(dados.CLIENTES), 1)


class TestContas(BaseTeste):
    def test_abrir_corrente_e_poupanca(self):
        executar(contas.abrir_conta, "1", "1")
        executar(contas.abrir_conta, "1", "2")
        self.assertEqual([c["tipo"] for c in dados.CONTAS], ["Corrente", "Poupança"])
        self.assertEqual(dados.CONTAS[0]["limite"], contas.LIMITE_PADRAO)
        self.assertEqual(dados.CONTAS[1]["limite"], 0.0)

    def test_conta_duplicada_do_mesmo_tipo(self):
        executar(contas.abrir_conta, "1", "1")
        saida = executar(contas.abrir_conta, "1", "1")
        self.assertIn("já possui uma conta Corrente", saida)
        self.assertEqual(len(dados.CONTAS), 1)

    def test_cliente_inexistente(self):
        saida = executar(contas.abrir_conta, "9", "0")
        self.assertIn("não encontrado", saida)
        self.assertEqual(len(dados.CONTAS), 0)

    def test_alterar_limite(self):
        executar(contas.abrir_conta, "1", "1")
        executar(contas.alterar_limite, "1", "2000")
        self.assertEqual(dados.CONTAS[0]["limite"], 2000.0)
        saida = executar(contas.alterar_limite, "1", "99999", "1000")
        self.assertIn("Erro", saida)

    def test_limite_nao_pode_ficar_menor_que_saldo_negativo(self):
        executar(contas.abrir_conta, "1", "1")
        executar(transacoes.sacar, "1", "400")  # saldo -400
        saida = executar(contas.alterar_limite, "1", "100", "500")
        self.assertIn("não cobre", saida)
        self.assertEqual(dados.CONTAS[0]["limite"], 500.0)

    def test_encerrar_so_com_saldo_zero(self):
        executar(contas.abrir_conta, "1", "1")
        executar(transacoes.depositar, "1", "100")
        self.assertIn("saldo da conta deve ser", executar(contas.encerrar_conta, "1"))
        executar(transacoes.sacar, "1", "100")
        executar(contas.encerrar_conta, "1", "s")
        self.assertEqual(len(dados.CONTAS), 0)
        executar(clientes.excluir_cliente, "1", "s")  # agora pode excluir o cliente
        self.assertEqual(len(dados.CLIENTES), 0)


class TestOperacoes(BaseTeste):
    def setUp(self):
        super().setUp()
        self.cadastrar_maria("390.533.447-05")
        executar(contas.abrir_conta, "1", "1")  # conta 1 corrente
        executar(contas.abrir_conta, "2", "2")  # conta 2 poupança

    def test_deposito(self):
        executar(transacoes.depositar, "1", "1.000,50")
        self.assertEqual(dados.CONTAS[0]["saldo"], 1000.50)

    def test_deposito_valor_invalido(self):
        saida = executar(transacoes.depositar, "1", "abc", "-5", "0", "50")
        self.assertEqual(saida.count("Erro:"), 3)
        self.assertEqual(dados.CONTAS[0]["saldo"], 50.0)

    def test_saque_usa_limite_da_corrente(self):
        executar(transacoes.depositar, "1", "100")
        executar(transacoes.sacar, "1", "600")  # 100 + limite 500
        self.assertEqual(dados.CONTAS[0]["saldo"], -500.0)
        saida = executar(transacoes.sacar, "1", "0,01")
        self.assertIn("Saldo insuficiente", saida)

    def test_poupanca_nao_tem_limite(self):
        executar(transacoes.depositar, "2", "100")
        saida = executar(transacoes.sacar, "2", "100,01")
        self.assertIn("Saldo insuficiente", saida)
        self.assertEqual(dados.CONTAS[1]["saldo"], 100.0)

    def test_transferencia(self):
        executar(transacoes.depositar, "1", "300")
        executar(transacoes.transferir, "1", "2", "120,25")
        self.assertEqual(dados.CONTAS[0]["saldo"], 179.75)
        self.assertEqual(dados.CONTAS[1]["saldo"], 120.25)
        self.assertEqual(len(dados.TRANSACOES), 3)

    def test_transferencia_para_mesma_conta(self):
        executar(transacoes.depositar, "1", "300")
        saida = executar(transacoes.transferir, "1", "1")
        self.assertIn("devem ser diferentes", saida)

    def test_transferencia_saldo_insuficiente(self):
        saida = executar(transacoes.transferir, "2", "1", "10")
        self.assertIn("Saldo insuficiente", saida)
        self.assertEqual(len(dados.TRANSACOES), 0)

    def test_conta_inexistente_e_cancelar(self):
        saida = executar(transacoes.depositar, "99", "0")
        self.assertIn("não encontrado", saida)

    def test_extrato(self):
        executar(transacoes.depositar, "1", "100")
        executar(transacoes.sacar, "1", "30")
        saida = executar(transacoes.extrato, "1")
        self.assertIn("Depósito", saida)
        self.assertIn("Saque", saida)
        self.assertIn("R$ 70,00", saida)


class TestRelatorios(BaseTeste):
    def test_relatorios_vazios_nao_quebram(self):
        for funcao in (relatorios.relatorio_saldos, relatorios.relatorio_movimentacoes):
            executar(funcao)
        executar(relatorios.ranking_clientes)

    def test_relatorios_com_exemplos(self):
        dados.CLIENTES.clear()
        for chave in dados.CONTADORES:
            dados.CONTADORES[chave] = 0
        executar(exemplos.carregar_exemplos)
        self.assertEqual((len(dados.CLIENTES), len(dados.CONTAS)), (3, 4))
        saldos = executar(relatorios.relatorio_saldos)
        self.assertIn("R$ 4.150,00", saldos)  # 2200 + 1000 + 800 + 150
        ranking = executar(relatorios.ranking_clientes)
        self.assertLess(ranking.index("Maria Souza"), ranking.index("Ana Lima"))
        self.assertIn("Saque", executar(relatorios.relatorio_movimentacoes))


if __name__ == "__main__":
    unittest.main(verbosity=1)
