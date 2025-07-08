from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import PedidoCono
from .serializers import PedidoConoSerializer
from .logger import obtener_logger
from .factory import ConoFactory
from .builder import ConoPersonalizadoBuilder

class PedidoConoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para el manejo de pedidos de conos
    Proporciona operaciones CRUD completas y endpoints adicionales
    """
    
    queryset = PedidoCono.objects.all()
    serializer_class = PedidoConoSerializer
    
    def get_queryset(self):
        """
        Personaliza el queryset con filtros opcionales
        """
        queryset = PedidoCono.objects.all()
        
        # Filtros opcionales por parámetros de consulta
        variante = self.request.query_params.get('variante')
        tamanio = self.request.query_params.get('tamanio')
        cliente = self.request.query_params.get('cliente')
        
        if variante:
            queryset = queryset.filter(variante=variante)
        if tamanio:
            queryset = queryset.filter(tamanio_cono=tamanio)
        if cliente:
            queryset = queryset.filter(cliente__icontains=cliente)
            
        return queryset.order_by('-fecha_pedido')
    
    def perform_create(self, serializer):
        """
        Registra la creación de un nuevo pedido en el log
        """
        logger = obtener_logger()
        instance = serializer.save()
        
        logger.registrar_operacion(
            tipo_operacion='creacion_cono',
            detalle=f'Nuevo pedido creado - ID: {instance.id}, Cliente: {instance.cliente}',
            datos_extra={
                'pedido_id': instance.id,
                'cliente': instance.cliente,
                'variante': instance.variante,
                'tamanio': instance.tamanio_cono,
                'toppings': instance.toppings
            }
        )
    
    @action(detail=False, methods=['get'])
    def tipos_disponibles(self, request):
        """
        Endpoint para obtener los tipos de conos disponibles
        """
        try:
            tipos = ConoFactory.obtener_info_tipos()
            return Response({
                'tipos_disponibles': tipos,
                'total_tipos': len(tipos)
            })
        except Exception as e:
            return Response({
                'error': 'Error al obtener tipos disponibles',
                'detalle': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['get'])
    def toppings_disponibles(self, request):
        """
        Endpoint para obtener los toppings disponibles y sus precios
        """
        try:
            toppings = ConoPersonalizadoBuilder.obtener_precios_toppings()
            return Response({
                'toppings_disponibles': toppings,
                'total_toppings': len(toppings)
            })
        except Exception as e:
            return Response({
                'error': 'Error al obtener toppings disponibles',
                'detalle': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['get'])
    def estadisticas(self, request):
        """
        Endpoint para obtener estadísticas del sistema
        """
        try:
            logger = obtener_logger()
            stats = logger.obtener_estadisticas()
            
            # Estadísticas adicionales de pedidos
            total_pedidos = PedidoCono.objects.count()
            pedidos_por_variante = {}
            pedidos_por_tamanio = {}
            
            for variante, _ in PedidoCono.VARIANTES_CHOICES:
                count = PedidoCono.objects.filter(variante=variante).count()
                pedidos_por_variante[variante] = count
            
            for tamanio, _ in PedidoCono.TAMANIOS_CHOICES:
                count = PedidoCono.objects.filter(tamanio_cono=tamanio).count()
                pedidos_por_tamanio[tamanio] = count
            
            return Response({
                'estadisticas_sistema': stats,
                'estadisticas_pedidos': {
                    'total_pedidos': total_pedidos,
                    'pedidos_por_variante': pedidos_por_variante,
                    'pedidos_por_tamanio': pedidos_por_tamanio
                }
            })
        except Exception as e:
            return Response({
                'error': 'Error al obtener estadísticas',
                'detalle': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['get'])
    def logs_recientes(self, request):
        """
        Endpoint para obtener los logs recientes del sistema
        """
        try:
            logger = obtener_logger()
            limite = int(request.query_params.get('limite', 10))
            logs = logger.obtener_logs(limite=limite)
            
            return Response({
                'logs_recientes': logs,
                'total_logs': len(logs)
            })
        except Exception as e:
            return Response({
                'error': 'Error al obtener logs',
                'detalle': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=True, methods=['get'])
    def detalle_construccion(self, request, pk=None):
        """
        Endpoint para obtener el detalle completo de construcción de un pedido específico
        """
        try:
            pedido = get_object_or_404(PedidoCono, pk=pk)
            serializer = self.get_serializer(pedido)
            
            # Obtener información adicional de construcción
            from .factory import ConoFactory
            from .builder import ConoPersonalizadoBuilder, ConoDirector
            
            cono_base = ConoFactory.crear_cono_base(pedido.variante, pedido.tamanio_cono)
            builder = ConoPersonalizadoBuilder(cono_base)
            director = ConoDirector(builder)
            construccion_completa = director.construir_cono_personalizado(pedido.toppings or [])
            
            return Response({
                'pedido': serializer.data,
                'construccion_detallada': construccion_completa,
                'patron_factory': f'Usado para crear cono base: {cono_base.__class__.__name__}',
                'patron_builder': f'Usado para personalizar con {len(pedido.toppings or [])} toppings'
            })
        except Exception as e:
            return Response({
                'error': 'Error al obtener detalle de construcción',
                'detalle': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)