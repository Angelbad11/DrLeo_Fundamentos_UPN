import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk
from datetime import date, datetime
from collections import Counter

from PIL import Image, ImageTk

from services.clinica_service import ClinicaService
from services.algoritmos_fundamentos import ordenar_pares_burbuja


class AppVeterinaria:
    COLORES = {
        "azul_oscuro": "#112B46",
        "azul": "#176DAB",
        "celeste": "#05AEC6",
        "verde": "#008F84",
        "fondo": "#F3F7FC",
        "panel": "#FFFFFF",
        "borde": "#E0E9F4",
        "texto": "#132A48",
        "gris": "#68819B",
        "advertencia": "#DA9341",
        "verde_claro": "#DFF8EB",
        "azul_claro": "#E6F3FF",
        "sombra": "#EAF1F9",
    }

    def __init__(self):
        self.servicio = ClinicaService()
        self.paginas = {}
        self.botones_menu = {}
        self.seccion_actual = None
        self.indice_propietario_editando = None
        self.indices_propietarios = []
        self.indices_mascotas = []
        # Ordenar solo la vista: no cambiar los registros ni sus relaciones.
        self.filtro_mascotas = ""
        self.indices_citas = []
        self.indices_pagos = []
        self.indices_atenciones = []
        # Las ediciones usan los formularios originales, no ventanas aparte.
        self.indice_mascota_editando = None
        self.indice_cita_editando = None
        self.indice_pago_editando = None
        self.indice_atencion_editando = None

        self.ventana = tk.Tk()
        self.criterio_orden_mascotas = tk.StringVar(master=self.ventana, value="Registro original")
        self.ventana.title("Dr. Leo | Sistema de Gestión Veterinaria | UPN")
        self.ventana.geometry("1440x870")
        self.ventana.minsize(1200, 760)
        self.ventana.configure(bg=self.COLORES["fondo"])

        self.configurar_estilos()
        # Conservamos assets/fondo.png; el nuevo panel usa fondo claro.
        self.crear_interfaz()

    def configurar_estilos(self):
        estilo = ttk.Style()
        estilo.theme_use("clam")
        estilo.configure(
            "Vertical.TScrollbar",
            background=self.COLORES["sombra"],
            troughcolor=self.COLORES["fondo"],
            bordercolor=self.COLORES["fondo"],
            arrowcolor=self.COLORES["gris"],
        )
        estilo.configure(
            "TCombobox",
            fieldbackground="#ffffff",
            background="#ffffff",
            foreground=self.COLORES["texto"],
            bordercolor=self.COLORES["borde"],
            lightcolor=self.COLORES["borde"],
            darkcolor=self.COLORES["borde"],
            arrowsize=13,
            padding=6,
            font=("Segoe UI", 10),
        )
        estilo.map(
            "TCombobox",
            fieldbackground=[("readonly", "#ffffff")],
            selectbackground=[("readonly", "#ffffff")],
            selectforeground=[("readonly", self.COLORES["texto"])],
        )

    def cargar_fondo(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        ruta_fondo = os.path.join(base_dir, "assets", "fondo.png")

        if os.path.exists(ruta_fondo):
            imagen = Image.open(ruta_fondo)
            imagen = imagen.resize((1100, 730))
            self.imagen_fondo = ImageTk.PhotoImage(imagen)

            self.etiqueta_fondo = tk.Label(self.ventana, image=self.imagen_fondo)
            self.etiqueta_fondo.place(x=0, y=0, relwidth=1, relheight=1)
        else:
            self.ventana.configure(bg=self.COLORES["fondo"])

    def crear_interfaz(self):
        self.contenedor = tk.Frame(
            self.ventana,
            bg=self.COLORES["panel"],
            highlightbackground=self.COLORES["borde"],
            highlightthickness=1,
        )
        self.contenedor.place(x=0, y=0, relwidth=1, relheight=1)

        self.crear_menu_lateral()
        self.crear_area_principal()

        self.tab_inicio = self.crear_pagina("Inicio")
        self.tab_propietarios = self.crear_pagina("Propietarios")
        self.tab_mascotas = self.crear_pagina("Mascotas")
        self.tab_citas = self.crear_pagina("Citas")
        self.tab_atenciones = self.crear_pagina("Consultas")
        self.tab_pagos = self.crear_pagina("Pagos")
        self.tab_historial = self.crear_pagina("Historial")
        self.tab_recordatorios = self.crear_pagina("Recordatorios")
        self.tab_reportes = self.crear_pagina("Reportes")

        self.crear_tab_inicio()
        self.crear_tab_propietarios()
        self.crear_tab_mascotas()
        self.crear_tab_citas()
        self.crear_tab_atenciones()
        self.crear_tab_pagos()
        self.crear_tab_historial()
        self.crear_tab_recordatorios()
        self.crear_tab_reportes()

        self.actualizar_todo()
        self.mostrar_seccion("Inicio")

    def crear_menu_lateral(self):
        self.menu_lateral = tk.Frame(self.contenedor, bg=self.COLORES["azul_oscuro"])
        self.menu_lateral.place(x=0, y=0, width=252, relheight=1)

        tk.Label(
            self.menu_lateral,
            text="Dr. Leo",
            bg=self.COLORES["azul_oscuro"],
            fg="#ffffff",
            font=("Segoe UI", 24, "bold"),
        ).pack(anchor="w", padx=22, pady=(24, 0))

        tk.Label(
            self.menu_lateral,
            text="Sistema de Gestión Veterinaria",
            bg=self.COLORES["azul_oscuro"],
            fg="#b9d7e6",
            font=("Segoe UI", 10),
        ).pack(anchor="w", padx=24, pady=(2, 17))

        tk.Frame(
            self.menu_lateral,
            bg="#355769",
            height=1,
        ).pack(fill="x", padx=18, pady=(0, 14))

        tk.Label(
            self.menu_lateral,
            text="MENÚ PRINCIPAL",
            bg=self.COLORES["azul_oscuro"],
            fg="#91B1BD",
            font=("Segoe UI", 8, "bold"),
        ).pack(anchor="w", padx=23, pady=(0, 6))

        opciones = [
            ("⌂  Inicio / Dashboard", "Inicio"),
            ("♧  Gestión de mascotas", "Mascotas"),
            ("☷  Gestión de propietarios", "Propietarios"),
            ("▤  Historial médico", "Historial"),
            ("▦  Citas veterinarias", "Citas"),
            ("✚  Consultas y vacunas", "Consultas"),
            ("▣  Pagos", "Pagos"),
            ("◷  Recordatorios", "Recordatorios"),
            ("▥  Reportes", "Reportes"),
        ]

        for texto, pagina in opciones:
            boton = tk.Button(
                self.menu_lateral,
                text=texto,
                command=lambda nombre=pagina: self.mostrar_seccion(nombre),
                font=("Segoe UI", 10, "bold"),
                bg=self.COLORES["azul_oscuro"],
                fg="#dff3f8",
                activebackground=self.COLORES["azul"],
                activeforeground="#ffffff",
                bd=0,
                relief="flat",
                anchor="w",
                padx=18,
                pady=8,
                cursor="hand2",
            )
            boton.pack(fill="x", padx=10, pady=2)
            boton.bind(
                "<Enter>",
                lambda evento, nombre=pagina: self._hover_menu(nombre, True),
            )
            boton.bind(
                "<Leave>",
                lambda evento, nombre=pagina: self._hover_menu(nombre, False),
            )
            self.botones_menu[pagina] = boton

        tk.Label(
            self.menu_lateral,
            text="Fundamentos de Programación | UPN",
            bg=self.COLORES["azul_oscuro"],
            fg="#9dc3d4",
            font=("Segoe UI", 9),
        ).pack(side="bottom", anchor="w", padx=22, pady=16)

    def crear_area_principal(self):
        self.area_principal = tk.Frame(self.contenedor, bg=self.COLORES["fondo"])
        self.area_principal.place(x=252, y=0, relwidth=1, width=-252, relheight=1)

        encabezado = tk.Frame(self.area_principal, bg=self.COLORES["fondo"])
        encabezado.pack(fill="x", padx=24, pady=(18, 11))

        fila_encabezado = tk.Frame(encabezado, bg=self.COLORES["fondo"])
        fila_encabezado.pack(fill="x")

        bloque_titulo = tk.Frame(fila_encabezado, bg=self.COLORES["fondo"])
        bloque_titulo.pack(side="left", fill="x", expand=True)

        tk.Label(
            bloque_titulo,
            text="CLÍNICA VETERINARIA",
            bg=self.COLORES["fondo"],
            fg=self.COLORES["verde"],
            font=("Segoe UI", 8, "bold"),
        ).pack(anchor="w", pady=(0, 1))

        self.titulo_seccion = tk.Label(
            bloque_titulo,
            text="Inicio",
            bg=self.COLORES["fondo"],
            fg=self.COLORES["azul_oscuro"],
            font=("Segoe UI", 19, "bold"),
        )
        self.titulo_seccion.pack(anchor="w")

        caja_derecha = tk.Frame(fila_encabezado, bg=self.COLORES["fondo"])
        caja_derecha.pack(side="right", anchor="n", padx=(8, 0))
        tk.Label(
            caja_derecha, text=date.today().strftime("%d/%m/%Y"),
            bg=self.COLORES["fondo"], fg=self.COLORES["azul"],
            font=("Segoe UI", 9, "bold")
        ).pack(anchor="e", pady=(0, 6))
        self.busqueda_general = tk.StringVar()
        entrada_busqueda = tk.Entry(
            caja_derecha, textvariable=self.busqueda_general,
            font=("Segoe UI", 10), width=29,
            bg="#FFFFFF", fg=self.COLORES["texto"], bd=0,
            highlightthickness=1, highlightbackground=self.COLORES["borde"]
        )
        entrada_busqueda.pack(ipady=7)
        entrada_busqueda.insert(0, "")
        entrada_busqueda.bind("<Return>", self.buscar_general)

        tk.Label(
            fila_encabezado,
            text="FUNDAMENTOS UPN",
            bg=self.COLORES["verde_claro"],
            fg=self.COLORES["verde"],
            font=("Segoe UI", 8, "bold"),
            padx=11,
            pady=6,
        ).pack(side="right", anchor="n", pady=(5, 0))

        self.descripcion_seccion = tk.Label(
            encabezado,
            text="Resumen de la actividad de la clínica",
            bg=self.COLORES["fondo"],
            fg=self.COLORES["gris"],
            font=("Segoe UI", 9),
        )
        self.descripcion_seccion.pack(anchor="w", pady=(3, 0))

        tk.Frame(encabezado, bg=self.COLORES["borde"], height=1).pack(
            fill="x", pady=(12, 0)
        )

        self.contenido = tk.Frame(self.area_principal, bg=self.COLORES["fondo"])
        self.contenido.pack(fill="both", expand=True, padx=24, pady=(0, 18))
        self.contenido.grid_rowconfigure(0, weight=1)
        self.contenido.grid_columnconfigure(0, weight=1)

    def crear_pagina(self, nombre):
        pagina = tk.Frame(self.contenido, bg=self.COLORES["fondo"])
        pagina.grid(row=0, column=0, sticky="nsew")
        pagina.grid_rowconfigure(0, weight=1)
        pagina.grid_columnconfigure(1, weight=1)
        self.paginas[nombre] = pagina
        return pagina

    def mostrar_seccion(self, nombre):
        for pagina in self.paginas.values():
            pagina.grid_remove()

        self.paginas[nombre].grid()
        self.seccion_actual = nombre
        self.titulo_seccion.config(text=nombre)
        descripciones = {
            "Inicio": "Resumen de la actividad de la clínica",
            "Propietarios": "Administra los datos de contacto de los propietarios",
            "Mascotas": "Registra y organiza las mascotas atendidas",
            "Citas": "Agenda, actualiza y consulta las citas",
            "Consultas": "Registra diagnósticos, tratamientos y vacunas",
            "Pagos": "Controla los cobros y los ingresos confirmados",
            "Historial": "Revisa las consultas y vacunas de cada mascota",
            "Recordatorios": "Prepara mensajes para recordar las citas",
            "Reportes": "Consulta y exporta la información de gestión",
        }
        self.descripcion_seccion.config(text=descripciones.get(nombre, ""))

        for pagina, boton in self.botones_menu.items():
            if pagina == nombre:
                boton.config(bg="#058EC2", fg="#ffffff")
            else:
                boton.config(bg=self.COLORES["azul_oscuro"], fg="#dff3f8")

        if nombre == "Inicio":
            self.actualizar_dashboard()
        elif nombre == "Historial":
            self.actualizar_lista_mascotas()

    def _hover_menu(self, nombre, entrando):
        boton = self.botones_menu.get(nombre)
        if boton is None or nombre == self.seccion_actual:
            return
        boton.config(
            bg=self.COLORES["azul"] if entrando else self.COLORES["azul_oscuro"]
        )

    def crear_panel(self, padre, titulo, columna, ancho=260):
        panel = tk.Frame(
            padre,
            bg=self.COLORES["panel"],
            highlightbackground=self.COLORES["borde"],
            highlightthickness=1,
        )
        panel.grid(
            row=0,
            column=columna,
            sticky="nsew",
            padx=(0, 14) if columna == 0 else 0,
        )
        panel.grid_propagate(False)
        panel.config(width=ancho)

        tk.Label(
            panel,
            text=titulo,
            bg=self.COLORES["panel"],
            fg=self.COLORES["azul_oscuro"],
            font=("Segoe UI", 12, "bold"),
        ).pack(anchor="w", padx=16, pady=(14, 8))
        tk.Frame(panel, bg=self.COLORES["borde"], height=1).pack(
            fill="x", padx=16, pady=(0, 8)
        )

        return panel

    def crear_campo(self, padre, texto, ancho=28):
        tk.Label(
            padre,
            text=texto,
            bg=self.COLORES["panel"],
            fg=self.COLORES["gris"],
            font=("Segoe UI", 9, "bold"),
        ).pack(anchor="w", padx=16, pady=(8, 2))

        entrada = tk.Entry(
            padre,
            width=ancho,
            font=("Segoe UI", 10),
            bg="#ffffff",
            fg=self.COLORES["texto"],
            relief="flat",
            highlightbackground=self.COLORES["borde"],
            highlightcolor=self.COLORES["celeste"],
            highlightthickness=1,
            insertbackground=self.COLORES["azul_oscuro"],
        )
        entrada.pack(anchor="w", padx=16, ipady=6)
        return entrada

    def crear_combo(self, padre, texto, ancho=25, valores=None):
        tk.Label(
            padre,
            text=texto,
            bg=self.COLORES["panel"],
            fg=self.COLORES["gris"],
            font=("Segoe UI", 9, "bold"),
        ).pack(anchor="w", padx=16, pady=(8, 2))

        combo = ttk.Combobox(
            padre,
            width=ancho,
            state="readonly",
            values=valores if valores else [],
        )
        combo.pack(anchor="w", padx=16, ipady=3)
        return combo

    def crear_boton_accion(self, padre, texto, comando, color=None):
        boton = tk.Button(
            padre,
            text=texto,
            command=comando,
            bg=color if color else self.COLORES["verde"],
            fg="#ffffff",
            activebackground=self.COLORES["azul"],
            activeforeground="#ffffff",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            bd=0,
            padx=12,
            pady=8,
            cursor="hand2",
        )
        boton.pack(anchor="w", padx=16, pady=6)
        self._agregar_hover_boton(boton, boton.cget("bg"))
        return boton

    def _agregar_hover_boton(self, boton, color_base):
        boton.bind(
            "<Enter>",
            lambda evento: boton.config(bg=self.COLORES["azul"]),
        )
        boton.bind(
            "<Leave>",
            lambda evento: boton.config(bg=color_base),
        )

    def crear_listbox(self, padre, ancho=54, alto=20):
        contenedor = tk.Frame(padre, bg=self.COLORES["panel"])
        contenedor.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        barra = ttk.Scrollbar(contenedor)
        barra.pack(side="right", fill="y")

        lista = tk.Listbox(
            contenedor,
            width=ancho,
            height=alto,
            bg="#FCFEFE",
            fg=self.COLORES["texto"],
            selectbackground=self.COLORES["verde"],
            selectforeground="#ffffff",
            font=("Segoe UI", 9),
            activestyle="none",
            relief="flat",
            highlightbackground=self.COLORES["borde"],
            highlightthickness=1,
            yscrollcommand=barra.set,
        )
        lista.pack(side="left", fill="both", expand=True)
        barra.config(command=lista.yview)
        return lista

    def crear_barra_lista(self, padre, acciones):
        barra = tk.Frame(padre, bg=self.COLORES["panel"])
        barra.pack(fill="x", padx=16, pady=(0, 8))

        for texto, comando, color in acciones:
            boton = tk.Button(
                barra,
                text=texto,
                command=comando,
                bg=color,
                fg="#ffffff",
                activebackground=self.COLORES["azul"],
                activeforeground="#ffffff",
                font=("Segoe UI", 8, "bold"),
                relief="flat",
                bd=0,
                padx=7,
                pady=5,
                cursor="hand2",
            )
            boton.pack(side="left", padx=(0, 5))
            self._agregar_hover_boton(boton, color)

        return barra

    def crear_texto(self, padre, ancho=62, alto=22):
        contenedor = tk.Frame(padre, bg=self.COLORES["panel"])
        contenedor.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        barra = ttk.Scrollbar(contenedor)
        barra.pack(side="right", fill="y")

        texto = tk.Text(
            contenedor,
            width=ancho,
            height=alto,
            bg="#FCFEFE",
            fg=self.COLORES["texto"],
            font=("Segoe UI", 10),
            relief="flat",
            highlightbackground=self.COLORES["borde"],
            highlightthickness=1,
            wrap="word",
            yscrollcommand=barra.set,
        )
        texto.pack(side="left", fill="both", expand=True)
        barra.config(command=texto.yview)
        return texto

    def crear_tab_inicio(self):
        """Página Inicio usando las colecciones REALES del servicio original."""
        marco = self.tab_inicio
        for columna in range(5):
            marco.grid_columnconfigure(columna, weight=1, uniform="tarjeta")
        marco.grid_rowconfigure(2, weight=3)
        marco.grid_rowconfigure(3, weight=2)

        tk.Label(
            marco, text="Vista general de la clínica",
            fg=self.COLORES["texto"], bg=self.COLORES["fondo"],
            font=("Segoe UI", 13, "bold")
        ).grid(row=0, column=0, columnspan=5, sticky="w", pady=(0, 13))

        metricas = [
            ("Pacientes registrados", "#E2F1FF", "#1264C0", "valor_mascotas"),
            ("Citas del día", "#DFF8ED", "#008766", "valor_citas"),
            ("Propietarios", "#EEEAFE", "#5942BC", "valor_propietarios"),
            ("Ingresos confirmados", "#FFF2DE", "#BA7609", "valor_pagos_inicio"),
            ("Citas pendientes", "#FFE8F0", "#BE4C70", "valor_pendientes_inicio"),
        ]
        for columna, (titulo, fondo, acento, atributo) in enumerate(metricas):
            tarjeta = tk.Frame(marco, bg=fondo, height=113)
            tarjeta.grid(row=1, column=columna, sticky="nsew", padx=(0, 9) if columna < 4 else 0)
            tarjeta.grid_propagate(False)
            tk.Label(tarjeta, text=titulo, bg=fondo, fg=self.COLORES["texto"],
                    font=("Segoe UI", 9, "bold"), wraplength=155, justify="left").pack(
                anchor="w", padx=13, pady=(19, 4))
            valor = tk.Label(tarjeta, text="0", bg=fondo, fg=acento,
                            font=("Segoe UI", 23, "bold"))
            valor.pack(anchor="w", padx=13)
            setattr(self, atributo, valor)

        # Panel de citas del día, sin números ficticios.
        panel_citas = self._panel_inicio(marco, "Citas de hoy", row=2, column=0, span=3)
        encabezados = ("Hora", "Mascota", "Propietario", "Motivo", "Estado")
        self.tabla_citas_inicio = ttk.Treeview(
            panel_citas, columns=encabezados, show="headings", height=8)
        for nombre, ancho in zip(encabezados, (65, 115, 130, 170, 100)):
            self.tabla_citas_inicio.heading(nombre, text=nombre)
            self.tabla_citas_inicio.column(nombre, width=ancho, anchor="w", stretch=True)
        self.tabla_citas_inicio.pack(fill="both", expand=True, padx=12, pady=(4, 12))
        self.tabla_citas_inicio.bind("<Double-1>", lambda _: self.mostrar_seccion("Citas"))

        # Gráfico de barras con las atenciones y citas mensuales registradas.
        panel_grafico = self._panel_inicio(marco, "Actividad últimos 6 meses", row=2, column=3, span=2)
        self.canvas_dashboard = tk.Canvas(panel_grafico, bg="#FFFFFF", highlightthickness=0)
        self.canvas_dashboard.pack(fill="both", expand=True, padx=13, pady=(5, 15))
        self.canvas_dashboard.bind("<Configure>", lambda _: self.dibujar_grafico_dashboard())

        panel_pacientes = self._panel_inicio(marco, "Pacientes recientes", row=3, column=0, span=3)
        encabezados_p = ("Mascota", "Especie", "Edad", "Propietario")
        self.tabla_pacientes_inicio = ttk.Treeview(
            panel_pacientes, columns=encabezados_p, show="headings", height=6)
        for nombre, ancho in zip(encabezados_p, (130, 115, 75, 175)):
            self.tabla_pacientes_inicio.heading(nombre, text=nombre)
            self.tabla_pacientes_inicio.column(nombre, width=ancho, stretch=True)
        self.tabla_pacientes_inicio.pack(fill="both", expand=True, padx=12, pady=(4, 12))
        self.tabla_pacientes_inicio.bind("<Double-1>", lambda _: self.mostrar_seccion("Mascotas"))

        panel_estados = self._panel_inicio(marco, "Atenciones y estado de citas", row=3, column=3, span=2)
        self.valor_atenciones_inicio = self._etiqueta_resumen(panel_estados, "Consultas registradas", "#096BBD")
        self.valor_estado_atendidas = self._etiqueta_resumen(panel_estados, "Citas atendidas", "#008F84")
        self.valor_estado_canceladas = self._etiqueta_resumen(panel_estados, "Citas canceladas", "#C05D66")

    def _panel_inicio(self, padre, titulo, row, column, span):
        panel = tk.Frame(padre, bg="#FFFFFF", highlightbackground=self.COLORES["borde"], highlightthickness=1)
        panel.grid(row=row, column=column, columnspan=span, sticky="nsew",
                padx=(0, 10) if column == 0 else 0, pady=(15, 0))
        tk.Label(panel, text=titulo, bg="#FFFFFF", fg=self.COLORES["texto"],
                font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=14, pady=(12, 6))
        return panel

    def _etiqueta_resumen(self, padre, etiqueta, color):
        fila = tk.Frame(padre, bg="#FFFFFF")
        fila.pack(fill="x", padx=16, pady=10)
        tk.Label(fila, text=etiqueta, bg="#FFFFFF", fg=self.COLORES["texto"],
                font=("Segoe UI", 10)).pack(side="left")
        valor = tk.Label(fila, text="0", bg="#FFFFFF", fg=color,
                        font=("Segoe UI", 15, "bold"))
        valor.pack(side="right")
        return valor

    def dibujar_grafico_dashboard(self):
        if not hasattr(self, "canvas_dashboard"):
            return
        canvas = self.canvas_dashboard
        canvas.delete("all")
        ancho = max(canvas.winfo_width(), 240)
        alto = max(canvas.winfo_height(), 170)
        hoy = date.today()
        indice_actual = hoy.year * 12 + hoy.month - 1
        nombres = ("Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic")
        series = []
        for desplazamiento in range(5, -1, -1):
            anio, mes0 = divmod(indice_actual - desplazamiento, 12)
            mes = mes0 + 1
            citas = sum(1 for c in self.servicio.listar_citas()
                        if (self.servicio._normalizar_fecha(c.fecha) or datetime.min).date().year == anio
                        and (self.servicio._normalizar_fecha(c.fecha) or datetime.min).date().month == mes)
            atenciones = sum(1 for a in self.servicio.listar_atenciones()
                            if (self.servicio._normalizar_fecha(a.fecha) or datetime.min).date().year == anio
                            and (self.servicio._normalizar_fecha(a.fecha) or datetime.min).date().month == mes)
            series.append((nombres[mes0], citas, atenciones))
        maximo = max(1, *(max(c, a) for _, c, a in series))
        margen_izq, margen_der = 35, 14
        superior, inferior = 23, alto - 40
        base = max(inferior - superior, 35)
        for n in range(4):
            y = superior + n * base / 3
            canvas.create_line(margen_izq, y, ancho - margen_der, y, fill="#EDF1F7")
            canvas.create_text(margen_izq - 6, y, text=str(round(maximo * (3-n)/3)),
                               anchor="e", fill="#72859A", font=("Segoe UI", 8))
        espacio = (ancho - margen_izq - margen_der) / 6
        for i, (mes, citas, atenciones) in enumerate(series):
            x = margen_izq + espacio * (i + 0.5)
            for n, valor, color in ((0, citas, "#1B84D2"), (1, atenciones, "#00A98E")):
                altura = (valor/maximo) * base
                cx = x - 13 if n == 0 else x + 2
                canvas.create_rectangle(cx, inferior-altura, cx+11, inferior,
                                        fill=color, outline="")
            canvas.create_text(x, inferior+13, text=mes, font=("Segoe UI", 8), fill="#69809C")
        canvas.create_text(ancho-8, alto-10, text="Azul: citas  ·  Verde: consultas",
                           anchor="e", font=("Segoe UI", 8), fill="#5A708D")

    def buscar_general(self, evento=None):
        termino = self.busqueda_general.get().strip()
        if not termino:
            return
        pagina = self.seccion_actual
        if pagina == "Citas":
            self.filtrar_citas_dialogo()
        elif pagina == "Pagos":
            self.filtrar_pagos_dialogo()
        elif pagina == "Consultas":
            self.filtrar_atenciones_dialogo()
        elif pagina == "Propietarios":
            self.filtrar_propietarios_dialogo()
        elif pagina == "Mascotas":
            self.filtrar_mascotas_dialogo()
        else:
            mascotas = self.servicio.buscar_mascotas(termino)
            if mascotas:
                self.actualizar_lista_mascotas(mascotas)
                self.mostrar_seccion("Mascotas")
                return
            propietarios = self.servicio.buscar_propietarios(termino)
            if propietarios:
                self.actualizar_lista_propietarios(propietarios)
                self.mostrar_seccion("Propietarios")
                return
            self.actualizar_lista_mascotas([])
            self.mostrar_seccion("Mascotas")

    def crear_tarjeta(self, padre, titulo, columna, fila, color):
        tarjeta = tk.Frame(
            padre,
            bg=self.COLORES["panel"],
            highlightbackground=self.COLORES["borde"],
            highlightthickness=1,
        )
        tarjeta.grid(row=fila, column=columna, sticky="ew", padx=(0, 12), ipady=10)

        tk.Frame(tarjeta, bg=color, height=3).pack(fill="x")

        tk.Label(
            tarjeta,
            text=titulo,
            bg=self.COLORES["panel"],
            fg=self.COLORES["gris"],
            font=("Segoe UI", 9, "bold"),
        ).pack(anchor="w", padx=14, pady=(12, 2))

        valor = tk.Label(
            tarjeta,
            text="0",
            bg=self.COLORES["panel"],
            fg=color,
            font=("Segoe UI", 21, "bold"),
        )
        valor.pack(anchor="w", padx=14, pady=(0, 8))
        return valor

    def crear_tab_propietarios(self):
        formulario = self.crear_panel(self.tab_propietarios, "Nuevo propietario", 0, ancho=270)
        listado = self.crear_panel(self.tab_propietarios, "Propietarios registrados", 1, ancho=470)

        self.entrada_nombre_propietario = self.crear_campo(formulario, "Nombre del propietario")
        self.entrada_dni_propietario = self.crear_campo(formulario, "DNI")
        self.entrada_telefono_propietario = self.crear_campo(formulario, "Teléfono")
        self.crear_boton_accion(formulario, "Registrar propietario", self.registrar_propietario)
        self.crear_boton_accion(
            formulario,
            "Cargar seleccionado",
            self.cargar_propietario_para_editar,
            color=self.COLORES["azul"],
        )
        self.crear_boton_accion(
            formulario,
            "Guardar cambios",
            self.guardar_cambios_propietario,
            color=self.COLORES["advertencia"],
        )
        self.crear_boton_accion(
            formulario,
            "Cancelar edición",
            self.limpiar_formulario_propietario,
            color=self.COLORES["gris"],
        )

        self.etiqueta_modo_propietario = tk.Label(
            formulario,
            text="Modo: nuevo propietario",
            bg=self.COLORES["panel"],
            fg=self.COLORES["gris"],
            font=("Segoe UI", 9, "italic"),
        )
        self.etiqueta_modo_propietario.pack(anchor="w", padx=16, pady=(0, 10))

        self.crear_barra_lista(
            listado,
            [
                ("Buscar", self.filtrar_propietarios_dialogo, self.COLORES["azul"]),
                ("Todos", self.mostrar_todos_propietarios, self.COLORES["gris"]),
                ("Eliminar", self.eliminar_propietario, self.COLORES["advertencia"]),
            ],
        )
        self.lista_propietarios = self.crear_listbox(listado, ancho=58, alto=24)
        self.lista_propietarios.bind(
            "<Double-Button-1>",
            lambda evento: self.cargar_propietario_para_editar(),
        )

    def crear_tab_mascotas(self):
        formulario = self.crear_panel(self.tab_mascotas, "Nueva mascota", 0, ancho=270)
        listado = self.crear_panel(self.tab_mascotas, "Mascotas registradas", 1, ancho=470)

        self.entrada_nombre_mascota = self.crear_campo(formulario, "Nombre de la mascota")
        self.entrada_especie_mascota = self.crear_campo(formulario, "Especie")
        self.entrada_edad_mascota = self.crear_campo(formulario, "Edad")
        self.combo_sexo_mascota = self.crear_combo(
            formulario,
            "Sexo",
            valores=["No especificado", "Macho", "Hembra"],
        )
        self.combo_sexo_mascota.current(0)
        self.combo_esterilizado_mascota = self.crear_combo(
            formulario,
            "Esterilizado",
            valores=["No especificado", "Sí", "No"],
        )
        self.combo_esterilizado_mascota.current(0)
        self.combo_propietarios = self.crear_combo(formulario, "Propietario")
        self.crear_boton_accion(formulario, "Registrar mascota", self.registrar_mascota)
        self.crear_boton_accion(formulario, "Guardar edición", self.guardar_edicion_mascota,
                            color=self.COLORES["azul"])
        self.crear_boton_accion(formulario, "Cancelar edición", self.cancelar_edicion_mascota,
                            color=self.COLORES["gris"])

        self.crear_barra_lista(
            listado,
            [
                ("Editar", self.editar_mascota, self.COLORES["azul"]),
                ("Eliminar", self.eliminar_mascota, self.COLORES["advertencia"]),
                ("Buscar", self.filtrar_mascotas_dialogo, self.COLORES["verde"]),
                ("Todos", self.mostrar_todas_mascotas, self.COLORES["gris"]),
            ],
        )
        # Control de ordenamiento dentro de la MISMA pagina de mascotas.
        barra_orden = tk.Frame(listado, bg=self.COLORES["panel"])
        barra_orden.pack(fill="x", padx=16, pady=(0, 10))
        tk.Label(
            barra_orden,
            text="Ordenar por:",
            bg=self.COLORES["panel"],
            fg=self.COLORES["texto"],
            font=("Segoe UI", 9, "bold"),
        ).pack(side="left", padx=(0, 9))
        selector_orden = ttk.Combobox(
            barra_orden,
            textvariable=self.criterio_orden_mascotas,
            values=(
                "Registro original",
                "Nombre A-Z",
                "Nombre Z-A",
                "Edad: menor a mayor",
                "Edad: mayor a menor",
            ),
            state="readonly",
            width=23,
        )
        selector_orden.pack(side="left")
        selector_orden.bind(
            "<<ComboboxSelected>>", lambda evento: self.actualizar_lista_mascotas()
        )

        self.lista_mascotas = self.crear_listbox(listado, ancho=58, alto=24)

    def crear_tab_citas(self):
        formulario = self.crear_panel(self.tab_citas, "Nueva cita", 0, ancho=270)
        listado = self.crear_panel(self.tab_citas, "Citas programadas", 1, ancho=470)

        self.combo_mascotas = self.crear_combo(formulario, "Mascota", ancho=25)
        self.entrada_fecha_cita = self.crear_campo(formulario, "Fecha de la cita")
        self.entrada_fecha_cita.insert(0, "06/10/2026")
        self.entrada_hora_cita = self.crear_campo(formulario, "Hora")
        self.entrada_hora_cita.insert(0, "10:30")
        self.entrada_motivo_cita = self.crear_campo(formulario, "Motivo")
        self.combo_estado_cita = self.crear_combo(
            formulario,
            "Estado",
            valores=["Pendiente", "Atendida", "Cancelada"],
        )
        self.combo_estado_cita.current(0)
        self.crear_boton_accion(formulario, "Registrar cita", self.registrar_cita)
        self.crear_boton_accion(formulario, "Guardar edición", self.guardar_edicion_cita,
                               color=self.COLORES["azul"])
        self.crear_boton_accion(formulario, "Cancelar edición", self.cancelar_edicion_cita,
                               color=self.COLORES["gris"])

        self.crear_barra_lista(
            listado,
            [
                ("Editar/reprogramar", self.editar_cita, self.COLORES["azul"]),
                ("Eliminar", self.eliminar_cita, self.COLORES["advertencia"]),
                ("Filtrar", self.filtrar_citas_dialogo, self.COLORES["verde"]),
                ("Todas", self.mostrar_todas_citas, self.COLORES["gris"]),
            ],
        )
        self.lista_citas = self.crear_listbox(listado, ancho=58, alto=24)

    def crear_tab_pagos(self):
        formulario = self.crear_panel(self.tab_pagos, "Nuevo pago", 0, ancho=270)
        listado = self.crear_panel(self.tab_pagos, "Pagos registrados", 1, ancho=470)

        self.entrada_concepto_pago = self.crear_campo(formulario, "Concepto del pago")
        self.entrada_monto_pago = self.crear_campo(formulario, "Monto")
        self.combo_metodo_pago = self.crear_combo(
            formulario,
            "Método de pago",
            valores=["Efectivo", "Yape", "Plin", "POS", "Transferencia"],
        )
        self.combo_estado_pago = self.crear_combo(
            formulario,
            "Estado",
            valores=["Pendiente", "Confirmado", "Anulado"],
        )
        self.crear_boton_accion(formulario, "Registrar pago", self.registrar_pago)
        self.crear_boton_accion(formulario, "Guardar edición", self.guardar_edicion_pago,
                               color=self.COLORES["azul"])
        self.crear_boton_accion(formulario, "Cancelar edición", self.cancelar_edicion_pago,
                               color=self.COLORES["gris"])

        self.etiqueta_total_pagos = tk.Label(
            listado,
            text="Total confirmado: S/ 0.00",
            bg=self.COLORES["panel"],
            fg=self.COLORES["verde"],
            font=("Segoe UI", 12, "bold"),
        )
        self.etiqueta_total_pagos.pack(anchor="w", padx=16, pady=(0, 10))

        self.crear_barra_lista(
            listado,
            [
                ("Editar", self.editar_pago, self.COLORES["azul"]),
                ("Eliminar", self.eliminar_pago, self.COLORES["advertencia"]),
                ("Filtrar", self.filtrar_pagos_dialogo, self.COLORES["verde"]),
                ("Todos", self.mostrar_todos_pagos, self.COLORES["gris"]),
            ],
        )
        self.lista_pagos = self.crear_listbox(listado, ancho=58, alto=21)

    def crear_tab_atenciones(self):
        formulario = self.crear_panel(self.tab_atenciones, "Nueva consulta", 0, ancho=270)
        listado = self.crear_panel(self.tab_atenciones, "Consultas registradas", 1, ancho=470)

        self.combo_mascotas_atencion = self.crear_combo(formulario, "Mascota", ancho=25)
        self.entrada_fecha_atencion = self.crear_campo(formulario, "Fecha de consulta")
        self.entrada_fecha_atencion.insert(0, "06/10/2026")
        self.entrada_diagnostico = self.crear_campo(formulario, "Diagnóstico")
        self.entrada_tratamiento = self.crear_campo(formulario, "Tratamiento")
        self.entrada_vacuna = self.crear_campo(formulario, "Vacuna aplicada")
        self.crear_boton_accion(formulario, "Registrar consulta", self.registrar_atencion)
        self.crear_boton_accion(formulario, "Guardar edición", self.guardar_edicion_atencion,
                            color=self.COLORES["azul"])
        self.crear_boton_accion(formulario, "Cancelar edición", self.cancelar_edicion_atencion,
                            color=self.COLORES["gris"])

        self.crear_barra_lista(
            listado,
            [
                ("Editar", self.editar_atencion, self.COLORES["azul"]),
                ("Eliminar", self.eliminar_atencion, self.COLORES["advertencia"]),
                ("Filtrar", self.filtrar_atenciones_dialogo, self.COLORES["verde"]),
                ("Todas", self.mostrar_todas_atenciones, self.COLORES["gris"]),
            ],
        )
        self.lista_atenciones = self.crear_listbox(listado, ancho=58, alto=24)

    def crear_tab_reportes(self):
        self.tab_reportes.grid_columnconfigure(0, weight=1)
        panel = self.crear_panel(self.tab_reportes, "Reporte diario de consultas e ingresos", 0, ancho=740)

        botones = tk.Frame(panel, bg=self.COLORES["panel"])
        botones.pack(fill="x", padx=16, pady=(0, 12))

        tk.Button(
            botones,
            text="Generar reporte diario",
            command=self.generar_reporte_diario,
            bg=self.COLORES["verde"],
            fg="#ffffff",
            activebackground=self.COLORES["azul"],
            activeforeground="#ffffff",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            bd=0,
            padx=12,
            pady=8,
            cursor="hand2",
        ).pack(side="left", padx=(0, 8))

        tk.Button(
            botones,
            text="Exportar reporte a TXT",
            command=self.exportar_reporte_diario,
            bg=self.COLORES["azul"],
            fg="#ffffff",
            activebackground=self.COLORES["verde"],
            activeforeground="#ffffff",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            bd=0,
            padx=12,
            pady=8,
            cursor="hand2",
        ).pack(side="left")

        tk.Button(
            botones,
            text="Exportar datos CSV",
            command=self.exportar_datos_csv,
            bg=self.COLORES["advertencia"],
            fg="#ffffff",
            activebackground=self.COLORES["azul"],
            activeforeground="#ffffff",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            bd=0,
            padx=12,
            pady=8,
            cursor="hand2",
        ).pack(side="left", padx=(8, 0))

        tk.Button(
            botones,
            text="Importar propietarios CSV",
            command=self.importar_propietarios_csv,
            bg=self.COLORES["gris"],
            fg="#ffffff",
            activebackground=self.COLORES["azul"],
            activeforeground="#ffffff",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            bd=0,
            padx=12,
            pady=8,
            cursor="hand2",
        ).pack(side="left", padx=(8, 0))

        self.texto_reporte = self.crear_texto(panel, ancho=80, alto=24)

    def crear_tab_recordatorios(self):
        self.tab_recordatorios.grid_columnconfigure(0, weight=1)
        panel = self.crear_panel(self.tab_recordatorios, "Recordatorio para WhatsApp", 0, ancho=740)

        self.combo_citas_recordatorio = self.crear_combo(panel, "Selecciona una cita", ancho=70)
        self.crear_boton_accion(panel, "Generar mensaje", self.generar_recordatorio)
        self.texto_recordatorio = self.crear_texto(panel, ancho=80, alto=15)

        tk.Label(
            panel,
            text="El sistema solo prepara el mensaje. El envío se realiza manualmente.",
            bg=self.COLORES["panel"],
            fg=self.COLORES["gris"],
            font=("Segoe UI", 9, "italic"),
        ).pack(anchor="w", padx=16, pady=(0, 12))

    def crear_tab_historial(self):
        self.tab_historial.grid_columnconfigure(0, weight=1)
        panel = self.crear_panel(self.tab_historial, "Historial clínico ordenado por mascota", 0, ancho=740)

        self.combo_mascotas_historial = self.crear_combo(panel, "Selecciona una mascota", ancho=45)
        self.crear_boton_accion(panel, "Generar historial", self.generar_historial_mascota)
        self.texto_historial = self.crear_texto(panel, ancho=80, alto=20)

    def registrar_propietario(self):
        if self.indice_propietario_editando is not None:
            messagebox.showwarning(
                "Edición activa",
                "Guarda los cambios o cancela la edición antes de registrar otro propietario.",
            )
            return

        nombre = self.entrada_nombre_propietario.get().strip()
        dni = self.entrada_dni_propietario.get().strip()
        telefono = self.entrada_telefono_propietario.get().strip()

        if nombre == "" or dni == "" or telefono == "":
            messagebox.showwarning("Datos incompletos", "Completa nombre, DNI y teléfono.")
            return

        if not dni.isdigit() or len(dni) != 8:
            messagebox.showerror("DNI inválido", "El DNI debe tener 8 números.")
            return

        try:
            self.servicio.registrar_propietario(nombre, dni, telefono)
        except ValueError as error:
            messagebox.showerror("No se pudo registrar", str(error))
            return

        self.limpiar_formulario_propietario()

        self.actualizar_todo()
        messagebox.showinfo("Registro exitoso", "Propietario registrado correctamente.")

    def cargar_propietario_para_editar(self):
        seleccion = self.lista_propietarios.curselection()

        if len(seleccion) == 0:
            messagebox.showwarning(
                "Sin selección",
                "Selecciona un propietario de la lista para editar.",
            )
            return

        posicion = seleccion[0]
        if posicion >= len(self.indices_propietarios):
            messagebox.showwarning("Selección inválida", "Actualiza la lista e inténtalo nuevamente.")
            return
        indice = self.indices_propietarios[posicion]
        propietario = self.servicio.listar_propietarios()[indice]

        self.entrada_nombre_propietario.delete(0, tk.END)
        self.entrada_dni_propietario.delete(0, tk.END)
        self.entrada_telefono_propietario.delete(0, tk.END)

        self.entrada_nombre_propietario.insert(0, propietario.nombre)
        self.entrada_dni_propietario.insert(0, propietario.dni)
        self.entrada_telefono_propietario.insert(0, propietario.telefono)

        self.indice_propietario_editando = indice
        self.etiqueta_modo_propietario.config(
            text=f"Modo: editando a {propietario.nombre}",
            fg=self.COLORES["azul"],
        )

    def guardar_cambios_propietario(self):
        if self.indice_propietario_editando is None:
            messagebox.showwarning(
                "Sin edición",
                "Primero selecciona un propietario y pulsa Cargar seleccionado.",
            )
            return

        nombre = self.entrada_nombre_propietario.get().strip()
        dni = self.entrada_dni_propietario.get().strip()
        telefono = self.entrada_telefono_propietario.get().strip()

        try:
            self.servicio.actualizar_propietario(
                self.indice_propietario_editando,
                nombre,
                dni,
                telefono,
            )
        except ValueError as error:
            messagebox.showerror("No se pudo actualizar", str(error))
            return

        self.limpiar_formulario_propietario()
        self.actualizar_todo()
        messagebox.showinfo("Datos actualizados", "Propietario actualizado correctamente.")

    def limpiar_formulario_propietario(self):
        self.indice_propietario_editando = None
        self.entrada_nombre_propietario.delete(0, tk.END)
        self.entrada_dni_propietario.delete(0, tk.END)
        self.entrada_telefono_propietario.delete(0, tk.END)
        self.etiqueta_modo_propietario.config(
            text="Modo: nuevo propietario",
            fg=self.COLORES["gris"],
        )

    def registrar_mascota(self):
        if self.indice_mascota_editando is not None:
            messagebox.showwarning("Edición activa", "Guarda o cancela la edición primero.")
            return
        nombre = self.entrada_nombre_mascota.get().strip()
        especie = self.entrada_especie_mascota.get().strip()
        edad = self.entrada_edad_mascota.get().strip()
        sexo = self.combo_sexo_mascota.get()
        esterilizado = self.combo_esterilizado_mascota.get()
        indice_propietario = self.combo_propietarios.current()

        if nombre == "" or especie == "" or edad == "":
            messagebox.showwarning(
                "Datos incompletos",
                "Completa todos los datos de la mascota.",
            )
            return

        if indice_propietario == -1:
            messagebox.showwarning("Sin propietario", "Primero selecciona un propietario.")
            return

        propietarios = self.servicio.listar_propietarios()
        propietario = propietarios[indice_propietario]

        try:
            self.servicio.registrar_mascota(
                nombre,
                especie,
                edad,
                propietario,
                sexo,
                esterilizado,
            )
        except ValueError as error:
            messagebox.showerror("No se pudo registrar", str(error))
            return

        self.entrada_nombre_mascota.delete(0, tk.END)
        self.entrada_especie_mascota.delete(0, tk.END)
        self.entrada_edad_mascota.delete(0, tk.END)
        self.combo_sexo_mascota.current(0)
        self.combo_esterilizado_mascota.current(0)

        self.actualizar_todo()
        messagebox.showinfo("Registro exitoso", "Mascota registrada correctamente.")

    def registrar_cita(self):
        if self.indice_cita_editando is not None:
            messagebox.showwarning("Edición activa", "Guarda o cancela la edición primero.")
            return
        indice_mascota = self.combo_mascotas.current()
        fecha = self.entrada_fecha_cita.get().strip()
        hora = self.entrada_hora_cita.get().strip()
        motivo = self.entrada_motivo_cita.get().strip()
        estado = self.combo_estado_cita.get()

        if indice_mascota == -1:
            messagebox.showwarning("Sin mascota", "Primero selecciona una mascota.")
            return

        if fecha == "" or hora == "" or motivo == "" or estado == "":
            messagebox.showwarning("Datos incompletos", "Completa fecha, hora y motivo.")
            return

        mascotas = self.servicio.listar_mascotas()
        mascota = mascotas[indice_mascota]

        try:
            self.servicio.registrar_cita(mascota, fecha, hora, motivo, estado)
        except ValueError as error:
            messagebox.showerror("No se pudo registrar", str(error))
            return

        self.entrada_fecha_cita.delete(0, tk.END)
        self.entrada_hora_cita.delete(0, tk.END)
        self.entrada_motivo_cita.delete(0, tk.END)
        self.combo_estado_cita.current(0)

        self.actualizar_todo()
        messagebox.showinfo("Registro exitoso", "Cita registrada correctamente.")

    def registrar_pago(self):
        if self.indice_pago_editando is not None:
            messagebox.showwarning("Edición activa", "Guarda o cancela la edición primero.")
            return
        concepto = self.entrada_concepto_pago.get().strip()
        monto = self.entrada_monto_pago.get().strip()
        metodo = self.combo_metodo_pago.get()
        estado = self.combo_estado_pago.get()

        if concepto == "" or monto == "" or metodo == "" or estado == "":
            messagebox.showwarning(
                "Datos incompletos",
                "Completa todos los datos del pago.",
            )
            return

        try:
            self.servicio.registrar_pago(concepto, monto, metodo, estado)
        except ValueError as error:
            messagebox.showerror("No se pudo registrar", str(error))
            return

        self.entrada_concepto_pago.delete(0, tk.END)
        self.entrada_monto_pago.delete(0, tk.END)
        self.combo_metodo_pago.set("")
        self.combo_estado_pago.set("")

        self.actualizar_todo()
        messagebox.showinfo("Registro exitoso", "Pago registrado correctamente.")

    def registrar_atencion(self):
        if self.indice_atencion_editando is not None:
            messagebox.showwarning("Edición activa", "Guarda o cancela la edición primero.")
            return
        indice_mascota = self.combo_mascotas_atencion.current()
        fecha = self.entrada_fecha_atencion.get().strip()
        diagnostico = self.entrada_diagnostico.get().strip()
        tratamiento = self.entrada_tratamiento.get().strip()
        vacuna = self.entrada_vacuna.get().strip()

        if indice_mascota == -1:
            messagebox.showwarning("Sin mascota", "Primero selecciona una mascota.")
            return

        if fecha == "" or diagnostico == "" or tratamiento == "" or vacuna == "":
            messagebox.showwarning(
                "Datos incompletos",
                "Completa todos los datos de la consulta.",
            )
            return

        mascotas = self.servicio.listar_mascotas()
        mascota = mascotas[indice_mascota]

        try:
            self.servicio.registrar_atencion(
                mascota,
                fecha,
                diagnostico,
                tratamiento,
                vacuna,
            )
        except ValueError as error:
            messagebox.showerror("No se pudo registrar", str(error))
            return

        self.entrada_fecha_atencion.delete(0, tk.END)
        self.entrada_diagnostico.delete(0, tk.END)
        self.entrada_tratamiento.delete(0, tk.END)
        self.entrada_vacuna.delete(0, tk.END)

        self.actualizar_todo()
        messagebox.showinfo(
            "Registro exitoso",
            "Consulta registrada correctamente.",
        )

    def generar_reporte_diario(self):
        reporte = self.servicio.generar_reporte_diario()

        self.texto_reporte.delete("1.0", tk.END)
        self.texto_reporte.insert(tk.END, reporte)

    def exportar_reporte_diario(self):
        ruta_reporte = self.servicio.exportar_reporte_diario()

        messagebox.showinfo(
            "Reporte exportado",
            f"El reporte fue guardado en:\n{ruta_reporte}",
        )

    def generar_recordatorio(self):
        indice_cita = self.combo_citas_recordatorio.current()

        if indice_cita == -1:
            messagebox.showwarning("Sin cita", "Primero selecciona una cita.")
            return

        mensaje = self.servicio.preparar_recordatorio_cita(indice_cita)

        self.texto_recordatorio.delete("1.0", tk.END)
        self.texto_recordatorio.insert(tk.END, mensaje)

    def generar_historial_mascota(self):
        indice_mascota = self.combo_mascotas_historial.current()

        if indice_mascota == -1:
            messagebox.showwarning("Sin mascota", "Primero selecciona una mascota.")
            return

        historial = self.servicio.generar_historial_mascota(indice_mascota)

        self.texto_historial.delete("1.0", tk.END)
        self.texto_historial.insert(tk.END, historial)

    def actualizar_lista_propietarios(self, propietarios=None):
        self.lista_propietarios.delete(0, tk.END)
        propietarios = (
            self.servicio.listar_propietarios()
            if propietarios is None
            else propietarios
        )
        self.indices_propietarios = [
            self.servicio.listar_propietarios().index(propietario)
            for propietario in propietarios
        ]
        for propietario in propietarios:
            self.lista_propietarios.insert(tk.END, str(propietario))

        todos = self.servicio.listar_propietarios()
        nombres = [propietario.nombre for propietario in todos]
        self.combo_propietarios["values"] = nombres
        if nombres and self.combo_propietarios.current() == -1:
            self.combo_propietarios.current(0)
        if not nombres:
            self.combo_propietarios.set("")

    def ordenar_mascotas_burbuja(self, pares):
        """Ordena solo la vista, conservando el índice real para editar o eliminar."""
        criterio = self.criterio_orden_mascotas.get()
        pares[:] = ordenar_pares_burbuja(pares, criterio)
        return pares

    def actualizar_lista_mascotas(self, mascotas=None):
        self.lista_mascotas.delete(0, tk.END)
        todos = self.servicio.listar_mascotas()
        # Buscar devuelve las mismas instancias que listar: se usan sus id()
        # para evitar confundir dos mascotas con nombres iguales.
        if mascotas is None:
            termino = self.filtro_mascotas.strip().casefold()
            pares = [
                (indice, mascota) for indice, mascota in enumerate(todos)
                if not termino or termino in (
                    str(mascota) + " " + mascota.propietario.nombre
                ).casefold()
            ]
        else:
            identificadores = {id(mascota) for mascota in mascotas}
            pares = [
                (indice, mascota) for indice, mascota in enumerate(todos)
                if id(mascota) in identificadores
            ]

        self.ordenar_mascotas_burbuja(pares)
        self.indices_mascotas = [indice for indice, _ in pares]
        for _, mascota in pares:
            self.lista_mascotas.insert(tk.END, str(mascota))

        # Conservar la correspondencia de los ComboBox con el orden real.
        nombres_mascotas = [mascota.nombre for mascota in todos]
        self.combo_mascotas["values"] = nombres_mascotas
        self.combo_mascotas_atencion["values"] = nombres_mascotas
        self.combo_mascotas_historial["values"] = nombres_mascotas
        for combo in (
            self.combo_mascotas,
            self.combo_mascotas_atencion,
            self.combo_mascotas_historial,
        ):
            if nombres_mascotas and combo.current() == -1:
                combo.current(0)
            if not nombres_mascotas:
                combo.set("")

    def actualizar_lista_citas(self, citas=None):
        self.lista_citas.delete(0, tk.END)
        citas = self.servicio.listar_citas() if citas is None else citas
        todos = self.servicio.listar_citas()
        self.indices_citas = [todos.index(cita) for cita in citas]
        citas_texto = []
        for cita in citas:
            texto_cita = str(cita)
            self.lista_citas.insert(tk.END, texto_cita)
            citas_texto.append(texto_cita)

        todas_las_citas = [str(cita) for cita in todos]
        self.combo_citas_recordatorio["values"] = todas_las_citas
        if todas_las_citas and self.combo_citas_recordatorio.current() == -1:
            self.combo_citas_recordatorio.current(0)
        if not todas_las_citas:
            self.combo_citas_recordatorio.set("")

    def actualizar_lista_pagos(self, pagos=None):
        self.lista_pagos.delete(0, tk.END)
        pagos = self.servicio.listar_pagos() if pagos is None else pagos
        todos = self.servicio.listar_pagos()
        self.indices_pagos = [todos.index(pago) for pago in pagos]
        for pago in pagos:
            self.lista_pagos.insert(tk.END, str(pago))

        total = self.servicio.calcular_total_confirmado()
        self.etiqueta_total_pagos.config(text=f"Total confirmado: S/ {total:.2f}")

    def actualizar_lista_atenciones(self, atenciones=None):
        self.lista_atenciones.delete(0, tk.END)
        atenciones = (
            self.servicio.listar_atenciones() if atenciones is None else atenciones
        )
        todos = self.servicio.listar_atenciones()
        self.indices_atenciones = [todos.index(atencion) for atencion in atenciones]
        for atencion in atenciones:
            self.lista_atenciones.insert(tk.END, str(atencion))

    def _indice_seleccionado(self, lista, indices, mensaje):
        seleccion = lista.curselection()
        if not seleccion:
            messagebox.showwarning("Sin selección", mensaje)
            return None
        posicion = seleccion[0]
        if posicion >= len(indices):
            messagebox.showwarning("Selección inválida", "Actualiza la lista e inténtalo nuevamente.")
            return None
        return indices[posicion]

    def filtrar_propietarios_dialogo(self):
        termino = self.busqueda_general.get().strip()
        self.actualizar_lista_propietarios(self.servicio.buscar_propietarios(termino))

    def mostrar_todos_propietarios(self):
        self.actualizar_lista_propietarios()

    def eliminar_propietario(self):
        indice = self._indice_seleccionado(
            self.lista_propietarios,
            self.indices_propietarios,
            "Selecciona un propietario para eliminar.",
        )
        if indice is None:
            return
        propietario = self.servicio.listar_propietarios()[indice]
        if not messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Eliminar a {propietario.nombre}?",
        ):
            return
        try:
            self.servicio.eliminar_propietario(indice)
        except ValueError as error:
            messagebox.showerror("No se puede eliminar", str(error))
            return
        self.actualizar_todo()

    def filtrar_mascotas_dialogo(self):
        self.filtro_mascotas = self.busqueda_general.get().strip()
        self.actualizar_lista_mascotas(self.servicio.buscar_mascotas(self.filtro_mascotas))

    def mostrar_todas_mascotas(self):
        self.filtro_mascotas = ""
        self.actualizar_lista_mascotas()

    def eliminar_mascota(self):
        indice = self._indice_seleccionado(
            self.lista_mascotas,
            self.indices_mascotas,
            "Selecciona una mascota para eliminar.",
        )
        if indice is None:
            return
        mascota = self.servicio.listar_mascotas()[indice]
        if not messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Eliminar a {mascota.nombre} y sus citas y consultas vinculadas?",
        ):
            return
        self.servicio.eliminar_mascota(indice)
        self.actualizar_todo()

    def filtrar_citas_dialogo(self):
        termino = self.busqueda_general.get().strip().casefold()
        citas = [c for c in self.servicio.listar_citas()
                 if termino in (str(c) + " " + c.mascota.propietario.nombre).casefold()]
        self.actualizar_lista_citas(citas)

    def mostrar_todas_citas(self):
        self.actualizar_lista_citas()

    def eliminar_cita(self):
        indice = self._indice_seleccionado(
            self.lista_citas,
            self.indices_citas,
            "Selecciona una cita para eliminar.",
        )
        if indice is None:
            return
        if not messagebox.askyesno("Confirmar eliminación", "¿Eliminar la cita seleccionada?"):
            return
        self.servicio.eliminar_cita(indice)
        self.actualizar_todo()

    def filtrar_pagos_dialogo(self):
        termino = self.busqueda_general.get().strip().casefold()
        pagos = [p for p in self.servicio.listar_pagos()
                 if termino in str(p).casefold()]
        self.actualizar_lista_pagos(pagos)

    def mostrar_todos_pagos(self):
        self.actualizar_lista_pagos()

    def eliminar_pago(self):
        indice = self._indice_seleccionado(
            self.lista_pagos,
            self.indices_pagos,
            "Selecciona un pago para eliminar.",
        )
        if indice is None:
            return
        if not messagebox.askyesno("Confirmar eliminación", "¿Eliminar el pago seleccionado?"):
            return
        self.servicio.eliminar_pago(indice)
        self.actualizar_todo()

    def filtrar_atenciones_dialogo(self):
        termino = self.busqueda_general.get().strip().casefold()
        atenciones = [a for a in self.servicio.listar_atenciones()
                     if termino in str(a).casefold()]
        self.actualizar_lista_atenciones(atenciones)

    def mostrar_todas_atenciones(self):
        self.actualizar_lista_atenciones()

    def eliminar_atencion(self):
        indice = self._indice_seleccionado(
            self.lista_atenciones,
            self.indices_atenciones,
            "Selecciona una consulta para eliminar.",
        )
        if indice is None:
            return
        if not messagebox.askyesno("Confirmar eliminación", "¿Eliminar la consulta seleccionada?"):
            return
        self.servicio.eliminar_atencion(indice)
        self.actualizar_todo()

    def _entrada_dialogo(self, padre, texto, valor="", ancho=30):
        tk.Label(
            padre,
            text=texto,
            bg=self.COLORES["panel"],
            fg=self.COLORES["gris"],
            font=("Segoe UI", 9, "bold"),
        ).pack(anchor="w", padx=16, pady=(7, 2))
        entrada = tk.Entry(padre, width=ancho, font=("Segoe UI", 10))
        entrada.pack(anchor="w", padx=16, ipady=4)
        entrada.insert(0, str(valor or ""))
        return entrada

    def _combo_dialogo(self, padre, texto, valores, indice=0):
        tk.Label(
            padre,
            text=texto,
            bg=self.COLORES["panel"],
            fg=self.COLORES["gris"],
            font=("Segoe UI", 9, "bold"),
        ).pack(anchor="w", padx=16, pady=(7, 2))
        combo = ttk.Combobox(padre, state="readonly", values=valores, width=27)
        combo.pack(anchor="w", padx=16, ipady=3)
        if valores:
            combo.current(max(0, min(indice, len(valores) - 1)))
        return combo

    def _ventana_edicion(self, titulo):
        ventana = tk.Toplevel(self.ventana)
        ventana.title(titulo)
        ventana.configure(bg=self.COLORES["panel"])
        ventana.resizable(False, False)
        ventana.transient(self.ventana)
        ventana.grab_set()
        return ventana

    def editar_mascota(self):
        indice = self._indice_seleccionado(
            self.lista_mascotas, self.indices_mascotas,
            "Selecciona una mascota para editar.")
        if indice is None:
            return
        mascota = self.servicio.listar_mascotas()[indice]
        self.indice_mascota_editando = indice
        for entrada, valor in (
            (self.entrada_nombre_mascota, mascota.nombre),
            (self.entrada_especie_mascota, mascota.especie),
            (self.entrada_edad_mascota, mascota.edad),
        ):
            entrada.delete(0, tk.END)
            entrada.insert(0, str(valor))
        self.combo_sexo_mascota.set(mascota.sexo)
        self.combo_esterilizado_mascota.set(mascota.esterilizado)
        propietarios = self.servicio.listar_propietarios()
        if mascota.propietario in propietarios:
            self.combo_propietarios.current(propietarios.index(mascota.propietario))
        self.mostrar_seccion("Mascotas")

    def guardar_edicion_mascota(self):
        i = self.indice_mascota_editando
        if i is None:
            messagebox.showwarning("Sin edición", "Selecciona una mascota y pulsa Editar.")
            return
        propietarios = self.servicio.listar_propietarios()
        indice_propietario = self.combo_propietarios.current()
        if indice_propietario < 0 or indice_propietario >= len(propietarios):
            messagebox.showwarning("Propietario", "Selecciona un propietario.")
            return
        try:
            self.servicio.actualizar_mascota(
                i, self.entrada_nombre_mascota.get(),
                self.entrada_especie_mascota.get(),
                self.entrada_edad_mascota.get(), propietarios[indice_propietario],
                self.combo_sexo_mascota.get(), self.combo_esterilizado_mascota.get())
        except (ValueError, IndexError) as error:
            messagebox.showerror("Edición", str(error))
            return
        self.cancelar_edicion_mascota()
        self.actualizar_todo()
        self.mostrar_seccion("Mascotas")

    def cancelar_edicion_mascota(self):
        self.indice_mascota_editando = None
        for entrada in (self.entrada_nombre_mascota,
                        self.entrada_especie_mascota, self.entrada_edad_mascota):
            entrada.delete(0, tk.END)
        self.combo_sexo_mascota.current(0)
        self.combo_esterilizado_mascota.current(0)

    def editar_cita(self):
        indice = self._indice_seleccionado(
            self.lista_citas, self.indices_citas, "Selecciona una cita para editar.")
        if indice is None:
            return
        cita = self.servicio.listar_citas()[indice]
        self.indice_cita_editando = indice
        mascotas = self.servicio.listar_mascotas()
        if cita.mascota in mascotas:
            self.combo_mascotas.current(mascotas.index(cita.mascota))
        for entrada, valor in ((self.entrada_fecha_cita, cita.fecha),
                            (self.entrada_hora_cita, cita.hora),
                            (self.entrada_motivo_cita, cita.motivo)):
            entrada.delete(0, tk.END)
            entrada.insert(0, str(valor))
        self.combo_estado_cita.set(cita.estado)
        self.mostrar_seccion("Citas")

    def guardar_edicion_cita(self):
        indice = self.indice_cita_editando
        if indice is None:
            messagebox.showwarning("Sin edición", "Selecciona una cita y pulsa Editar.")
            return
        mascotas = self.servicio.listar_mascotas()
        i = self.combo_mascotas.current()
        if i < 0 or i >= len(mascotas):
            messagebox.showwarning("Mascota", "Selecciona una mascota.")
            return
        try:
            self.servicio.actualizar_cita(
                indice, mascotas[i], self.entrada_fecha_cita.get(),
                self.entrada_hora_cita.get(), self.entrada_motivo_cita.get(),
                self.combo_estado_cita.get())
        except (ValueError, IndexError) as error:
            messagebox.showerror("Edición", str(error))
            return
        self.cancelar_edicion_cita()
        self.actualizar_todo()
        self.mostrar_seccion("Citas")

    def cancelar_edicion_cita(self):
        self.indice_cita_editando = None
        for entrada in (self.entrada_fecha_cita,
                        self.entrada_hora_cita, self.entrada_motivo_cita):
            entrada.delete(0, tk.END)
        self.combo_estado_cita.current(0)

    def editar_pago(self):
        indice = self._indice_seleccionado(
            self.lista_pagos, self.indices_pagos, "Selecciona un pago para editar.")
        if indice is None:
            return
        pago = self.servicio.listar_pagos()[indice]
        self.indice_pago_editando = indice
        for entrada, valor in ((self.entrada_concepto_pago, pago.concepto),
                              (self.entrada_monto_pago, pago.monto)):
            entrada.delete(0, tk.END)
            entrada.insert(0, str(valor))
        self.combo_metodo_pago.set(pago.metodo)
        self.combo_estado_pago.set(pago.estado)
        self.mostrar_seccion("Pagos")

    def guardar_edicion_pago(self):
        indice = self.indice_pago_editando
        if indice is None:
            messagebox.showwarning("Sin edición", "Selecciona un pago y pulsa Editar.")
            return
        try:
            self.servicio.actualizar_pago(
                indice, self.entrada_concepto_pago.get(),
                self.entrada_monto_pago.get(), self.combo_metodo_pago.get(),
                self.combo_estado_pago.get())
        except (ValueError, IndexError) as error:
            messagebox.showerror("Edición", str(error))
            return
        self.cancelar_edicion_pago()
        self.actualizar_todo()
        self.mostrar_seccion("Pagos")

    def cancelar_edicion_pago(self):
        self.indice_pago_editando = None
        self.entrada_concepto_pago.delete(0, tk.END)
        self.entrada_monto_pago.delete(0, tk.END)
        self.combo_metodo_pago.set("")
        self.combo_estado_pago.set("")

    def editar_atencion(self):
        indice = self._indice_seleccionado(
            self.lista_atenciones, self.indices_atenciones,
            "Selecciona una consulta para editar.")
        if indice is None:
            return
        atencion = self.servicio.listar_atenciones()[indice]
        self.indice_atencion_editando = indice
        mascotas = self.servicio.listar_mascotas()
        if atencion.mascota in mascotas:
            self.combo_mascotas_atencion.current(mascotas.index(atencion.mascota))
        for entrada, valor in (
            (self.entrada_fecha_atencion, atencion.fecha),
            (self.entrada_diagnostico, atencion.diagnostico),
            (self.entrada_tratamiento, atencion.tratamiento),
            (self.entrada_vacuna, atencion.vacuna),
        ):
            entrada.delete(0, tk.END)
            entrada.insert(0, str(valor))
        self.mostrar_seccion("Consultas")

    def guardar_edicion_atencion(self):
        indice = self.indice_atencion_editando
        if indice is None:
            messagebox.showwarning("Sin edición", "Selecciona una consulta y pulsa Editar.")
            return
        mascotas = self.servicio.listar_mascotas()
        i = self.combo_mascotas_atencion.current()
        if i < 0 or i >= len(mascotas):
            messagebox.showwarning("Mascota", "Selecciona una mascota.")
            return
        try:
            self.servicio.actualizar_atencion(
                indice, mascotas[i], self.entrada_fecha_atencion.get(),
                self.entrada_diagnostico.get(), self.entrada_tratamiento.get(),
                self.entrada_vacuna.get())
        except (ValueError, IndexError) as error:
            messagebox.showerror("Edición", str(error))
            return
        self.cancelar_edicion_atencion()
        self.actualizar_todo()
        self.mostrar_seccion("Consultas")

    def cancelar_edicion_atencion(self):
        self.indice_atencion_editando = None
        for entrada in (self.entrada_fecha_atencion, self.entrada_diagnostico,
                        self.entrada_tratamiento, self.entrada_vacuna):
            entrada.delete(0, tk.END)

    def exportar_datos_csv(self):
        carpeta, _ = self.servicio.exportar_datos_csv()
        messagebox.showinfo(
            "Exportación completada",
            f"Los archivos CSV fueron guardados en:\n{carpeta}",
        )

    def importar_propietarios_csv(self):
        ruta = filedialog.askopenfilename(
            title="Selecciona un CSV de propietarios",
            filetypes=[("Archivos CSV", "*.csv"), ("Todos los archivos", "*.*")],
        )
        if not ruta:
            return
        try:
            cantidad = self.servicio.importar_propietarios_csv(ruta)
        except (OSError, ValueError) as error:
            messagebox.showerror("No se pudo importar", str(error))
            return
        self.actualizar_todo()
        messagebox.showinfo("Importación completada", f"Propietarios agregados: {cantidad}")

    def actualizar_dashboard(self):
        propietarios = len(self.servicio.listar_propietarios())
        mascotas = len(self.servicio.listar_mascotas())
        citas = self.servicio.listar_citas()
        atenciones = self.servicio.listar_atenciones()
        hoy = date.today()
        citas_hoy = sorted(
            (c for c in citas
             if (self.servicio._normalizar_fecha(c.fecha) or datetime.min).date() == hoy),
            key=lambda c: c.hora,
        )
        pendientes = sum(1 for c in citas if c.estado == "Pendiente")
        atendidas = sum(1 for c in citas if c.estado == "Atendida")
        canceladas = sum(1 for c in citas if c.estado == "Cancelada")
        total = self.servicio.calcular_total_confirmado()

        self.valor_propietarios.config(text=str(propietarios))
        self.valor_mascotas.config(text=str(mascotas))
        self.valor_citas.config(text=str(len(citas_hoy)))
        self.valor_pagos_inicio.config(text=f"S/ {total:,.2f}")
        self.valor_atenciones_inicio.config(text=str(len(atenciones)))
        self.valor_pendientes_inicio.config(text=str(pendientes))
        self.valor_estado_atendidas.config(text=str(atendidas))
        self.valor_estado_canceladas.config(text=str(canceladas))

        for tabla in (self.tabla_citas_inicio, self.tabla_pacientes_inicio):
            for elemento in tabla.get_children():
                tabla.delete(elemento)

        for cita in citas_hoy:
            self.tabla_citas_inicio.insert("", "end", values=(
                cita.hora, cita.mascota.nombre, cita.mascota.propietario.nombre,
                cita.motivo, cita.estado))
        for mascota in self.servicio.listar_mascotas()[-8:][::-1]:
            self.tabla_pacientes_inicio.insert("", "end", values=(
                mascota.nombre, mascota.especie, f"{mascota.edad} años",
                mascota.propietario.nombre))
        self.dibujar_grafico_dashboard()

    def actualizar_todo(self):
        self.actualizar_lista_propietarios()
        self.actualizar_lista_mascotas()
        self.actualizar_lista_citas()
        self.actualizar_lista_pagos()
        self.actualizar_lista_atenciones()
        self.actualizar_dashboard()

    def ejecutar(self):
        self.ventana.mainloop()


def iniciar_app():
    app = AppVeterinaria()
    app.ejecutar()
