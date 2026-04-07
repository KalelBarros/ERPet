from Pessoa import Pessoa

class Usuario(Pessoa):
    def __init__(self, id, nome, email, telefone, cpf, senha, is_superuser=False):
        super().__init__(id, nome, email, telefone, cpf)
        self.__senha = senha
        self.__is_superuser = is_superuser

    def get_senha(self):
        return self.__senha

    def senha(self, value):
        self.__senha = value

    def get_is_superuser(self):
        return self.__is_superuser
