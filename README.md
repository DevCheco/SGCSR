# Software FJ - Sistema Integral de Gestión de Clientes, Servicios y Reservas

Proyecto POO en **Python 3.12 + Tkinter**, sin base de datos. Solo se usan archivos para el log (`logs/sistema.log`).

## Ejecución
```bash
python main.py          # Interfaz gráfica (pestaña "Log y simulación" ejecuta las 16 operaciones)
python simulacion.py    # Simulación por consola
```

## Estructura
| Archivo | Contenido |
|---|---|
| `excepciones.py` | Excepciones personalizadas (`ErrorSistemaFJ` y derivadas) |
| `logger_config.py` | Configuración del log |
| `modelos/entidad_base.py` | Clase abstracta `EntidadBase` |
| `modelos/cliente.py` | `Cliente` con validaciones y encapsulación |
| `modelos/servicio.py` | `Servicio` abstracta, `calcular_costo` sobrecargado |
| `modelos/servicios_concretos.py` | `ReservaSala`, `AlquilerEquipo`, `AsesoriaEspecializada` |
| `modelos/reserva.py` | `Reserva`: confirmar, cancelar, procesar |
| `gestor.py` | Listas internas y lógica de negocio |
| `simulacion.py` | 16 operaciones válidas e inválidas |
| `interfaz/ventana_principal.py` | GUI Tkinter |

## Conceptos aplicados
Abstracción, herencia, polimorfismo, encapsulación, sobrecarga simulada (parámetros opcionales), `try/except`, `try/except/else`, `try/except/finally` y encadenamiento (`raise ... from ...`).

## Integrantes
(Completar con los 5 integrantes y sus aportes por commit.)
