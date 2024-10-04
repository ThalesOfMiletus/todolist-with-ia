# ToDo List com IA

Este é um projeto de uma aplicação de ToDo List que utiliza inteligência artificial para gerar automaticamente tarefas com base em relatos de voz, texto ou imagens fornecidas pelo usuário. O frontend é desenvolvido com [Flet](https://flet.dev/) e o backend utiliza [Django](https://www.djangoproject.com/) com uma integração de IA via API externa do Gemini e OCR (Optical Character Recognition).

## Funcionalidades

- **Adicionar nova tarefa**: O usuário pode adicionar novas tarefas via relato de texto, voz ou imagem.
- **Prompt textual**: O usuário pode escrever um relato textual para a criação de uma tarefa da ToDo List.
- **Captura de voz**: O usuário pode capturar a voz para gerar um relato de tarefa, que será processado pela IA.
- **Reconhecimento ótico de caracteres**: O usuário pode enviar uma imagem ao app que a IA irá reconhecer textos e gerar tarefas com base na imagem.
- **Listar tarefas**: A interface exibe uma lista de tarefas cadastradas.

## Tecnologias Utilizadas

### Frontend

- **[Flet](https://flet.dev/)**: Framework de interface gráfica baseado em Flutter para Python.
- **[SpeechRecognition](https://pypi.org/project/SpeechRecognition/)**: Biblioteca para reconhecimento de voz.
- **[Requests](https://pypi.org/project/requests/)**: Biblioteca para fazer requisições HTTP.

### Backend

- **[Django](https://www.djangoproject.com/)**: Framework web em Python.
- **[Django Rest Framework (DRF)](https://www.django-rest-framework.org/)**: Ferramenta para construir APIs REST com Django.
- **[Google Generative AI](https://cloud.google.com/ai)**: Integração de IA para processar o relato e gerar tarefas.

## Requisitos

Certifique-se de que você tem os seguintes requisitos instalados:

- **Python 3.8 ou superior**
- **Django 3.2 ou superior**
- **Flet 0.1.0 ou superior**
- **SpeechRecognition**
- **PyAudio**
- **Requests**

### Instalação
1. Instalar Dependências dentro de uma virtualenv
- Certifique-se de ter o pip instalado. Em seguida, instale as dependências do backend:
- pip install virtualenv
- python -m venv <"nome_da_env">
- <"nome_da_env">/Scripts/activate ou source <"nome_da_env">/bin/activate em linux
- pip install -r requirements.txt

2. Configurar o Tesseract OCR
- Para utilizar o Tesseract OCR no backend, você precisa instalá-lo no seu sistema.

- Windows: Baixe e instale o Tesseract **[aqui](https://github.com/UB-Mannheim/tesseract/wiki)**.
- Linux: sudo apt-get install tesseract-ocr
- macOS: brew install tesseract

- Adicione o caminho do executável Tesseract ao PATH do sistema.
- Ou defina manualmente no código: pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
- No local que você instalou o Tesseract (apenas para windows)

3. Configuração da API do Google Generative AI
- Obtenha a chave de API no Google Cloud Console.
- No backend, crie um arquivo apikey.py e adicione a chave da API: APIKEYGEMINI = "sua-chave-de-api-aqui"

4. Migrar o Banco de Dados e rodar do Backend
- Depois de configurar os modelos no app tasks, migre o banco de dados:
- python manage.py makemigrations
- python manage.py migrate
- python manage.py runserver 

5. Rodar o front em Flet
- python main.py
- python ocr_tela.py
