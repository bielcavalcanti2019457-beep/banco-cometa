# Guia GitHub (o PDF exige repositório compartilhado, branches, commits e Pull Requests)

## 1. Criar e compartilhar o repositório (manual, no GitHub)
1. Um integrante cria o repositório `banco-cometa` (público ou privado) em github.com.
2. Em *Settings → Collaborators*, adicione os outros integrantes e o professor, se pedido.
3. Em *Settings → Branches*, proteja a `main` exigindo Pull Request (opcional, mas mostra boa prática).

## 2. Enviar o projeto
```bash
cd banco_cometa
git remote add origin https://github.com/SEU_USUARIO/banco-cometa.git
git push -u origin main
git push origin --all        # envia também as branches de desenvolvimento
```

## 3. Fluxo de trabalho de cada integrante
```bash
git checkout main && git pull
git checkout -b feature/nome-da-tarefa     # ex.: feature/validacao-saque
# ...editar os arquivos...
git add arquivo_alterado.py
git commit -m "feat: descreve o que mudou"
git push -u origin feature/nome-da-tarefa
```
No GitHub: **Compare & pull request** → descreva a mudança → outro integrante revisa → **Merge**.

## 4. Padrão de commits
`feat:` nova funcionalidade · `fix:` correção · `docs:` documentação · `test:` testes · `refactor:` organização.

## 5. O que o grupo precisa fazer
- Cada integrante deve criar **ao menos uma branch, commits e um Pull Request** com a própria conta, para o histórico mostrar o trabalho colaborativo.
- Sugestões de tarefas para dividir: `feature/relatorios-extras`, `feature/melhorias-extrato`, `docs/readme-autores`, `test/novos-testes`.
- Preencher os nomes dos autores no `README.md`.
- Pull Requests só existem no GitHub: o projeto não traz nenhum, e nada deve ser inventado.

## 6. Histórico local já preparado
O repositório local já tem `main` e branches de desenvolvimento mescladas (`git log --graph --oneline --all`).
Esses commits foram feitos localmente com identidade provisória. Para trocar o autor pelo seu:
```bash
git config user.name "Seu Nome" && git config user.email "seu@email.com"
git rebase -r --root --exec 'git commit --amend --no-edit --reset-author'
```
