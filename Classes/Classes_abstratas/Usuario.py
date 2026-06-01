# Classes/Classes_abstratas/Usuario.py
from Classes.Classes_abstratas.Pessoa import Pessoa

class Usuario(Pessoa):
    def __init__(self, id, nome, email, telefone, cpf, senha, is_superuser=False):
        super().__init__(id, nome, email, telefone, cpf)
        self.__senha = senha
        self.__is_superuser = is_superuser

    # Getters próprios — os de Pessoa já são herdados, não precisa redeclarar
    def get_senha(self):            return self.__senha
    def get_is_superuser(self):     return self.__is_superuser

    # Setters
    def set_senha(self, v):         self.__senha = v