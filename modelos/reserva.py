"""Clase Reserva: integra cliente, servicio, duración y estado."""
from enum import Enum

from excepciones import (CalculoInconsistenteError, ErrorSistemaFJ,
                         OperacionNoPermitidaError, ReservaInvalidaError,
                         ServicioNoDisponibleError)
from logger_config import obtener_logger
from modelos.cliente import Cliente
from modelos.entidad_base import EntidadBase
from modelos.servicio import Servicio

log = obtener_logger()


class EstadoReserva(Enum):
    """Estados posibles del ciclo de vida de una reserva."""
    PENDIENTE = "Pendiente"
    CONFIRMADA = "Confirmada"
    PROCESADA = "Procesada"
    CANCELADA = "Cancelada"


class Reserva(EntidadBase):
    """Reserva de un servicio por parte de un cliente."""

    def __init__(self, identificador: str, cliente: Cliente,
                 servicio: Servicio, horas: float):
        super().__init__(identificador)
        if not isinstance(cliente, Cliente) or not isinstance(servicio, Servicio):
            raise ReservaInvalidaError("Cliente o servicio inválidos")
        if (isinstance(horas, bool) or not isinstance(horas, (int, float))
                or not 0 < horas <= 24):
            raise ReservaInvalidaError(f"Duración inválida: {horas!r} (0-24 h)")
        self.cliente = cliente
        self.servicio = servicio
        self.horas = horas
        self.estado = EstadoReserva.PENDIENTE  # Estado inicial
        self.costo_total: float | None = None  # Se fija al procesar

    def confirmar(self) -> None:
        """Pendiente -> Confirmada, si el servicio sigue disponible."""
        if self.estado is not EstadoReserva.PENDIENTE:
            raise OperacionNoPermitidaError(
                f"No se puede confirmar una reserva {self.estado.value}")
        if not self.servicio.disponible:
            raise ServicioNoDisponibleError(
                f"El servicio {self.servicio.nombre} no está disponible")
        self.estado = EstadoReserva.CONFIRMADA
        log.info("Reserva %s confirmada", self.id)

    def cancelar(self) -> None:
        """Cancela una reserva pendiente o confirmada."""
        if self.estado in (EstadoReserva.CANCELADA, EstadoReserva.PROCESADA):
            raise OperacionNoPermitidaError(
                f"No se puede cancelar una reserva {self.estado.value}")
        self.estado = EstadoReserva.CANCELADA
        log.info("Reserva %s cancelada", self.id)

    def procesar(self, impuesto: float | None = None,
                 descuento: float | None = None) -> float:
        """Confirmada -> Procesada, calculando el costo total."""
        try:
            if self.estado is not EstadoReserva.CONFIRMADA:
                raise OperacionNoPermitidaError(
                    "Solo se procesan reservas confirmadas "
                    f"(actual: {self.estado.value})")
            try:
                costo = self.servicio.calcular_costo(self.horas, impuesto, descuento)
            except ErrorSistemaFJ:
                raise  # Errores propios pasan sin cambios
            except Exception as error:  # Imprevistos: se encadenan
                raise CalculoInconsistenteError(
                    "Fallo inesperado calculando el costo") from error
        except ErrorSistemaFJ as error:
            log.error("Procesar reserva %s falló: %s", self.id, error)
            raise  # Se propaga para que el llamador decida
        else:  # Solo si no hubo excepciones
            self.costo_total = costo
            self.estado = EstadoReserva.PROCESADA
            log.info("Reserva %s procesada. Total: $%s", self.id, f"{costo:,.2f}")
            return costo
        finally:  # Siempre se ejecuta
            log.debug("Fin de procesamiento de la reserva %s", self.id)

    def describir(self) -> str:
        total = f"${self.costo_total:,.2f}" if self.costo_total else "-"
        return (f"{self.id} | {self.cliente.nombre} -> {self.servicio.nombre} | "
                f"{self.horas} h | {self.estado.value} | {total}")
