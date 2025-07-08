# api_conos/serializers.py
from rest_framework import serializers
from .models import PedidoCono
from .factory import ConoFactory
from .builder import ConoPersonalizadoBuilder, ConoDirector
from .logger import obtener_logger

class PedidoConoSerializer(serializers.ModelSerializer):
    """Serializador para el modelo PedidoCono con atributos calculados"""
    
    # Atributos calculados (solo lectura)
    precio_final = serializers.SerializerMethodField()
    ingredientes_finales = serializers.SerializerMethodField()
    resumen_construccion = serializers.SerializerMethodField()
    
    class Meta:
        model = PedidoCono
        fields = [
            'id',
            'cliente',
            'variante',
            'toppings',
            'tamanio_cono',
            'fecha_pedido',
            'precio_final',
            'ingredientes_finales',
            'resumen_construccion'
        ]
        read_only_fields = ['fecha_pedido']
    
    def get_precio_final(self, obj):
        """
        Calcula el precio final del cono utilizando los patrones Factory y Builder
        
        Args:
            obj (PedidoCono): Instancia del pedido
        
        Returns:
            float: Precio final calculado
        """
        logger = obtener_logger()
        
        try:
            # Paso 1: Usar Factory para crear el cono base
            cono_base = ConoFactory.crear_cono_base(obj.variante, obj.tamanio_cono)
            
            # Paso 2: Usar Builder para personalizar el cono
            builder = ConoPersonalizadoBuilder(cono_base)
            director = ConoDirector(builder)
            
            # Construir el cono personalizado con los toppings
            cono_personalizado = director.construir_cono_personalizado(obj.toppings or [])
            
            precio_final = cono_personalizado['precio_total']
            
            # Registrar la operación en el log
            logger.registrar_operacion(
                tipo_operacion='precio_final',
                detalle=f'Cálculo de precio para pedido {obj.id} - Cliente: {obj.cliente}',
                datos_extra={
                    'pedido_id': obj.id,
                    'variante': obj.variante,
                    'tamanio': obj.tamanio_cono,
                    'toppings': obj.toppings,
                    'precio_base': cono_personalizado['precio_base'],
                    'precio_toppings': cono_personalizado['precio_toppings'],
                    'precio_final': precio_final
                }
            )
            
            return round(precio_final, 2)
            
        except Exception as e:
            logger.registrar_operacion(
                tipo_operacion='precio_final',
                detalle=f'Error al calcular precio para pedido {obj.id}: {str(e)}',
                datos_extra={'pedido_id': obj.id, 'error': str(e)}
            )
            return 0.0
    
    def get_ingredientes_finales(self, obj):
        """
        Calcula los ingredientes finales del cono utilizando los patrones Factory y Builder
        
        Args:
            obj (PedidoCono): Instancia del pedido
        
        Returns:
            list: Lista de ingredientes finales
        """
        logger = obtener_logger()
        
        try:
            # Paso 1: Usar Factory para crear el cono base