# Estoque.py
class Estoque:
    def __init__(self, id, nome, categoria, quantidade, preco_unitario, qtd_minima):
        self.__id = id
        self.__nome = nome
        self.__categoria = categoria      # racao / remedio / higiene / acessorio
        self.__quantidade = quantidade
        self.__preco_unitario = preco_unitario
        self.__qtd_minima = qtd_minima

    # Getters
    def get_id(self):               return self.__id
    def get_nome(self):             return self.__nome
    def get_categoria(self):        return self.__categoria
    def get_quantidade(self):       return self.__quantidade
    def get_preco_unitario(self):   return self.__preco_unitario
    def get_qtd_minima(self):       return self.__qtd_minima

    # Setters
    def set_nome(self, v):          self.__nome = v
    def set_categoria(self, v):     self.__categoria = v
    def set_quantidade(self, v):    self.__quantidade = v
    def set_preco_unitario(self, v):self.__preco_unitario = v
    def set_qtd_minima(self, v):    self.__qtd_minima = v

    def baixar_estoque(self, qtd):
        if qtd > self.__quantidade:
            print(f"⚠ Estoque insuficiente de '{self.__nome}'!")
            return False
        self.__quantidade -= qtd
        print(f"✔ Baixa de {qtd} unidade(s) de '{self.__nome}'. Restam: {self.__quantidade}")
        return True

    def verificar_alerta(self):
        if self.__quantidade <= self.__qtd_minima:
            print(f"⚠ ALERTA: '{self.__nome}' abaixo do mínimo! Quantidade atual: {self.__quantidade}")

    def exibir_dados(self):
        print(f"ID: {self.__id} | Produto: {self.__nome} | Categoria: {self.__categoria}")
        print(f"Quantidade: {self.__quantidade} | Preço unitário: R${self.__preco_unitario:.2f} | Mínimo: {self.__qtd_minima}")