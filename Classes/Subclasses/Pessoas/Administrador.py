# Classes/Subclasses/Pessoas/Administrador.py
from Classes.Classes_abstratas.Usuario import Usuario
from Sistema.Sistema import Sistema

class Administrador(Usuario):
    def __init__(self, id, nome, email, telefone, cpf, senha):
        super().__init__(id, nome, email, telefone, cpf, senha, is_superuser=True)

    @staticmethod
    def criar_usuario(usuario_logado=None):
        # Import aqui dentro para evitar importação circular
        from Classes.Subclasses.Pessoas.Funcionario import Funcionario

        id_user = input("ID: ")
        nome = input("Nome: ")
        email = input("Email: ")
        telefone = input("Telefone: ")
        cpf = input("CPF: ")
        senha = input("Senha: ")
        is_admin = input("Será Administrador? (S/N): ")

        if is_admin.upper() == 'S':
            novo_usuario = Administrador(id_user, nome, email, telefone, cpf, senha)
        else:
            novo_usuario = Funcionario(id_user, nome, email, telefone, cpf, senha)

        Sistema.Cadastrar(novo_usuario, usuario_logado)

    @staticmethod
    def excluir_entidade():
        print("O que deseja excluir?\n0 - Usuário\n1 - Cliente\n2 - Animal")
        op = input("Opção: ")
        id_alvo = input("ID a excluir: ")

        if op == "0":
            Sistema.Excluir(Sistema.lista_usuarios, id_alvo)
        elif op == "1":
            Sistema.Excluir(Sistema.lista_clientes, id_alvo)
        elif op == "2":
            Sistema.Excluir(Sistema.lista_animais, id_alvo)
        else:
            print("Opção inválida.")