"""Interfaz gráfica Tkinter de Software FJ (pestañas por módulo)."""
import tkinter as tk
from tkinter import messagebox, ttk

from excepciones import ErrorSistemaFJ
from gestor import GestorFJ
from logger_config import leer_log, obtener_logger
from simulacion import ejecutar_simulacion

log = obtener_logger()


def _numero(texto: str):
    """Convierte texto a int/float; si no puede, devuelve el texto tal cual
    para que la validación del modelo lance el error correspondiente."""
    try:
        return int(texto)
    except ValueError:
        try:
            return float(texto)
        except ValueError:
            return texto.strip()


class VentanaPrincipal(tk.Tk):
    """Ventana principal con pestañas: Clientes, Servicios, Reservas, Log."""

    def __init__(self):
        super().__init__()
        self.title("Software FJ - Gestión de Clientes, Servicios y Reservas")
        self.geometry("900x560")
        self.gestor = GestorFJ()  # Lógica de negocio en memoria
        # Ningún error no capturado cierra la aplicación
        self.report_callback_exception = self._error_inesperado
        pestanas = ttk.Notebook(self)
        pestanas.pack(fill="both", expand=True, padx=6, pady=6)
        self._construir_clientes(pestanas)
        self._construir_servicios(pestanas)
        self._construir_reservas(pestanas)
        self._construir_log(pestanas)

    # ---------- Utilidades ----------
    def _error_inesperado(self, tipo, valor, traza):
        """Maneja errores imprevistos: log + aviso, sin cerrar la app."""
        log.error("Error inesperado en la GUI: %r", valor, exc_info=(tipo, valor, traza))
        messagebox.showerror("Error inesperado", f"{valor}\nLa aplicación sigue activa.")

    def _ejecutar(self, accion, mensaje_ok=None):
        """Ejecuta una acción mostrando los errores sin detener el programa."""
        try:
            resultado = accion()
        except ErrorSistemaFJ as error:  # Errores controlados del dominio
            messagebox.showwarning(type(error).__name__, str(error))
            return None
        else:
            if mensaje_ok:
                messagebox.showinfo("Éxito", mensaje_ok)
            return resultado
        finally:
            self._refrescar()  # Siempre actualiza tablas y listas

    def _tabla(self, padre, columnas, alto=10):
        """Crea un Treeview con las columnas dadas."""
        tabla = ttk.Treeview(padre, columns=columnas, show="headings", height=alto)
        for col in columnas:
            tabla.heading(col, text=col)
            tabla.column(col, width=120)
        tabla.pack(fill="both", expand=True, padx=6, pady=6)
        return tabla

    def _campo(self, padre, etiqueta, fila, col=0):
        """Crea una etiqueta con su Entry y devuelve la variable."""
        ttk.Label(padre, text=etiqueta).grid(row=fila, column=col, sticky="e", padx=4, pady=2)
        var = tk.StringVar()
        ttk.Entry(padre, textvariable=var, width=24).grid(row=fila, column=col + 1, padx=4, pady=2)
        return var

    # ---------- Pestaña Clientes ----------
    def _construir_clientes(self, pestanas):
        marco = ttk.Frame(pestanas)
        pestanas.add(marco, text="Clientes")
        form = ttk.Frame(marco)
        form.pack(anchor="w", padx=6, pady=6)
        self.c_nombre = self._campo(form, "Nombre", 0)
        self.c_doc = self._campo(form, "Documento", 1)
        self.c_email = self._campo(form, "Correo", 0, 2)
        self.c_tel = self._campo(form, "Teléfono", 1, 2)
        ttk.Button(form, text="Registrar cliente", command=self._registrar_cliente).grid(row=2, column=1, pady=6)
        self.t_clientes = self._tabla(marco, ("ID", "Nombre", "Documento", "Correo"))

    def _registrar_cliente(self):
        cliente = self._ejecutar(lambda: self.gestor.registrar_cliente(
            nombre=self.c_nombre.get(), documento=self.c_doc.get(),
            email=self.c_email.get(), telefono=self.c_tel.get()), "Cliente registrado")
        if cliente:  # Limpia el formulario solo si fue exitoso
            for var in (self.c_nombre, self.c_doc, self.c_email, self.c_tel):
                var.set("")

    # ---------- Pestaña Servicios ----------
    def _construir_servicios(self, pestanas):
        marco = ttk.Frame(pestanas)
        pestanas.add(marco, text="Servicios")
        form = ttk.Frame(marco)
        form.pack(anchor="w", padx=6, pady=6)
        ttk.Label(form, text="Tipo").grid(row=0, column=0, sticky="e")
        self.s_tipo = ttk.Combobox(form, values=["sala", "equipo", "asesoria"], state="readonly", width=21)
        self.s_tipo.current(0)
        self.s_tipo.grid(row=0, column=1, padx=4)
        self.s_tipo.bind("<<ComboboxSelected>>", self._cambiar_tipo)
        self.s_nombre = self._campo(form, "Nombre", 1)
        self.s_tarifa = self._campo(form, "Tarifa/hora", 2)
        self.s_p1_lbl = ttk.Label(form, text="Capacidad")
        self.s_p1_lbl.grid(row=0, column=2, sticky="e")
        self.s_p1 = tk.StringVar()
        ttk.Entry(form, textvariable=self.s_p1, width=24).grid(row=0, column=3, padx=4)
        self.s_p2_lbl = ttk.Label(form, text="Proyector (si/no)")
        self.s_p2_lbl.grid(row=1, column=2, sticky="e")
        self.s_p2 = tk.StringVar(value="no")
        ttk.Entry(form, textvariable=self.s_p2, width=24).grid(row=1, column=3, padx=4)
        ttk.Button(form, text="Crear servicio", command=self._crear_servicio).grid(row=3, column=1, pady=6)
        ttk.Button(form, text="Alternar disponibilidad", command=self._alternar_disp).grid(row=3, column=3, pady=6)
        self.t_servicios = self._tabla(marco, ("ID", "Descripción", "Disponible"))
        self.t_servicios.column("Descripción", width=520)

    def _cambiar_tipo(self, _evento=None):
        """Ajusta las etiquetas de parámetros según el tipo elegido."""
        etiquetas = {"sala": ("Capacidad", "Proyector (si/no)"),
                     "equipo": ("Tipo de equipo", "Cantidad"),
                     "asesoria": ("Especialidad", "Nivel (1-3)")}[self.s_tipo.get()]
        self.s_p1_lbl.config(text=etiquetas[0])
        self.s_p2_lbl.config(text=etiquetas[1])
        self.s_p1.set("")
        self.s_p2.set("")

    def _crear_servicio(self):
        tipo = self.s_tipo.get()
        p1, p2 = self.s_p1.get(), self.s_p2.get()
        base = {"nombre": self.s_nombre.get(), "tarifa_hora": _numero(self.s_tarifa.get())}
        if tipo == "sala":
            base.update(capacidad=_numero(p1), proyector=p2.strip().lower() in ("si", "sí", "s", "1"))
        elif tipo == "equipo":
            base.update(tipo_equipo=p1, cantidad=_numero(p2) if p2.strip() else 1)
        else:
            base.update(especialidad=p1, nivel=_numero(p2) if p2.strip() else 1)
        self._ejecutar(lambda: self.gestor.crear_servicio(tipo, **base), "Servicio creado")

    def _alternar_disp(self):
        """Cambia la disponibilidad del servicio seleccionado."""
        seleccion = self.t_servicios.selection()
        if not seleccion:
            messagebox.showinfo("Aviso", "Seleccione un servicio")
            return
        idx = self.t_servicios.index(seleccion[0])
        servicio = self.gestor.servicios[idx]
        servicio.disponible = not servicio.disponible
        log.info("Disponibilidad de %s -> %s", servicio.id, servicio.disponible)
        self._refrescar()

    # ---------- Pestaña Reservas ----------
    def _construir_reservas(self, pestanas):
        marco = ttk.Frame(pestanas)
        pestanas.add(marco, text="Reservas")
        form = ttk.Frame(marco)
        form.pack(anchor="w", padx=6, pady=6)
        ttk.Label(form, text="Cliente").grid(row=0, column=0, sticky="e")
        self.r_cliente = ttk.Combobox(form, width=14)
        self.r_cliente.grid(row=0, column=1, padx=4)
        ttk.Label(form, text="Servicio").grid(row=0, column=2, sticky="e")
        self.r_servicio = ttk.Combobox(form, width=14)
        self.r_servicio.grid(row=0, column=3, padx=4)
        self.r_horas = self._campo(form, "Horas", 1)
        self.r_imp = self._campo(form, "Impuesto %", 1, 2)
        self.r_dto = self._campo(form, "Descuento %", 2, 2)
        botones = ttk.Frame(marco)
        botones.pack(anchor="w", padx=6)
        for texto, cmd in (("Crear", self._crear_reserva), ("Confirmar", self._confirmar),
                           ("Procesar", self._procesar), ("Cancelar", self._cancelar)):
            ttk.Button(botones, text=texto, command=cmd).pack(side="left", padx=3)
        self.t_reservas = self._tabla(marco, ("ID", "Detalle"))
        self.t_reservas.column("Detalle", width=640)

    def _crear_reserva(self):
        self._ejecutar(lambda: self.gestor.crear_reserva(
            self.r_cliente.get(), self.r_servicio.get(), _numero(self.r_horas.get())), "Reserva creada")

    def _reserva_seleccionada(self):
        """Obtiene la reserva elegida en la tabla (o lanza error de dominio)."""
        from excepciones import ReservaInvalidaError
        seleccion = self.t_reservas.selection()
        if not seleccion:
            raise ReservaInvalidaError("Seleccione una reserva de la tabla")
        return self.gestor.obtener_reserva(self.t_reservas.item(seleccion[0])["values"][0])

    def _confirmar(self):
        self._ejecutar(lambda: self._reserva_seleccionada().confirmar(), "Reserva confirmada")

    def _cancelar(self):
        self._ejecutar(lambda: self._reserva_seleccionada().cancelar(), "Reserva cancelada")

    def _porcentaje(self, texto):
        """Convierte '19' en 0.19; vacío -> None."""
        if not texto.strip():
            return None
        valor = _numero(texto)
        return valor / 100 if isinstance(valor, (int, float)) else valor  # str provoca error controlado

    def _procesar(self):
        def accion():
            reserva = self._reserva_seleccionada()
            return reserva.procesar(self._porcentaje(self.r_imp.get()), self._porcentaje(self.r_dto.get()))
        total = self._ejecutar(accion)
        if total is not None:
            messagebox.showinfo("Reserva procesada", f"Total: ${total:,.2f}")

    # ---------- Pestaña Log y simulación ----------
    def _construir_log(self, pestanas):
        marco = ttk.Frame(pestanas)
        pestanas.add(marco, text="Log y simulación")
        botones = ttk.Frame(marco)
        botones.pack(anchor="w", padx=6, pady=6)
        ttk.Button(botones, text="Ejecutar simulación (16 operaciones)", command=self._simular).pack(side="left", padx=3)
        ttk.Button(botones, text="Refrescar log", command=self._refrescar_log).pack(side="left", padx=3)
        self.txt = tk.Text(marco, height=20, state="disabled")
        self.txt.pack(fill="both", expand=True, padx=6, pady=6)

    def _escribir(self, texto):
        """Agrega una línea al cuadro de texto."""
        self.txt.config(state="normal")
        self.txt.insert("end", texto + "\n")
        self.txt.see("end")
        self.txt.config(state="disabled")

    def _simular(self):
        self.txt.config(state="normal")
        self.txt.delete("1.0", "end")
        self.txt.config(state="disabled")
        ejecutar_simulacion(self.gestor, salida=self._escribir)
        self._refrescar()

    def _refrescar_log(self):
        self.txt.config(state="normal")
        self.txt.delete("1.0", "end")
        self.txt.insert("end", leer_log())
        self.txt.config(state="disabled")

    # ---------- Refresco general ----------
    def _refrescar(self):
        """Actualiza tablas y listas desplegables con los datos en memoria."""
        for tabla in (self.t_clientes, self.t_servicios, self.t_reservas):
            tabla.delete(*tabla.get_children())
        for c in self.gestor.clientes:
            self.t_clientes.insert("", "end", values=(c.id, c.nombre, c.documento, c.email))
        for s in self.gestor.servicios:
            self.t_servicios.insert("", "end", values=(s.id, s.describir(), "Sí" if s.disponible else "No"))
        for r in self.gestor.reservas:
            self.t_reservas.insert("", "end", values=(r.id, r.describir()))
        self.r_cliente["values"] = [c.id for c in self.gestor.clientes]
        self.r_servicio["values"] = [s.id for s in self.gestor.servicios]
