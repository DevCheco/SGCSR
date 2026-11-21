"""Servicios especializados: sala, equipo y asesoría (herencia)."""
from excepciones import ServicioInvalidoError
from modelos.servicio import Servicio


class ReservaSala(Servicio):
    """Reserva de salas de reuniones."""

    def __init__(self, identificador, nombre, tarifa_hora, capacidad,
                 proyector=False, disponible=True):
        super().__init__(identificador, nombre, tarifa_hora, disponible)
        self._capacidad = capacidad
        self._proyector = proyector
        self.validar_parametros()  # Falla al crear si hay datos malos

    def validar_parametros(self) -> None:
        super().validar_parametros()  # Validaciones comunes
        if (isinstance(self._capacidad, bool)
                or not isinstance(self._capacidad, int)
                or not 1 <= self._capacidad <= 200):
            raise ServicioInvalidoError(f"Capacidad inválida: {self._capacidad!r}")

    def calcular_costo_base(self, horas: float) -> float:
        extra = 15000 * horas if self._proyector else 0  # Recargo proyector
        return self._tarifa_hora * horas + extra

    def describir(self) -> str:
        pro = "con proyector" if self._proyector else "sin proyector"
        return (f"{self.id} | Sala '{self.nombre}' | {self._capacidad} personas, "
                f"{pro} | ${self.tarifa_hora:,.0f}/h")


class AlquilerEquipo(Servicio):
    """Alquiler de equipos tecnológicos."""

    def __init__(self, identificador, nombre, tarifa_hora, tipo_equipo,
                 cantidad=1, disponible=True):
        super().__init__(identificador, nombre, tarifa_hora, disponible)
        self._tipo_equipo = tipo_equipo
        self._cantidad = cantidad
        self.validar_parametros()

    def validar_parametros(self) -> None:
        super().validar_parametros()
        if not isinstance(self._tipo_equipo, str) or not self._tipo_equipo.strip():
            raise ServicioInvalidoError("Tipo de equipo vacío o inválido")
        if (isinstance(self._cantidad, bool)
                or not isinstance(self._cantidad, int)
                or not 1 <= self._cantidad <= 50):
            raise ServicioInvalidoError(f"Cantidad inválida: {self._cantidad!r}")

    def calcular_costo_base(self, horas: float) -> float:
        return self._tarifa_hora * horas * self._cantidad  # Por unidad

    def describir(self) -> str:
        return (f"{self.id} | Equipo '{self.nombre}' | {self._cantidad} x "
                f"{self._tipo_equipo} | ${self.tarifa_hora:,.0f}/h")


class AsesoriaEspecializada(Servicio):
    """Asesoría con un especialista; el nivel (1-3) encarece la tarifa."""

    _FACTOR = {1: 1.0, 2: 1.5, 3: 2.0}  # Multiplicador por nivel

    def __init__(self, identificador, nombre, tarifa_hora, especialidad,
                 nivel=1, disponible=True):
        super().__init__(identificador, nombre, tarifa_hora, disponible)
        self._especialidad = especialidad
        self._nivel = nivel
        self.validar_parametros()

    def validar_parametros(self) -> None:
        super().validar_parametros()
        if not isinstance(self._especialidad, str) or len(self._especialidad.strip()) < 3:
            raise ServicioInvalidoError("Especialidad inválida")
        if self._nivel not in self._FACTOR:
            raise ServicioInvalidoError(f"Nivel inválido (1-3): {self._nivel!r}")

    def calcular_costo_base(self, horas: float) -> float:
        return self._tarifa_hora * horas * self._FACTOR[self._nivel]

    def describir(self) -> str:
        return (f"{self.id} | Asesoría '{self.nombre}' | {self._especialidad}, "
                f"nivel {self._nivel} | ${self.tarifa_hora:,.0f}/h")
