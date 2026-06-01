# Classes/Subclasses/Pessoas/Funcionario.py
from Classes.Classes_abstratas.Usuario import Usuario
from Classes.Subclasses.Pessoas.Cliente import Cliente
from Classes.Subclasses.Animais.Canino import Canino
from Classes.Subclasses.Animais.Felino import Felino
from Classes.Subclasses.Animais.Ave import Ave
from Classes.Subclasses.Animais.Roedor import Roedor
from Sistema.Sistema import Sistema

class Funcionario(Usuario):
    def __init__(self, id, nome, email, telefone, cpf, senha):
        super().__init__(id, nome, email, telefone, cpf, senha, is_superuser=False)

    @staticmethod
    def CadastrarCliente(usuario_logado=None):
        id = input("ID do cliente: ")
        nome = input("Nome: ")
        email = input("Email: ")
        telefone = input("Telefone: ")
        cpf = input("CPF: ")
        endereco = input("Endereço: ")

        cliente = Cliente(id, nome, email, telefone, cpf, endereco)
        Sistema.Cadastrar(cliente, usuario_logado)

    @staticmethod
    def CadastrarAnimal(usuario_logado=None):
        tipo = input("Tipo do animal (Canino / Felino / Ave / Roedor): ").strip()

        if tipo not in ["Canino", "Felino", "Ave", "Roedor"]:
            print("Tipo inválido.")
            return

        id = input("ID: ")
        nome = input("Nome: ")
        idade = int(input("Idade: "))
        sexo = input("Sexo (M/F): ")
        raca = input("Raça: ")
        peso = float(input("Peso (kg): "))
        cor = input("Cor: ")
        historico = input("Histórico: ")
        id_dono = input("ID do dono: ")

        if tipo == "Canino":
            porte = input("Porte (Pequeno/Médio/Grande): ")
            is_vacinado = input("Vacinado? (Sim/Não): ")
            is_castrado = input("Castrado? (Sim/Não): ")
            tipo_pelo = input("Tipo de pelo (Curto/Médio/Longo): ")
            animal = Canino(id, nome, idade, sexo, raca, peso, cor, historico,
                           id_dono, porte, is_vacinado, is_castrado, tipo_pelo)

        elif tipo == "Felino":
            is_castrado = input("Castrado? (Sim/Não): ")
            tipo_pelo = input("Tipo de pelo (Curto/Longo): ")
            animal = Felino(id, nome, idade, sexo, raca, peso, cor, historico,
                           id_dono, is_castrado, tipo_pelo)

        elif tipo == "Ave":
            anilha = input("Número da anilha: ")
            is_asas_cortadas = input("Asas cortadas? (Sim/Não): ")
            animal = Ave(id, nome, idade, sexo, raca, peso, cor, historico,
                        id_dono, anilha, is_asas_cortadas)

        elif tipo == "Roedor":
            especie = input("Espécie (Hamster/Coelho/Porquinho): ")
            substrato = input("Substrato (Maravalha/Papel/Serragem): ")
            animal = Roedor(id, nome, idade, sexo, raca, peso, cor, historico,
                           id_dono, especie, substrato)

        Sistema.Cadastrar(animal, usuario_logado)
