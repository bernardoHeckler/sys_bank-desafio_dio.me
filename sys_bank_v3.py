import os, sys
from datetime import datetime, timedelta
from abc import ABC, abstractclassmethod, abstractproperty

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')
    
def continuar():
    input("Pressione ENTER para continuar...")

# Classes
class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []
        
    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)
        
class PessoaFisica(Cliente):
    def __init__(self, nome, cpf, data_nascimento, endereco, senha):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf
        self.senha = senha
        
class Conta:
    def __init__(self, numero , cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = '0001'
        self._cliente = cliente
        self._historico = Historico()
        
    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)
    
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero
    @property
    def agencia(self):
        return self._agencia
    @property
    def historico(self):
        return self._historico
        
    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo
        
        # if not saques_diarios():
        #     return

        if excedeu_saldo:
            print("Você não tem saldo suficiente para saque!")
        
        # elif valor > limite:
        #     clear()
        #     print("### ATENÇÃO ###")
        #     print("Valor máximo para saque excedido.")
        #     return sacar(float(input("Digite o valor do saque: ")))
        
        elif valor > 0:
            self._saldo -= valor
            print(f"Saque realizado com sucesso!")
            return True
        else:
            print("Operação falhou! O valor informado é inválido.")
            
        return False
    
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print(f"Deposito realizado com sucesso!")
        else:
            print("Operação falhou! O valor informado é inválido.")
            return False
        
        return True
        
class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques
    def sacar(self, valor):
        excedeu_limite = valor > self.limite
        
        numero_saques = len(
            [t for t in self.historico.transacoes if t['tipo'] == 'Saque']
        )
        excedeu_saques = numero_saques >= self.limite_saques # Use >= e não >-

        if excedeu_limite:
            print(f"\n@@@ Falhou! O valor excede o limite de R$ {self.limite:.2f} @@@")
        elif excedeu_saques:
            print("\n@@@ Falhou! Número máximo de saques atingido. @@@")
        else:
            # Se passou pelas regras da Corrente, chama o sacar da Conta (pai)
            return super().sacar(valor)
        
        return False
    
    def __str__(self):
        return f"""
            Agência: {self._agencia}
            C/C: {self._numero}
            Titular: {self._cliente.nome}
        """
        
class Historico:
    def __init__(self):
        self._transacoes = []
        
    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                'tipo': transacao.__class__.__name__,
                'valor': transacao.valor,
                'data': datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            }
        )
        
class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass
    
    @abstractclassmethod
    def registrar(self, conta):
        pass
        
class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor
        
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)
        
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)
            
class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor
        
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)
        
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)
        
# Interfaces e Lógica

clientes = []

def filtrar_cliente(cpf):
    resultado = [c for c in clientes if c.cpf == cpf]
    return resultado[0] if resultado else None

def cadastro():
    clear()
    cpf = input("Informe o CPF: ")
    if filtrar_cliente(cpf):
        print("\n Já existe usuário com esse CPF!")
        continuar()
        return
    nome = input('Nome: ')
    data_nascimento = input('Data de nascimento: ')
    endereco = input('Endereco: ')
    senha = input('Crie uma senha: ')
    
    novo_cliente = PessoaFisica(nome, cpf, data_nascimento, endereco, senha)
    # se for cliente novo, automaticamente uma conta corrente criada
    nova_conta = ContaCorrente(numero=len(clientes)+1, cliente=novo_cliente)
    novo_cliente.adicionar_conta(nova_conta)
    
    clientes.append(novo_cliente)
    
    print("Conta Criada com Sucesso!")
    continuar()

def login():
    clear()
    cpf = input("Informe o CPF: ")
    senha = input("Digite sua Senha: ")
    cliente = filtrar_cliente(cpf)
    
    if cliente and cliente.senha == senha:
        menu_operacoes(cliente)
    else:
        print("CPF ou senha inválidos.")
        continuar()

def extrato(cliente, conta):
    clear()
    print(f"--- EXTRATO DE {cliente.nome.upper()} ---")
    transacoes = conta.historico.transacoes
    
    if not transacoes:
        print("Nenhum depósito realizado.")
    else:
        for t in transacoes:
            print(f'{t['tipo']}:\t\tR$ {t['valor']:.2f} | {t['data']}')

    print(f"\nSaldo:\t\tR$ {conta.saldo:.2f}\n")
    continuar()

def menu_operacoes(cliente):
    conta = cliente.contas[0]
    while True:
        clear()
        print(f"Olá {cliente.nome}| Ag: {conta._agencia} | C/C: {conta._numero}")
        print(f"Saldo atual: R$ {conta._saldo:.2f}")
        print("Depositar(1) \nSacar(2) \nExtrato(3) \nLogout(0)")
        opcao = input('\nEscolha: ')
        if opcao == "1":
            valor = float(input("Digite o valor do depósito: "))
            cliente.realizar_transacao(conta, Deposito(valor))
        elif opcao == "2":
            valor = float(input("Digite o valor do saque: "))
            cliente.realizar_transacao(conta, Saque(valor))
        elif opcao == "3":
            extrato(cliente, conta)
        elif opcao == "0":
            break
        
        
def menu_principal():
    while True:
        clear()
        print("Bem Vindo ao Sys Bank 3.0:")
        print("Cadastrar-se(1)")
        print("Entrar na sua conta(2)")
        print("Sair(0)")
        opcoes =  input("Escolha: ")
        if opcoes == "0":
            print("Programa encerrado.")
            sys.exit()
        elif opcoes == "1":
            cadastro()
        elif opcoes == "2":
            login()


if __name__ == "__main__":
    menu_principal()