# app.py — ERPet Interface Flet
# Coloque este arquivo na raiz do projeto, junto com Main.py
#
# Instalação: pip install flet
# Execução:   python app.py

import sys
import os
import flet as ft
import uuid
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from Sistema.Sistema import Sistema
from Classes.Subclasses.Pessoas.Administrador import Administrador
from Classes.Subclasses.Pessoas.Funcionario import Funcionario
from Classes.Subclasses.Pessoas.Cliente import Cliente
from Classes.Subclasses.Animais.Canino import Canino
from Classes.Subclasses.Animais.Felino import Felino
from Classes.Subclasses.Animais.Ave import Ave
from Classes.Subclasses.Animais.Roedor import Roedor
import Banco.banco as banco

# ═══════════════════════════════════════════════════════════
# PALETA DE CORES — tema natureza/animal
# ═══════════════════════════════════════════════════════════
VERDE_ESCURO   = "#1B4332"
VERDE_MEDIO    = "#2D6A4F"
VERDE_CLARO    = "#52B788"
VERDE_MENTA    = "#95D5B2"
BEGE           = "#F8F4E3"
BEGE_ESCURO    = "#EDE8D0"
MARROM         = "#7F5539"
MARROM_CLARO   = "#B08968"
BRANCO         = "#FAFAF7"
TEXTO_ESCURO   = "#1A1A2E"
TEXTO_MEDIO    = "#4A4A6A"
ERRO           = "#C0392B"
SUCESSO        = "#27AE60"
LARANJA        = "#E07B39"

# ═══════════════════════════════════════════════════════════
# ESTADO GLOBAL
# ═══════════════════════════════════════════════════════════
usuario_logado = None


# ═══════════════════════════════════════════════════════════
# UTILITÁRIOS — Geração de IDs
# ═══════════════════════════════════════════════════════════

def gerar_id(prefixo=""):
    """Gera um ID único usando UUID. Útil para criar IDs automáticos."""
    timestamp = str(int(time.time() * 1000))[-8:]  # últimos 8 dígitos do timestamp
    uuid_short = str(uuid.uuid4()).replace("-", "")[:8]  # primeiros 8 chars do UUID
    return f"{prefixo}{uuid_short}{timestamp}" if prefixo else f"{uuid_short}{timestamp}"


# ═══════════════════════════════════════════════════════════
# COMPONENTES REUTILIZÁVEIS
# ═══════════════════════════════════════════════════════════

def campo_texto(label, hint="", senha=False, largura=320, valor=""):
    """Campo de texto estilizado."""
    return ft.TextField(
        label=label,
        hint_text=hint,
        value=valor,
        password=senha,
        can_reveal_password=senha,
        width=largura,
        height=56,
        border_radius=12,
        border_color=VERDE_MEDIO,
        border_width=1.5,
        focused_border_color=VERDE_CLARO,
        label_style=ft.TextStyle(color=TEXTO_MEDIO, size=13),
        text_style=ft.TextStyle(color=TEXTO_ESCURO, size=14),
        bgcolor=BRANCO,
        cursor_color=VERDE_ESCURO,
    )


def dropdown_campo(label, opcoes, largura=320, valor=None, on_change=None):
    """Dropdown estilizado."""
    return ft.Dropdown(
        label=label,
        width=largura,
        border_radius=12,
        margin=ft.Margin(0, 0, 0, 8),
        border_color=VERDE_MEDIO,
        focused_border_color=VERDE_CLARO,
        label_style=ft.TextStyle(color=TEXTO_MEDIO, size=13),
        text_style=ft.TextStyle(color=TEXTO_ESCURO, size=14),
        bgcolor=BRANCO,
        value=valor,
        on_select=on_change,
        options=[ft.dropdown.Option(o) for o in opcoes],
    )


def botao_primario(texto, on_click, largura=320, cor=VERDE_ESCURO):
    return ft.Container(
        content=ft.Text(texto, color=BRANCO, size=14, weight=ft.FontWeight.W_600),
        width=largura,
        height=48,
        bgcolor=cor,
        border_radius=12,
        alignment=ft.Alignment(0, 0),
        on_click=on_click,
        ink=True,
    )


def botao_secundario(texto, on_click, largura=150):
    return ft.Container(
        content=ft.Text(texto, color=BRANCO, size=13, weight=ft.FontWeight.W_500),
        width=largura,
        height=48,
        border_radius=12,
        alignment=ft.Alignment(0, 0),
        border=ft.Border.all(1.5, VERDE_MEDIO),
        on_click=on_click,
        ink=True,
    )

def botao_perigo(texto, on_click, largura=130):
    return ft.Container(
        content=ft.Text(texto, color=BRANCO, size=13, weight=ft.FontWeight.W_600),
        width=largura,
        height=40,
        bgcolor=ERRO,
        border_radius=10,
        alignment=ft.Alignment(0, 0),
        on_click=on_click,
        ink=True,
    )


def card(conteudo, padding=20, largura=None):
    """Card com fundo branco e sombra suave."""
    return ft.Container(
        content=conteudo,
        bgcolor=BRANCO,
        border_radius=16,
        padding=padding,
        width=largura,
        shadow=ft.BoxShadow(
            blur_radius=12,
            color=ft.Colors.with_opacity(0.08, TEXTO_ESCURO),
            offset=ft.Offset(0, 4),
        ),
    )


def titulo_secao(texto):
    return ft.Text(
        texto,
        size=20,
        weight=ft.FontWeight.BOLD,
        color=VERDE_ESCURO,
    )


def snack(page, mensagem, erro=False):
    """Exibe uma notificação na parte inferior."""
    snack_bar = ft.SnackBar(
        content=ft.Text(mensagem, color=BRANCO),
        bgcolor=ERRO if erro else SUCESSO,
        duration=3000,
    )
    if hasattr(page, "show_snack_bar"):
        page.show_snack_bar(snack_bar)
    elif hasattr(page, "snackbar"):
        page.snackbar = snack_bar
        snack_bar.open = True
    else:
        page.snack_bar = snack_bar
        snack_bar.open = True
    page.update()


def limpar_pagina(page):
    if hasattr(page, "clean"):
        page.clean()
    elif hasattr(page, "controls"):
        page.controls.clear()


def exibir_dialogo(page, dialog):
    if hasattr(page, "show_dialog"):
        page.show_dialog(dialog)
    else:
        page.dialog = dialog
        dialog.open = True
    page.update()


def fechar_dialogo_global(page, dialog=None):
    if hasattr(page, "pop_dialog"):
        page.pop_dialog()
    elif dialog is not None:
        dialog.open = False
        page.update()


def emoji_tipo(tipo):
    """Emoji para cada tipo de animal."""
    return {"Canino": "🐶", "Felino": "🐱", "Ave": "🐦", "Roedor": "🐹"}.get(tipo, "🐾")


# ═══════════════════════════════════════════════════════════
# TELA DE LOGIN
# ═══════════════════════════════════════════════════════════

