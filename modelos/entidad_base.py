"""Clase abstracta que representa las entidades generales del sistema."""
from abc import ABC, abstractmethod


class EntidadBase(ABC):
    """Toda entidad (Cliente, Servicio, Reserva) tiene id y descripción."""

    def __init__(self, identificador: str):
        self._id = identificador  # Atributo protegido (encapsulación)

    @property
    def id(self) -> str:
        """Identificador de solo lectura."""
        return self._id

    @abstractmethod
    def describir(self) -> str:
        """Texto descriptivo; cada subclase lo implementa a su manera."""

    def __str__(self) -> str:
        return self.describir()  # str() reutiliza el método polimórfico
