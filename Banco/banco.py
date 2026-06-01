# Banco/banco.py
import sqlite3
import os

# Caminho do arquivo do banco — fica na pasta Banco/
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CAMINHO_BANCO = os.path.join(BASE_DIR, "erpet.db")


def conectar():
    """Retorna uma conexão com o banco de dados."""
    return sqlite3.connect(CAMINHO_BANCO)


def criar_tabelas():
    """Cria todas as tabelas do sistema caso ainda não existam."""
    conn = conectar()
    cursor = conn.cursor()

    # ── Tabela: usuarios ─────────────────────────────────────────────
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id          TEXT PRIMARY KEY,
            nome        TEXT NOT NULL,
            email       TEXT NOT NULL,
            telefone    TEXT NOT NULL,
            cpf         TEXT NOT NULL,
            senha       TEXT NOT NULL,
            is_superuser INTEGER NOT NULL DEFAULT 0
        )
    """)

    # ── Tabela: clientes ──────────────────────────────────────────────
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id          TEXT PRIMARY KEY,
            nome        TEXT NOT NULL,
            email       TEXT NOT NULL,
            telefone    TEXT NOT NULL,
            cpf         TEXT NOT NULL UNIQUE,
            endereco    TEXT
        )
    """)

    # ── Tabela: animais ───────────────────────────────────────────────
    # Guarda os dados comuns + tipo + colunas específicas de cada subclasse
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS animais (
            id              TEXT PRIMARY KEY,
            nome            TEXT NOT NULL,
            idade           INTEGER NOT NULL,
            sexo            TEXT NOT NULL,
            raca            TEXT NOT NULL,
            peso            REAL NOT NULL,
            cor             TEXT NOT NULL,
            historico       TEXT,
            id_dono         TEXT NOT NULL,
            tipo            TEXT NOT NULL,

            -- Canino
            porte           TEXT,
            is_vacinado     TEXT,
            is_castrado     TEXT,
            tipo_pelo       TEXT,

            -- Ave
            anilha          TEXT,
            is_asas_cortadas TEXT,

            -- Roedor
            especie         TEXT,
            substrato       TEXT,

            FOREIGN KEY (id_dono) REFERENCES clientes(id)
        )
    """)

    # ── Tabela: estoque ───────────────────────────────────────────────
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS estoque (
            id              TEXT PRIMARY KEY,
            nome            TEXT NOT NULL,
            categoria       TEXT NOT NULL,
            quantidade      INTEGER NOT NULL,
            preco_unitario  REAL NOT NULL,
            qtd_minima      INTEGER NOT NULL
        )
    """)

    # ── Tabela: servicos ──────────────────────────────────────────────
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS servicos (
            id              TEXT PRIMARY KEY,
            tipo            TEXT NOT NULL,
            preco           REAL NOT NULL,
            data_hora       TEXT NOT NULL,
            id_animal       TEXT NOT NULL,
            id_funcionario  TEXT NOT NULL,
            FOREIGN KEY (id_animal)      REFERENCES animais(id),
            FOREIGN KEY (id_funcionario) REFERENCES usuarios(id)
        )
    """)

    # ── Tabela: servico_produtos (produtos usados em cada serviço) ────
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS servico_produtos (
            id_servico      TEXT NOT NULL,
            id_produto      TEXT NOT NULL,
            quantidade      INTEGER NOT NULL,
            PRIMARY KEY (id_servico, id_produto),
            FOREIGN KEY (id_servico) REFERENCES servicos(id),
            FOREIGN KEY (id_produto) REFERENCES estoque(id)
        )
    """)

    # ── Tabela: logs ──────────────────────────────────────────────────
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            data_hora   TEXT NOT NULL,
            usuario     TEXT NOT NULL,
            acao        TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()
    print("✔ Banco de dados inicializado com sucesso!")


# ═══════════════════════════════════════════════════════════════════════
# USUÁRIOS
# ═══════════════════════════════════════════════════════════════════════

