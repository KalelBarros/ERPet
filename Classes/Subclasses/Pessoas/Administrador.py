from Usuario import Usuario

class Administrador(Usuario):
    def __init__(self, id, nome, email, telefone, cpf, senha):
        super().__init__(id, nome, email, telefone, cpf, senha, is_superuser=True)

    def criar_usuario(self, id, nome, email, telefone, cpf, senha):
        return Usuario(id, nome, email, telefone, cpf, senha)

    def excluir_usuario(self, usuario):
        # Lógica para excluir um usuário do sistema
        pass

    

