# Banco Digital - V2
# Autor: Rodrigo Duarte Coelho
# Data: 2024-06-20


def depositar(saldo, valor, extrato, /):  # positional-only
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
        print(f"\n=== Depósito de R$ {valor:.2f} realizado! ===")
    else:
        print("\n@@@ Operação falhou: valor inválido. @@@")
    return saldo, extrato


def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):  # keyword-only
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("\n@@@ Operação falhou: saldo insuficiente. @@@")

    elif excedeu_limite:
        print("\n@@@ Operação falhou: valor acima do limite por saque. @@@")

    elif excedeu_saques:
        print("\n@@@ Operação falhou: número máximo de saques diários atingido. @@@")

    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1
        print(f"\n=== Saque de R$ {valor:.2f} realizado! ===")

    else:
        print("\n@@@ Operação falhou: valor inválido. @@@")

    return saldo, extrato, numero_saques


def exibir_extrato(saldo, /, *, extrato, conta):  # saldo posicional, extrato keyword
    print("\n================= EXTRATO =================")
    print(f"Agência: {conta['agencia']} | Conta: {conta['numero_conta']} | Titular: {conta['usuario']['nome']}")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("===========================================")


# -------------------------
# Usuários e contas
# -------------------------
def filtrar_usuario(cpf, usuarios):
    for u in usuarios:
        if u["cpf"] == cpf:
            return u
    return None


def criar_usuario(usuarios, cpf_prefill=None):
    if cpf_prefill is None:
        raw = input("Informe o CPF (somente números): ").strip()
    else:
        raw = cpf_prefill

    cpf = "".join(filter(str.isdigit, raw))
    if not cpf:
        print("\n@@@ CPF inválido. Operação cancelada. @@@")
        return None

    if filtrar_usuario(cpf, usuarios):
        print("\n@@@ Já existe usuário com esse CPF. @@@")
        return None

    nome = input("Informe o nome completo: ").strip()
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/UF): ").strip()

    usuario = {"nome": nome, "cpf": cpf, "endereco": endereco}
    usuarios.append(usuario)
    print("\n=== Usuário criado com sucesso! ===")
    return usuario


def criar_conta(agencia, numero_conta, usuario):
    conta = {
        "agencia": agencia,
        "numero_conta": numero_conta,
        "usuario": usuario,
        "saldo": 0.0,
        "extrato": "",
        "numero_saques": 0,
    }
    print(f"\n=== Conta {numero_conta} criada (Ag {agencia}) para {usuario['nome']} ===")
    return conta


def listar_contas(contas):
    if not contas:
        print("\nNenhuma conta cadastrada.")
        return
    print("\n=== Contas cadastradas ===")
    for c in contas:
        print(f"Agência: {c['agencia']} | Conta: {c['numero_conta']} | Titular: {c['usuario']['nome']} (CPF: {c['usuario']['cpf']})")
    print("==========================")


def contas_do_cpf(cpf, contas):
    return [c for c in contas if c["usuario"]["cpf"] == cpf]


def escolher_conta_da_lista(contas_usuario):
    if not contas_usuario:
        return None
    if len(contas_usuario) == 1:
        return contas_usuario[0]
    print("\nContas do usuário:")
    for c in contas_usuario:
        print(f"- Conta: {c['numero_conta']} (Ag {c['agencia']})")
    try:
        num = int(input("Informe o número da conta que deseja usar: "))
    except ValueError:
        print("Entrada inválida.")
        return None
    for c in contas_usuario:
        if c["numero_conta"] == num:
            return c
    print("Conta não encontrada.")
    return None


def obter_conta_via_cpf(usuarios, contas, agencia):
    raw = input("Informe o CPF (somente números): ").strip()
    cpf = "".join(filter(str.isdigit, raw))
    if not cpf:
        print("\n@@@ CPF inválido. @@@")
        return None

    usuario = filtrar_usuario(cpf, usuarios)
    if not usuario:
        print("\nUsuário não encontrado para o CPF informado.")
        choice = input("Deseja cadastrar usuário e criar conta agora? (s/n): ").strip().lower()
        if choice != "s":
            return None
        usuario = criar_usuario(usuarios, cpf_prefill=cpf)
        if not usuario:
            return None
        numero_conta = len(contas) + 1
        conta = criar_conta(agencia, numero_conta, usuario)
        contas.append(conta)
        return conta

    contas_usuario = contas_do_cpf(cpf, contas)
    if not contas_usuario:
        print("\nUsuário não possui conta.")
        choice = input("Deseja criar uma conta para esse usuário agora? (s/n): ").strip().lower()
        if choice != "s":
            return None
        numero_conta = len(contas) + 1
        conta = criar_conta(agencia, numero_conta, usuario)
        contas.append(conta)
        return conta

    return escolher_conta_da_lista(contas_usuario)


# -------------------------
# Programa principal
# -------------------------
def main():
    AGENCIA = "0001"
    LIMITE = 500
    LIMITE_SAQUES = 3

    usuarios = []
    contas = []

    menu = """
================= BEM VINDO AO SEU BANCO DIGITAL V3 =================

Escolha a operação desejada:

(1) Depositar
(2) Sacar
(3) Extrato
(4) Criar usuário
(5) Criar conta
(6) Listar contas
(7) Consultar saldo
(0) Sair

====================================================================
=> """

    while True:
        opcao = input(menu).strip()

        if opcao == "0":
            print("\nObrigado por usar nosso sistema! Até logo.")
            break

        elif opcao == "1":  # Depositar
            conta = obter_conta_via_cpf(usuarios, contas, AGENCIA)
            if not conta:
                continue
            try:
                valor = float(input("Informe o valor do depósito: ").strip())
            except ValueError:
                print("Valor inválido.")
                continue
            conta["saldo"], conta["extrato"] = depositar(conta["saldo"], valor, conta["extrato"])

        elif opcao == "2":  # Sacar
            conta = obter_conta_via_cpf(usuarios, contas, AGENCIA)
            if not conta:
                continue
            try:
                valor = float(input("Informe o valor do saque: ").strip())
            except ValueError:
                print("Valor inválido.")
                continue
            conta["saldo"], conta["extrato"], conta["numero_saques"] = sacar(
                saldo=conta["saldo"],
                valor=valor,
                extrato=conta["extrato"],
                limite=LIMITE,
                numero_saques=conta["numero_saques"],
                limite_saques=LIMITE_SAQUES,
            )

        elif opcao == "3":  # Extrato
            conta = obter_conta_via_cpf(usuarios, contas, AGENCIA)
            if not conta:
                continue
            exibir_extrato(conta["saldo"], extrato=conta["extrato"], conta=conta)

        elif opcao == "4":  # Criar usuário
            criar_usuario(usuarios)

        elif opcao == "5":  # Criar conta
            conta = obter_conta_via_cpf(usuarios, contas, AGENCIA)
            if conta:
                print("Conta criada/registrada com sucesso.")

        elif opcao == "6":
            listar_contas(contas)

        elif opcao == "7":  # Consultar saldo
            conta = obter_conta_via_cpf(usuarios, contas, AGENCIA)
            if not conta:
                continue
            print("\n================= SALDO =================")
            print(f"Agência: {conta['agencia']} | Conta: {conta['numero_conta']} | Titular: {conta['usuario']['nome']}")
            print(f"Saldo disponível: R$ {conta['saldo']:.2f}")
            print("=========================================")

        else:
            print("\nOpção inválida. Tente novamente.")


if __name__ == "__main__":
    main()