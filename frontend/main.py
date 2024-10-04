import flet as ft
import requests
import speech_recognition as sr

# URL do seu backend (certifique-se de que o backend esteja rodando corretamente)
API_URL_POST = "http://localhost:8000/api/tarefa-ia/"
API_URL_GET = "http://localhost:8000/api/tasks/"

def main(page: ft.Page):
    page.title = "ToDo List com IA"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.padding = 20

    # Função para capturar voz
    def capturar_voz(e):
        reconhecedor = sr.Recognizer()
        with sr.Microphone() as fonte:
            audio = reconhecedor.listen(fonte)
            try:
                texto_falado = reconhecedor.recognize_google(audio, language="pt-BR")
                campo_relato.value = texto_falado  # Preenche o input com o texto falado
                page.update()
            except sr.UnknownValueError:
                campo_relato.value = "Não foi possível entender o áudio."
                page.update()

    # Função para enviar tarefa ao backend
    def enviar_tarefa(e):
        relato = campo_relato.value  # O relato é preenchido manualmente ou via voz
        if relato:
            try:
                resposta = requests.post(API_URL_POST, json={"relato": relato})
                if resposta.status_code == 201:
                    relato = resposta.json()
                    lista_tarefas.controls.append(ft.Text(f"Sucesso ao criar tarefa. Detalhes: {relato}"))
                    campo_relato.value = ""  # Limpa o campo de texto após o envio
                else:
                    lista_tarefas.controls.append(ft.Text(f"Erro ao criar tarefa. Detalhes: {resposta.json()}"))
            except Exception as ex:
                lista_tarefas.controls.append(ft.Text(f"Erro: {str(ex)}"))
            page.update()

    # Função para carregar todas as tarefas do backend
    def carregar_tarefas(e=None):
        try:
            resposta = requests.get(API_URL_GET)
            if resposta.status_code == 200:
                tasks = resposta.json()
                lista_tarefas.controls.clear()  # Limpa a lista antes de carregar as tarefas
                for task in tasks:
                    lista_tarefas.controls.append(
                        criar_card_tarefa(task['titulo'], task['descricao'])
                    )
                page.update()
            else:
                lista_tarefas.controls.append(ft.Text("Erro ao carregar tarefas."))
        except Exception as e:
            lista_tarefas.controls.append(ft.Text(f"Erro: {str(e)}"))
        page.update()

    # Função para criar blocos visuais (cards) para cada tarefa
    def criar_card_tarefa(titulo, descricao):
        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Text(titulo, weight="bold", color="black", size=18),
                        ft.Text(descricao, size=14, color="black"),
                    ],
                    spacing=10
                ),
                padding=20,
                border_radius=10,
                bgcolor=ft.colors.WHITE,
                shadow=ft.BoxShadow(
                    blur_radius=4,
                    spread_radius=1,
                    color=ft.colors.with_opacity(0.6, ft.colors.BLACK),
                )
            ),
            width=400
        )

    # Interface do usuário
    titulo_app = ft.Text("ToDo List Inteligente", size=30, weight="bold", color="blue")
    campo_relato = ft.TextField(label="Digite ou fale o relato da tarefa", expand=True)
    botao_falar = ft.ElevatedButton(
        icon=ft.icons.MIC,
        text="Falar",
        color="white",
        on_click=capturar_voz,
        icon_color="white",
        bgcolor=ft.colors.BLUE
    )
    botao_enviar = ft.ElevatedButton(text="Enviar Tarefa", color="white", on_click=enviar_tarefa, bgcolor=ft.colors.GREEN)
    botao_refresh = ft.ElevatedButton(text="Refresh", color="white", on_click=carregar_tarefas, bgcolor=ft.colors.ORANGE)

    # ListView para a lista de tarefas com suporte a rolagem
    lista_tarefas = ft.ListView(expand=True, spacing=10)

    carregar_tarefas()  # Carrega as tarefas inicialmente

    # Adiciona os componentes à página
    page.add(
        ft.Column(
            [
                titulo_app,
                ft.Row([campo_relato, botao_falar, botao_enviar, botao_refresh], spacing=10),
                lista_tarefas,  # ListView com rolagem
            ],
            expand=True,
            spacing=20,
            horizontal_alignment=ft.CrossAxisAlignment.START
        )
    )

    # Atualiza a interface inicialmente
    page.update()

# Inicia a aplicação Flet
ft.app(target=main)