def inserir_usuario(usuario):
    """Salva um Administrador ou Funcionario no banco."""
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO usuarios (id, nome, email, telefone, cpf, senha, is_superuser)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            usuario.get_id(),
            usuario.get_nome(),
            usuario.get_email(),
            usuario.get_telefone(),
            usuario.get_cpf(),
            usuario.get_senha(),
            1 if usuario.get_is_superuser() else 0
        ))
        conn.commit()
        print(f"✔ Usuário '{usuario.get_nome()}' (ID: {usuario.get_id()}) salvo no banco com sucesso!")
        return True
    except sqlite3.IntegrityError as e:
        print(f"✘ Erro ao inserir usuário: {e}")
        print(f"   ID: {usuario.get_id()}, Nome: {usuario.get_nome()}")
        return False
    finally:
        conn.close()


def buscar_usuario_login(nome, senha):
    """Busca usuário pelo nome e senha — usado no login."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, nome, email, telefone, cpf, senha, is_superuser
        FROM usuarios WHERE nome = ? AND senha = ?
    """, (nome, senha))
    row = cursor.fetchone()
    conn.close()
    return row  # retorna tupla ou None


def listar_usuarios():
    """Retorna todos os usuários cadastrados."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, email, telefone, cpf, senha, is_superuser FROM usuarios")
    rows = cursor.fetchall()
    conn.close()
    return rows


def excluir_usuario(id_usuario):
    """Remove um usuário pelo ID."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM usuarios WHERE id = ?", (id_usuario,))
    conn.commit()
    conn.close()


# ═══════════════════════════════════════════════════════════════════════
# CLIENTES
# ═══════════════════════════════════════════════════════════════════════

def inserir_cliente(cliente):
    """Salva um Cliente no banco."""
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO clientes (id, nome, email, telefone, cpf, endereco)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            cliente.get_id(),
            cliente.get_nome(),
            cliente.get_email(),
            cliente.get_telefone(),
            cliente.get_cpf(),
            cliente.get_endereco()
        ))
        conn.commit()
    except sqlite3.IntegrityError:
        print(f"Erro: Cliente com CPF '{cliente.get_cpf()}' já cadastrado.")
    finally:
        conn.close()


def listar_clientes():
    """Retorna todos os clientes cadastrados."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, email, telefone, cpf, endereco FROM clientes")
    rows = cursor.fetchall()
    conn.close()
    return rows


def editar_cliente(id_cliente, campo, novo_valor):
    """Atualiza um campo específico de um cliente."""
    campos_permitidos = {"nome", "email", "telefone", "endereco"}
    if campo not in campos_permitidos:
        print(f"Erro: Campo '{campo}' não permitido para edição.")
        return
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(f"UPDATE clientes SET {campo} = ? WHERE id = ?", (novo_valor, id_cliente))
    conn.commit()
    conn.close()


def excluir_cliente(id_cliente):
    """Remove um cliente pelo ID."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM clientes WHERE id = ?", (id_cliente,))
    conn.commit()
    conn.close()


# ═══════════════════════════════════════════════════════════════════════
# ANIMAIS
# ═══════════════════════════════════════════════════════════════════════

def inserir_animal(animal):
    """Salva qualquer subclasse de Animal no banco."""
    from Classes.Subclasses.Animais.Canino import Canino
    from Classes.Subclasses.Animais.Ave import Ave
    from Classes.Subclasses.Animais.Roedor import Roedor

    tipo = type(animal).__name__

    # Coleta atributos específicos conforme o tipo
    porte = is_vacinado = is_castrado = tipo_pelo = None
    anilha = is_asas_cortadas = None
    especie = substrato = None

    if isinstance(animal, Canino):
        porte = animal.get_porte()
        is_vacinado = animal.get_is_vacinado()
        is_castrado = animal.get_is_castrado()
        tipo_pelo = animal.get_tipo_pelo()
    elif isinstance(animal, Ave):
        anilha = animal.get_anilha()
        is_asas_cortadas = animal.get_is_asas_cortadas()
    elif isinstance(animal, Roedor):
        especie = animal.get_especie()
        substrato = animal.get_substrato()

    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO animais (
                id, nome, idade, sexo, raca, peso, cor, historico, id_dono, tipo,
                porte, is_vacinado, is_castrado, tipo_pelo,
                anilha, is_asas_cortadas,
                especie, substrato
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            animal.get_id(), animal.get_nome(), animal.get_idade(),
            animal.get_sexo(), animal.get_raca(), animal.get_peso(),
            animal.get_cor(), animal.get_historico(), animal.get_id_dono(), tipo,
            porte, is_vacinado, is_castrado, tipo_pelo,
            anilha, is_asas_cortadas,
            especie, substrato
        ))
        conn.commit()
    except sqlite3.IntegrityError:
        print(f"Erro: Animal com ID '{animal.get_id()}' já existe.")
    finally:
        conn.close()


