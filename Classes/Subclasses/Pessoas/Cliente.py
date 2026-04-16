
from Classes.Classes_abstratas.Pessoa import Pessoa 

class Cliente(Pessoa):
    def __init__(self, id, nome, email, telefone, cpf):
        super().__init__(id, nome, email, telefone, cpf)

    def get_id(self):
        return super().get_id()
    
    def get_nome(self):
        return super().get_nome()
    
    def get_email(self):
        return super().get_email()
    
    def get_telefone(self):
        return super().get_telefone()
    
    def get_cpf(self):
        return super().get_cpf()