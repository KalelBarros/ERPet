from abc import ABC

class Animal(ABC):

    def __init__(self, id, nome, idade, sexo, raca, peso, cor, historico,id_dono):
        self.__id = id
        self.__nome = nome
        self.__idade = idade
        self.__sexo = sexo
        self.__raca = raca
        self.__peso = peso
        self.__cor = cor
        self.__historico = historico
        self.__id_dono = id_dono

    def get_id(self):       return self.__id
    def get_nome(self):     return self.__nome
    def get_idade(self):    return self.__idade
    def get_sexo(self):     return self.__sexo
    def get_raca(self):     return self.__raca
    def get_peso(self):     return self.__peso
    def get_cor(self):      return self.__cor
    def get_historico(self):return self.__historico
    def get_id_dono(self):  return self.__id_dono

    def set_nome(self, nome):         self.__nome = nome
    def set_idade(self, idade):       self.__idade = idade
    def set_peso(self, peso):         self.__peso = peso
    def set_historico(self, h):       self.__historico = h

    def exibir_dados(self):
        print(f"ID: {self.__id} | Nome: {self.__nome} | Idade: {self.__idade} anos")
        print(f"Sexo: {self.__sexo} | Raça: {self.__raca} | Peso: {self.__peso}kg | Cor: {self.__cor}")
        print(f"Histórico: {self.__historico} | ID Dono: {self.__id_dono}")



        