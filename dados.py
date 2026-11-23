"""
dados.py - Armazenamento em memória do sistema bancário.

Todos os dados ficam em listas Python; cada item é um dicionário.
Ao fechar o programa os dados são perdidos (regra do projeto avaliativo).
"""

CLIENTES = []
CONTAS = []
TRANSACOES = []

# Contadores para gerar o código (ID) automático de cada registro.
# O ID da conta é o número da conta.
CONTADORES = {"cliente": 0, "conta": 0, "transacao": 0}
