import os, sys

def clear():
    os.system('cls')

# Simulador de Sistema Bancário
depositos = []
saques = []
limite_max = 500.00 # por saque


# sistema que identifica um limite de até 3 saques diarios pela data
def saques_diarios():
    if len(saques) >= 3:
        print("Limite de saques diários atingido.")
        return False
    

saldo = 0.00

def saldo_atual():
    global saldo
    if len(depositos) > 0:
        saldo = sum(depositos)
    else:
        print("Não é possível realizar Saques, Saldo Indisponível.")
    return saldo

def depositar(valor):
    clear()
    if valor <= 0:
        print("Valor inválido para depósito.")
        return depositar(float(input("Digite o valor do depósito: ")))
    depositos.append(valor)
    print(f"Depósito de R$ {valor:.2f} realizado com sucesso.")
    return saldo_atual()

def sacar(valor):
    clear()
    if saques_diarios() != False:
        if valor <= 0:
            print("Valor inválido para saque.")
            return sacar(float(input("Digite o valor do saque: ")))
        if valor > limite_max:
            print("Valor máximo para saque excedido.")
            return sacar(float(input("Digite o valor do saque: ")))
        
        global saldo
        if saldo >= valor:
            saques.append(valor)
            saldo -= valor
            print(f"Saque de R$ {valor:.2f} realizado com sucesso.")
            return saldo_atual()
    else:
        return False
def extrato():
    print("Extrato:")
    clear()
    print("Depósitos Feitos:")
    for deposito in depositos:
        print(f"R$ {deposito:.2f}")
    print("Saques Feitos:")
    for saque in saques:
        print(f"R$ {saque:.2f}")
    global saldo
    print(f"Saldo atual: R$ {sum(depositos) - sum(saques)}")
clear()
while True:
    opcao_user = float(input("Depositar(1) \nSacar(2) \nExtrato(3) \nFechar(0) \nEscolha uma opção: "))
    
    clear()
    if opcao_user == 0:
        print("Programa encerrado.")
        sys.exit()
        clear()
    elif opcao_user == 1:
       depositar(float(input("Digite o valor do depósito: ")))
    elif opcao_user == 2:
       sacar(float(input("Digite o valor do saque: ")))
    elif opcao_user == 3:
        extrato()
        input("\nPressione ENTER para continuar...")
