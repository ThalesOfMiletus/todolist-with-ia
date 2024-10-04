import flet as ft
import requests

# URL do seu backend (certifique-se de que o backend esteja rodando corretamente)
API_URL_OCR = "http://localhost:8000/api/tarefa-ocr/"

def main(page: ft.Page):
    page.title = "ToDo List com OCR"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.padding = 20

    # Função para enviar a imagem ao backend
    def enviar_imagem(e):
        if file_picker.result is not None:
            arquivo_imagem = file_picker.result.files[0].path

            with open(arquivo_imagem, 'rb') as f:
                files = {'imagem': f}
                resposta = requests.post(API_URL_OCR, files=files)
                
                if resposta.status_code == 201:
                    tarefa = resposta.json()
                    lista_tarefas.controls.append(
                        ft.Text(f"Tarefa criada: {tarefa['titulo']} - {tarefa['descricao']}")
                    )
                else:
                    # lista_tarefas.controls.append(ft.Text(f"Erro ao criar tarefa. Detalhes: {resposta.json()}"))
                    pass
                page.update()

        # Evento que será acionado quando um arquivo for selecionado
    def file_picker_result(e):
        enviar_imagem(e)

    # Função para abrir o seletor de arquivos
    def selecionar_imagem(e):
        file_picker.pick_files(allowed_extensions=['png', 'jpg', 'jpeg'])

    # Interface do usuário
    titulo_app = ft.Text("ToDo List com OCR", size=30, weight="bold", color="blue")
    botao_upload = ft.ElevatedButton(text="Carregar Imagem",color="white", on_click=selecionar_imagem, bgcolor=ft.colors.GREEN)
    lista_tarefas = ft.Column(spacing=10)

    file_picker = ft.FilePicker(on_result=file_picker_result)

    # Adiciona os componentes à página
    page.add(
        ft.Column(
            [
                titulo_app,
                botao_upload,
                lista_tarefas,
            ],
            expand=True,
            spacing=20,
            horizontal_alignment=ft.CrossAxisAlignment.START
        )
    )

    # Adiciona o file picker à página
    page.overlay.append(file_picker)
    page.update()

# Inicia a aplicação Flet
ft.app(target=main)
