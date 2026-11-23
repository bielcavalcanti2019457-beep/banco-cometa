"""
utilidades.py - Funções reutilizadas por todo o sistema.

Aqui ficam: leitura segura de dados (input), validações, formatações
e o gerador de menus. Assim evitamos repetir código nos outros módulos.
"""

from datetime import datetime

import dados

LARGURA = 50
FORMATO_DATA = "%d/%m/%Y"


# ----------------------------------------------------------------------
# Exibição
# ----------------------------------------------------------------------
def exibir_linha():
    print("=" * LARGURA)


def exibir_titulo(titulo, subtitulo=None):
    """Mostra um cabeçalho centralizado entre linhas."""
    print()
    exibir_linha()
    print(titulo.center(LARGURA))
    if subtitulo:
        print(subtitulo.center(LARGURA))
    exibir_linha()


def pausar():
    input("\nPressione ENTER para continuar...")


def cortar(texto, tamanho):
    """Corta textos longos para caber nas colunas das tabelas."""
    texto = str(texto)
    if len(texto) > tamanho:
        return texto[: tamanho - 3] + "..."
    return texto


def formatar_moeda(valor):
    """Converte 1234.5 em 'R$ 1.234,50'."""
    texto = f"{valor:,.2f}"  # exemplo: 1,234.50
    texto = texto.replace(",", "X").replace(".", ",").replace("X", ".")
    return "R$ " + texto


# ----------------------------------------------------------------------
# Datas
# ----------------------------------------------------------------------
def hoje():
    return datetime.now().strftime(FORMATO_DATA)


def agora():
    return datetime.now().strftime(FORMATO_DATA + " %H:%M")


def converter_data(texto):
    """Transforma 'dd/mm/aaaa' em objeto de data (para comparar datas)."""
    return datetime.strptime(texto, FORMATO_DATA)


# ----------------------------------------------------------------------
# Validadores
# Cada validador recebe o texto digitado e devolve uma tupla:
#   (True, valor_convertido)  -> entrada válida
#   (False, "mensagem de erro") -> entrada inválida
# ----------------------------------------------------------------------
def somente_digitos(texto):
    return "".join(caractere for caractere in texto if caractere.isdigit())


def validar_nome(texto):
    if len(texto) < 3:
        return False, "O nome deve ter pelo menos 3 caracteres."
    if texto.isdigit():
        return False, "O nome não pode conter apenas números."
    return True, texto


def validar_telefone(texto):
    digitos = somente_digitos(texto)
    if len(digitos) not in (10, 11):
        return False, "Telefone deve ter 10 ou 11 números (com DDD)."
    ddd, numero = digitos[:2], digitos[2:]
    if len(numero) == 9:
        return True, f"({ddd}) {numero[:5]}-{numero[5:]}"
    return True, f"({ddd}) {numero[:4]}-{numero[4:]}"


def validar_cpf(texto):
    """Confere os 11 números e os dígitos verificadores do CPF."""
    digitos = somente_digitos(texto)
    if len(digitos) != 11:
        return False, "O CPF deve ter 11 números."
    if digitos == digitos[0] * 11:
        return False, "CPF inválido (todos os números iguais)."
    for tamanho in (9, 10):
        soma = sum(int(digitos[i]) * (tamanho + 1 - i) for i in range(tamanho))
        digito = (soma * 10 % 11) % 10
        if digito != int(digitos[tamanho]):
            return False, "CPF inválido (dígitos verificadores não conferem)."
    return True, f"{digitos[:3]}.{digitos[3:6]}.{digitos[6:9]}-{digitos[9:]}"


def validar_email(texto):
    if texto == "":
        return True, ""  # e-mail é opcional
    if " " in texto or "@" not in texto:
        return False, "E-mail inválido. Exemplo: nome@dominio.com"
    usuario, _, dominio = texto.partition("@")
    if usuario == "" or "." not in dominio or dominio.startswith(".") or dominio.endswith("."):
        return False, "E-mail inválido. Exemplo: nome@dominio.com"
    return True, texto.lower()


def converter_valor(texto):
    """Converte '1.500,50' ou '150.5' em número. Devolve None se inválido."""
    texto = texto.replace("R$", "").strip()
    if "," in texto:
        texto = texto.replace(".", "").replace(",", ".")
    try:
        return round(float(texto), 2)
    except ValueError:
        return None


def validar_valor(texto):
    """Valor monetário maior que zero (depósitos, saques, transferências)."""
    valor = converter_valor(texto)
    if valor is None:
        return False, "Digite um valor numérico. Exemplo: 150,00"
    if valor <= 0:
        return False, "O valor deve ser maior que zero."
    if valor > 1000000:
        return False, "Valor acima do máximo permitido por operação (R$ 1.000.000,00)."
    return True, valor


def validar_limite(saldo_atual):
    """Limite de cheque especial: de 0 a 10.000, cobrindo o saldo negativo."""

    def validar(texto):
        valor = converter_valor(texto)
        if valor is None:
            return False, "Digite um valor numérico. Exemplo: 500,00"
        if valor < 0 or valor > 10000:
            return False, "O limite deve estar entre R$ 0,00 e R$ 10.000,00."
        if saldo_atual < 0 and valor < -saldo_atual:
            return False, "O novo limite não cobre o saldo negativo da conta."
        return True, valor

    return validar


