from abc import ABC, abstractmethod

class ConoBase(ABC):
    """Clase base abstracta para todos los tipos de conos"""
    
    def __init__(self, tamanio="Mediano"):
        self.tamanio = tamanio
        self.ingredientes = []
        self.precio_base = 0.0
    
    @abstractmethod
    def preparar_base(self):
        """Método abstracto para preparar la base del cono"""
        pass
    
    def calcular_precio_base(self):
        """Calcular precio base según el tamaño"""
        multiplicadores = {
            'Pequeño': 0.8,
            'Mediano': 1.0,
            'Grande': 1.3
        }
        return self.precio_base * multiplicadores.get(self.tamanio, 1.0)
    
    def obtener_info(self):
        """Obtener información del cono"""
        return {
            'tipo': self.__class__.__name__,
            'tamanio': self.tamanio,
            'ingredientes': self.ingredientes.copy(),
            'precio_base': self.calcular_precio_base()
        }

class ConoCarnivoro(ConoBase):
    """Cono carnívoro con ingredientes de carne"""
    
    def __init__(self, tamanio="Mediano"):
        super().__init__(tamanio)
        self.precio_base = 18.0
        self.preparar_base()
    
    def preparar_base(self):
        self.ingredientes = [
            'tortilla_de_maíz',
            'carne_molida',
            'queso_cheddar',
            'lechuga',
            'tomate',
            'salsa_picante'
        ]

class ConoVegetariano(ConoBase):
    """Cono vegetariano con ingredientes vegetales"""
    
    def __init__(self, tamanio="Mediano"):
        super().__init__(tamanio)
        self.precio_base = 15.0
        self.preparar_base()
    
    def preparar_base(self):
        self.ingredientes = [
            'tortilla_de_maíz',
            'frijoles_refritos',
            'queso_vegano',
            'lechuga',
            'tomate',
            'aguacate',
            'salsa_verde'
        ]

class ConoSaludable(ConoBase):
    """Cono saludable con ingredientes bajos en grasa"""
    
    def __init__(self, tamanio="Mediano"):
        super().__init__(tamanio)
        self.precio_base = 16.0
        self.preparar_base()
    
    def preparar_base(self):
        self.ingredientes = [
            'tortilla_integral',
            'pollo_a_la_plancha',
            'queso_bajo_en_grasa',
            'espinaca',
            'tomate_cherry',
            'pepino',
            'aderezo_yogurt'
        ]