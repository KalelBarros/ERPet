from abc import ABC

class Pessoa(ABC):
    def __init__(self, id, nome, email, telefone, cpf):
        self.__id = id
        self.__nome = nome
        self.__email = email
        self.__telefone = telefone
        self.__cpf = cpf


    def get_id(self): return self.__id

    def get_nome(self):
        return self.__nome

    def nome(self, value):
        self.__nome = value

    def get_email(self):
        return self.__email

    def email(self, value):
        self.__email = value

    def get_telefone(self):
        return self.__telefone

    def telefone(self, value):
        self.__telefone = value

    def get_cpf(self):
        return self.__cpf
        
    def cpf(self, value):
        self.__cpf = value