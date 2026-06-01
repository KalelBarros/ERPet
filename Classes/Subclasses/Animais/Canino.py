# Classes/Subclasses/Animais/Canino.py
from Classes.Classes_abstratas.Animal import Animal

class Canino(Animal):
    def __init__(self, id, nome, idade, sexo, raca, peso, cor, historico, id_dono,
                 porte, is_vacinado, is_castrado, tipo_pelo):
        super().__init__(id, nome, idade, sexo, raca, peso, cor, historico, id_dono)
        self.__porte = porte
        self.__is_vacinado = is_vacinado
        self.__is_castrado = is_castrado
        self.__tipo_pelo = tipo_pelo

    # Getters
    def get_porte(self):            return self.__porte
    def get_is_vacinado(self):      return self.__is_vacinado
    def get_is_castrado(self):      return self.__is_castrado
    def get_tipo_pelo(self):        return self.__tipo_pelo

    # Setters
    def set_porte(self, v):         self.__porte = v
    def set_is_vacinado(self, v):   self.__is_vacinado = v
    def set_is_castrado(self, v):   self.__is_castrado = v
    def set_tipo_pelo(self, v):     self.__tipo_pelo = v

    def exibir_dados(self):
        super().exibir_dados()
        print(f"Porte: {self.__porte} | Vacinado: {self.__is_vacinado} | "
              f"Castrado: {self.__is_castrado} | Tipo Pelo: {self.__tipo_pelo}")