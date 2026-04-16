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
    

    def CadastrarCliente():

        id = input("Digite o ID do cliente: ")
        nome = input("Digite o nome do cliente: ")
        email = input("Digite o email do cliente: ")
        telefone = input("Digite o telefone do cliente: ")
        cpf = input("Digite o CPF do cliente: ")

        cliente = Cliente(id, nome, email, telefone, cpf)
        Sistema.Cadastrar(cliente)

    def CadastrarAnimal():

        tipo = input("Digite o tipo do animal (Canino, Felino, Ave ou Roedor): ")

        if tipo not in ["Canino", "Felino", "Ave", "Roedor"]:
            print("Tipo de animal inválido. Por favor, tente novamente.")
            return
        
        id = input("Digite o ID do animal: ")
        nome = input("Digite o nome do animal: ")
        idade = input("Digite a idade do animal: ")
        sexo = input("Digite o sexo do animal (M/F): ")
        raca = input("Digite a raça do animal: ")
        peso = input("Digite o peso do animal: ")
        cor = input("Digite a cor do animal: ")
        historico = input("Digite o histórico do animal: ")
        id_dono = input("Digite o ID do dono do animal: ")

        if tipo == "Canino":
            porte = input("Digite o porte do canino (Pequeno, Médio, Grande): ")
            is_vacinado = input("O canino é vacinado? (Sim/Não): ")
            is_castrado = input("O canino é castrado? (Sim/Não): ")
            tipo_pelo = input("Digite o tipo de pelo do canino (Curto, Médio, Longo): ")

            animal = Canino(id, nome, idade, sexo, raca, peso, cor, historico, id_dono, porte, is_vacinado, is_castrado, tipo_pelo)
            Sistema.Cadastrar(animal)

        elif tipo == "Felino":
            porte = input("Digite o porte do felino (Pequeno, Médio, Grande): ")
            is_vacinado = input("O felino é vacinado? (Sim/Não): ")
            is_castrado = input("O felino é castrado? (Sim/Não): ")
            tipo_pelo = input("Digite o tipo de pelo do felino (Curto, Médio, Longo): ")

            animal = Felino(id, nome, idade, sexo, raca, peso, cor, historico, id_dono, porte, is_vacinado, is_castrado, tipo_pelo)
            Sistema.Cadastrar(animal)

        elif tipo == "Ave":
            anilha = input("Digite o número da anilha da ave: ")
            is_asas_cortadas = input("A ave tem asas cortadas? (Sim/Não): ")

            animal = Ave(id, nome, idade, sexo, raca, peso, cor, historico, id_dono, anilha, is_asas_cortadas)
            Sistema.Cadastrar(animal)

        elif tipo == "Roedor":
            tipo_roedor = input("Digite o tipo do roedor (Hamster, Porquinho-da-índia, Rato, Camundongo): ")

            animal = Roedor(id, nome, idade, sexo, raca, peso, cor, historico, id_dono, tipo_roedor)
            Sistema.Cadastrar(animal)
    def CadastrarServico():
        print("--- Cadastrar Serviço (Banho/Tosa) ---")
        id_servico = input("Digite o ID do serviço: ")
        
        # Define as opções de tipo conforme solicitado
        print("Tipos disponíveis: 1 - Banho, 2 - Tosa, 3 - Banho e Tosa")
        op_tipo = input("Escolha o tipo: ")
        if op_tipo == "1":
            tipo = "Banho"
        elif op_tipo == "2":
            tipo = "Tosa"
        else:
            tipo = "Banho e Tosa"

        preco = float(input("Digite o preço do serviço: "))
        id_animal = input("Digite o ID do animal: ")
        id_funcionario = input("Digite o ID do funcionário: ")

        # Cria o objeto de serviço sem a lógica de produtos adicionais
        from Classes.Subclasses.Servicos.Servico import Servico
        novo_servico = Servico(id_servico, tipo, preco, id_animal, id_funcionario)

        # Registra o serviço e salva no sistema
        print(f"✔ Serviço '{tipo}' registrado com sucesso!")
        Sistema.Cadastrar(novo_servico)

    
