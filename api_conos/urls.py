from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PedidoConoViewSet

# Crear el router y registrar el ViewSet
router = DefaultRouter()
router.register(r'pedidos_conos', PedidoConoViewSet, basename='pedidos_conos')

urlpatterns = [
    # Incluir las URLs del router
    path('', include(router.urls)),
]
