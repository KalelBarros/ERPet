from Classes.Classes_abstratas.Animal import Animal

class Felino(Animal):
    def __init__(self, id, nome, idade, sexo, raca, peso, cor, historico, id_dono, is_castrado, tipo_pelo):
        super().__init__(id, nome, idade, sexo, raca, peso, cor, historico, id_dono)
        self.__is_castrado = is_castrado  # True / False
        self.__tipo_pelo = tipo_pelo      # curto / longo

    def get_is_castrado(self):      return self.__is_castrado
    def get_tipo_pelo(self):        return self.__tipo_pelo
    def set_is_castrado(self, v):   self.__is_castrado = v
    def set_tipo_pelo(self, p):     self.__tipo_pelo = p

    def exibir_dados(self):
        super().exibir_dados()
        print(f"Castrado: {self.__is_castrado} | Tipo de pelo: {self.__tipo_pelo}")