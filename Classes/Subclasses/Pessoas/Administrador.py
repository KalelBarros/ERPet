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
        cpf = input("Digite o CPF: ")
        senha = input("Digite a senha: ")
        is_admin = input("O usuário será um Administrador? (S/N): ")
        
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
