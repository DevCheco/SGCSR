"""Configuración del archivo de logs (único uso de archivos del sistema)."""
import logging
import os

# Carpeta y ruta del archivo de log, relativas a este módulo
DIR_LOGS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
RUTA_LOG = os.path.join(DIR_LOGS, "sistema.log")


def obtener_logger() -> logging.Logger:
    """Devuelve el logger global; lo configura solo la primera vez."""
    os.makedirs(DIR_LOGS, exist_ok=True)  # Crea la carpeta si no existe
    logger = logging.getLogger("software_fj")  # Logger con nombre propio
    if not logger.handlers:  # Evita duplicar handlers
        logger.setLevel(logging.DEBUG)  # Registra todos los niveles
        manejador = logging.FileHandler(RUTA_LOG, encoding="utf-8")
        manejador.setFormatter(logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(message)s"))  # Formato
        logger.addHandler(manejador)  # Asocia el handler al logger
    return logger


def leer_log() -> str:
    """Devuelve el contenido del archivo de log (cadena vacía si no existe)."""
    try:
        with open(RUTA_LOG, "r", encoding="utf-8") as archivo:
            return archivo.read()
    except OSError:  # Si falla la lectura, el sistema sigue activo
        return ""
