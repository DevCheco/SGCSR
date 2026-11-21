"""Clase abstracta Servicio con costos sobrecargados."""
from abc import abstractmethod

from excepciones import CalculoInconsistenteError, ServicioInvalidoError
from modelos.entidad_base import EntidadBase

IVA = 0.19  # Impuesto de referencia (19 %)


class Servicio(EntidadBase):
    """Servicio genérico que ofrece Software FJ."""

    def __init__(self, identificador: str, nombre: str, tarifa_hora: float,
                 disponible: bool = True):
        super().__init__(identificador)
        self._nombre = nombre
        self._tarifa_hora = tarifa_hora
        self._disponible = disponible

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def tarifa_hora(self) -> float:
        return self._tarifa_hora

    @property
    def disponible(self) -> bool:
        return self._disponible

    @disponible.setter
    def disponible(self, valor: bool) -> None:
        self._disponible = bool(valor)

    def validar_parametros(self) -> None:
        """Valida los datos comunes; las hijas lo extienden con super()."""
        if not isinstance(self._nombre, str) or len(self._nombre.strip()) < 3:
            raise ServicioInvalidoError(f"Nombre de servicio inválido: {self._nombre!r}")
        if (isinstance(self._tarifa_hora, bool)
                or not isinstance(self._tarifa_hora, (int, float))
                or self._tarifa_hora <= 0):
            raise ServicioInvalidoError(
                f"Tarifa por hora inválida: {self._tarifa_hora!r}")

    @abstractmethod
    def calcular_costo_base(self, horas: float) -> float:
        """Costo sin impuestos ni descuentos (polimórfico)."""

    def calcular_costo(self, horas: float, impuesto: float | None = None,
                       descuento: float | None = None) -> float:
        """Sobrecarga simulada con parámetros opcionales. Variantes:
        calcular_costo(h)              -> costo base
        calcular_costo(h, imp)         -> con impuesto
        calcular_costo(h, descuento=d) -> con descuento
        calcular_costo(h, imp, d)      -> con ambos
        """
        total = self.calcular_costo_base(horas)  # Costo base polimórfico
        if descuento is not None:  # Variante con descuento
            if not 0 <= descuento < 1:
                raise CalculoInconsistenteError(
                    f"Descuento fuera de rango [0,1): {descuento}")
            total *= (1 - descuento)
        if impuesto is not None:  # Variante con impuesto
            if not 0 <= impuesto <= 1:
                raise CalculoInconsistenteError(
                    f"Impuesto fuera de rango [0,1]: {impuesto}")
            total *= (1 + impuesto)
        if total <= 0:  # Resultado imposible
            raise CalculoInconsistenteError(f"Costo no positivo: {total}")
        return round(total, 2)
