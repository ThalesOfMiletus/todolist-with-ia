from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Task
from .serializers import TaskSerializer
import google.generativeai as genai
from rest_framework import viewsets
from .apikey import APIKEYGEMINI
import pytesseract
from PIL import Image
import io

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


# Configurando a API do Gemini
genai.configure(api_key=APIKEYGEMINI)

@api_view(['POST'])
def criar_tarefa_por_ia(request):
    relato = request.data.get('relato', '')

    # Logando o relato recebido
    print(f"Relato recebido: {relato}")

    # Validação para garantir que o relato foi enviado
    if not relato:
        return Response({"error": "Relato não fornecido"}, status=400)

    # Enviando o prompt para a IA do Gemini
    prompt = (
        "Você é um assistente virtual especializado em anotar tarefas. "
        "Com base no seguinte relato do usuário, forneça o título da tarefa e sua descrição. "
        f"Relato: '{relato}'"
    )

    try:
        # Enviando o prompt para a IA e processando a resposta
        print(f"Enviando prompt para a IA: {prompt}")  # Log para depuração
        response = genai.GenerativeModel('gemini-pro').generate_content(prompt)

        # Verificação de erro na resposta da IA
        if not response:
            return Response({"error": "Erro na resposta da IA. Nenhuma resposta recebida."}, status=500)

        resposta_gerada = response.text
        print(f"Resposta da IA: {resposta_gerada}")  # Log para depuração

        if resposta_gerada and resposta_gerada.strip():
            # Tratando a resposta para extrair o título e a descrição
            linhas = resposta_gerada.split("\n")
            titulo = None
            descricao = None

            for linha in linhas:
                if "**Título da Tarefa:**" in linha:
                    titulo = linha.replace("**Título da Tarefa:**", "").strip()
                elif "**Descrição da Tarefa:**" in linha:
                    descricao_index = linhas.index(linha) + 1  # A descrição começa logo após essa linha
                    descricao = "\n".join(linhas[descricao_index:]).strip()

            # Garantindo que o título e a descrição não sejam vazios
            print(f"Título extraído: {titulo}, Descrição extraída: {descricao}")  # Log para depuração
            if (titulo and descricao) or (titulo and not descricao):
                # Criando a tarefa com base na resposta da IA
                task = Task.objects.create(
                    titulo=titulo,
                    descricao=descricao
                )
                return Response(TaskSerializer(task).data, status=201)
            else:
                # Se a IA não fornecer título ou descrição válidos
                return Response({"error": "A IA não conseguiu gerar título e/ou descrição válidos."}, status=500)
        else:
            return Response({"error": "Não foi possível gerar uma resposta da IA"}, status=500)

    except Exception as e:
        print(f"Erro durante o processamento: {str(e)}")  # Log para depuração
        return Response({"error": f"Erro no servidor: {str(e)}"}, status=500)
    
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

@api_view(['POST'])
def criar_tarefa_por_ocr(request):
    if 'imagem' not in request.FILES:
        return Response({"error": "Nenhuma imagem fornecida."}, status=400)

    imagem = request.FILES['imagem']
    img = Image.open(imagem)

    # Usa o Tesseract OCR para extrair texto da imagem
    texto_extraido = pytesseract.image_to_string(img)

    if texto_extraido.strip() == "":
        return Response({"error": "Nenhum texto foi extraído da imagem."}, status=400)

    prompt = (
        "Você é um assistente virtual especializado em anotar tarefas. "
        "Com base no seguinte relato do usuário, forneça o título da tarefa e sua descrição. "
        f"Relato: '{texto_extraido}'"
    )
    response = genai.GenerativeModel('gemini-pro').generate_content(prompt)

    # Verificação de erro na resposta da IA
    if not response:
            return Response({"error": "Erro na resposta da IA. Nenhuma resposta recebida."}, status=500)

    resposta_gerada = response.text
    print(f"Resposta da IA: {resposta_gerada}")  # Log para depuração

    if resposta_gerada and resposta_gerada.strip():
            # Tratando a resposta para extrair o título e a descrição
            linhas = resposta_gerada.split("\n")
            titulo = None
            descricao = None

            for linha in linhas:
                if "**Título da Tarefa:**" in linha:
                    titulo = linha.replace("**Título da Tarefa:**", "").strip()
                elif "**Descrição da Tarefa:**" in linha:
                    descricao_index = linhas.index(linha) + 1  # A descrição começa logo após essa linha
                    descricao = "\n".join(linhas[descricao_index:]).strip()

            # Garantindo que o título e a descrição não sejam vazios
            print(f"Título extraído: {titulo}, Descrição extraída: {descricao}")  # Log para depuração
            if (titulo and descricao) or (titulo and not descricao):
                # Criando a tarefa com base na resposta da IA
                task = Task.objects.create(
                    titulo=titulo,
                    descricao=descricao
                )
                return Response(TaskSerializer(task).data, status=201)
            else:
                # Se a IA não fornecer título ou descrição válidos
                return Response({"error": "A IA não conseguiu gerar título e/ou descrição válidos."}, status=500)
    else:
        return Response({"error": "Não foi possível gerar uma resposta da IA"}, status=500)
