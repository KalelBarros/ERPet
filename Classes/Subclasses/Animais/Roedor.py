# Classes/Subclasses/Animais/Roedor.py
from Classes.Classes_abstratas.Animal import Animal

class Roedor(Animal):
    def __init__(self, id, nome, idade, sexo, raca, peso, cor, historico, id_dono,
                 especie, substrato):
        super().__init__(id, nome, idade, sexo, raca, peso, cor, historico, id_dono)
        self.__especie = especie
        self.__substrato = substrato

    # Getters
    def get_especie(self):      return self.__especie
    def get_substrato(self):    return self.__substrato

    # Setters
    def set_especie(self, v):   self.__especie = v
    def set_substrato(self, v): self.__substrato = v

    def exibir_dados(self):
        super().exibir_dados()
        print(f"Espécie: {self.__especie} | Substrato: {self.__substrato}")