import sys
import os

# Adiciona a pasta raiz (ERPet) ao caminho de busca do Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Classes.Subclasses.Animais import *
from Classes.Subclasses.Pessoas import *


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
       if resposta == 's' or resposta == 'S':
         criar_usuario()
       else:
         return "você não tem autorização para adicionar um usuario" 
    elif opCadastrar == "1"
        us = input("\nvocê é um funcionario? S/N ")
        if resposta == 's' or resposta == 'S':
            CadastrarCliente()
        else:
            return "você não tem autorização para adicionar um cliente" 
     elif opCadastrar == "2"
        us = input("\nvocê é um funcionario? S/N ")
        if resposta == 's' or resposta == 'S':
            CadastrarAnimal()
        else:
            return "você não tem autorização para adicionar um animal" 
            
       


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

def Listar():

Main()