import os, sys
from datetime import datetime, timedelta

def clear():
    os.system('cls')

def registro():
    data_do_saque = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    return data_do_saque

def saques_diarios():
    if len(usuario_atual['saques']) > 0:
        ultimo_saque = usuario_atual['saques'][-1].split(" --- ")[1]
        data_ultimo_saque = datetime.strptime(ultimo_saque, "%d/%m/%Y %H:%M:%S")
        diferenca = datetime.now() - data_ultimo_saque
        if diferenca.total_seconds() / (60 * 60 * 24) >= 1:
            usuario_atual['saques'] = []
    
    if len(usuario_atual['saques']) >= 10:
        ultimo_saque = usuario_atual['saques'][-1].split(" --- ")[1]
        data_ultimo_saque = datetime.strptime(ultimo_saque, "%d/%m/%Y %H:%M:%S")
        print("Você atingiu o Limite de saques diários (10 permitidos).")
        data_disponivel = data_ultimo_saque + timedelta(days=1)
        print(f"Espere até as {data_disponivel.strftime('%H:%M:%S')} de amanhã para realizar novos saques")
        input("Pressione ENTER para continuar...")
        return False
    return True

usuario_atual = None

def saldo_atual():
    total_depositos = sum(float(d.split(" --- ")[0]) for d in usuario_atual["depositos"])
    total_saques = sum(float(s.split(" --- ")[0]) for s in usuario_atual["saques"])
    saldo = total_depositos - total_saques
    return saldo


def depositar(valor):
    clear()
    try:
        valor = float(valor)
        if valor <= 0:
            print("Valor inválido para depósito.")
            return depositar(input("Digite o valor do depósito: "))

        usuario_atual["depositos"].append(f"{valor} --- {registro()}")
        print(f"Depósito de R$ {valor:.2f} realizado com sucesso.")
        saldo_atual()
        input("Pressione ENTER para continuar...")
        
    except ValueError:
        print("Por favor digite apenas números.")
        return depositar(input("Digite o valor do depósito: "))



limite_max = 500.00 # por saque
def sacar(valor):
    clear()
    try:
        valor = float(valor)
        if not saques_diarios():
            return

        if valor <= 0:
            print("Valor inválido para saque.")
            return sacar(float(input("Digite o valor do saque: ")))
        
        if valor > limite_max:
            clear()
            print("### ATENÇÃO ###")
            print("Valor máximo para saque excedido.")
            return sacar(float(input("Digite o valor do saque: ")))
        
        if saldo_atual() >= valor:
            usuario_atual["saques"].append(f"{valor} --- {registro()}")
            print(f"Saque de R$ {valor:.2f} realizado com sucesso.")
            input("Pressione ENTER para continuar...")
        else:
            print("Saldo insuficiente.")
                
    except ValueError:
        print("Por favor digite apenas números.")
        return sacar(float(input("Digite o valor do saque: ")))
    
def extrato():
    clear()
    print(f"--- EXTRATO DE {usuario_atual['nome'].upper()} ---")
    print("Depósitos Feitos:")
    
    if not usuario_atual["depositos"]:
        print("Nenhum depósito realizado.")
    else:
        for deposito in usuario_atual['depositos']:
            valor = float(deposito.split(" --- ")[0])
            data = deposito.split(" --- ")[1]
            print(f"R$ {valor:.2f} no dia: {data}")

    print("\nSaques Feitos:")
    if not usuario_atual["saques"]:
        print("Nenhum saque realizado.")
    else:
        for saque in usuario_atual['saques']:
            valor = float(saque.split(" --- ")[0])
            data = saque.split(" --- ")[1]
            print(f"R$ {valor:.2f} no dia: {data}")

    print(f"\nSaldo atual: R$ {saldo_atual():.2f}")

clear()

usuarios = []

def cadastro():
    clear()
    print("Cadastro de usuário:")
    nome = input("Digite seu nome: ")
    cpf = input("Digite seu CPF: ")
    senha = input("Digite sua senha: ")
    novo_usuario = {
        "nome": nome,
        "cpf": cpf,
        "senha": senha,
        "depositos": [],
        "saques": [],
        "saldo": 0.0
    }
    usuarios.append(novo_usuario)
    print("Sua Conta foi Criada!")
    input("Pressione ENTER para continuar...")

def login():
    global usuario_atual
    clear()
    print("--- TELA DE LOGIN ---")
    cpf = input("Digite seu CPF: ")
    senha = input("Digite sua senha: ")
    for usuario in usuarios:
        if usuario["cpf"] == cpf and usuario["senha"] == senha:
            usuario_atual = usuario
            clear()
            print(f"Login realizado com sucesso. \n\nSeja Bem-vindo, {usuario['nome']}!")
            input("\nPressione ENTER para continuar...")
            return True
    print("CPF ou senha inválidos.")
    input("Pressione ENTER para continuar...")
    return False

def menu():
    while True:
        clear()
        print("Bem Vindo ao Sys Bank 2.0:")
        print("Cadastrar-se(1)")
        print("Entrar na sua conta(2)")
        print("Sair(0)")
        try:
            opcoes = float(input("Escolha uma opção: "))
            if opcoes == 0:
                print("Programa encerrado.")
                sys.exit()
            elif opcoes == 1:
                cadastro()
            elif opcoes == 2:
                if login():
                    menu_operacoes()
                    
        except ValueError:
            print("Opção inválida. Digite apenas números.")
            input("Pressione ENTER para continuar...")

def menu_operacoes():
    while True:
        try:
            clear()
            print(f"Seja Bem Vindo {usuario_atual['nome'].upper()} ao seu Banco:")
            print(f"Saldo atual: R$ {saldo_atual():.2f}")
            opcao_user = float(input("Depositar(1) \nSacar(2) \nExtrato(3) \nLogout(0) \nEscolha uma opção: "))

            if opcao_user == 0:
                break
            elif opcao_user == 1:
               depositar(float(input("Digite o valor do depósito: ")))
            elif opcao_user == 2:
               sacar(float(input("Digite o valor do saque: ")))
            elif opcao_user == 3:
                extrato()
                input("\nPressione ENTER para continuar...")
        except ValueError:
            print("Opção inválida. Digite apenas números.")
            input("Pressione ENTER para continuar...")

if __name__ == "__main__":
    menu()