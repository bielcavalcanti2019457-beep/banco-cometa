# Explicação simples do código (para a apresentação)

**Ideia geral:** o programa é um menu que chama funções. Os dados ficam em listas na memória.

## Os dados (`dados.py`)
Três listas: `CLIENTES`, `CONTAS`, `TRANSACOES`. Cada item é um **dicionário**:
```python
{"id": 1, "nome": "Maria Souza", "cpf": "529.982.247-25", ...}
```
`CONTADORES` gera o ID automático (1, 2, 3...). O ID da conta é o número da conta.
Ao fechar o programa, as listas somem (regra do professor).

## Funções reutilizáveis (`utilidades.py`)
- **Validadores** (`validar_cpf`, `validar_valor`...): recebem o texto e devolvem `(True, valor)` ou `(False, "mensagem de erro")`.
- **`ler_campo`**: faz `input()` repetidamente até o validador aceitar. É por isso que digitar errado não quebra o programa.
- **`selecionar_por_id`**: pede o ID e procura na lista; 0 cancela.
- **`executar_menu`**: mostra um menu, lê a opção e chama a função escolhida. Todos os menus usam essa mesma função, evitando repetição.

## Um módulo por assunto
- `clientes.py` e `contas.py`: **CRUD** (Create = cadastrar/abrir, Read = listar/consultar, Update = alterar, Delete = excluir/encerrar).
- `transacoes.py`: `registrar_transacao` muda o saldo e guarda a movimentação no histórico; depósito, saque e transferência chamam essa função.
- `relatorios.py`: percorre as listas somando valores com `sum()` e `for`.
- `main.py`: monta o menu principal chamando os menus dos outros módulos.

## Regras de negócio mais importantes (podem perguntar)
1. CPF válido e único (`validar_cpf`, `_validar_cpf_unico`).
2. Saque/transferência só até `saldo + limite` (`saldo_disponivel`).
3. Conta só encerra com saldo zero; cliente só é excluído sem contas.
4. Uma conta de cada tipo por cliente.

## Exemplo de fluxo: depósito
`main` → menu Operações → `depositar()` → `selecionar_por_id` acha a conta → `ler_campo` valida o valor → `registrar_transacao` soma no saldo e guarda no histórico → `print` mostra o novo saldo.

## Testes
`python testes.py` simula as digitações (`unittest.mock`) e confere os resultados, incluindo entradas inválidas.
