"""Excepciones personalizadas del sistema Software FJ."""


class ErrorSistemaFJ(Exception):
    """Excepción base: todas las excepciones propias heredan de ella."""


class ClienteInvalidoError(ErrorSistemaFJ):
    """Se lanza cuando los datos de un cliente no cumplen las validaciones."""


class ServicioInvalidoError(ErrorSistemaFJ):
    """Se lanza cuando los parámetros de un servicio son inválidos."""


class ParametroFaltanteError(ErrorSistemaFJ):
    """Se lanza cuando falta un parámetro obligatorio."""


class ServicioNoDisponibleError(ErrorSistemaFJ):
    """Se lanza cuando se intenta usar un servicio no disponible."""


class OperacionNoPermitidaError(ErrorSistemaFJ):
    """Se lanza cuando el estado actual no permite la operación pedida."""


class ReservaInvalidaError(ErrorSistemaFJ):
    """Se lanza ante intentos de reserva incorrectos (ids, horas, etc.)."""


class CalculoInconsistenteError(ErrorSistemaFJ):
    """Se lanza cuando un cálculo de costos produce un resultado inválido."""
