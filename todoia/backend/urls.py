# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, criar_tarefa_por_ia, criar_tarefa_por_ocr

router = DefaultRouter()
router.register(r'tasks', TaskViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/tarefa-ia/', criar_tarefa_por_ia),
    path('api/tarefa-ocr/', criar_tarefa_por_ocr),
]