def validar_data(texto):
    """Aceita dd/mm/aaaa e devolve a data normalizada."""
    try:
        data = converter_data(texto)
    except ValueError:
        return False, "Data inválida. Use o formato dd/mm/aaaa."
    if data.year < 1900:
        return False, "Ano inválido (use 1900 ou mais)."
    return True, data.strftime(FORMATO_DATA)


def validar_data_nao_futura(texto):
    ok, resultado = validar_data(texto)
    if not ok:
        return ok, resultado
    if converter_data(resultado) > converter_data(hoje()):
        return False, "A data não pode ser futura."
    return True, resultado


def validar_nascimento(texto):
    """Data válida e cliente maior de 18 anos."""
    ok, resultado = validar_data_nao_futura(texto)
    if not ok:
        return ok, resultado
    nascimento = converter_data(resultado)
    agora = datetime.now()
    idade = agora.year - nascimento.year - (
        (agora.month, agora.day) < (nascimento.month, nascimento.day)
    )
    if idade < 18:
        return False, "O cliente deve ter 18 anos ou mais."
    if idade > 120:
        return False, "Data de nascimento improvável. Confira a data."
    return True, resultado


def validar_opcao(opcoes_validas):
    """Cria um validador que só aceita as opções de um menu."""

    def validar(texto):
        if texto in opcoes_validas:
            return True, texto
        return False, "Opção inválida. Digite um número do menu."

    return validar


def validar_numero_positivo(texto):
    if not texto.isdigit() or int(texto) < 0:
        return False, "Digite apenas números inteiros."
    return True, int(texto)


# ----------------------------------------------------------------------
# Leitura de dados (sempre repete até o usuário digitar algo válido)
# ----------------------------------------------------------------------
def ler_campo(mensagem, validar, atual=None, texto_atual=None):
    """
    Pergunta ao usuário até receber um valor válido.

    - validar: função validadora (veja a seção acima).
    - atual: valor padrão. Se o usuário apenas apertar ENTER, ele é mantido.
      (usado na alteração de cadastros e em datas, que sugerem 'hoje').
    """
    sufixo = ""
    if atual not in (None, ""):
        sufixo = f" [{texto_atual if texto_atual else atual}]"
    while True:
        texto = input(f"{mensagem}{sufixo}: ").strip()
        if texto == "" and atual is not None:
            return atual
        ok, resultado = validar(texto)
        if ok:
            return resultado
        print(f"  Erro: {resultado}")


def escolher_da_lista(titulo, opcoes, atual=None):
    """Mostra opções numeradas e devolve o texto da opção escolhida."""
    print(titulo)
    for numero, opcao in enumerate(opcoes, start=1):
        print(f"  {numero} - {opcao}")

    def validar(texto):
        if texto.isdigit() and 1 <= int(texto) <= len(opcoes):
            return True, opcoes[int(texto) - 1]
        return False, f"Escolha um número de 1 a {len(opcoes)}."

    if atual is not None:
        print(f"  (ENTER mantém: {atual})")
        return ler_campo("Opção", validar, atual)
    return ler_campo("Opção", validar)


def confirmar(pergunta):
    """Pergunta sim/não e devolve True ou False."""
    while True:
        resposta = input(f"{pergunta} (s/n): ").strip().lower()
        if resposta in ("s", "sim"):
            return True
        if resposta in ("n", "nao", "não"):
            return False
        print("  Erro: responda com 's' para sim ou 'n' para não.")


# ----------------------------------------------------------------------
# Busca e seleção de registros
# ----------------------------------------------------------------------
def proximo_id(entidade):
    dados.CONTADORES[entidade] += 1
    return dados.CONTADORES[entidade]


def buscar_por_id(lista, id_procurado):
    for item in lista:
        if item["id"] == id_procurado:
            return item
    return None


def selecionar_por_id(lista, mensagem, nome_entidade):
    """
    Pede um ID até encontrar um registro existente.
    Digite 0 para cancelar (devolve None).
    """
    if not lista:
        print(f"\nNenhum(a) {nome_entidade.lower()} cadastrado(a) ainda.")
        return None

    def validar(texto):
        ok, numero = validar_numero_positivo(texto)
        if not ok:
            return ok, numero
        if numero == 0:
            return True, None
        item = buscar_por_id(lista, numero)
        if item is None:
            return False, f"{nome_entidade} com ID {numero} não encontrado(a)."
        return True, item

    return ler_campo(f"{mensagem} (0 para cancelar)", validar)


# ----------------------------------------------------------------------
# Menus
# ----------------------------------------------------------------------
def executar_menu(titulo, opcoes, subtitulo=None, texto_voltar="Voltar ao menu principal",
                  pausar_apos=True):
    """
    Mostra um menu e executa a função da opção escolhida, até o usuário
    escolher 0.

    opcoes: lista de tuplas (texto_da_opcao, funcao_a_executar)
    """
    validos = [str(numero) for numero in range(len(opcoes) + 1)]
    while True:
        exibir_titulo(titulo, subtitulo)
        for numero, (texto, _) in enumerate(opcoes, start=1):
            print(f"{numero} - {texto}")
        print(f"0 - {texto_voltar}")
        exibir_linha()
        escolha = ler_campo("Digite a opção desejada", validar_opcao(validos))
        if escolha == "0":
            return
        opcoes[int(escolha) - 1][1]()
        if pausar_apos:
            pausar()
