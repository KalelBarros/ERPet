from Classes.Classes_abstratas.Pessoa import Pessoa 

class Usuario(Pessoa):
    def __init__(self, id, nome, email, telefone, cpf, senha, is_superuser=False):
        super().__init__(id, nome, email, telefone, cpf)
        self.__senha = senha
        self.__is_superuser = is_superuser


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

    def get_senha(self):
        return self.__senha

    def senha(self, value):
        self.__senha = value

    def get_is_superuser(self):
        return self.__is_superuser
