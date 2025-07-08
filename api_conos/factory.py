from .base import ConoCarnivoro, ConoVegetariano, ConoSaludable

class ConoFactory:
    """Factory para crear diferentes tipos de conos según la variante"""
    
    _tipos_disponibles = {
        'Carnívoro': ConoCarnivoro,
        'Vegetariano': ConoVegetariano,
        'Saludable': ConoSaludable
    }
    
    @classmethod
    def crear_cono_base(cls, variante, tamanio="Mediano"):
        """
        Crea un cono base según la variante especificada
        
        Args:
            variante (str): Tipo de cono ('Carnívoro', 'Vegetariano', 'Saludable')
            tamanio (str): Tamaño del cono ('Pequeño', 'Mediano', 'Grande')
        
        Returns:
            ConoBase: Instancia del cono correspondiente
        
        Raises:
            ValueError: Si la variante no es válida
        """
        if variante not in cls._tipos_disponibles:
            raise ValueError(
                f"Variante '{variante}' no disponible. "
                f"Opciones válidas: {list(cls._tipos_disponibles.keys())}"
            )
        
        cono_class = cls._tipos_disponibles[variante]
        return cono_class(tamanio)
    
    @classmethod
    def obtener_tipos_disponibles(cls):
        """Obtiene la lista de tipos de conos disponibles"""
        return list(cls._tipos_disponibles.keys())
    
    @classmethod
    def obtener_info_tipos(cls):
        """Obtiene información detallada de todos los tipos disponibles"""
        info = {}
        for variante, cono_class in cls._tipos_disponibles.items():
            # Crear instancia temporal para obtener información
            cono_temp = cono_class()
            info[variante] = {
                'precio_base': cono_temp.precio_base,
                'ingredientes_base': cono_temp.ingredientes.copy(),
                'descripcion': cono_temp.__class__.__doc__
            }
        return info