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
        Sistema._carregar_estoque() 
        Sistema._carregar_servicos()

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
            
            
    @staticmethod
    def _carregar_estoque():
        """Reconstrói os objetos da classe Estoque a partir do banco de dados erpet.db."""
        from Classes.Subclasses.Servicos.Estoque import Estoque # Ajustar se necessário
        
        Sistema.lista_estoque.clear()
        for row in banco.listar_estoque():
            # Estrutura no banco.py: id, nome, categoria, quantidade, preco_unitario, qtd_minima
            id_prod, nome, categoria, quantidade, preco_unitario, qtd_minima = row
            
            obj = Estoque(
                id=id_prod,
                nome=nome,
                categoria=categoria,
                quantidade=int(quantidade),
                preco_unitario=float(preco_unitario),
                qtd_minima=int(qtd_minima)
            )
            Sistema.lista_estoque.append(obj)
        print(f"✔ {len(Sistema.lista_estoque)} produtos carregados na memória.")

    @staticmethod
    def _carregar_servicos():
        """Reconstrói os objetos da classe Servico a partir do banco de dados."""
        from Classes.Subclasses.Servicos.Servico import Servico # Ajustar se necessário
        from datetime import datetime
        
        Sistema.lista_servicos.clear()
        for row in banco.listar_servicos():
            # Estrutura no banco.py: id, tipo, preco, data_hora, id_animal, id_funcionario
            id_serv, tipo, preco, data_hora_str, id_animal, id_funcionario = row
            
            obj = Servico(
                id=id_serv,
                tipo=tipo,
                preco=float(preco),
                id_animal=id_animal,
                id_funcionario=id_funcionario
            )
            
            # Reconstrói o atributo de data e hora salvo como texto no SQLite
            try:
                obj._Servico__data_hora = datetime.strptime(data_hora_str, "%Y-%m-%d %H:%M:%S")
            except Exception:
                pass # Caso a data esteja em outro formato, mantém o datetime.now() padrão do init
                
            Sistema.lista_servicos.append(obj)
        print(f"✔ {len(Sistema.lista_servicos)} serviços carregados na memória.")

    # ═══════════════════════════════════════════════
    # CADASTRAR — VERSÃO COMPLETA E CORRIGIDA
    # ═══════════════════════════════════════════════

    @staticmethod
    def Cadastrar(objeto, usuario_logado=None):
        """Salva o objeto na memória e no banco, e registra o log de forma segura."""
        from Classes.Subclasses.Servicos.Servico import Servico
        from Classes.Subclasses.Servicos.Estoque import Estoque
        # Se você tiver uma classe Produto, mude o import abaixo para o caminho correto do seu projeto:
        # from Classes.Subclasses.Estoque.Produto import Produto 

        usuario_acao = usuario_logado or Main.usuario_logado

        if isinstance(objeto, Cliente):
            Sistema.lista_clientes.append(objeto)
            banco.inserir_cliente(objeto)
            if usuario_acao:
                banco.inserir_log(usuario_acao.get_nome(), f"Cadastro de cliente: {objeto.get_nome()}")
            print(f"✔ Cliente '{objeto.get_nome()}' cadastrado com sucesso!")

        elif isinstance(objeto, Usuario):
            Sistema.lista_usuarios.append(objeto)
            banco.inserir_usuario(objeto)
            if usuario_acao:
                banco.inserir_log(usuario_acao.get_nome(), f"Cadastro de usuário: {objeto.get_nome()} ({type(objeto).__name__})")
            print(f"✔ Usuário '{objeto.get_nome()}' ({type(objeto).__name__}) cadastrado!")

        elif isinstance(objeto, Animal):
            Sistema.lista_animais.append(objeto)
            banco.inserir_animal(objeto)
            if usuario_acao:
                banco.inserir_log(usuario_acao.get_nome(), f"Cadastro de animal: {objeto.get_nome()} ({type(objeto).__name__})")
            print(f"✔ Animal '{objeto.get_nome()}' cadastrado com sucesso!")

        # ─── CORREÇÃO: ADICIONADO SUPORTE A SERVIÇO NO BANCO ───
        elif isinstance(objeto, Servico):
            Sistema.lista_servicos.append(objeto)
            banco.inserir_servico(objeto) # Chama a função do banco.py que salva o serviço e produtos usados
            if usuario_acao:
                banco.inserir_log(usuario_acao.get_nome(), f"Registrou serviço: {objeto.get_tipo()} para o Animal ID {objeto.get_id_animal()}")
            print(f"✔ Serviço '{objeto.get_tipo()}' registrado com sucesso!")
            
        # ─── CORREÇÃO: ADICIONADO SUPORTE A PRODUTO/ESTOQUE NO BANCO ───
        # ─── SUPORTE A PRODUTO/ESTOQUE NO BANCO ───
        elif isinstance(objeto, Estoque):
            Sistema.lista_estoque.append(objeto)
            banco.inserir_estoque(objeto)
            if usuario_acao:
                banco.inserir_log(usuario_acao.get_nome(), f"Cadastrou produto no estoque: {objeto.get_nome()}")
            print(f"✔ Produto '{objeto.get_nome()}' adicionado ao estoque com sucesso!")

        else:
            print("Erro: Tipo de objeto desconhecido.")


    # ═══════════════════════════════════════════════
    # EDITAR — VERSÃO UNIFICADA E TOTALMENTE LIMPA
    # ═══════════════════════════════════════════════

    @staticmethod
    def Editar(lista_alvo, id_alvo, campo, novo_valor, usuario_logado=None):
        """Atualiza o objeto na memória e no banco de dados de forma consistente."""
        objeto = next((obj for obj in lista_alvo if obj.get_id() == id_alvo), None)

        if not objeto:
            print(f"Erro: ID '{id_alvo}' não encontrado.")
            return

        # Normaliza o nome do método (aceita tanto 'nome' quanto 'set_nome')
        campo_puro = campo.replace("set_", "")
        nome_metodo = f"set_{campo_puro}"

        # Verifica e executa o setter na memória
        if hasattr(objeto, nome_metodo):
            metodo = getattr(objeto, nome_metodo)
            metodo(novo_valor)
        else:
            print(f"Erro: O campo '{campo_puro}' não existe ou não pode ser editado.")
            return

        # Mapeia o campo puro para a coluna correspondente no banco de dados
        mapa_campos = {
            "nome":      "nome",
            "email":     "email",
            "telefone":  "telefone",
            "endereco":  "endereco",
            "cpf":       "cpf",
            "senha":     "senha",
            "peso":      "peso",
            "historico": "historico",
            "raca":      "raca",
            "cor":       "cor",
            "idade":     "idade",
        }

        campo_banco = mapa_campos.get(campo_puro)
        if campo_banco:
            if isinstance(objeto, Cliente):
                banco.editar_cliente(id_alvo, campo_banco, novo_valor)
            elif isinstance(objeto, Animal):
                banco.editar_animal(id_alvo, campo_banco, novo_valor)
            elif isinstance(objeto, Usuario):
                banco.editar_usuario(id_alvo, campo_banco, novo_valor)

        # Registra no histórico de auditoria se um usuário disparou a ação
        if usuario_logado:
            banco.inserir_log(
                usuario_logado.get_nome(),
                f"Edição de {type(objeto).__name__} ID '{id_alvo}': {campo_banco} → {novo_valor}"
            )

        print(f"✔ Sucesso: {campo_banco} do ID {id_alvo} atualizado para {novo_valor}.")


    # ═══════════════════════════════════════════════
    # EXCLUIR
    # ═══════════════════════════════════════════════

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