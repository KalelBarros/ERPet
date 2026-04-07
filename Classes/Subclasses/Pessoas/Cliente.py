from Pessoa import Pessoa

class Usuario(Pessoa):
    def __init__(self, id, nome, email, telefone, cpf, senha):
        super().__init__(id, nome, email, telefone, cpf)