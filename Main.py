# Main.py
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Classes.Subclasses.Pessoas.Administrador import Administrador
from Classes.Subclasses.Pessoas.Funcionario import Funcionario
from Sistema.Sistema import Sistema
import Banco.banco as banco

# Usuário logado na sessão atual
usuario_logado = None


def Main():
    global usuario_logado

    # Inicializa o banco e carrega os dados na memória
    Sistema.inicializar()

    # Cria admin padrão se não houver nenhum usuário no banco
    if not Sistema.lista_usuarios:
        admin = Administrador("1", "admin", "admin@erpet.com", "0000", "000.000.000-00", "admin123")
        Sistema.Cadastrar(admin)
        Sistema.lista_usuarios.append(admin)
        print("✔ Admin padrão criado! Login: 'admin' | Senha: 'admin123'")
        Pausar()

    if not fazer_login():
        return

    op = ""
    while op != "5":
        LimparTela()
        CriarMenuPrincipal()
        op = input("\nDigite a opção desejada: ")
        LimparTela()

        if op == "0":
            Cadastrar()
        elif op == "1":
            Listar()
        elif op == "2":
            Editar()
        elif op == "3":
            Remover()
        elif op == "4":
            VerLogs()
        elif op == "5":
            banco.inserir_log(usuario_logado.get_nome(), "Logout")
            print("Encerrando o programa. Até logo!")
        else:
            print("Opção inválida.")
            Pausar()


def fazer_login():
    global usuario_logado
    LimparTela()
    print("=======================")
    print("\t  ERPet - Login")
    print("=======================\n")

    nome  = input("Usuário: ")
    senha = input("Senha:   ")

    row = banco.buscar_usuario_login(nome, senha)

    if row:
        id, nome_db, email, telefone, cpf, senha_db, is_superuser = row
        if is_superuser:
            from Classes.Subclasses.Pessoas.Administrador import Administrador
            usuario_logado = Administrador(id, nome_db, email, telefone, cpf, senha_db)
        else:
            from Classes.Subclasses.Pessoas.Funcionario import Funcionario
            usuario_logado = Funcionario(id, nome_db, email, telefone, cpf, senha_db)

        banco.inserir_log(usuario_logado.get_nome(), "Login no sistema")
        print(f"\n✔ Bem-vindo, {usuario_logado.get_nome()}! ({type(usuario_logado).__name__})")
        Pausar()
        return True
    else:
        print("\n✘ Usuário ou senha incorretos.")
        Pausar()
        return False


# ═══════════════════════════════════════════════
# CADASTRAR
# ═══════════════════════════════════════════════

def Cadastrar():
    print("=======================")
    print("\tCadastrar")
    print("=======================\n")
    print("0 - Cadastrar Usuário")
    print("1 - Cadastrar Cliente")
    print("2 - Cadastrar Animal")
    op = input("\nDigite a opção: ")
    LimparTela()

    if op == "0":
        if not usuario_logado.get_is_superuser():
            print("✘ Apenas administradores podem cadastrar usuários.")
        else:
            Administrador.criar_usuario(usuario_logado)

    elif op == "1":
        Funcionario.CadastrarCliente(usuario_logado)

    elif op == "2":
        Funcionario.CadastrarAnimal(usuario_logado)

    else:
        print("Opção inválida.")

    Pausar()


# ═══════════════════════════════════════════════
# LISTAR
# ═══════════════════════════════════════════════

def Listar():
    print("=======================")
    print("\tListar")
    print("=======================\n")
    print("0 - Listar Usuários")
    print("1 - Listar Clientes")
    print("2 - Listar Animais")
    print("3 - Listar Serviços")
    print("4 - Listar Estoque")
    op = input("\nDigite a opção: ")
    LimparTela()

    if op == "0":
        print("─── Usuários ───")
        if not Sistema.lista_usuarios:
            print("Nenhum usuário cadastrado.")
        for u in Sistema.lista_usuarios:
            print(f"ID: {u.get_id()} | Nome: {u.get_nome()} | "
                  f"Email: {u.get_email()} | Tipo: {type(u).__name__}")

    elif op == "1":
        print("─── Clientes ───")
        if not Sistema.lista_clientes:
            print("Nenhum cliente cadastrado.")
        for c in Sistema.lista_clientes:
            c.exibir_dados()
            print("-" * 40)

    elif op == "2":
        print("─── Animais ───")
        if not Sistema.lista_animais:
            print("Nenhum animal cadastrado.")
        for a in Sistema.lista_animais:
            a.exibir_dados()
            print(f"Idade humana equiv.: {a.calcular_idade_humana()} anos")
            print("-" * 40)

    elif op == "3":
        print("─── Serviços ───")
        if not Sistema.lista_servicos:
            print("Nenhum serviço registrado.")
        for s in Sistema.lista_servicos:
            s.exibir_dados()
            print("-" * 40)

    elif op == "4":
        print("─── Estoque ───")
        if not Sistema.lista_estoque:
            print("Nenhum produto no estoque.")
        for e in Sistema.lista_estoque:
            e.exibir_dados()
            print("-" * 40)

    else:
        print("Opção inválida.")

    Pausar()


