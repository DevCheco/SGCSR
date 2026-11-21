"""Clase Cliente con datos personales encapsulados y validados."""
import re

from excepciones import ClienteInvalidoError
from modelos.entidad_base import EntidadBase

# Expresiones regulares de validación
_RE_NOMBRE = re.compile(r"^[A-Za-zÁÉÍÓÚáéíóúÑñÜü ]{3,60}$")
_RE_EMAIL = re.compile(r"^[\w.+-]+@[\w-]+(\.[\w-]+)+$")


class Cliente(EntidadBase):
    """Cliente de Software FJ. Los datos son privados y se validan."""

    def __init__(self, identificador: str, nombre: str, documento: str,
                 email: str, telefono: str):
        super().__init__(identificador)
        # Cada asignación pasa por su setter (y por tanto por la validación)
        self.nombre = nombre
        self.documento = documento
        self.email = email
        self.telefono = telefono

    # ---- nombre ----
    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        if not isinstance(valor, str) or not _RE_NOMBRE.match(valor.strip()):
            raise ClienteInvalidoError(
                f"Nombre inválido: {valor!r} (3-60 letras y espacios)")
        self.__nombre = valor.strip()

    # ---- documento ----
    @property
    def documento(self) -> str:
        return self.__documento

    @documento.setter
    def documento(self, valor: str) -> None:
        valor = str(valor).strip()
        if not valor.isdigit() or not 6 <= len(valor) <= 12:
            raise ClienteInvalidoError(
                f"Documento inválido: {valor!r} (6 a 12 dígitos)")
        self.__documento = valor

    # ---- email ----
    @property
    def email(self) -> str:
        return self.__email

    @email.setter
    def email(self, valor: str) -> None:
        if not isinstance(valor, str) or not _RE_EMAIL.match(valor.strip()):
            raise ClienteInvalidoError(f"Correo inválido: {valor!r}")
        self.__email = valor.strip().lower()

    # ---- teléfono ----
    @property
    def telefono(self) -> str:
        return self.__telefono

    @telefono.setter
    def telefono(self, valor: str) -> None:
        valor = str(valor).strip()
        if not valor.isdigit() or not 7 <= len(valor) <= 10:
            raise ClienteInvalidoError(
                f"Teléfono inválido: {valor!r} (7 a 10 dígitos)")
        self.__telefono = valor

    def describir(self) -> str:
        """Implementa el método abstracto de EntidadBase."""
        return f"{self.id} | {self.nombre} | CC {self.documento} | {self.email}"
