from .base import ConoBase

class ConoPersonalizadoBuilder:
    """Builder para construir conos personalizados paso a paso"""
    
    # Precios de los toppings adicionales
    _precios_toppings = {
        'queso_extra': 2.5,
        'papas_al_hilo': 3.0,
        'salchicha_extra': 4.0,
        'bacon': 4.5,
        'cebolla_caramelizada': 2.0,
        'guacamole': 3.5,
        'jalapeños': 1.5,
        'tomate_cherry': 2.0,
        'aguacate': 3.0,
        'pollo_desmenuzado': 4.0,
        'champiñones': 2.5,
        'pimiento_asado': 2.0,
        'salsa_chipotle': 1.0,
        'salsa_ranch': 1.0,
        'salsa_barbacoa': 1.0
    }
    
    def __init__(self, cono_base: ConoBase):
        """
        Inicializa el builder con un cono base
        
        Args:
            cono_base (ConoBase): Cono base creado por el factory
        """
        self.cono = cono_base
        self.toppings_agregados = []
        self.precio_toppings = 0.0
    
    def agregar_topping(self, topping):
        """
        Agrega un topping al cono
        
        Args:
            topping (str): Nombre del topping a agregar
        
        Returns:
            ConoPersonalizadoBuilder: Self para method chaining
        """
        if topping in self._precios_toppings:
            if topping not in self.toppings_agregados:
                self.toppings_agregados.append(topping)
                self.cono.ingredientes.append(topping)
                self.precio_toppings += self._precios_toppings[topping]
        return self
    
    def agregar_multiples_toppings(self, toppings):
        """
        Agrega múltiples toppings al cono
        
        Args:
            toppings (list): Lista de toppings a agregar
        
        Returns:
            ConoPersonalizadoBuilder: Self para method chaining
        """
        for topping in toppings:
            self.agregar_topping(topping)
        return self
    
    def calcular_precio_total(self):
        """
        Calcula el precio total del cono personalizado
        
        Returns:
            float: Precio total
        """
        return self.cono.calcular_precio_base() + self.precio_toppings
    
    def construir(self):
        """
        Construye y retorna el cono personalizado final
        
        Returns:
            dict: Información completa del cono construido
        """
        return {
            'tipo_base': self.cono.__class__.__name__,
            'variante': self.cono.__class__.__name__.replace('Cono', ''),
            'tamanio': self.cono.tamanio,
            'ingredientes_base': [ing for ing in self.cono.ingredientes 
                                if ing not in self.toppings_agregados],
            'toppings_agregados': self.toppings_agregados.copy(),
            'ingredientes_finales': self.cono.ingredientes.copy(),
            'precio_base': self.cono.calcular_precio_base(),
            'precio_toppings': self.precio_toppings,
            'precio_total': self.calcular_precio_total()
        }
    
    @classmethod
    def obtener_precios_toppings(cls):
        """Obtiene la lista de precios de toppings disponibles"""
        return cls._precios_toppings.copy()
    
    @classmethod
    def obtener_toppings_disponibles(cls):
        """Obtiene la lista de toppings disponibles"""
        return list(cls._precios_toppings.keys())

class ConoDirector:
    """Director que conoce las recetas específicas para construir conos"""
    
    def __init__(self, builder: ConoPersonalizadoBuilder):
        self.builder = builder
    
    def construir_cono_premium(self):
        """Construye un cono premium con toppings selectos"""
        return (self.builder
                .agregar_topping('queso_extra')
                .agregar_topping('guacamole')
                .agregar_topping('bacon')
                .construir())
    
    def construir_cono_economico(self):
        """Construye un cono económico con toppings básicos"""
        return (self.builder
                .agregar_topping('queso_extra')
                .agregar_topping('jalapeños')
                .construir())
    
    def construir_cono_personalizado(self, toppings):
        """
        Construye un cono con toppings específicos
        
        Args:
            toppings (list): Lista de toppings deseados
        
        Returns:
            dict: Información del cono construido
        """
        return (self.builder
                .agregar_multiples_toppings(toppings)
                .construir())