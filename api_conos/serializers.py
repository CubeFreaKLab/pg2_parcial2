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
            cono_base = ConoFactory.crear_cono_base(obj.variante, obj.tamanio_cono)
            
            # Paso 2: Usar Builder para personalizar el cono
            builder = ConoPersonalizadoBuilder(cono_base)
            director = ConoDirector(builder)
            
            # Construir el cono personalizado con los toppings
            cono_personalizado = director.construir_cono_personalizado(obj.toppings or [])
            
            ingredientes_finales = cono_personalizado['ingredientes_finales']
            
            # Registrar la operación en el log
            logger.registrar_operacion(
                tipo_operacion='ingredientes_finales',
                detalle=f'Cálculo de ingredientes para pedido {obj.id} - Cliente: {obj.cliente}',
                datos_extra={
                    'pedido_id': obj.id,
                    'variante': obj.variante,
                    'tamanio': obj.tamanio_cono,
                    'toppings': obj.toppings,
                    'ingredientes_base': cono_personalizado['ingredientes_base'],
                    'toppings_agregados': cono_personalizado['toppings_agregados'],
                    'ingredientes_finales': ingredientes_finales
                }
            )
            
            return ingredientes_finales
            
        except Exception as e:
            logger.registrar_operacion(
                tipo_operacion='ingredientes_finales',
                detalle=f'Error al calcular ingredientes para pedido {obj.id}: {str(e)}',
                datos_extra={'pedido_id': obj.id, 'error': str(e)}
            )
            return []
    
    def get_resumen_construccion(self, obj):
        """
        Proporciona un resumen detallado de la construcción del cono
        
        Args:
            obj (PedidoCono): Instancia del pedido
        
        Returns:
            dict: Resumen detallado de la construcción
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
            
            # Registrar la operación en el log
            logger.registrar_operacion(
                tipo_operacion='personalizacion',
                detalle=f'Construcción completa del cono para pedido {obj.id}',
                datos_extra={
                    'pedido_id': obj.id,
                    'construccion_completa': cono_personalizado
                }
            )
            
            return {
                'tipo_base': cono_personalizado['tipo_base'],
                'variante': cono_personalizado['variante'],
                'tamanio': cono_personalizado['tamanio'],
                'precio_base': cono_personalizado['precio_base'],
                'precio_toppings': cono_personalizado['precio_toppings'],
                'precio_total': cono_personalizado['precio_total'],
                'total_ingredientes': len(cono_personalizado['ingredientes_finales']),
                'total_toppings': len(cono_personalizado['toppings_agregados'])
            }
            
        except Exception as e:
            logger.registrar_operacion(
                tipo_operacion='personalizacion',
                detalle=f'Error en construcción del cono para pedido {obj.id}: {str(e)}',
                datos_extra={'pedido_id': obj.id, 'error': str(e)}
            )
            return {
                'error': 'No se pudo construir el resumen',
                'detalle': str(e)
            }