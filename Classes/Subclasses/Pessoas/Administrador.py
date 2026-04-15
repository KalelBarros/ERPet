from Usuario import Usuario
from Sistema import Sistema

class Administrador(Usuario):
    def __init__(self, id, nome, email, telefone, cpf, senha):
        super().__init__(id, nome, email, telefone, cpf, senha, is_superuser=True)
        
    def criar_usuario(self, id, nome, email, telefone, cpf, senha):
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
        Pausar()

    def excluir_usuario(self, usuario):
        # Lógica para excluir um usuário do sistema
        pass

    