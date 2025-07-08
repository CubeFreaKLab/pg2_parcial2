from django.db import models
from django.core.exceptions import ValidationError
import json

class PedidoCono(models.Model):
    VARIANTES_CHOICES = [
        ('Carnívoro', 'Carnívoro'),
        ('Vegetariano', 'Vegetariano'),
        ('Saludable', 'Saludable'),
    ]
    
    TAMANIOS_CHOICES = [
        ('Pequeño', 'Pequeño'),
        ('Mediano', 'Mediano'),
        ('Grande', 'Grande'),
    ]
    
    # Toppings predefinidos permitidos
    TOPPINGS_PERMITIDOS = [
        'queso_extra',
        'papas_al_hilo',
        'salchicha_extra',
        'bacon',
        'cebolla_caramelizada',
        'guacamole',
        'jalapeños',
        'tomate_cherry',
        'aguacate',
        'pollo_desmenuzado',
        'champiñones',
        'pimiento_asado',
        'salsa_chipotle',
        'salsa_ranch',
        'salsa_barbacoa'
    ]
    
    cliente = models.CharField(max_length=100)
    variante = models.CharField(max_length=20, choices=VARIANTES_CHOICES)
    toppings = models.JSONField(default=list, blank=True)
    tamanio_cono = models.CharField(max_length=20, choices=TAMANIOS_CHOICES)
    fecha_pedido = models.DateField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Pedido de Cono"
        verbose_name_plural = "Pedidos de Conos"
        ordering = ['-fecha_pedido']
    
    def clean(self):
        """Validación personalizada para los toppings"""
        super().clean()
        
        if self.toppings:
            # Verificar que todos los toppings estén en la lista permitida
            toppings_invalidos = []
            for topping in self.toppings:
                if topping not in self.TOPPINGS_PERMITIDOS:
                    toppings_invalidos.append(topping)
            
            if toppings_invalidos:
                raise ValidationError({
                    'toppings': f'Los siguientes toppings no están permitidos: {", ".join(toppings_invalidos)}. '
                              f'Toppings permitidos: {", ".join(self.TOPPINGS_PERMITIDOS)}'
                })
    
    def save(self, *args, **kwargs):
        """Override save para ejecutar validaciones"""
        self.clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Pedido de {self.cliente} - {self.variante} {self.tamanio_cono}"
    
    @property
    def toppings_display(self):
        """Propiedad para mostrar los toppings de forma legible"""
        if not self.toppings:
            return "Sin toppings extra"
        return ", ".join(self.toppings)