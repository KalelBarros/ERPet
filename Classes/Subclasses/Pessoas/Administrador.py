from Classes.Classes_abstratas.Pessoa import Pessoa
from Classes.Subclasses.Pessoas.Funcionario import Funcionario
from Classes.Classes_abstratas.Usuario import Usuario
from Sistema.Sistema import Sistema


class Administrador(Usuario):
    def __init__(self, id, nome, email, telefone, cpf, senha):
        super().__init__(id, nome, email, telefone, cpf, senha, is_superuser=True)
        
    def criar_usuario():
        id_user = input("Digite o ID: ")
        nome = input("Digite o nome: ")
        email = input("Digite o email: ")
        telefone = input("Digite o telefone: ")
  
        while True:
            cpf = Funcionario.input_obrigatorio("Digite o CPF do cliente (apenas números): ")
            if Pessoa.validar_cpf(cpf):
                break
            print("Erro: CPF inválido. Certifique-se de que tem 11 dígitos.")
         
        senha = input("Digite a senha: ")
        is_admin = input("O usuário será um Administrador? (S/N): ")
        
        #validar se há campos vazios
        if not all([id_user, nome, email, telefone, cpf, senha]):
            print("Erro: Todos os campos são obrigatórios. Por favor, preencha todos os campos.")
            return

        if is_admin.upper() == 'S':
            novo_usuario = Administrador(id_user, nome, email, telefone, cpf, senha)
        else:
            novo_usuario = Funcionario(id_user, nome, email, telefone, cpf, senha)
            
        Sistema.Cadastrar(novo_usuario)

    def excluir_entidade():
        print("O que deseja excluir? (0 - Usuário, 1 - Cliente, 2 - Animal)")
        op = input("Digite a opção: ")
        
        id = input("Digite o ID a ser excluído: ")
        if op == "0":
            Sistema.Excluir(Sistema.lista_usuarios, id)
        elif op == "1":
            Sistema.Excluir(Sistema.lista_clientes, id)
        elif op == "2":
            Sistema.Excluir(Sistema.lista_animais, id)
