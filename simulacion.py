"""Simulación de 16 operaciones (válidas e inválidas) sin detener el sistema."""
from excepciones import ErrorSistemaFJ
from gestor import GestorFJ
from logger_config import obtener_logger
from modelos.servicio import IVA

log = obtener_logger()


def ejecutar_simulacion(gestor: GestorFJ, salida=print) -> None:
    """Ejecuta las operaciones; `salida` recibe cada línea de resultado."""

    def operacion(numero, titulo, funcion):
        """Corre una operación capturando cualquier error."""
        try:
            resultado = funcion()
            salida(f"[{numero:02d}] OK     {titulo} -> {resultado}")
        except ErrorSistemaFJ as error:  # Error controlado del dominio
            salida(f"[{numero:02d}] ERROR  {titulo} -> {type(error).__name__}: {error}")
        except Exception as error:  # Error imprevisto: no se cae el sistema
            log.exception("Error inesperado en operación %s", numero)
            salida(f"[{numero:02d}] FATAL  {titulo} -> {error!r} (el sistema continúa)")

    log.info("=== INICIO DE SIMULACIÓN ===")
    operacion(1, "Cliente válido (Ana Pérez)", lambda: gestor.registrar_cliente(
        nombre="Ana Pérez", documento="1020304050", email="ana@correo.com", telefono="3001234567"))
    operacion(2, "Cliente con correo inválido", lambda: gestor.registrar_cliente(
        nombre="Luis Gómez", documento="1098765432", email="luis-correo", telefono="3109876543"))
    operacion(3, "Cliente sin teléfono (parámetro faltante)", lambda: gestor.registrar_cliente(
        nombre="Marta Ruiz", documento="52525252", email="marta@correo.com", telefono=""))
    operacion(4, "Cliente válido (Carlos Díaz)", lambda: gestor.registrar_cliente(
        nombre="Carlos Díaz", documento="79797979", email="carlos@correo.com", telefono="3151112233"))
    operacion(5, "Sala válida", lambda: gestor.crear_servicio(
        "sala", nombre="Sala Innovación", tarifa_hora=50000, capacidad=12, proyector=True))
    operacion(6, "Equipo con cantidad inválida", lambda: gestor.crear_servicio(
        "equipo", nombre="Portátiles", tarifa_hora=20000, tipo_equipo="Laptop", cantidad=-3))
    operacion(7, "Asesoría válida", lambda: gestor.crear_servicio(
        "asesoria", nombre="Asesoría Cloud", tarifa_hora=80000, especialidad="Cloud", nivel=3))
    operacion(8, "Servicio de tipo inexistente", lambda: gestor.crear_servicio(
        "catering", nombre="Café", tarifa_hora=1000))
    operacion(9, "Reserva exitosa (RES-001)", lambda: gestor.crear_reserva("CLI-001", "SRV-001", 3))
    operacion(10, "Reserva con cliente inexistente", lambda: gestor.crear_reserva("CLI-999", "SRV-001", 2))
    operacion(11, "Reserva con duración inválida (30 h)", lambda: gestor.crear_reserva("CLI-001", "SRV-001", 30))
    operacion(12, "Confirmar y procesar RES-001 con IVA y 10% dto", lambda: (
        gestor.obtener_reserva("RES-001").confirmar(),
        gestor.obtener_reserva("RES-001").procesar(impuesto=IVA, descuento=0.10))[1])
    operacion(13, "Procesar de nuevo RES-001 (no permitido)",
              lambda: gestor.obtener_reserva("RES-001").procesar())
    operacion(14, "Reserva sobre servicio no disponible", lambda: (
        setattr(gestor.servicios[1], "disponible", False),
        gestor.crear_reserva("CLI-001", "SRV-002", 1))[1])
    operacion(15, "Cancelar reserva y volver a cancelar", lambda: (
        gestor.crear_reserva("CLI-001", "SRV-001", 1),
        gestor.obtener_reserva("RES-002").cancelar(),
        gestor.obtener_reserva("RES-002").cancelar()))
    operacion(16, "Descuento fuera de rango (cálculo inconsistente)", lambda: (
        gestor.obtener_reserva("RES-002"), gestor.servicios[0].calcular_costo(2, descuento=1.5)))
    salida("Simulación terminada: el sistema siguió operando tras todos los errores.")
    log.info("=== FIN DE SIMULACIÓN ===")


if __name__ == "__main__":
    ejecutar_simulacion(GestorFJ())
