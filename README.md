# Banco Cometa – Sistema de Gerenciamento Bancário

Projeto avaliativo da disciplina **Coding** – Análise e Desenvolvimento de Sistemas (UNINASSAU).
Professor: Joseph Donald de Maceno Vieira.

## Descrição
Sistema bancário em Python que funciona **exclusivamente pelo terminal** (`input()` e `print()`).
Os dados ficam **somente em memória**, em listas Python (sem arquivos e sem banco de dados).

## Objetivo
Aplicar programação em Python, organização de código em funções e módulos, validações e
desenvolvimento colaborativo com Git e GitHub.

## Problema que resolve
Controlar manualmente clientes, contas e movimentações gera erros (saldo incorreto, CPF
repetido, saques acima do disponível). O sistema centraliza o cadastro e aplica as regras
do banco automaticamente.

## Funcionalidades
| Menu | O que faz |
|---|---|
| Clientes (CRUD) | Cadastrar, listar, consultar (ID, CPF ou nome), alterar e excluir |
| Contas (CRUD) | Abrir conta corrente/poupança, listar, consultar, alterar limite e encerrar |
| Operações | Depósito, saque, transferência e extrato |
| Relatórios | Saldos do banco, ranking de clientes por saldo e movimentações por tipo |
| Dados de exemplo | Carrega clientes e contas de demonstração |

### Regras de negócio e validações
- CPF com dígitos verificadores válidos e **único** por cliente.
- Cliente maior de 18 anos; datas válidas e não futuras; telefone com DDD; e-mail opcional válido.
- Cada cliente tem no máximo **uma conta de cada tipo** (Corrente e Poupança).
- Conta corrente tem limite (cheque especial, padrão R$ 500,00); poupança não tem limite.
- Saque e transferência só até `saldo + limite`; valores devem ser maiores que zero.
- Transferência exige contas diferentes.
- Conta só pode ser encerrada com **saldo zero**; cliente só pode ser excluído **sem contas**.
- Entradas inválidas mostram o erro e a pergunta é repetida (o programa não quebra).

## Tecnologias
Python 3.10+ (somente biblioteca padrão: `datetime`, `unittest`). Git e GitHub.

## Estrutura dos arquivos
```
banco_cometa/
├── main.py          # menu principal e início do programa
├── dados.py         # listas em memória (clientes, contas, transações)
├── utilidades.py    # validações, leitura de dados e gerador de menus
├── clientes.py      # CRUD de clientes
├── contas.py        # CRUD de contas
├── transacoes.py    # depósito, saque, transferência e extrato
├── relatorios.py    # relatórios
├── exemplos.py      # dados de demonstração
├── testes.py        # testes automáticos
├── docs/            # roteiro do vídeo, guia do GitHub e explicação do código
└── README.md
```

## Como executar
```bash
python main.py      # iniciar o sistema
python testes.py    # rodar os testes (29 testes)
```
No Windows, use `python` ou `py`. Dica: no menu principal, a opção **5** carrega dados de exemplo.

## Exemplo de utilização
```
==================================================
                   BANCO COMETA
             Sistema de Gerenciamento
==================================================
1 - Gerenciar Clientes
2 - Gerenciar Contas
3 - Operações Bancárias
4 - Relatórios
5 - Carregar dados de exemplo
0 - Sair do Sistema
==================================================
Digite a opção desejada: 3
...
Número da conta (0 para cancelar): 1
Valor do depósito: 1.000,50
Depósito realizado! Novo saldo: R$ 3.200,50
```

## Utilização de Inteligência Artificial
A IA (Claude) foi usada para gerar e revisar o código. Todos os integrantes devem conseguir
explicar o que foi produzido (veja `docs/EXPLICACAO_CODIGO.md`). Prompts utilizados:

**Prompt 1 – Especificação inicial do projeto**
- *Prompt:* "Atue como um desenvolvedor Python sênior, professor de programação e especialista em
  organização de projetos acadêmicos. Quero que você desenvolva comigo um projeto completo para a
  avaliação da disciplina Coding […] Utilize como referência obrigatória o PDF 'PROJETO AVALIATIVO.pdf' […]
  funcionar exclusivamente pelo terminal […] listas em memória […] módulos […] validações […] README […] roteiro de vídeo […] GitHub."
- *Objetivo:* definir o escopo, as regras técnicas e os entregáveis do trabalho.
- *Resultado:* a IA leu o PDF do professor, montou o plano e começou o sistema, inicialmente com outro tema (serviços de segurança eletrônica).

**Prompt 2 – Mudança de tema**
- *Prompt:* "vou querer fazer um banco" (confirmado como sistema bancário no lugar do tema anterior).
- *Objetivo:* trocar o estudo de caso por um banco, um dos temas sugeridos no PDF.
- *Resultado:* o projeto virou o Banco Cometa, com clientes, contas e operações; reaproveitou a base de validações e menus.

**Prompt 3 – Critérios e funcionamento no terminal**
- *Prompt:* "siga os critérios de forma concisa" e "o sistema deve funcionar através do terminal utilizando as regras".
- *Objetivo:* garantir o cumprimento dos critérios de avaliação do PDF, sem excessos.
- *Resultado:* sistema 100% em terminal, sem arquivos, banco de dados ou interface gráfica; 29 testes automáticos passando e documentação enxuta.

## Desenvolvimento colaborativo
Branches, commits e Pull Requests: veja `docs/GUIA_GITHUB.md`.

## Autores
Preencher com os nomes dos integrantes do grupo (máximo 3).