def listar_animais():
    """Retorna todos os animais cadastrados."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM animais")
    rows = cursor.fetchall()
    conn.close()
    return rows


def editar_animal(id_animal, campo, novo_valor):
    """Atualiza um campo específico de um animal."""
    campos_permitidos = {"nome", "idade", "peso", "historico", "raca", "cor"}
    if campo not in campos_permitidos:
        print(f"Erro: Campo '{campo}' não permitido para edição.")
        return
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(f"UPDATE animais SET {campo} = ? WHERE id = ?", (novo_valor, id_animal))
    conn.commit()
    conn.close()


def excluir_animal(id_animal):
    """Remove um animal pelo ID."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM animais WHERE id = ?", (id_animal,))
    conn.commit()
    conn.close()


# ═══════════════════════════════════════════════════════════════════════
# ESTOQUE
# ═══════════════════════════════════════════════════════════════════════

def inserir_estoque(produto):
    """Salva um item de Estoque no banco."""
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO estoque (id, nome, categoria, quantidade, preco_unitario, qtd_minima)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            produto.get_id(), produto.get_nome(), produto.get_categoria(),
            produto.get_quantidade(), produto.get_preco_unitario(), produto.get_qtd_minima()
        ))
        conn.commit()
    except sqlite3.IntegrityError:
        print(f"Erro: Produto com ID '{produto.get_id()}' já existe.")
    finally:
        conn.close()


def listar_estoque():
    """Retorna todos os produtos do estoque."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM estoque")
    rows = cursor.fetchall()
    conn.close()
    return rows


def atualizar_quantidade_estoque(id_produto, nova_quantidade):
    """Atualiza a quantidade de um produto no banco."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("UPDATE estoque SET quantidade = ? WHERE id = ?",
                   (nova_quantidade, id_produto))
    conn.commit()
    conn.close()


def excluir_estoque(id_produto):
    """Remove um produto do estoque."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM estoque WHERE id = ?", (id_produto,))
    conn.commit()
    conn.close()


# ═══════════════════════════════════════════════════════════════════════
# SERVIÇOS
# ═══════════════════════════════════════════════════════════════════════

def inserir_servico(servico):
    """Salva um Servico no banco junto com os produtos usados."""
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO servicos (id, tipo, preco, data_hora, id_animal, id_funcionario)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            servico.get_id(), servico.get_tipo(), servico.get_preco(),
            servico.get_data_hora().strftime("%Y-%m-%d %H:%M:%S"),
            servico.get_id_animal(), servico.get_id_funcionario()
        ))

        # Salva os produtos usados na tabela de relacionamento
        for produto, qtd in servico.get_produtos_usados():
            cursor.execute("""
                INSERT INTO servico_produtos (id_servico, id_produto, quantidade)
                VALUES (?, ?, ?)
            """, (servico.get_id(), produto.get_id(), qtd))

        conn.commit()
    except sqlite3.IntegrityError:
        print(f"Erro: Serviço com ID '{servico.get_id()}' já existe.")
    finally:
        conn.close()


def listar_servicos():
    """Retorna todos os serviços registrados."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM servicos")
    rows = cursor.fetchall()
    conn.close()
    return rows


# ═══════════════════════════════════════════════════════════════════════
# LOGS
# ═══════════════════════════════════════════════════════════════════════

def inserir_log(usuario, acao):
    """Registra uma ação no banco e no arquivo log.txt."""
    from datetime import datetime
    data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Salva no banco
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO logs (data_hora, usuario, acao) VALUES (?, ?, ?)
    """, (data_hora, usuario, acao))
    conn.commit()
    conn.close()

    # Salva no log.txt conforme formato exigido pelo trabalho
    log_path = os.path.join(BASE_DIR, "..", "log.txt")
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"[{data_hora}] {usuario} - {acao}\n")


def listar_logs():
    """Retorna todos os logs registrados."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT data_hora, usuario, acao FROM logs ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows