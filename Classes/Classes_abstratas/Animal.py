from abc import ABC, abstractmethod

class Animal(ABC):

    def __init__(self, id, nome, idade, sexo, raca, peso, cor, historico, id_dono):
        self.__id = id
        self.__nome = nome
        self.__idade = idade
        self.__sexo = sexo
        self.__raca = raca
        self.__peso = peso
        self.__cor = cor
        self.__historico = historico
        self.__id_dono = id_dono

    # Getters
    def get_id(self):           return self.__id
    def get_nome(self):         return self.__nome
    def get_idade(self):        return self.__idade
    def get_sexo(self):         return self.__sexo
    def get_raca(self):         return self.__raca
    def get_peso(self):         return self.__peso
    def get_cor(self):          return self.__cor
    def get_historico(self):    return self.__historico
    def get_id_dono(self):      return self.__id_dono

    # Setters
    def set_nome(self, v):      self.__nome = v
    def set_idade(self, v):     self.__idade = v
    def set_peso(self, v):      self.__peso = v
    def set_historico(self, v): self.__historico = v
    def set_raca(self, v):      self.__raca = v
    def set_cor(self, v):       self.__cor = v

    def exibir_dados(self):
        print(f"ID: {self.__id} | Nome: {self.__nome} | Idade: {self.__idade} anos")
        print(f"Sexo: {self.__sexo} | Raça: {self.__raca} | Peso: {self.__peso}kg | Cor: {self.__cor}")
        print(f"Histórico: {self.__historico} | ID Dono: {self.__id_dono}")