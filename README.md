# Sistema-Banc-rio-vers-o-1
Sistema bancário em Python com operações de depósito, saque e extrato.


# 🏦 Sistema Bancário em Python

Desafio proposto pelo instrutor **Guilherme Arthur de Carvalho**.  
O objetivo é criar um sistema bancário simples em Python que permita realizar depósitos, saques e visualizar o extrato.

---

## 🚀 Funcionalidades

- **Depósito**
  - Permite adicionar valores positivos ao saldo.
  - Todos os depósitos ficam registrados no extrato.

- **Saque**
  - Máximo de **3 saques diários**.
  - Limite de **R$ 500,00 por saque**.
  - Bloqueia se não houver saldo suficiente.
  - Todos os saques ficam registrados no extrato.

- **Extrato**
  - Lista todas as operações (depósitos e saques).
  - Mostra o saldo atual formatado no padrão monetário (`R$ 0.00`).

---

### ✅ Versão 2
- **Depósito, Saque e Extrato** foram separados em funções.
- **Cadastro de Usuário**
  - Nome, CPF (apenas números) e endereço.
  - Não é permitido cadastrar dois usuários com o mesmo CPF.
- **Cadastro de Conta Corrente**
  - Agência fixa `0001`.
  - Número da conta sequencial.
  - Uma conta pertence a apenas um usuário, mas um usuário pode ter várias contas.
- **Extrato (atualizado)**
  - Exibe também agência, número da conta e titular.
- **Consulta de Saldo (nova função)**
  - Consulta saldo de um cliente pelo CPF.
  - Mostra agência, número da conta e nome do titular.

---

## 📂 Estrutura do projeto
- `desafio1.py` → Versão 1 do sistema
- `desafio2.py` → Versão 2 do sistema
- `README.md` → Documentação do projeto