def tela_login(page: ft.Page, on_login_success):
    limpar_pagina(page)
    page.bgcolor = BEGE

    campo_nome  = campo_texto("Usuário", "Digite seu nome de usuário", False, 320, "")
    campo_senha = campo_texto("Senha", "Digite sua senha", senha=True)
    msg_erro    = ft.Text("", color=ERRO, size=13)

    def fazer_login(e):
        global usuario_logado
        nome  = campo_nome.value.strip()
        senha = campo_senha.value.strip()

        if not nome or not senha:
            msg_erro.value = "Preencha todos os campos."
            page.update()
            return

        row = banco.buscar_usuario_login(nome, senha)
        if row:
            id_, nome_db, email, telefone, cpf, senha_db, is_superuser = row
            if is_superuser:
                usuario_logado = Administrador(id_, nome_db, email, telefone, cpf, senha_db)
            else:
                usuario_logado = Funcionario(id_, nome_db, email, telefone, cpf, senha_db)
            banco.inserir_log(usuario_logado.get_nome(), "Login no sistema")
            on_login_success()
        else:
            msg_erro.value = "Usuário ou senha incorretos."
            campo_senha.value = ""
            page.update()

    campo_nome.on_submit  = fazer_login
    campo_senha.on_submit = fazer_login

    decoracao = ft.Container(
        width=400,
        height=200,
        border_radius=ft.border_radius.BorderRadius.only(top_left=24, top_right=24),
        gradient=ft.LinearGradient(
            begin=ft.alignment.Alignment.TOP_LEFT,
            end=ft.alignment.Alignment.BOTTOM_RIGHT,
            colors=[VERDE_ESCURO, VERDE_MEDIO, VERDE_CLARO],
        ),
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Text("🐾", size=52),
                ft.Text("ERPet", size=32, weight=ft.FontWeight.BOLD, color=BRANCO),
                ft.Text("Sistema de Gestão para Petshop", size=13, color=ft.Colors.with_opacity(0.85, BRANCO)),
            ],
        ),
    )

    formulario = ft.Container(
        width=400,
        border_radius=ft.border_radius.BorderRadius.only(bottom_left=24, bottom_right=24),
        bgcolor=BRANCO,
        padding=ft.Padding.symmetric(horizontal=36, vertical=28),
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=16,
            controls=[
                ft.Text("Entrar na conta", size=18, weight=ft.FontWeight.W_600, color=TEXTO_ESCURO),
                campo_nome,
                campo_senha,
                msg_erro,
                botao_primario("Entrar", fazer_login),
            ],
        ),
    )

    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    page.add(
        ft.Container(
            content=ft.Column(
                spacing=0,
                controls=[decoracao, formulario],
            ),
            width=400,
            border_radius=ft.border_radius.BorderRadius.all(24),
            shadow=ft.BoxShadow(
                blur_radius=18,
                color=ft.Colors.with_opacity(0.5, TEXTO_ESCURO),
                offset=ft.Offset(0, 0),
            ),
        )
    )


# ═══════════════════════════════════════════════════════════
# NAVEGAÇÃO LATERAL
# ═══════════════════════════════════════════════════════════

def item_nav(icone, texto, on_click, selecionado=False):
    return ft.Container(
        content=ft.Row(
            controls=[
                ft.Icon(icone, size=20, color=BRANCO if selecionado else ft.Colors.with_opacity(0.7, BRANCO)),
                ft.Text(texto, size=14, color=BRANCO if selecionado else ft.Colors.with_opacity(0.7, BRANCO),
                        weight=ft.FontWeight.W_600 if selecionado else ft.FontWeight.NORMAL),
            ],
            spacing=12,
        ),
        padding=ft.Padding.symmetric(horizontal=16, vertical=12),
        border_radius=10,
        bgcolor=ft.Colors.with_opacity(0.2, BRANCO) if selecionado else ft.Colors.with_opacity(0, BRANCO),
        on_click=on_click,
        on_hover=lambda e: setattr(e.control, 'bgcolor',
            ft.Colors.with_opacity(0.2, BRANCO) if selecionado else
            ft.Colors.with_opacity(0.1, BRANCO) if e.data == "true" else
            ft.Colors.with_opacity(0, BRANCO)) or page_ref[0].update() if not selecionado else None,
        ink=True,
    )


# ═══════════════════════════════════════════════════════════
# LAYOUT PRINCIPAL COM SIDEBAR
# ═══════════════════════════════════════════════════════════

page_ref = [None]

