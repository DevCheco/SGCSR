"""Punto de entrada: lanza la interfaz Tkinter de Software FJ."""
from interfaz.ventana_principal import VentanaPrincipal
from logger_config import obtener_logger

if __name__ == "__main__":
    obtener_logger().info("Aplicación iniciada")
    VentanaPrincipal().mainloop()  # Bucle principal de Tkinter