# ═══════════════════════════════════════════════
# EDITAR
# ═══════════════════════════════════════════════

def Editar():
    print("=======================")
    print("\tEditar")
    print("=======================\n")
    print("0 - Editar Cliente")
    print("1 - Editar Animal")
    op = input("\nDigite a opção: ")
    LimparTela()

    mapa_setters = {
        "nome":      "set_nome",
        "email":     "set_email",
        "telefone":  "set_telefone",
        "endereco":  "set_endereco",
        "peso":      "set_peso",
        "historico": "set_historico",
        "raca":      "set_raca",
        "cor":       "set_cor",
        "idade":     "set_idade",
    }

    if op == "0":
        id_alvo = input("ID do cliente: ")
        print("Campos disponíveis: nome / email / telefone / endereco")
        campo = input("Campo a editar: ")
        novo_valor = input(f"Novo valor para '{campo}': ")
        setter = mapa_setters.get(campo)
        if setter:
            Sistema.Editar(Sistema.lista_clientes, id_alvo,
                           setter, novo_valor, usuario_logado)
        else:
            print("Campo inválido.")

    elif op == "1":
        id_alvo = input("ID do animal: ")
        print("Campos disponíveis: nome / peso / historico / raca / cor / idade")
        campo = input("Campo a editar: ")
        novo_valor = input(f"Novo valor para '{campo}': ")
        setter = mapa_setters.get(campo)
        if setter:
            Sistema.Editar(Sistema.lista_animais, id_alvo,
                           setter, novo_valor, usuario_logado)
        else:
            print("Campo inválido.")

    else:
        print("Opção inválida.")

    Pausar()


# ═══════════════════════════════════════════════
# REMOVER
# ═══════════════════════════════════════════════

def Remover():
    print("=======================")
    print("\tRemover")
    print("=======================\n")

    if not usuario_logado.get_is_superuser():
        print("✘ Apenas administradores podem remover registros.")
        Pausar()
        return

    print("0 - Remover Usuário")
    print("1 - Remover Cliente")
    print("2 - Remover Animal")
    op = input("\nDigite a opção: ")
    id_alvo = input("ID a remover: ")
    LimparTela()

    if op == "0":
        Sistema.Excluir(Sistema.lista_usuarios, id_alvo, usuario_logado)
    elif op == "1":
        Sistema.Excluir(Sistema.lista_clientes, id_alvo, usuario_logado)
    elif op == "2":
        Sistema.Excluir(Sistema.lista_animais, id_alvo, usuario_logado)
    else:
        print("Opção inválida.")

    Pausar()


# ═══════════════════════════════════════════════
# LOGS
# ═══════════════════════════════════════════════

def VerLogs():
    if not usuario_logado.get_is_superuser():
        print("✘ Apenas administradores podem visualizar os logs.")
        Pausar()
        return

    print("=======================")
    print("\tLogs do Sistema")
    print("=======================\n")

    logs = banco.listar_logs()
    if not logs:
        print("Nenhuma atividade registrada.")
    for data_hora, usuario, acao in logs:
        print(f"[{data_hora}] {usuario} - {acao}")

    Pausar()


# ═══════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════

def CriarMenuPrincipal():
    tipo = type(usuario_logado).__name__
    print(f"=======================")
    print(f"\t ERPet [{tipo}]")
    print(f"=======================\n")
    print("0 - Cadastrar")
    print("1 - Listar")
    print("2 - Editar")
    print("3 - Remover")
    print("4 - Ver Logs")
    print("5 - Encerrar Programa")


def LimparTela():
    os.system('cls' if os.name == 'nt' else 'clear')


def Pausar():
    input("\nPressione Enter para continuar...")


Main()