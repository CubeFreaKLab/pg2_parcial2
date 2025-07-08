# Parcial 2 - PG2 
:card_index: Carrera: *Sistemas Informaticos*

:notebook: Materia: *Programación 2* 

:bust_in_silhouette: Nombre Completo: *Jorge Daniel Choque Ferrufino*

:calendar: Fecha: *7 de Julio del 2025*
## Descripción del Proyecto

Este proyecto implementa una API REST con Django Rest Framework para la simulación de un módulo de negocio de comida rápida en conos.
## Arquitectura y Patrones de Diseño

### 1. Factory Method Pattern

**Ubicación:** `api_conos/factory.py`

El patrón Factory Method se aplica en la clase `ConoFactory` para crear diferentes tipos de conos base según la variante especificada:

```python
def get_precio_final(self, obj):
    # Paso 1: Usar Factory para crear el cono base
    cono_base = ConoFactory.crear_cono_base(obj.variante, obj.tamanio_cono)
```

**Propósito:** Encapsula la lógica de creación de objetos `ConoBase` y sus subclases (`ConoCarnivoro`, `ConoVegetariano`, `ConoSaludable`) sin exponer la lógica de instanciación al cliente.

**Ventajas:**
- Desacopla la creación de objetos de su uso
- Facilita la adición de nuevos tipos de conos
- Mantiene el principio de responsabilidad única

### 2. Builder Pattern

**Ubicación:** `api_conos/builder.py`

El patrón Builder se implementa en `ConoPersonalizadoBuilder` para construir conos personalizados paso a paso:

```python
def get_ingredientes_finales(self, obj):
    # Paso 2: Usar Builder para personalizar el cono
    builder = ConoPersonalizadoBuilder(cono_base)
    director = ConoDirector(builder)
    
    # Construir el cono personalizado con los toppings
    cono_personalizado = director.construir_cono_personalizado(obj.toppings or [])
```

**Propósito:** Permite la construcción paso a paso de conos complejos, agregando toppings y calculando precios de manera controlada.

**Componentes:**
- **Builder:** `ConoPersonalizadoBuilder` - Construye el producto paso a paso
- **Director:** `ConoDirector` - Conoce la secuencia de construcción
- **Producto:** Diccionario con la información completa del cono

### 3. Singleton Pattern

**Ubicación:** `api_conos/logger.py`

El patrón Singleton se implementa en `LoggerSingleton` para mantener un registro único de logs del sistema:

```python
def get_precio_final(self, obj):
    logger = obtener_logger()  # Obtiene la instancia única
    
    # Registrar la operación en el log
    logger.registrar_operacion(
        tipo_operacion='precio_final',
        detalle=f'Cálculo de precio para pedido {obj.id}',
        datos_extra={...}
    )
```

**Propósito:** Garantiza que exista una única instancia del logger en toda la aplicación, manteniendo un registro centralizado y consistente de todas las operaciones.

**Características:**
- Thread-safe utilizando `threading.Lock()`
- Lazy initialization
- Registro de operaciones de cálculo de precios e ingredientes


### Endpoints Adicionales

- `GET /api/pedidos_conos/tipos_disponibles/` - Tipos de conos disponibles
- `GET /api/pedidos_conos/toppings_disponibles/` - Toppings y precios
- `GET /api/pedidos_conos/estadisticas/` - Estadísticas del sistema
- `GET /api/pedidos_conos/logs_recientes/` - Logs recientes
- `GET /api/pedidos_conos/{id}/detalle_construccion/` - Detalle de construcción

## Instalación y Uso

### 1. Clonar el repositorio

```bash
https://github.com/CubeFreaKLab/pg2_parcial2.git
cd pg2_parcial2
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Ejecutar migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Crear superusuario

```bash
python manage.py createsuperuser
```

### 5. Ejecutar el servidor

```bash
python manage.py runserver
```

### 6. Acceder a la aplicación

- **Admin:** http://localhost:8000/admin/
- **API:** http://localhost:8000/api/pedidos_conos/

## Ejemplo de Uso de la API

### Crear un pedido

```json
POST /api/pedidos_conos/
{
    "cliente": "Jorge Daniel",
    "variante": "Carnívoro",
    "tamanio_cono": "Grande",
    "toppings": ["queso_extra", "bacon", "guacamole"]
}
```

### Respuesta con atributos calculados

```json
{
    "id": 1,
    "cliente": "Jorge Daniel",
    "variante": "Carnívoro",
    "tamanio_cono": "Grande",
    "toppings": ["queso_extra", "bacon", "guacamole"],
    "fecha_pedido": "2025-01-15",
    "precio_final": 33.40,
    "ingredientes_finales": [
        "tortilla_de_maíz",
        "carne_molida",
        "queso_cheddar",
        "lechuga",
        "tomate",
        "salsa_picante",
        "queso_extra",
        "bacon",
        "guacamole"
    ],
    "resumen_construccion": {
        "tipo_base": "ConoCarnivoro",
        "variante": "Carnívoro",
        "tamanio": "Grande",
        "precio_base": 23.40,
        "precio_toppings": 10.00,
        "precio_total": 33.40,
        "total_ingredientes": 9,
        "total_toppings": 3
    }
}
```

## Capturas de Pantalla

![Demo](https://raw.githubusercontent.com/CubeFreaKLab/pg2_parcial2/refs/heads/main/captura.png)



### Administrador de Django
*[Aquí deberías incluir capturas de pantalla del admin de Django mostrando la interfaz de registro de pedidos]*

### API REST con atributos calculados
*[Aquí deberías incluir capturas de pantalla de la API mostrando las respuestas con los atributos calculados]*

## Toppings Disponibles

| Topping | Precio |
|---------|--------|
| queso_extra | $2.50 |
| papas_al_hilo | $3.00 |
| salchicha_extra | $4.00 |
| bacon | $4.50 |
| cebolla_caramelizada | $2.00 |
| guacamole | $3.50 |
| jalapeños | $1.50 |
| aguacate | $3.00 |
| pollo_desmenuzado | $4.00 |
| champiñones | $2.50 |

## Validaciones Implementadas

- **Toppings:** Solo se permiten toppings de la lista predefinida
- **Variantes:** Solo se permiten las variantes configuradas (Carnívoro, Vegetariano, Saludable)
- **Tamaños:** Solo se permiten los tamaños configurados (Pequeño, Mediano, Grande)

## Logs del Sistema

El sistema registra automáticamente:
- Cálculos de precios finales
- Cálculos de ingredientes finales
- Creación de nuevos pedidos
- Personalizaciones de conos

