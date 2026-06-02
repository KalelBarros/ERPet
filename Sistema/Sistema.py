# Sistema/Sistema.py
from Classes.Subclasses.Pessoas.Cliente import Cliente
from Classes.Classes_abstratas.Usuario import Usuario
from Classes.Classes_abstratas.Animal import Animal

from Classes.Subclasses.Animais.Canino import Canino
from Classes.Subclasses.Animais.Felino import Felino
from Classes.Subclasses.Animais.Ave import Ave
from Classes.Subclasses.Animais.Roedor import Roedor
import Banco.banco as banco

from Classes.Subclasses.Servicos.Servico import Servico
import Main

class Sistema:

    lista_animais  = []
    lista_usuarios = []
    lista_clientes = []
    lista_servicos = []
    lista_estoque  = []

    # ═══════════════════════════════════════════════
    # INICIALIZAÇÃO — carrega o banco na memória
    # ═══════════════════════════════════════════════

    @staticmethod
    def inicializar():
        """Cria as tabelas e carrega todos os dados do banco para memória."""
        banco.criar_tabelas()
        Sistema._carregar_usuarios()
        Sistema._carregar_clientes()
        Sistema._carregar_animais()

    @staticmethod
    def _carregar_usuarios():
        """Reconstrói os objetos Usuario a partir do banco."""
        from Classes.Subclasses.Pessoas.Administrador import Administrador
        from Classes.Subclasses.Pessoas.Funcionario import Funcionario

        Sistema.lista_usuarios.clear()
        for row in banco.listar_usuarios():
            id, nome, email, telefone, cpf, senha, is_superuser = row
            if is_superuser:
                obj = Administrador(id, nome, email, telefone, cpf, senha)
            else:
                obj = Funcionario(id, nome, email, telefone, cpf, senha)
            Sistema.lista_usuarios.append(obj)

    @staticmethod
    def _carregar_clientes():
        """Reconstrói os objetos Cliente a partir do banco."""
        from Classes.Subclasses.Pessoas.Cliente import Cliente

        Sistema.lista_clientes.clear()
        for row in banco.listar_clientes():
            id, nome, email, telefone, cpf, endereco = row
            obj = Cliente(id, nome, email, telefone, cpf, endereco or "")
            Sistema.lista_clientes.append(obj)

    @staticmethod
    def _carregar_animais():
        """Reconstrói os objetos Animal a partir do banco."""
        Sistema.lista_animais.clear()
        for row in banco.listar_animais():
            (id, nome, idade, sexo, raca, peso, cor, historico, id_dono, tipo,
             porte, is_vacinado, is_castrado, tipo_pelo,
             anilha, is_asas_cortadas,
             especie, substrato) = row

            if tipo == "Canino":
                obj = Canino(id, nome, idade, sexo, raca, peso, cor, historico,
                             id_dono, porte, is_vacinado, is_castrado, tipo_pelo)
            elif tipo == "Felino":
                obj = Felino(id, nome, idade, sexo, raca, peso, cor, historico,
                             id_dono, is_castrado, tipo_pelo)
            elif tipo == "Ave":
                obj = Ave(id, nome, idade, sexo, raca, peso, cor, historico,
                          id_dono, anilha, is_asas_cortadas)
            elif tipo == "Roedor":
                obj = Roedor(id, nome, idade, sexo, raca, peso, cor, historico,
                             id_dono, especie, substrato)
            else:
                continue

            Sistema.lista_animais.append(obj)

    # ═══════════════════════════════════════════════
    # CADASTRAR
    # ═══════════════════════════════════════════════

    @staticmethod
    def Cadastrar(objeto, usuario_logado=None):
        """Salva o objeto na memória e no banco, e registra o log de forma segura."""
        from Classes.Subclasses.Servicos.Servico import Servico

        # Define qual usuário usar para o Log (usa o passado por parâmetro ou o global do Main)
        usuario_acao = usuario_logado or Main.usuario_logado

        if isinstance(objeto, Cliente):
            Sistema.lista_clientes.append(objeto)
            banco.inserir_cliente(objeto)
            if usuario_acao:
                banco.inserir_log(
                    usuario_acao.get_nome(),
                    f"Cadastro de cliente: {objeto.get_nome()}"
                )
            print(f"✔ Cliente '{objeto.get_nome()}' cadastrado com sucesso!")

        elif isinstance(objeto, Usuario):
            Sistema.lista_usuarios.append(objeto)
            banco.inserir_usuario(objeto)
            if usuario_acao:
                banco.inserir_log(
                    usuario_acao.get_nome(),
                    f"Cadastro de usuário: {objeto.get_nome()} ({type(objeto).__name__})"
                )
            print(f"✔ Usuário '{objeto.get_nome()}' ({type(objeto).__name__}) cadastrado!")

        elif isinstance(objeto, Animal):
            Sistema.lista_animais.append(objeto)
            banco.inserir_animal(objeto)
            if usuario_acao:
                banco.inserir_log(
                    usuario_acao.get_nome(),
                    f"Cadastro de animal: {objeto.get_nome()} ({type(objeto).__name__})"
                )
            print(f"✔ Animal '{objeto.get_nome()}' cadastrado com sucesso!")

        elif isinstance(objeto, Servico):
            Sistema.lista_servicos.append(objeto)
            print(f"Serviço '{objeto.get_tipo()}' registrado com sucesso!")
            
        else:
            print("Erro: Tipo de objeto desconhecido.")

    # ═══════════════════════════════════════════════
    # EDITAR
    # ═══════════════════════════════════════════════

    @staticmethod
    def Editar(lista_alvo, id_alvo, setter_nome, novo_valor, usuario_logado=None):
        """Atualiza o objeto na memória e no banco."""
        objeto = next((obj for obj in lista_alvo if obj.get_id() == id_alvo), None)

        if not objeto:
            print(f"Erro: ID '{id_alvo}' não encontrado.")
            return

        # Atualiza na memória via setter
        setter = getattr(objeto, setter_nome, None)
        if not callable(setter):
            print(f"Erro: Setter '{setter_nome}' não existe.")
            return

        setter(novo_valor)

        # Mapeia setter → campo no banco
        mapa_campos = {
            "set_nome":      "nome",
            "set_email":     "email",
            "set_telefone":  "telefone",
            "set_endereco":  "endereco",
            "set_peso":      "peso",
            "set_historico": "historico",
            "set_raca":      "raca",
            "set_cor":       "cor",
            "set_idade":     "idade",
        }

        campo_banco = mapa_campos.get(setter_nome)
        if campo_banco:
            if isinstance(objeto, Cliente):
                banco.editar_cliente(id_alvo, campo_banco, novo_valor)
            elif isinstance(objeto, Animal):
                banco.editar_animal(id_alvo, campo_banco, novo_valor)

        if usuario_logado:
            banco.inserir_log(
                usuario_logado.get_nome(),
                f"Edição de {type(objeto).__name__} ID '{id_alvo}': {campo_banco} → {novo_valor}"
            )

        print(f"✔ '{campo_banco}' do ID '{id_alvo}' atualizado para '{novo_valor}'.")

    # ═══════════════════════════════════════════════
    # EXCLUIR
    # ═══════════════════════════════════════════════
    def Editar(lista_alvo, id_alvo, campo, novo_valor):
        # Procura o objeto pelo ID
        objeto = next((obj for obj in lista_alvo if obj.get_id() == id_alvo), None)

        if objeto:
            # Constrói o nome do método setter, ex: campo 'nome' vira 'set_nome'
            nome_metodo = f"set_{campo}"
            
            # Verifica se o método setter existe na classe do objeto
            if hasattr(objeto, nome_metodo):
                # Obtém a função do método e executa-a com o novo valor
                metodo = getattr(objeto, nome_metodo)
                metodo(novo_valor) 
                print(f"Sucesso: {campo} do ID {id_alvo} atualizado para {novo_valor}.")
            else:
                print(f"Erro: O campo '{campo}' não existe ou não pode ser editado.")
        else:
            print(f"Erro: Registro com ID {id_alvo} não encontrado.")

    @staticmethod
    def Excluir(lista_alvo, id_alvo, usuario_logado=None):
        """Remove o objeto da memória e do banco."""
        objeto = next((obj for obj in lista_alvo if obj.get_id() == id_alvo), None)

        if not objeto:
            print(f"Erro: ID '{id_alvo}' não encontrado.")
            return

        lista_alvo.remove(objeto)

        # Remove do banco conforme o tipo
        if isinstance(objeto, Cliente):
            banco.excluir_cliente(id_alvo)
        elif isinstance(objeto, Usuario):
            banco.excluir_usuario(id_alvo)
        elif isinstance(objeto, Animal):
            banco.excluir_animal(id_alvo)

        if usuario_logado:
            banco.inserir_log(
                usuario_logado.get_nome(),
                f"Remoção de {type(objeto).__name__} ID '{id_alvo}': {objeto.get_nome()}"
            )

        print(f"✔ '{objeto.get_nome()}' (ID: {id_alvo}) removido com sucesso.")

    # ═══════════════════════════════════════════════
    # BUSCAR
    # ═══════════════════════════════════════════════

    @staticmethod
    def Buscar(lista_alvo, id_alvo):
        """Retorna um objeto pelo ID ou None se não encontrar."""
        return next((obj for obj in lista_alvo if obj.get_id() == id_alvo), None)