from Classes.Subclasses.Pessoas.Cliente import Cliente
from Classes.Classes_abstratas.Usuario import Usuario
from Classes.Classes_abstratas.Animal import Animal
from Classes.Subclasses.Servicos.Servico import Servico

class Sistema:

    lista_animais = []
    lista_usuarios = []
    lista_clientes = []
    lista_servicos = []

    @staticmethod
    def Cadastrar(objeto):
        from Classes.Subclasses.Servicos.Servico import Servico
        if isinstance(objeto, Cliente):
            Sistema.lista_clientes.append(objeto)
            print(f"Cliente {objeto.get_nome()} cadastrado com sucesso!")
        elif isinstance(objeto, Usuario):
            Sistema.lista_usuarios.append(objeto)
            print(f"Usuário {objeto.get_nome()} ({type(objeto).__name__}) cadastrado!")
        elif isinstance(objeto, Animal):
            Sistema.lista_animais.append(objeto)
            print(f"Animal {objeto.get_nome()} cadastrado com sucesso!")
        elif isinstance(objeto, Servico):
            Sistema.lista_servicos.append(objeto)
            print(f"Serviço '{objeto.get_tipo()}' registrado com sucesso!")

        else:
            print("Erro: Tipo de objeto desconhecido para o sistema.")

    @staticmethod
    def Editar(lista_alvo, id_alvo, campo, novo_valor):
        # Busca o objeto na lista pelo ID
        objeto = next((obj for obj in lista_alvo if obj.get_id() == id_alvo), None)

        if objeto:
            # Transforma o nome do campo no método setter (ex: 'nome' vira 'set_nome')
            nome_metodo = f"set_{campo}"
            
            if hasattr(objeto, nome_metodo):
                metodo = getattr(objeto, nome_metodo)
                metodo(novo_valor) # Chama o setter da classe
                print(f"Sucesso: {campo} atualizado!")
            else:
                print(f"Erro: Atributo '{campo}' não pode ser editado.")
        else:
            print("Erro: ID não encontrado.")

    @staticmethod
    def Excluir(lista_alvo, id_alvo):
        # Busca o objeto pelo ID na lista fornecida (animais, clientes ou usuarios)
        objeto = next((obj for obj in lista_alvo if obj.get_id() == id_alvo), None)

        if objeto:
            lista_alvo.remove(objeto)
            print(f"Sucesso: Registro com ID {id_alvo} excluído.")
        else:
            print(f"Erro: Registro com ID {id_alvo} não encontrado nesta lista.")
    