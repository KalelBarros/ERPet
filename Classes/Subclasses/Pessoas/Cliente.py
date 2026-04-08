from Pessoa import Pessoa

class Cliente(Pessoa):
    def __init__(self, id, nome, email, telefone, cpf):
        super().__init__(id, nome, email, telefone, cpf)