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
    def input_obrigatorio(mensagem):
        """Garante que o utilizador não deixa o campo em branco."""
        while True:
            valor = input(mensagem).strip()
            if valor:
                return valor
            print("Erro: Este campo é obrigatório e não pode ficar vazio.")

    @staticmethod
    def validar_cpf(cpf):
        """Valida se o CPF tem 11 dígitos e não é uma sequência repetida."""
        cpf = re.sub(r'\D', '', cpf)
        if len(cpf) != 11 or cpf == cpf[0] * 11:
            return False
        return True

    def CadastrarCliente():
        print("--- Cadastrar Cliente ---")
        id = Funcionario.input_obrigatorio("Digite o ID do cliente: ")
        nome = Funcionario.input_obrigatorio("Digite o nome do cliente: ")
        email = Funcionario.input_obrigatorio("Digite o email do cliente: ")
        telefone = Funcionario.input_obrigatorio("Digite o telefone do cliente: ")
        
        while True:
            cpf = Funcionario.input_obrigatorio("Digite o CPF do cliente (apenas números): ")
            if Funcionario.validar_cpf(cpf):
                break
            print("Erro: CPF inválido. Certifique-se de que tem 11 dígitos.")

        cliente = Cliente(id, nome, email, telefone, cpf)
        Sistema.Cadastrar(cliente)

    def CadastrarAnimal():
        tipo = Funcionario.input_obrigatorio("Digite o tipo do animal (Canino, Felino, Ave ou Roedor): ")

        if tipo not in ["Canino", "Felino", "Ave", "Roedor"]:
            print("Tipo de animal inválido. Por favor, tente novamente.")
            return
        
        id = Funcionario.input_obrigatorio("Digite o ID do animal: ")
        nome = Funcionario.input_obrigatorio("Digite o nome do animal: ")
        idade = Funcionario.input_obrigatorio("Digite a idade do animal: ")
        sexo = Funcionario.input_obrigatorio("Digite o sexo do animal (M/F): ")
        raca = Funcionario.input_obrigatorio("Digite a raça do animal: ")
        peso = Funcionario.input_obrigatorio("Digite o peso do animal: ")
        cor = Funcionario.input_obrigatorio("Digite a cor do animal: ")
        historico = Funcionario.input_obrigatorio("Digite o histórico do animal: ")
        id_dono = Funcionario.input_obrigatorio("Digite o ID do dono do animal: ")

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

            animal = Felino(id, nome, idade, sexo, raca, peso, cor, historico, id_dono, is_castrado, tipo_pelo)
            Sistema.Cadastrar(animal)

        elif tipo == "Ave":
            anilha = input("Digite o número da anilha da ave: ")
            is_asas_cortadas = input("A ave tem asas cortadas? (Sim/Não): ")

            animal = Ave(id, nome, idade, sexo, raca, peso, cor, historico, id_dono, anilha, is_asas_cortadas)
            Sistema.Cadastrar(animal)

        elif tipo == "Roedor":
            tipo_roedor = input("Digite o tipo do roedor (Hamster, Porquinho-da-índia, Rato, Camundongo): ")

            animal = Roedor(id, nome, idade, sexo, raca, peso, cor, historico, id_dono, especie, substrato)
            Sistema.Cadastrar(animal)

            
    def CadastrarServico():
        print("--- Cadastrar Serviço (Banho/Tosa) ---")
        id_servico = input("Digite o ID do serviço: ")
        
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

        # Importação local para evitar importação circular
        from Classes.Subclasses.Servicos.Servico import Servico
        novo_servico = Servico(id_servico, tipo, preco, id_animal, id_funcionario)

        from Sistema.Sistema import Sistema
        Sistema.Cadastrar(novo_servico)
    
