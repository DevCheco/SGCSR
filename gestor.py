"""Gestor: listas internas y lógica de negocio (sin base de datos)."""
from excepciones import (ClienteInvalidoError, ErrorSistemaFJ,
                         ParametroFaltanteError, ReservaInvalidaError,
                         ServicioInvalidoError, ServicioNoDisponibleError)
from logger_config import obtener_logger
from modelos.cliente import Cliente
from modelos.reserva import Reserva
from modelos.servicios_concretos import (AlquilerEquipo, AsesoriaEspecializada,
                                         ReservaSala)

log = obtener_logger()

# Tipos de servicio disponibles y sus parámetros obligatorios
TIPOS_SERVICIO = {
    "sala": (ReservaSala, ["nombre", "tarifa_hora", "capacidad"]),
    "equipo": (AlquilerEquipo, ["nombre", "tarifa_hora", "tipo_equipo"]),
    "asesoria": (AsesoriaEspecializada, ["nombre", "tarifa_hora", "especialidad"]),
}


class GestorFJ:
    """Administra clientes, servicios y reservas en listas en memoria."""

    def __init__(self):
        self.clientes: list[Cliente] = []
        self.servicios: list = []
        self.reservas: list[Reserva] = []

    # ---------- Clientes ----------
    def registrar_cliente(self, **datos) -> Cliente:
        """Crea un cliente validado; registra el resultado en el log."""
        try:
            faltan = [c for c in ("nombre", "documento", "email", "telefono")
                      if not str(datos.get(c, "")).strip()]
            if faltan:
                raise ParametroFaltanteError(f"Faltan datos del cliente: {faltan}")
            if any(c.documento == str(datos["documento"]).strip() for c in self.clientes):
                raise ClienteInvalidoError(
                    f"Ya existe un cliente con documento {datos['documento']}")
            cliente = Cliente(f"CLI-{len(self.clientes) + 1:03d}", **datos)
        except TypeError as error:  # Argumentos desconocidos: se encadena
            log.error("Registro de cliente falló: %s", error)
            raise ClienteInvalidoError("Datos de cliente mal formados") from error
        except ErrorSistemaFJ as error:
            log.error("Registro de cliente falló: %s", error)
            raise
        else:  # Solo si todo salió bien
            self.clientes.append(cliente)
            log.info("Cliente registrado: %s", cliente.describir())
            return cliente
        finally:
            log.debug("Fin de registrar_cliente")

    # ---------- Servicios ----------
    def crear_servicio(self, tipo: str, **params):
        """Crea un servicio del tipo indicado (polimorfismo de creación)."""
        try:
            if tipo not in TIPOS_SERVICIO:
                raise ServicioInvalidoError(f"Tipo de servicio desconocido: {tipo!r}")
            clase, requeridos = TIPOS_SERVICIO[tipo]
            faltan = [p for p in requeridos if params.get(p) in (None, "")]
            if faltan:
                raise ParametroFaltanteError(f"Faltan parámetros: {faltan}")
            servicio = clase(f"SRV-{len(self.servicios) + 1:03d}", **params)
        except TypeError as error:
            log.error("Creación de servicio falló: %s", error)
            raise ServicioInvalidoError("Parámetros de servicio mal formados") from error
        except ErrorSistemaFJ as error:
            log.error("Creación de servicio falló: %s", error)
            raise
        else:
            self.servicios.append(servicio)
            log.info("Servicio creado: %s", servicio.describir())
            return servicio
        finally:
            log.debug("Fin de crear_servicio")

    # ---------- Reservas ----------
    def _buscar(self, lista: list, identificador: str, nombre: str):
        """Busca una entidad por id o lanza ReservaInvalidaError."""
        for elemento in lista:
            if elemento.id == identificador:
                return elemento
        raise ReservaInvalidaError(f"{nombre} no encontrado: {identificador!r}")

    def crear_reserva(self, id_cliente: str, id_servicio: str, horas) -> Reserva:
        """Crea una reserva pendiente tras validar todos los datos."""
        try:
            cliente = self._buscar(self.clientes, id_cliente, "Cliente")
            servicio = self._buscar(self.servicios, id_servicio, "Servicio")
            if not servicio.disponible:
                raise ServicioNoDisponibleError(
                    f"El servicio {servicio.nombre} no está disponible")
            reserva = Reserva(f"RES-{len(self.reservas) + 1:03d}",
                              cliente, servicio, horas)
        except ErrorSistemaFJ as error:
            log.error("Creación de reserva falló: %s", error)
            raise
        else:
            self.reservas.append(reserva)
            log.info("Reserva creada: %s", reserva.describir())
            return reserva
        finally:
            log.debug("Fin de crear_reserva")

    def obtener_reserva(self, identificador: str) -> Reserva:
        """Devuelve una reserva por id (o lanza ReservaInvalidaError)."""
        return self._buscar(self.reservas, identificador, "Reserva")
