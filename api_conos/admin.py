from django.contrib import admin
from .models import PedidoCono

@admin.register(PedidoCono)
class PedidoConoAdmin(admin.ModelAdmin):
    list_display = [
        'id', 
        'cliente', 
        'variante', 
        'tamanio_cono', 
        'toppings_display', 
        'fecha_pedido'
    ]
    
    list_filter = [
        'variante', 
        'tamanio_cono', 
        'fecha_pedido'
    ]
    
    search_fields = [
        'cliente', 
        'variante'
    ]
    
    readonly_fields = ['fecha_pedido']
    
    fieldsets = (
        ('Información del Cliente', {
            'fields': ('cliente',)
        }),
        ('Detalles del Pedido', {
            'fields': ('variante', 'tamanio_cono', 'toppings')
        }),
        ('Información del Sistema', {
            'fields': ('fecha_pedido',),
            'classes': ('collapse',)
        }),
    )
    
    def toppings_display(self, obj):
        return obj.toppings_display
    toppings_display.short_description = 'Toppings Extra'
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # Agregar ayuda para el campo toppings
        if 'toppings' in form.base_fields:
            form.base_fields['toppings'].help_text = (
                f"Toppings disponibles: {', '.join(PedidoCono.TOPPINGS_PERMITIDOS)}"
            )
        return form