from Animal import Animal

class Roedor(Animal):
    def __init__(self, id, nome, idade, sexo, raca, peso, cor, historico, id_dono, especie, substrato):
        super().__init__(id, nome, idade, sexo, raca, peso, cor, historico, id_dono)
        self.__especie = especie  
        self.__substrato = substrato 

    def get_especie(self):          return self.__especie
    def get_substrato(self):        return self.__substrato
    def set_especie(self, e):       self.__especie = e
    def set_substrato(self, s):     self.__substrato = s

    def exibir_dados(self):
        super().exibir_dados()
        print(f"Espécie: {self.__especie} | Substrato: {self.__substrato}")