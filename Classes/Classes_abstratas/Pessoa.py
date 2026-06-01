# Classes/Classes_abstratas/Pessoa.py
from abc import ABC

class Pessoa(ABC):
    def __init__(self, id, nome, email, telefone, cpf):
        self.__id = id
        self.__nome = nome
        self.__email = email
        self.__telefone = telefone
        self.__cpf = cpf

    # Getters
    def get_id(self):           return self.__id
    def get_nome(self):         return self.__nome
    def get_email(self):        return self.__email
    def get_telefone(self):     return self.__telefone
    def get_cpf(self):          return self.__cpf

    # Setters — padrão set_campo()
    def set_nome(self, v):      self.__nome = v
    def set_email(self, v):     self.__email = v
    def set_telefone(self, v):  self.__telefone = v