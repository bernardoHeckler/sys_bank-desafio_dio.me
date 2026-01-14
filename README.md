# Criar um sistema bancario

### Desenvolver um novo sistema 2026

## 1 - Versão

- [x] Depósito
- [x] Saque
- [x] Extrato

## Regras

- Deve ser possivel sacar valores Positivos para minha conta bancária;
- Versão 1 - Trabalha apenas com 1 usuário;
- Todos os Depósitos devem ser armazenados em uma variável e exibidos na operação de extrato;
- O sistema deve permitir 3 saques diarios, com limite máximo de 500,00 por saque;
- Caso não tenha saldo, exibir mensagem informativa que não é possivel realizar por falta de saldo;
- Todos os saques devem ser armazenas em uma variavel e exibidos na operação de extrato;
- operação de extrato deve listar todos os depósitos e saques realizados na conta;
- Ao fim da listagem deve mostrar o saldo atual da conta;
- valores exemplo: R$ xx.xx = R$ 1500.45



# Limite de 10 Transações diárias para uma conta

## 2 - Versão

- [x] Registrando datas e horarios nos Saques e Depositos
- [x] Criado o Sistema de Cadastro sendo armazenado a lista de info do usuario
- [x] Criado o Login que pega info do usuario Logado
- [x] Usuario somente realizar até 10 saques diarios, e saques de ate 500 reais
- [x] Criado um verificador de tempo, entao quando atinge o limite diario, o usuario somente pode fazer outro saque novamente no dia seguinte, na mensagem mostra o horario que ele podera efetuar o saque denovo

## Regras

- Opções de poder cadastrar/logar, realizar as transações de deposito/saque e vizualizar seu extrato correspondente, e poder sair/trocar de conta;
- Estabelecer um limite de 10 transações diárias para uma conta;
- Se o Usuário tentar fazer uma transação após atingir o limite, deve ser informado que ele excedeu o número de transações permitidas para aquele dia;
- Mostre o Extrato, a data e hora de todas as alterações.