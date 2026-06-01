# Classes/Subclasses/Pessoas/Cliente.py
from Classes.Classes_abstratas.Pessoa import Pessoa

class Cliente(Pessoa):
    def __init__(self, id, nome, email, telefone, cpf, endereco=""):
        super().__init__(id, nome, email, telefone, cpf)
        self.__endereco = endereco
        self.__lista_animais = []   # IDs dos animais vinculados

    # Getter e setter do que é exclusivo de Cliente
    def get_endereco(self):             return self.__endereco
    def set_endereco(self, v):          self.__endereco = v

    def get_lista_animais(self):        return self.__lista_animais

    def adicionar_animal(self, id_animal):
        self.__lista_animais.append(id_animal)

    def exibir_dados(self):
        print(f"ID: {self.get_id()} | Nome: {self.get_nome()} | CPF: {self.get_cpf()}")
        print(f"Email: {self.get_email()} | Telefone: {self.get_telefone()} | Endereço: {self.__endereco}")