def tela_principal(page: ft.Page):
    global usuario_logado
    page_ref[0] = page
    limpar_pagina(page)
    page.bgcolor = BEGE_ESCURO

    area_conteudo = ft.Column(expand=True, scroll=ft.ScrollMode.AUTO, spacing=0)
    secao_atual   = {"valor": "dashboard"}

    def navegar(secao):
        secao_atual["valor"] = secao
        construir_sidebar()
        area_conteudo.controls.clear()

        if secao == "dashboard":    renderizar_dashboard()
        elif secao == "clientes":   renderizar_clientes()
        elif secao == "animais":    renderizar_animais()
        elif secao == "usuarios":   renderizar_usuarios()
        elif secao == "estoque":    renderizar_estoque()
        elif secao == "servicos":   renderizar_servicos()
        elif secao == "logs":       renderizar_logs()

        page.update()

    # ── Sidebar ──────────────────────────────────────────
    sidebar_container = ft.Container(width=220)

    def construir_sidebar():
        is_admin = usuario_logado.get_is_superuser()
        tipo_badge = ft.Container(
            content=ft.Text(
                "Admin" if is_admin else "Funcionário",
                size=11, color=BRANCO,
                weight=ft.FontWeight.W_600,
            ),
            bgcolor=MARROM_CLARO if is_admin else VERDE_CLARO,
            padding=ft.Padding.symmetric(horizontal=8, vertical=3),
            border_radius=20,
        )

        itens = [
            ("dashboard",  ft.Icons.DASHBOARD_ROUNDED,       "Dashboard"),
            ("clientes",   ft.Icons.PEOPLE_ROUNDED,          "Clientes"),
            ("animais",    ft.Icons.PETS_ROUNDED,             "Animais"),
            ("servicos",   ft.Icons.MEDICAL_SERVICES_ROUNDED, "Serviços"),
            ("estoque",    ft.Icons.INVENTORY_2_ROUNDED,      "Estoque"),
        ]
        if is_admin:
            itens += [
                ("usuarios", ft.Icons.MANAGE_ACCOUNTS_ROUNDED, "Usuários"),
                ("logs",     ft.Icons.HISTORY_ROUNDED,          "Logs"),
            ]

        nav_items = [
            item_nav(icone, texto, lambda e, s=secao: navegar(s), secao_atual["valor"] == secao)
            for secao, icone, texto in itens
        ]

        def logout(e):
            global usuario_logado
            banco.inserir_log(usuario_logado.get_nome(), "Logout")
            usuario_logado = None
            tela_login(page, on_login_success=lambda: tela_principal(page))

        sidebar_container.content = ft.Container(
            expand=True,
            bgcolor=VERDE_ESCURO,
            padding=ft.Padding.symmetric(horizontal=12, vertical=20),
            content=ft.Column(
                expand=True,
                spacing=4,
                controls=[
                    ft.Row(
                        controls=[
                            ft.Text("🐾", size=28),
                            ft.Text("ERPet", size=22, weight=ft.FontWeight.BOLD, color=BRANCO),
                        ],
                        spacing=8,
                    ),
                    ft.Divider(color=ft.Colors.with_opacity(0.2, BRANCO), height=24),
                    ft.Column(
                        controls=[
                            ft.Text("Menu", size=13, color=BRANCO,
                                    weight=ft.FontWeight.W_700),
                            ft.Container(height=8),
                            *nav_items,
                        ],
                        spacing=2,
                        expand=True,
                    ),
                    ft.Divider(color=ft.Colors.with_opacity(0.2, BRANCO)),
                    ft.Row(
                        controls=[
                            ft.Column(
                                controls=[
                                    ft.Text(usuario_logado.get_nome(), size=13,
                                            color=BRANCO, weight=ft.FontWeight.W_600),
                                    tipo_badge,
                                ],
                                spacing=4,
                            ),
                        ],
                    ),
                    ft.Container(height=8),
                    ft.TextButton(
                        content=ft.Text("Sair"),
                        icon=ft.Icons.LOGOUT_ROUNDED,
                        on_click=logout,
                        style=ft.ButtonStyle(color=ft.Colors.with_opacity(0.7, BRANCO)),
                    ),
                ],
            ),
        )

    construir_sidebar()

    page.add(
        ft.Row(
            expand=True,
            spacing=0,
            controls=[
                sidebar_container,
                ft.Container(
                    expand=True,
                    content=area_conteudo,
                    padding=ft.Padding.all(24),
                ),
            ],
        )
    )

    # ════════════════════════════════════════════════════
    # COMPONENTE DE BUSCA E FILTRO GENÉRICO (CORRIGIDO)
    # ════════════════════════════════════════════════════
    def criar_barra_busca_filtros(hint_busca, opcoes_filtro, on_change_callback):
        campo_busca = ft.TextField(
            hint_text=hint_busca,
            prefix_icon=ft.Icons.SEARCH_ROUNDED,
            expand=True,
            height=45,
            border_radius=10,
            border_color=VERDE_MEDIO,
            bgcolor=BRANCO,
            text_style=ft.TextStyle(color=TEXTO_ESCURO, size=14), # O peso (weight) se necessário vai aqui dentro
            on_change=on_change_callback
        )
        
        dropdown_filtro = ft.Dropdown(
            options=[ft.dropdown.Option("Todos")] + [ft.dropdown.Option(o) for o in opcoes_filtro],
            value="Todos",
            width=180,
            height=45,
            border_radius=10,
            border_color=VERDE_MEDIO,
            bgcolor=BRANCO,
            text_style=ft.TextStyle(color=TEXTO_ESCURO, size=13),
            on_select=on_change_callback
        )
        
        return ft.Row(controls=[campo_busca, dropdown_filtro], spacing=12), campo_busca, dropdown_filtro

    # ════════════════════════════════════════════════════
    # MODAL DE DETALHES DE ITENS
    # ════════════════════════════════════════════════════
    def mostrar_modal_detalhes(titulo, dicionario_dados):
        dialogo_ref = [None]
        
        linhas_detalhes = []
        for chave, valor in dicionario_dados.items():
            linhas_detalhes.append(
                ft.Row(
                    controls=[
                        ft.Text(f"{chave}:", weight=ft.FontWeight.BOLD, color=VERDE_ESCURO, size=14, width=130),
                        ft.Text(str(valor), color=TEXTO_ESCURO, size=14, expand=True)
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.START
                )
            )
            linhas_detalhes.append(ft.Divider(color=ft.Colors.with_opacity(0.1, TEXTO_MEDIO), height=8))
        
        if linhas_detalhes:
            linhas_detalhes.pop() # Remove o último divisor desnecessário

        def fechar(e):
            fechar_dialogo_global(page, dialogo_ref[0])

        dialogo_ref[0] = ft.AlertDialog(
            title=ft.Row(
                controls=[
                    ft.Text("🔍", size=22),
                    ft.Text(titulo, weight=ft.FontWeight.BOLD, color=BRANCO)
                ],
                spacing=8
            ),
            content=ft.Container(
                width=400,
                padding=10,
                content=ft.Column(controls=linhas_detalhes, spacing=8, tight=True, scroll=ft.ScrollMode.AUTO)
            ),
            actions=[botao_primario("Fechar", fechar, largura=120)],
            actions_alignment=ft.MainAxisAlignment.CENTER,
        )
        exibir_dialogo(page, dialogo_ref[0])

    # ════════════════════════════════════════════════════
    # DASHBOARD
    # ════════════════════════════════════════════════════

    def renderizar_dashboard():
        def stat_card(emoji, titulo, valor, cor):
            return ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text(emoji, size=32),
                        ft.Text(str(valor), size=28, weight=ft.FontWeight.BOLD, color=cor),
                        ft.Text(titulo, size=13, color=TEXTO_MEDIO),
                    ],
                    spacing=4,
                    horizontal_alignment=ft.CrossAxisAlignment.START,
                ),
                bgcolor=BRANCO,
                border_radius=16,
                padding=20,
                expand=True,
                shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.with_opacity(0.07, TEXTO_ESCURO), offset=ft.Offset(0, 3)),
            )

        logs_recentes = banco.listar_logs()[:5]
        
        # Estado local da busca e filtros no Dashboard para a listagem interna de Atividades Recentes
        col_logs = ft.Column(spacing=0)

        def filtrar_logs(e):
            texto = campo_b.value.strip().lower()
            usuario_filtro = drop_f.value
            
            col_logs.controls.clear()
            for data_hora, usuario, acao in logs_recentes:
                match_texto = texto in acao.lower() or texto in usuario.lower() or texto in data_hora.lower()
                match_usuario = usuario_filtro == "Todos" or usuario_filtro == usuario
                
                if match_texto and match_usuario:
                    col_logs.controls.append(
                        ft.ListTile(
                            leading=ft.Icon(ft.Icons.CIRCLE, size=8, color=VERDE_CLARO),
                            title=ft.Text(acao, size=13, color=TEXTO_ESCURO),
                            subtitle=ft.Text(f"{usuario} • {data_hora}", size=11, color=TEXTO_MEDIO),
                            trailing=ft.IconButton(
                                icon=ft.Icons.ZOOM_IN_ROUNDED, 
                                icon_color=VERDE_MEDIO,
                                on_click=lambda ev, d=data_hora, u=usuario, a=acao: mostrar_modal_detalhes(
                                    "Detalhes do Log", {"Data/Hora": d, "Usuário": u, "Ação Realizada": a}
                                )
                            ),
                            dense=True,
                        )
                    )
            if not col_logs.controls:
                col_logs.controls.append(ft.Text("Nenhuma atividade correspondente.", color=TEXTO_MEDIO, size=13))
            page.update()

        # Extrai usuários únicos dos logs recentes para popular o filtro dinamicamente
        usuarios_logs = list(set([l[1] for l in logs_recentes]))
        barra_componente, campo_b, drop_f = criar_barra_busca_filtros("Buscar nas atividades recentes...", usuarios_logs, filtrar_logs)

        # Dispara a renderização inicial dos logs
        filtrar_logs(None)

        area_conteudo.controls += [
            ft.Text(f"Olá, {usuario_logado.get_nome()} 👋", size=24,
                    weight=ft.FontWeight.BOLD, color=VERDE_ESCURO),
            ft.Text("Visão geral do sistema", size=14, color=TEXTO_MEDIO),
            ft.Container(height=16),
            ft.Row(
                controls=[
                    stat_card("👥", "Clientes",    len(Sistema.lista_clientes),  VERDE_MEDIO),
                    stat_card("🐾", "Animais",     len(Sistema.lista_animais),   MARROM),
                    stat_card("📦", "Estoque",     len(Sistema.lista_estoque),   LARANJA),
                    stat_card("🔧", "Serviços",    len(Sistema.lista_servicos),  VERDE_ESCURO),
                ],
                spacing=16,
            ),
            ft.Container(height=24),
            card(
                ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Icon(ft.Icons.HISTORY_ROUNDED, color=VERDE_ESCURO),
                                ft.Text("Atividade Recente", size=16,
                                        weight=ft.FontWeight.BOLD, color=VERDE_ESCURO),
                            ],
                            spacing=8,
                        ),
                        ft.Divider(height=16),
                        barra_componente,
                        ft.Container(height=10),
                        col_logs,
                    ],
                    spacing=0,
                ),
            ),
        ]

    # ════════════════════════════════════════════════════
    # CLIENTES
    # ════════════════════════════════════════════════════

    def renderizar_clientes():
        dialogo_ref = [None]
        col_listagem = ft.Column(spacing=10)

        def fechar_dialogo(e=None):
            if dialogo_ref[0]:
                fechar_dialogo_global(page, dialogo_ref[0])

        def abrir_cadastro(e, cliente=None):
            editando = cliente is not None
            id_gerado = cliente.get_id() if editando else gerar_id("CLI_")
            
            f_nome     = campo_texto("Nome completo", largura=280, valor=cliente.get_nome() if editando else "")
            f_email    = campo_texto("Email", largura=280, valor=cliente.get_email() if editando else "")
            f_telefone = campo_texto("Telefone", largura=280, valor=cliente.get_telefone() if editando else "")
            f_cpf      = campo_texto("CPF", largura=280, valor=cliente.get_cpf() if editando else "")
            f_endereco = campo_texto("Endereço", largura=280, valor=cliente.get_endereco() if editando else "")

            msg = ft.Text("", color=ERRO, size=12)

            def salvar(e):
                if not all([f_nome.value, f_cpf.value]):
                    msg.value = "Nome e CPF são obrigatórios."
                    page.update()
                    return

                if editando:
                    mapa = {
                        "set_nome": f_nome.value,
                        "set_email": f_email.value,
                        "cpf": f_cpf.value,
                        "set_telefone": f_telefone.value,
                        "set_endereco": f_endereco.value,
                    }
                    for setter, valor in mapa.items():
                        if valor:
                            Sistema.Editar(Sistema.lista_clientes, id_gerado,
                                           setter, valor)
                    snack(page, f"Cliente '{f_nome.value}' atualizado!")
                else:
                    cli = Cliente(id_gerado, f_nome.value, f_email.value,
                                  f_telefone.value, f_cpf.value, f_endereco.value)
                    Sistema.Cadastrar(cli)
                    snack(page, f"Cliente '{f_nome.value}' cadastrado!")

                fechar_dialogo()
                navegar("clientes")

            dialogo_ref[0] = ft.AlertDialog(
                title=ft.Text("Editar Cliente" if editando else "Novo Cliente",
                              color=BRANCO, weight=ft.FontWeight.BOLD),
                content=ft.Column(
                    controls=[f_nome, f_email, f_telefone, f_cpf, f_endereco, msg],
                    spacing=12,
                    width=300,
                    scroll=ft.ScrollMode.AUTO,
                ),
                actions=[
                    botao_secundario("Cancelar", fechar_dialogo, largura=130),
                    botao_primario("Salvar", salvar, largura=130),
                ],
                actions_alignment=ft.MainAxisAlignment.CENTER,
            )
            exibir_dialogo(page, dialogo_ref[0])

        def confirmar_excluir(e, cliente):
            if not usuario_logado.get_is_superuser():
                snack(page, "Apenas administradores podem remover.", erro=True)
                return

            def excluir(e):
                Sistema.Excluir(Sistema.lista_clientes, cliente.get_id(), usuario_logado)
                snack(page, f"Cliente '{cliente.get_nome()}' removido.")
                fechar_dialogo()
                navegar("clientes")

            dialogo_ref[0] = ft.AlertDialog(
                title=ft.Text("Confirmar exclusão", color=ERRO),
                content=ft.Text(f"Deseja remover o cliente '{cliente.get_nome()}'?"),
                actions=[
                    botao_secundario("Cancelar", fechar_dialogo, largura=130),
                    botao_perigo("Remover", excluir, largura=130),
                ],
                actions_alignment=ft.MainAxisAlignment.CENTER,
            )
            exibir_dialogo(page, dialogo_ref[0])

        def linha_cliente(c):
            return ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Container(
                            content=ft.Text("👤", size=24),
                            bgcolor=BEGE,
                            border_radius=10,
                            padding=10,
                        ),
                        ft.Column(
                            controls=[
                                ft.Text(c.get_nome(), size=15, weight=ft.FontWeight.W_600, color=TEXTO_ESCURO),
                                ft.Text(f"CPF: {c.get_cpf()} • {c.get_email()}", size=12, color=TEXTO_MEDIO),
                            ],
                            spacing=2,
                            expand=True,
                        ),
                        ft.Row(
                            controls=[
                                ft.IconButton(ft.Icons.ZOOM_IN_ROUNDED, icon_color=VERDE_ESCURO,
                                              tooltip="Ver Detalhes", on_click=lambda e: mostrar_modal_detalhes(
                                                  "Dados do Cliente", {
                                                      "ID": c.get_id(),
                                                      "Nome": c.get_nome(),
                                                      "CPF": c.get_cpf(),
                                                      "E-mail": c.get_email(),
                                                      "Telefone": c.get_telefone(),
                                                      "Endereço": c.get_endereco()
                                                  }
                                              )),
                                ft.IconButton(ft.Icons.EDIT_ROUNDED, icon_color=VERDE_MEDIO,
                                              tooltip="Editar", on_click=lambda e, cli=c: abrir_cadastro(e, cli)),
                                ft.IconButton(ft.Icons.DELETE_ROUNDED, icon_color=ERRO,
                                              tooltip="Remover", on_click=lambda e, cli=c: confirmar_excluir(e, cli)),
                            ],
                            spacing=0,
                        ),
                    ],
                    spacing=12,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                bgcolor=BRANCO,
                border_radius=12,
                padding=ft.Padding.symmetric(horizontal=16, vertical=12),
                shadow=ft.BoxShadow(blur_radius=6, color=ft.Colors.with_opacity(0.05, TEXTO_ESCURO), offset=ft.Offset(0, 2)),
            )

        def executar_busca_filtro(e):
            texto = campo_b.value.strip().lower()
            provedor_email = drop_f.value
            
            col_listagem.controls.clear()
            for c in Sistema.lista_clientes:
                match_texto = texto in c.get_nome().lower() or texto in c.get_cpf() or texto in c.get_email().lower()
                
                match_filtro = True
                if provedor_email != "Todos":
                    match_filtro = provedor_email.lower() in c.get_email().lower()
                
                if match_texto and match_filtro:
                    col_listagem.controls.append(linha_cliente(c))
            
            if not col_listagem.controls:
                col_listagem.controls.append(ft.Text("Nenhum cliente correspondente encontrado.", color=TEXTO_MEDIO))
            page.update()

        # Filtro por domínios comuns de e-mail cadastrados para Clientes
        barra_comp, campo_b, drop_f = criar_barra_busca_filtros("Buscar por nome, CPF ou e-mail...", ["@gmail.com", "@outlook.com", "@hotmail.com"], executar_busca_filtro)
        executar_busca_filtro(None)

        area_conteudo.controls += [
            ft.Row(
                controls=[
                    titulo_secao("👥 Clientes"),
                    ft.Row(expand=True),
                    botao_primario("+ Novo Cliente", abrir_cadastro, largura=160),
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            ft.Container(height=16),
            barra_comp,
            ft.Container(height=14),
            col_listagem,
        ]

    # ════════════════════════════════════════════════════
    # ANIMAIS
    # ════════════════════════════════════════════════════

    def renderizar_animais():
        dialogo_ref = [None]
        col_listagem = ft.Column(spacing=10)

        def fechar_dialogo(e=None):
            if dialogo_ref[0]:
                fechar_dialogo_global(page, dialogo_ref[0])

        def abrir_cadastro(e):
            id_gerado   = gerar_id("ANI_")
            f_nome      = campo_texto("Nome do animal", largura=280)
            f_idade     = campo_texto("Idade (anos)", largura=280)
            f_sexo      = dropdown_campo("Sexo", ["M", "F"], largura=280)
            f_raca      = campo_texto("Raça", largura=280)
            f_peso      = campo_texto("Peso (kg)", largura=280)
            f_cor       = campo_texto("Cor", largura=280)
            f_historico = campo_texto("Histórico", largura=280)
            f_id_dono   = campo_texto("ID do dono (cliente)", largura=280)
            
            col_extras = ft.Column(spacing=12)
            msg = ft.Text("", color=ERRO, size=12)

            def atualizar_campos_extras(ev):
                tipo = ev.control.value
                col_extras.controls.clear()

                if tipo == "Canino":
                    col_extras.controls.extend([
                        dropdown_campo("Porte", ["Pequeno", "Médio", "Grande", "GG"], largura=280),
                        dropdown_campo("Vacinado?", ["Sim", "Não"], largura=280),
                        dropdown_campo("Castrado?", ["Sim", "Não"], largura=280),
                        dropdown_campo("Tipo de pelo", ["Curto", "Médio", "Longo"], largura=280),
                    ])
                elif tipo == "Felino":
                    col_extras.controls.extend([
                        dropdown_campo("Castrado?", ["Sim", "Não"], largura=280),
                        dropdown_campo("Tipo de pelo", ["Curto", "Longo"], largura=280),
                    ])
                elif tipo == "Ave":
                    col_extras.controls.extend([
                        campo_texto("Número da anilha", largura=280),
                        dropdown_campo("Asas cortadas?", ["Sim", "Não"], largura=280),
                    ])
                elif tipo == "Roedor":
                    col_extras.controls.extend([
                        dropdown_campo("Espécie", ["Hamster", "Coelho", "Porquinho-da-índia", "Rato"], largura=280),
                        dropdown_campo("Substrato", ["Maravalha", "Papel", "Serragem"], largura=280),
                    ])
                
                col_extras.update()
                page.update()

            f_tipo = dropdown_campo(
                label="Tipo de animal",
                opcoes=["Canino", "Felino", "Ave", "Roedor"],
                largura=280,
                on_change=atualizar_campos_extras
            )

            def obtener_valor(componente):
                if hasattr(componente, "value") and componente.value is not None:
                    return str(componente.value).strip()
                
                if hasattr(componente, "controls"):
                    sub_controles = componente.controls
                elif hasattr(componente, "content"):
                    if hasattr(componente.content, "controls"):
                        sub_controles = componente.content.controls
                    else:
                        sub_controles = [componente.content]
                else:
                    sub_controles = []

                for sub in sub_controles:
                    if isinstance(sub, (ft.TextField, ft.Dropdown)):
                        return str(sub.value).strip() if sub.value is not None else ""
                    resultado_interno = obtener_valor(sub)
                    if resultado_interno:
                        return resultado_interno
                        
                return ""

            def salvar(e):
                tipo = obtener_valor(f_tipo)
                val_nome = obtener_valor(f_nome)
                val_idade = obtener_valor(f_idade)

                if not val_nome or not val_idade:
                    msg.value = "Nome e Idade são obrigatórios."
                    dialogo_ref[0].update()
                    return
                    
                if not tipo:
                    msg.value = "Selecione o tipo de animal."
                    dialogo_ref[0].update()
                    return

                val_sexo      = obtener_valor(f_sexo) or "M"
                val_raca      = obtener_valor(f_raca)
                val_peso      = obtener_valor(f_peso)
                val_cor       = obtener_valor(f_cor)
                val_historico = obtener_valor(f_historico)
                val_id_dono   = obtener_valor(f_id_dono)
                
                extras = [obtener_valor(c) for c in col_extras.controls]

                try:
                    if tipo == "Canino":
                        animal = Canino(id_gerado, val_nome, int(val_idade),
                                        val_sexo, val_raca, float(val_peso or 0),
                                        val_cor, val_historico, val_id_dono,
                                        extras[0], extras[1], extras[2], extras[3])
                    elif tipo == "Felino":
                        animal = Felino(id_gerado, val_nome, int(val_idade),
                                        val_sexo, val_raca, float(val_peso or 0),
                                        val_cor, val_historico, val_id_dono,
                                        extras[0], extras[1])
                    elif tipo == "Ave":
                        animal = Ave(id_gerado, val_nome, int(val_idade),
                                     val_sexo, val_raca, float(val_peso or 0),
                                     val_cor, val_historico, val_id_dono,
                                     extras[0], extras[1])
                    elif tipo == "Roedor":
                        animal = Roedor(id_gerado, val_nome, int(val_idade),
                                        val_sexo, val_raca, float(val_peso or 0),
                                        val_cor, val_historico, val_id_dono,
                                        extras[0], extras[1])

                    Sistema.Cadastrar(animal, usuario_logado)
                    snack(page, f"Animal '{val_nome}' cadastrado!")
                    fechar_dialogo()
                    navegar("animais")
                except Exception as ex:
                    msg.value = f"Erro: {ex}"
                    dialogo_ref[0].update()

            dialogo_ref[0] = ft.AlertDialog(
                title=ft.Text("Novo Animal", color=BRANCO, weight=ft.FontWeight.BOLD),
                bgcolor=VERDE_CLARO,
                content=ft.Container(
                    border_radius=12,
                    border=ft.Border.all(1.5, VERDE_MEDIO),
                    padding=12,
                    content=ft.Column(
                        controls=[
                            f_nome, f_tipo, f_idade, f_sexo, f_raca,
                            f_peso, f_cor, f_historico, f_id_dono,
                            col_extras,
                            msg
                        ],
                        spacing=5,
                        width=300,
                        height=420,
                        scroll=ft.ScrollMode.ALWAYS,
                    )
                ),
                actions=[
                    botao_secundario("Cancelar", fechar_dialogo, largura=130),
                    botao_primario("Salvar", salvar, largura=130),
                ],
                actions_alignment=ft.MainAxisAlignment.CENTER,
            )
            exibir_dialogo(page, dialogo_ref[0])

        def confirmar_excluir(e, animal):
            if not usuario_logado.get_is_superuser():
                snack(page, "Apenas administradores podem remover.", erro=True)
                return

            def excluir(ev):
                Sistema.Excluir(Sistema.lista_animais, animal.get_id(), usuario_logado)
                snack(page, f"Animal '{animal.get_nome()}' removido.")
                fechar_dialogo()
                navegar("animais")

            dialogo_ref[0] = ft.AlertDialog(
                title=ft.Text("Confirmar exclusão", color=ERRO),
                content=ft.Text(f"Deseja remover o animal '{animal.get_nome()}'?"),
                actions=[
                    botao_secundario("Cancelar", fechar_dialogo, largura=130),
                    botao_perigo("Remover", excluir, largura=130),
                ],
                actions_alignment=ft.MainAxisAlignment.CENTER,
            )
            exibir_dialogo(page, dialogo_ref[0])

        def obter_detalhes_completos_animal(a):
            type_name = type(a).__name__
            dados = {
                "ID": a.get_id(),
                "Nome": a.get_nome(),
                "Tipo Classe": type_name,
                "Idade": f"{a.get_idade()} anos",
                "Sexo": a.get_sexo(),
                "Raça": a.get_raca(),
                "Peso": f"{a.get_peso()} kg",
                "Cor": a.get_cor(),
                "Histórico Clínico": a.get_historico(),
                "ID do Dono": a.get_id_dono()
            }
            # Adiciona propriedades específicas baseadas em herança estrutural
            if isinstance(a, Canino):
                dados.update({"Porte": a.get_porte(), "Vacinado": a.get_is_vacinado(), "Castrado": a.get_is_castrado(), "Tipo de Pelo": a.get_tipo_pelo()})
            elif isinstance(a, Felino):
                dados.update({"Castrado": a.get_is_castrado(), "Tipo de Pelo": a.get_tipo_pelo()})
            elif isinstance(a, Ave):
                dados.update({"Número da Anilha": a.get_anilha(), "Asas Cortadas": a.get_is_asas_cortadas()})
            elif isinstance(a, Roedor):
                dados.update({"Espécie": a.get_especie(), "Tipo de Substrato": a.get_substrato()})
            return dados

        def linha_animal(a):
            type_name = type(a).__name__
            return ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Container(
                            content=ft.Text(emoji_tipo(type_name), size=26),
                            bgcolor=BEGE,
                            border_radius=10,
                            padding=10,
                        ),
                        ft.Column(
                            controls=[
                                ft.Text(a.get_nome(), size=15,
                                        weight=ft.FontWeight.W_600, color=TEXTO_ESCURO),
                                ft.Text(
                                    f"{type_name} • {a.get_raca()} • {a.get_idade()} anos • Dono: {a.get_id_dono()}",
                                    size=12, color=TEXTO_MEDIO,
                                ),
                            ],
                            spacing=2,
                            expand=True,
                        ),
                        ft.Container(
                            content=ft.Text(type_name, size=11, color=BRANCO,
                                            weight=ft.FontWeight.W_600),
                            bgcolor=VERDE_MEDIO,
                            padding=ft.Padding.symmetric(horizontal=10, vertical=4),
                            border_radius=20,
                        ),
                        ft.IconButton(ft.Icons.ZOOM_IN_ROUNDED, icon_color=VERDE_ESCURO,
                                      tooltip="Ver Detalhes", on_click=lambda e: mostrar_modal_detalhes(
                                          f"Ficha de {a.get_nome()}", obter_detalhes_completos_animal(a)
                                      )),
                        ft.IconButton(ft.Icons.DELETE_ROUNDED, icon_color=ERRO,
                                      tooltip="Remover",
                                      on_click=lambda e, an=a: confirmar_excluir(e, an)),
                    ],
                    spacing=12,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                bgcolor=BRANCO,
                border_radius=12,
                padding=ft.Padding.symmetric(horizontal=16, vertical=12),
                shadow=ft.BoxShadow(blur_radius=6,
                                    color=ft.Colors.with_opacity(0.05, TEXTO_ESCURO),
                                    offset=ft.Offset(0, 2)),
            )

        def executar_busca_filtro(e):
            texto = campo_b.value.strip().lower()
            tipo_selecionado = drop_f.value
            
            col_listagem.controls.clear()
            for a in Sistema.lista_animais:
                type_name = type(a).__name__
                match_texto = texto in a.get_nome().lower() or texto in a.get_raca().lower() or texto in a.get_id_dono().lower()
                match_tipo = tipo_selecionado == "Todos" or tipo_selecionado == type_name
                
                if match_texto and match_tipo:
                    col_listagem.controls.append(linha_animal(a))
            
            if not col_listagem.controls:
                col_listagem.controls.append(ft.Text("Nenhum animal correspondente encontrado.", color=TEXTO_MEDIO))
            page.update()

        # Filtro por sub-classe taxonômica do animal
        barra_comp, campo_b, drop_f = criar_barra_busca_filtros("Buscar por nome do pet, raça ou ID do dono...", ["Canino", "Felino", "Ave", "Roedor"], executar_busca_filtro)
        executar_busca_filtro(None)

        area_conteudo.controls += [
            ft.Row(
                controls=[
                    titulo_secao("🐾 Animais"),
                    ft.Row(expand=True),
                    botao_primario("+ Novo Animal", abrir_cadastro, largura=160),
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            ft.Container(height=16),
            barra_comp,
            ft.Container(height=14),
            col_listagem,
        ]
    
    # ════════════════════════════════════════════════════
    # USUÁRIOS (só admin)
    # ════════════════════════════════════════════════════

    def renderizar_usuarios():
        if not usuario_logado.get_is_superuser():
            area_conteudo.controls.append(
                ft.Text("⛔ Acesso restrito a administradores.", color=ERRO, size=16)
            )
            return

        dialogo_ref = [None]
        col_listagem = ft.Column(spacing=10)

        def fechar_dialogo(e=None):
            if dialogo_ref[0]:
                fechar_dialogo_global(page, dialogo_ref[0])

        def abrir_cadastro(e):
            id_gerado = gerar_id("USR_")
            f_nome   = campo_texto("Nome", largura=280)
            f_email  = campo_texto("Email", largura=280)
            f_tel    = campo_texto("Telefone", largura=280)
            f_cpf    = campo_texto("CPF", largura=280)
            f_senha  = campo_texto("Senha", largura=280, senha=True)
            f_tipo   = dropdown_campo("Perfil", ["Funcionário", "Administrador"], largura=280)
            msg      = ft.Text("", color=ERRO, size=12)

            def salvar(e):
                if not all([f_nome.value, f_senha.value, f_tipo.value]):
                    msg.value = "Preencha todos os campos obrigatórios."
                    page.update()
                    return

                if f_tipo.value == "Administrador":
                    novo = Administrador(id_gerado, f_nome.value, f_email.value,
                                        f_tel.value, f_cpf.value, f_senha.value)
                else:
                    novo = Funcionario(id_gerado, f_nome.value, f_email.value,
                                       f_tel.value, f_cpf.value, f_senha.value)

                Sistema.Cadastrar(novo, usuario_logado)
                snack(page, f"Usuário '{f_nome.value}' cadastrado!")
                fechar_dialogo()
                navegar("usuarios")

            dialogo_ref[0] = ft.AlertDialog(
                title=ft.Text("Novo Usuário", color=VERDE_ESCURO, weight=ft.FontWeight.BOLD),
                content=ft.Column(
                    controls=[f_nome, f_email, f_tel, f_cpf, f_senha, f_tipo, msg],
                    spacing=12,
                    width=300,
                    scroll=ft.ScrollMode.AUTO,
                ),
                actions=[
                    botao_secundario("Cancelar", fechar_dialogo, largura=130),
                    botao_primario("Salvar", salvar, largura=130),
                ],
                actions_alignment=ft.MainAxisAlignment.CENTER,
            )
            exibir_dialogo(page, dialogo_ref[0])

        def confirmar_excluir(e, usuario):
            def excluir(ev):
                Sistema.Excluir(Sistema.lista_usuarios, usuario.get_id(), usuario_logado)
                snack(page, f"Usuário '{usuario.get_nome()}' removido.")
                fechar_dialogo()
                navegar("usuarios")

            dialogo_ref[0] = ft.AlertDialog(
                title=ft.Text("Confirmar exclusão", color=ERRO),
                content=ft.Text(f"Remover '{usuario.get_nome()}'?"),
                actions=[
                    botao_secundario("Cancelar", fechar_dialogo, largura=130),
                    botao_perigo("Remover", excluir, largura=130),
                ],
                actions_alignment=ft.MainAxisAlignment.CENTER,
            )
            exibir_dialogo(page, dialogo_ref[0])

        def linha_usuario(u):
            is_adm = u.get_is_superuser()
            return ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Container(
                            content=ft.Text("👑" if is_adm else "👤", size=24),
                            bgcolor=BEGE,
                            border_radius=10,
                            padding=10,
                        ),
                        ft.Column(
                            controls=[
                                ft.Text(u.get_nome(), size=15,
                                        weight=ft.FontWeight.W_600, color=TEXTO_ESCURO),
                                ft.Text(f"Email: {u.get_email()} • CPF: {u.get_cpf()}",
                                        size=12, color=TEXTO_MEDIO),
                            ],
                            spacing=2,
                            expand=True,
                        ),
                        ft.Container(
                            content=ft.Text("Admin" if is_adm else "Funcionário",
                                            size=11, color=BRANCO, weight=ft.FontWeight.W_600),
                            bgcolor=MARROM if is_adm else VERDE_CLARO,
                            padding=ft.Padding.symmetric(horizontal=10, vertical=4),
                            border_radius=20,
                        ),
                        ft.IconButton(ft.Icons.ZOOM_IN_ROUNDED, icon_color=VERDE_ESCURO,
                                      tooltip="Ver Detalhes", on_click=lambda e: mostrar_modal_detalhes(
                                          "Perfil do Usuário Interno", {
                                              "ID Sistema": u.get_id(),
                                              "Nome": u.get_nome(),
                                              "E-mail": u.get_email(),
                                              "Telefone Corporativo": u.get_telefone(),
                                              "CPF": u.get_cpf(),
                                              "Cargo de Acesso": "Administrador / Superuser" if is_adm else "Funcionário Operacional"
                                          }
                                      )),
                        ft.IconButton(ft.Icons.DELETE_ROUNDED, icon_color=ERRO,
                                      tooltip="Remover",
                                      on_click=lambda e, us=u: confirmar_excluir(e, us)),
                    ],
                    spacing=12,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                bgcolor=BRANCO,
                border_radius=12,
                padding=ft.Padding.symmetric(horizontal=16, vertical=12),
                shadow=ft.BoxShadow(blur_radius=6,
                                    color=ft.Colors.with_opacity(0.05, TEXTO_ESCURO),
                                    offset=ft.Offset(0, 2)),
            )

        def executar_busca_filtro(e):
            texto = campo_b.value.strip().lower()
            tipo_perfil = drop_f.value
            
            col_listagem.controls.clear()
            for u in Sistema.lista_usuarios:
                match_texto = texto in u.get_nome().lower() or texto in u.get_email().lower() or texto in u.get_cpf()
                
                match_perfil = True
                if tipo_perfil == "Administrador":
                    match_perfil = u.get_is_superuser()
                elif tipo_perfil == "Funcionário":
                    match_perfil = not u.get_is_superuser()
                
                if match_texto and match_perfil:
                    col_listagem.controls.append(linha_usuario(u))
            
            if not col_listagem.controls:
                col_listagem.controls.append(ft.Text("Nenhum usuário correspondente encontrado.", color=TEXTO_MEDIO))
            page.update()

        # Filtro estruturado por privilégio de nível de usuário
        barra_comp, campo_b, drop_f = criar_barra_busca_filtros("Buscar por nome, e-mail ou CPF...", ["Administrador", "Funcionário"], executar_busca_filtro)
        executar_busca_filtro(None)

        area_conteudo.controls += [
            ft.Row(
                controls=[
                    titulo_secao("👑 Usuários"),
                    ft.Row(expand=True),
                    botao_primario("+ Novo Usuário", abrir_cadastro, largura=160),
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            ft.Container(height=16),
            barra_comp,
            ft.Container(height=14),
            col_listagem,
        ]

    # ════════════════════════════════════════════════════
    # ESTOQUE
    # ════════════════════════════════════════════════════

    def renderizar_estoque():
        from Classes.Subclasses.Servicos.Estoque import Estoque

        dialogo_ref = [None]
        col_listagem = ft.Column(spacing=10)

        def fechar_dialogo(e=None):
            if dialogo_ref[0]:
                fechar_dialogo_global(page, dialogo_ref[0])

        def abrir_cadastro(e):
            id_gerado  = gerar_id("PRD_")
            f_nome     = campo_texto("Nome do produto", largura=280)
            f_cat      = dropdown_campo("Categoria",
                                        ["Ração", "Medicamento", "Higiene", "Acessório"], largura=280)
            f_qtd      = campo_texto("Quantidade", largura=280)
            f_preco    = campo_texto("Preço unitário (R$)", largura=280)
            f_min      = campo_texto("Quantidade mínima", largura=280)
            msg        = ft.Text("", color=ERRO, size=12)

            def salvar(e):
                if not all([f_nome.value, f_qtd.value, f_preco.value]):
                    msg.value = "Preencha todos os campos obrigatórios."
                    page.update()
                    return
                try:
                    prod = Estoque(id_gerado, f_nome.value, f_cat.value or "Geral",
                                       int(f_qtd.value), float(f_preco.value),
                                       int(f_min.value or 0))
                    Sistema.lista_estoque.append(prod)
                    banco.inserir_estoque(prod)
                    banco.inserir_log(usuario_logado.get_nome(),
                                      f"Cadastro de produto: {f_nome.value}")
                    snack(page, f"Produto '{f_nome.value}' cadastrado!")
                    fechar_dialogo()
                    navegar("estoque")
                except Exception as ex:
                    msg.value = f"Erro: {ex} {ex.__traceback__.tb_lineno}"
                    page.update()

            dialogo_ref[0] = ft.AlertDialog(
                title=ft.Text("Novo Produto", color=BRANCO, weight=ft.FontWeight.BOLD),
                content=ft.Column(
                    controls=[f_nome, f_cat, f_qtd, f_preco, f_min, msg],
                    spacing=12,
                    width=300,
                    scroll=ft.ScrollMode.AUTO,
                ),
                actions=[
                    botao_secundario("Cancelar", fechar_dialogo, largura=130),
                    botao_primario("Salvar", salvar, largura=130),
                ],
                actions_alignment=ft.MainAxisAlignment.CENTER,
            )
            exibir_dialogo(page, dialogo_ref[0])

        def linha_estoque(p):
            alerta = p.get_quantidade() <= p.get_qtd_minima()
            return ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Container(
                            content=ft.Text("📦", size=24),
                            bgcolor=BEGE,
                            border_radius=10,
                            padding=10,
                        ),
                        ft.Column(
                            controls=[
                                ft.Text(p.get_nome(), size=15,
                                        weight=ft.FontWeight.W_600, color=TEXTO_ESCURO),
                                ft.Text(
                                    f"{p.get_categoria()} • Qtd: {p.get_quantidade()} • R$ {p.get_preco_unitario():.2f}",
                                    size=12, color=TEXTO_MEDIO,
                                ),
                            ],
                            spacing=2,
                            expand=True,
                        ),
                        ft.Container(
                            content=ft.Text(
                                "⚠ Baixo estoque" if alerta else "OK",
                                size=11, color=BRANCO, weight=ft.FontWeight.W_600,
                            ),
                            bgcolor=ERRO if alerta else SUCESSO,
                            padding=ft.Padding.symmetric(horizontal=10, vertical=4),
                            border_radius=20,
                        ),
                        ft.IconButton(ft.Icons.ZOOM_IN_ROUNDED, icon_color=VERDE_ESCURO,
                                      tooltip="Ver Detalhes", on_click=lambda e: mostrar_modal_detalhes(
                                          "Metadados do Produto", {
                                              "Código ID": p.get_id(),
                                              "Nome Comercial": p.get_nome(),
                                              "Categoria Alocada": p.get_categoria(),
                                              "Quantidade Atual": p.get_quantidade(),
                                              "Preço Unitário": f"R$ {p.get_preco_unitario():.2f}",
                                              "Estoque Mínimo Alerta": p.get_qtd_minima(),
                                              "Status de Reposição": "🚨 CRÍTICO - REPOOR JÁ" if alerta else "✓ SEGURO"
                                          }
                                      ))
                    ],
                    spacing=12,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                bgcolor=BRANCO,
                border_radius=12,
                padding=ft.Padding.symmetric(horizontal=16, vertical=12),
                shadow=ft.BoxShadow(blur_radius=6,
                                    color=ft.Colors.with_opacity(0.05, TEXTO_ESCURO),
                                    offset=ft.Offset(0, 2)),
            )

        def executar_busca_filtro(e):
            texto = campo_b.value.strip().lower()
            categoria = drop_f.value
            
            col_listagem.controls.clear()
            for p in Sistema.lista_estoque:
                match_texto = texto in p.get_nome().lower() or texto in p.get_categoria().lower()
                
                match_cat = True
                if categoria == "Abaixo Mínimo (Alerta)":
                    match_cat = p.get_quantidade() <= p.get_qtd_minima()
                elif categoria != "Todos":
                    match_cat = p.get_categoria() == categoria
                
                if match_texto and match_cat:
                    col_listagem.controls.append(linha_estoque(p))
            
            if not col_listagem.controls:
                col_listagem.controls.append(ft.Text("Nenhum item em estoque corresponde aos critérios.", color=TEXTO_MEDIO))
            page.update()

        # Filtro contendo categorias dinâmicas e o status crítico de alerta de baixo estoque
        barra_comp, campo_b, drop_f = criar_barra_busca_filtros("Buscar produto...", ["Ração", "Medicamento", "Higiene", "Acessório", "Abaixo Mínimo (Alerta)"], executar_busca_filtro)
        executar_busca_filtro(None)

        area_conteudo.controls += [
            ft.Row(
                controls=[
                    titulo_secao("📦 Estoque"),
                    ft.Row(expand=True),
                    botao_primario("+ Novo Produto", abrir_cadastro, largura=160),
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            ft.Container(height=16),
            barra_comp,
            ft.Container(height=14),
            col_listagem,
        ]

    # ════════════════════════════════════════════════════
    # SERVIÇOS
    # ════════════════════════════════════════════════════

    def renderizar_servicos():
        from Classes.Subclasses.Servicos import Servico as ServicoClass

        dialogo_ref = [None]
        col_listagem = ft.Column(spacing=10)

        def fechar_dialogo(e=None):
            if dialogo_ref[0]:
                fechar_dialogo_global(page, dialogo_ref[0])

        def abrir_cadastro(e):
            id_gerado     = gerar_id("SRV_")
            f_tipo       = dropdown_campo("Tipo", ["Banho", "Tosa", "Banho+Tosa", "Vacina", "Consulta"], largura=280)
            f_preco      = campo_texto("Preço base (R$)", largura=280)
            f_id_animal  = campo_texto("ID do animal", largura=280)
            msg          = ft.Text("", color=ERRO, size=12)

            def salvar(e):
                if not f_tipo.value or not f_preco.value or not f_id_animal.value:
                    msg.value = "Preencha todos os campos."
                    page.update()
                    return
                try:
                    serv = ServicoClass(id_gerado, f_tipo.value,
                                       float(f_preco.value), f_id_animal.value,
                                       usuario_logado.get_id())
                    serv.registrar_servico()
                    Sistema.lista_servicos.append(serv)
                    banco.inserir_servico(serv)
                    banco.inserir_log(usuario_logado.get_nome(),
                                      f"Serviço '{f_tipo.value}' para animal ID {f_id_animal.value}")
                    snack(page, f"Serviço '{f_tipo.value}' registrado!")
                    fechar_dialogo()
                    navegar("servicos")
                except Exception as ex:
                    msg.value = f"Erro: {ex}"
                    page.update()

            dialogo_ref[0] = ft.AlertDialog(
                title=ft.Text("Novo Serviço", color=BRANCO, weight=ft.FontWeight.BOLD),
                content=ft.Column(
                    controls=[f_tipo, f_preco, f_id_animal, msg],
                    spacing=12,
                    width=300,
                ),
                actions=[
                    botao_secundario("Cancelar", fechar_dialogo, largura=130),
                    botao_primario("Registrar", salvar, largura=130),
                ],
                actions_alignment=ft.MainAxisAlignment.CENTER,
            )
            exibir_dialogo(page, dialogo_ref[0])

        def linha_servico(s):
            return ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Container(
                            content=ft.Text("🔧", size=24),
                            bgcolor=BEGE,
                            border_radius=10,
                            padding=10,
                        ),
                        ft.Column(
                            controls=[
                                ft.Text(s.get_tipo(), size=15,
                                        weight=ft.FontWeight.W_600, color=TEXTO_ESCURO),
                                ft.Text(
                                    f"Animal: {s.get_id_animal()} • "
                                    f"R$ {s.get_preco():.2f} • "
                                    f"{s.get_data_hora().strftime('%d/%m/%Y %H:%M')}",
                                    size=12, color=TEXTO_MEDIO,
                                ),
                            ],
                            spacing=2,
                            expand=True,
                        ),
                        ft.IconButton(ft.Icons.ZOOM_IN_ROUNDED, icon_color=VERDE_ESCURO,
                                      tooltip="Ver Detalhes", on_click=lambda e: mostrar_modal_detalhes(
                                          "Ordem de Serviço", {
                                              "Código Protocolo": s.get_id(),
                                              "Tipo Procedimento": s.get_tipo(),
                                              "Valor Cobrado": f"R$ {s.get_preco():.2f}",
                                              "ID Identificador Animal": s.get_id_animal(),
                                              "ID Funcionário Executor": s.get_id_funcionario(),
                                              "Data/Hora Abertura": s.get_data_hora().strftime('%d/%m/%Y às %H:%M:%S')
                                          }
                                      ))
                    ],
                    spacing=12,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                bgcolor=BRANCO,
                border_radius=12,
                padding=ft.Padding.symmetric(horizontal=16, vertical=12),
                shadow=ft.BoxShadow(blur_radius=6,
                                    color=ft.Colors.with_opacity(0.05, TEXTO_ESCURO),
                                    offset=ft.Offset(0, 2)),
            )

        def executar_busca_filtro(e):
            texto = campo_b.value.strip().lower()
            tipo_servico = drop_f.value
            
            col_listagem.controls.clear()
            for s in Sistema.lista_servicos:
                match_texto = texto in s.get_tipo().lower() or texto in s.get_id_animal().lower()
                match_tipo = tipo_servico == "Todos" or s.get_tipo() == tipo_servico
                
                if match_texto and match_tipo:
                    col_listagem.controls.append(linha_servico(s))
            
            if not col_listagem.controls:
                col_listagem.controls.append(ft.Text("Nenhum histórico de serviço encontrado.", color=TEXTO_MEDIO))
            page.update()

        # Filtro fixo por tipos catalogados de serviços executáveis
        barra_comp, campo_b, drop_f = criar_barra_busca_filtros("Buscar por tipo ou ID do animal...", ["Banho", "Tosa", "Banho+Tosa", "Vacina", "Consulta"], executar_busca_filtro)
        executar_busca_filtro(None)

        area_conteudo.controls += [
            ft.Row(
                controls=[
                    titulo_secao("🔧 Serviços"),
                    ft.Row(expand=True),
                    botao_primario("+ Novo Serviço", abrir_cadastro, largura=160),
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            ft.Container(height=16),
            barra_comp,
            ft.Container(height=14),
            col_listagem,
        ]

    # ════════════════════════════════════════════════════
    # LOGS
    # ════════════════════════════════════════════════════

    def renderizar_logs():
        if not usuario_logado.get_is_superuser():
            area_conteudo.controls.append(
                ft.Text("⛔ Acesso restrito a administradores.", color=ERRO, size=16)
            )
            return

        logs = banco.listar_logs()
        col_listagem = ft.Column(spacing=8)

        def linha_log(data_hora, usuario, acao):
            return ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.CIRCLE, size=8, color=VERDE_CLARO),
                        ft.Column(
                            controls=[
                                ft.Text(acao, size=14, color=TEXTO_ESCURO),
                                ft.Text(f"{usuario} • {data_hora}", size=11, color=TEXTO_MEDIO),
                            ],
                            spacing=2,
                            expand=True,
                        ),
                        ft.IconButton(ft.Icons.ZOOM_IN_ROUNDED, icon_color=VERDE_ESCURO,
                                      tooltip="Ver Detalhes", on_click=lambda e: mostrar_modal_detalhes(
                                          "Log de Auditoria", {
                                              "Carimbo de Data/Hora": data_hora,
                                              "Operador": usuario,
                                              "Descrição Completa da Ação": acao
                                          }
                                      ))
                    ],
                    spacing=12,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                bgcolor=BRANCO,
                border_radius=10,
                padding=ft.Padding.symmetric(horizontal=16, vertical=10),
                shadow=ft.BoxShadow(blur_radius=4,
                                    color=ft.Colors.with_opacity(0.04, TEXTO_ESCURO),
                                    offset=ft.Offset(0, 2)),
            )

        def executar_busca_filtro(e):
            texto = campo_b.value.strip().lower()
            usuario_filtro = drop_f.value
            
            col_listagem.controls.clear()
            for data_hora, usuario, acao in logs:
                match_texto = texto in acao.lower() or texto in usuario.lower() or texto in data_hora.lower()
                match_usuario = usuario_filtro == "Todos" or usuario == usuario_filtro
                
                if match_texto and match_usuario:
                    col_listagem.controls.append(linha_log(data_hora, usuario, acao))
            
            if not col_listagem.controls:
                col_listagem.controls.append(ft.Text("Nenhum registro de log localizado.", color=TEXTO_MEDIO))
            page.update()

        # Coleta a lista completa de operadores de forma limpa para injetar no dropdown do filtro
        usuarios_unicos_sistema = list(set([l[1] for l in logs]))
        barra_comp, campo_b, drop_f = criar_barra_busca_filtros("Buscar termos contidos nas descrições de auditoria...", usuarios_unicos_sistema, executar_busca_filtro)
        executar_busca_filtro(None)

        area_conteudo.controls += [
            titulo_secao("📋 Logs de Atividade"),
            ft.Container(height=16),
            barra_comp,
            ft.Container(height=14),
            col_listagem,
        ]

    navegar("dashboard")


# ═══════════════════════════════════════════════════════════
# ENTRY POINT
# ═══════════════════════════════════════════════════════════

def main(page: ft.Page):
    page.title        = "ERPet 🐾"
    page.window_width  = 1100
    page.window_height = 720
    page.padding       = 0
    page.fonts         = {}
    
    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = ft.Theme(
        color_scheme_seed=VERDE_ESCURO,
        color_scheme=ft.ColorScheme(
            surface=BRANCO,
            on_surface=TEXTO_ESCURO
        )
    )

    Sistema.inicializar()

    if not Sistema.lista_usuarios:
        admin = Administrador("1", "admin", "admin@erpet.com",
                              "0000", "000.000.000-00", "admin123")
        Sistema.Cadastrar(admin)

    tela_login(page, on_login_success=lambda: tela_principal(page))


ft.run(main)