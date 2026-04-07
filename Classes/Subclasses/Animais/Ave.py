from Animal import Animal

class Ave(Animal):
    def __init__(self, id, nome, idade, sexo, raca, peso, cor, historico, id_dono, anilha, is_asas_cortadas):
        super().__init__(id, nome, idade, sexo, raca, peso, cor, historico, id_dono)
        self.__anilha = anilha
        self.__is_asas_cortadas = is_asas_cortadas  

    def get_anilha(self):               return self.__anilha
    def get_is_asas_cortadas(self):     return self.__is_asas_cortadas
    def set_anilha(self, a):            self.__anilha = a
    def set_is_asas_cortadas(self, v):  self.__is_asas_cortadas = v

    def exibir_dados(self):
        super().exibir_dados()
        print(f"Anilha: {self.__anilha} | Asas cortadas: {self.__is_asas_cortadas}")
