import sys
import os

# Adiciona a pasta raiz (ERPet) ao caminho de busca do Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Classes.Subclasses.Animais import *
from Classes.Subclasses.Pessoas import *
from Sistema import Sistema

def Main():
    
    Op = -1

    while Op != "4":
        LimparTela()
        CriarMenuPrincipal()
        Op = input("\nDigite a opção desejada: ")
         
        LimparTela()


        if Op == "0":
            CriarMenuCadastrar()

        elif Op == "1":
            pass

        elif Op == "2":
            pass

        elif Op == "3":
            pass

        elif Op == "4":
            print("Encerrando o programa. Até logo!")
            break

        else:
            print("Opção inválida. Por favor, tente novamente.")
            Pausar()
            LimparTela()



def CriarMenuCadastrar():

    opCadastrar = -1

    print("=======================\n\tCadastrar\n=======================\n")
    print("0 - Cadastrar Usuário")
    print("1 - Cadastrar Cliente")
    print("2 - Cadastrar Animal")
    print("3 - Cadastrar Servico")
    opCadastrar = input("\nDigite o que deseja cadastrar: ")

    if opCadastrar == "0":
       adm = input("\nvocê é um administrador? S/N ")
       if adm == 's' or adm == 'S':
        Administrador.criar_usuario()
       else:
         return "você não tem autorização para adicionar um usuario" 
    elif opCadastrar == "1":
        us = input("\nvocê é um funcionario? S/N ")
        if us == 's' or us == 'S':
            Funcionario.CadastrarCliente()
        else:
            return "você não tem autorização para adicionar um cliente" 
    elif opCadastrar == "2":
        us = input("\nvocê é um funcionario? S/N ")
        if us == 's' or us == 'S':
           Funcionario.CadastrarAnimal()
        else:
            return "você não tem autorização para adicionar um animal" 
    elif opCadastrar == "2":
        us = input("\nvocê é um funcionario? S/N ")
        if us == 's' or us == 'S':
           Funcionario.Cadastrar()
        else:
             return "você não tem autorização para adicionar um serviço" 
def Listar():
    print("=======================\n\tListar\n=======================\n")
    print("0 - Listar Usuários")
    print("1 - Listar Clientes")
    print("2 - Listar Animais")
    print("3 - Listar Serviços")
    
    opListar = input("\nDigite o que deseja listar: ")
    
    LimparTela()
    
    if opListar == "0":
        print("Lista de Usuários")
        if len(Sistema.lista_usuarios) == 0:
            print("Nenhum usuário cadastrado no sistema.")
        else:
            for usuario in Sistema.lista_usuarios:
                print(f"ID: {usuario.get_id()} | Nome: {usuario.get_nome()} | E-mail: {usuario.get_email()} | Tipo: {type(usuario).__name__}")
                
    elif opListar == "1":
        print("Lista de Clientes")
        if len(Sistema.lista_clientes) == 0:
            print("Nenhum cliente cadastrado no sistema.")
        else:
            for cliente in Sistema.lista_clientes:
                print(f"ID: {cliente.get_id()} | Nome: {cliente.get_nome()} | E-mail: {cliente.get_email()} | CPF: {cliente.get_cpf()}")
                
    elif opListar == "2":
        print("Lista de Animais")
        if len(Sistema.lista_animais) == 0:
            print("Nenhum animal cadastrado no sistema.")
        else:
            for animal in Sistema.lista_animais:
                animal.exibir_dados()
                print("-" * 50)
                
    elif opListar == "3":
        print("Lista de Serviços ")
        if len(Sistema.lista_servicos) == 0:
            print("Nenhum serviço registrado no sistema.")
        else:
            for servico in Sistema.lista_servicos:
                servico.exibir_dados()
                print("-" * 50)
                
    else:
        print("Opção inválida. Por favor, tente novamente.")
        
    Pausar()

def Remover():
    print("=======================\n\tRemover\n=======================\n")
    print("0 - Remover Usuário")
    print("1 - Remover Cliente")
    print("2 - Remover Animal")
    
    opRemover = input("\nEscolha o que deseja remover: ")
    LimparTela()
    
    if opRemover == "0":
        adm = input("Você é um administrador? S/N ")
        if adm == 's'  or adm == 'S':
            Administrador.excluir_usuario()
        else:
            print("Erro: Apenas administradores têm permissão para excluir usuários.")
    
    elif opRemover == "1":
        print("--- Remover Cliente ---")
        id_cliente = input("Digite o ID do cliente a remover: ")
        Sistema.Excluir(Sistema.lista_clientes, id_cliente)
        
    elif opRemover == "2":
        print("--- Remover Animal ---")
        id_animal = input("Digite o ID do animal a remover: ")
        Sistema.Excluir(Sistema.lista_animais, id_animal)
        
    else:
        print("Opção inválida. Por favor, tente novamente.")

    Pausar()

def remover():
    

def CriarMenuPrincipal():
    print("=======================\n\tERPet\n=======================\n")
    print("0 - Cadastrar")
    print("1 - Listar")
    print("2 - Remover")
    print("3 - Editar")
    print("4 - Encerrar Programa")

def LimparTela():
    os.system('cls' if os.name == 'nt' else 'clear')

def Pausar():
    input("Pressione Enter para continuar...")