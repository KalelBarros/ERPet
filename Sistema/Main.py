import sys
import os

# Adiciona a pasta raiz (ERPet) ao caminho de busca do Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Classes.Subclasses.Animais import *
from Classes.Subclasses.Pessoas import *


def Main():

    Op = 0

    while Op != "6":
        CriarMenu()
        Op = input("Digite a opção desejada: ")

        if Op == "0":
            print("Opção 0 selecionada: Adicionar Usuário, Cliente ou Animal")
            # Aqui você pode adicionar a lógica para cadastrar um novo usuário, cliente ou animal

        elif Op == "1":
            print("Opção 1 selecionada: Listar Usuários, Clientes e Animais")
            # Aqui você pode adicionar a lógica para listar os usuários, clientes e animais cadastrados

        elif Op == "4":
            print("Opção 4 selecionada: Remover Usuário, Cliente ou Animal")
            # Aqui você pode adicionar a lógica para remover um usuário, cliente ou animal

        elif Op == "5":
            print("Opção 5 selecionada: Editar Usuário, Cliente ou Animal")
            # Aqui você pode adicionar a lógica para editar um usuário, cliente ou animal

        elif Op == "6":
            print("Encerrando o programa. Até logo!")
            break

        else:
            LimparTela()
            print("Opção inválida. Por favor, tente novamente.")
            Pausar()
            LimparTela()





    CriarMenu()



def CriarMenu():
    print("=======================\n\tERPet\n=======================\n")
    print("0 - Adicionar Usuário, Cliente ou Animal")
    print("1 - Listar Usuários, Clientes e Animais")
    print("4 - Remover Usuário, Cliente ou Animal")
    print("5 - Editar Usuário, Cliente ou Animal")
    print("6 - Encerrar")

def LimparTela():
    os.system('cls' if os.name == 'nt' else 'clear')

def Pausar():
    input("Pressione Enter para continuar...")


Main()