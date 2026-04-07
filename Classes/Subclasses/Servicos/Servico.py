# Servico.py
from datetime import datetime

class Servico:
    def __init__(self, id, tipo, preco, id_animal, id_funcionario):
        self.__id = id
        self.__tipo = tipo                          # banho / tosa / banho+tosa / vacina
        self.__preco = preco
        self.__data_hora = datetime.now()
        self.__id_animal = id_animal
        self.__id_funcionario = id_funcionario
        self.__produtos_usados = []                 # lista de tuplas (Estoque, qtd)

    # Getters
    def get_id(self):               return self.__id
    def get_tipo(self):             return self.__tipo
    def get_preco(self):            return self.__preco
    def get_data_hora(self):        return self.__data_hora
    def get_id_animal(self):        return self.__id_animal
    def get_id_funcionario(self):   return self.__id_funcionario
    def get_produtos_usados(self):  return self.__produtos_usados

    # Setters
    def set_tipo(self, v):          self.__tipo = v
    def set_preco(self, v):         self.__preco = v

    def adicionar_produto(self, produto_estoque, qtd):
        # Adiciona um produto à lista antes de registrar o serviço
        self.__produtos_usados.append((produto_estoque, qtd))

    def calcular_total(self):
        total_produtos = sum(
            p.get_preco_unitario() * qtd
            for p, qtd in self.__produtos_usados
        )
        return self.__preco + total_produtos

    def registrar_servico(self):
        # Faz a baixa automática de cada produto usado
        for produto, qtd in self.__produtos_usados:
            sucesso = produto.baixar_estoque(qtd)
            if sucesso:
                produto.verificar_alerta()
        print(f"✔ Serviço '{self.__tipo}' registrado! Total: R${self.calcular_total():.2f}")

    def exibir_dados(self):
        print(f"ID: {self.__id} | Tipo: {self.__tipo} | Data: {self.__data_hora.strftime('%d/%m/%Y %H:%M')}")
        print(f"Animal ID: {self.__id_animal} | Funcionário ID: {self.__id_funcionario}")
        print(f"Preço base: R${self.__preco:.2f} | Total: R${self.calcular_total():.2f}")