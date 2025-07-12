import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog, messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from algoritmos_nuevos import (
    cargar_datos_simbolos,
    codificar_shannon_fano,
    codificar_huffman,
    obtener_codigos_ordenados,
    decodificar_shannon_fano,
    decodificar_huffman,
    guardar_codigos_codificacion,
    cargar_codigos_codificacion
)

from utils import (
    convertir_a_grises_y_mostrar,
    cargar_pixeles_como_texto,
    reconstruir_imagen_desde_texto
)

# Variables
texto_original = {}
datos_codificacion = {}
codificado_huffman = {}
codificado_shannon = {}
codigos_huffman = {}
codigos_shannon = {}
huffman = False
shannon = False
ancho = None
alto = None
textoImagen = None
json = False

# Ventanas
ventana_texto_codificado = None
ventana_tabla_codigos = None
ventana_opciones = None
widget_huffman = None
widget_shannon = None
ventana_comparacion = None
ventana_grafico_frecuencias = None
ventana_json = None

# Cuadro de Texto #
#----------------------------------------------------------
def verificar_contenido(event=None):
    global ventana_texto_codificado, ventana_tabla_codigos, widget_huffman, widget_shannon, ventana_comparacion, ventana_grafico_frecuencias, texto_original, datos_codificacion, shannon, huffman, codificado_shannon, codificado_huffman, codigos_huffman, codigos_shannon

    if archivo_cargado:
        datos_codificacion = cargar_datos_simbolos(texto_original)
        return
    
    if ventana_texto_codificado and ventana_texto_codificado.winfo_exists():
        ventana_texto_codificado.destroy()
    if ventana_tabla_codigos and ventana_tabla_codigos.winfo_exists():
        ventana_tabla_codigos.destroy()
    if widget_huffman:
        widget_huffman.destroy()
    if widget_shannon:
        widget_shannon.destroy()
    if ventana_comparacion and ventana_comparacion.winfo_exists():
        ventana_comparacion.destroy()
    if ventana_grafico_frecuencias and ventana_grafico_frecuencias.winfo_exists():
        ventana_grafico_frecuencias.destroy()
    if ventana_json and ventana_json.winfo_exists():
        ventana_json.destroy()

    boton_ver_texto_codificado.config(state=tk.DISABLED)
    boton_tabla_codigos.config(state=tk.DISABLED)
    boton_decodificar.config(state=tk.DISABLED)
    boton_comparar_resultados.config(state=tk.DISABLED)
    codificado_huffman = {}
    codificado_shannon = {}
    codigos_huffman = {}
    codigos_shannon = {}
    shannon = False
    huffman = False

    texto_original = cuadro_texto.get("1.0", tk.END).strip()
    datos_codificacion = cargar_datos_simbolos(texto_original)

def controlar_cuadro_texto(event=None):
    verificar_contenido(event)
    actualizar_estado_boton_archivo(event)
#----------------------------------------------------------

def manejar_boton_archivo():
    global archivo_cargado, texto_original, datos_codificacion, json

    if not archivo_cargado:
        archivo = filedialog.askopenfilename(filetypes=[("Archivos de Texto", "*.txt")])
        texto_original = cuadro_texto.get("1.0", tk.END).strip()
        datos_codificacion = cargar_datos_simbolos(texto_original)
        if archivo:
            with open(archivo, "r", encoding="utf-8") as f:
                contenido = f.read()
                cuadro_texto.insert("1.0", contenido)
                cuadro_texto.config(state=tk.DISABLED)
                boton_cargar_imagen.config(state=tk.DISABLED)
                archivo_cargado = True
                boton_cargar_archivo.config(text="Quitar Archivo")
            texto_original = cuadro_texto.get("1.0", tk.END).strip()
            datos_codificacion = cargar_datos_simbolos(texto_original)
            boton_cargar_imagen.config(state=tk.DISABLED)
            boton_cargar_json.config(state=tk.NORMAL)
    else:
        cuadro_texto.config(state=tk.NORMAL)
        cuadro_texto.delete("1.0", tk.END)
        archivo_cargado = False
        boton_cargar_archivo.config(text="Cargar Archivo")
        #actualizar_estado_boton_archivo()
        boton_cargar_imagen.config(state=tk.NORMAL)
        boton_cargar_json.config(state=tk.DISABLED)
        if json:
            json = False
            boton_huffman.config(state=tk.NORMAL)
            boton_shannon.config(state=tk.NORMAL)
        verificar_contenido()

def actualizar_estado_boton_archivo(event=None):
    global texto_original, json

    if texto_original:
        boton_cargar_archivo.config(state=tk.DISABLED)
        boton_cargar_imagen.config(state=tk.DISABLED)
        boton_cargar_json.config(state=tk.DISABLED)
        json = False
    elif not texto_original:
        boton_cargar_archivo.config(state=tk.NORMAL)
        boton_cargar_imagen.config(state=tk.NORMAL)

# Codificación #
#-------------------------------------------------------------
def codificar_texto(algoritmo):
    global texto_original, codificado_shannon, codificado_huffman, codigos_huffman, codigos_shannon, shannon, huffman, datos_codificacion

    texto_original = cuadro_texto.get("1.0", tk.END).strip()

    if not texto_original:
        messagebox.showwarning("Aviso", "No hay texto para codificar.")
        return

    if algoritmo == "shannon":
        codificar_shannon_fano(datos_codificacion)
        shannon = True
        codificado_shannon = datos_codificacion["Codificaciones"]["Shannon-Fano"]["TextoCodificado"]
        codigos_shannon = obtener_codigos_ordenados(datos_codificacion, "Shannon-Fano")
    else:
        codificar_huffman(datos_codificacion)
        huffman = True
        codificado_huffman = datos_codificacion["Codificaciones"]["Huffman"]["TextoCodificado"]
        codigos_huffman = obtener_codigos_ordenados(datos_codificacion, "Huffman")

    boton_tabla_codigos.config(state=tk.NORMAL)
    
    if huffman and shannon:
        boton_comparar_resultados.config(state=tk.NORMAL)

    if not imagen_cargada:
        boton_ver_texto_codificado.config(state=tk.NORMAL)

    if imagen_cargada:
        boton_decodificar.config(state=tk.NORMAL)

def ver_texto_codificado():
    global ventana_texto_codificado, widget_huffman, widget_shannon, codificado_huffman, codificado_shannon

    boton_decodificar.config(state=tk.NORMAL)

    if ventana_texto_codificado is not None and ventana_texto_codificado.winfo_exists():
        ventana_texto_codificado.destroy()

    ventana_texto_codificado = tk.Toplevel(ventana_principal)
    ventana_texto_codificado.title("Texto codificado")
    ventana_texto_codificado.configure(bg="white")
    
    ventana_texto_codificado.attributes('-topmost', True)
    ventana_texto_codificado.rowconfigure(0, weight=1)
    ventana_texto_codificado.columnconfigure(0, weight=1)

    ventana_texto_codificado.protocol("WM_DELETE_WINDOW", lambda: (boton_decodificar.config(state="disabled"), ventana_texto_codificado.destroy()))

    frame_contenedor = tk.Frame(ventana_texto_codificado, bg="black")
    frame_contenedor.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    if codificado_shannon:
        widget_shannon = tk.Text(frame_contenedor, height=15, wrap=tk.WORD, font=("Arial", 12), bg="white", fg="black")
        widget_shannon.insert(tk.END, f"Texto codificado con Shannon:\n\n{codificado_shannon}")
        widget_shannon.pack(fill=tk.X, pady=5)

    if codificado_huffman: 
        widget_huffman = tk.Text(frame_contenedor, height=15, wrap=tk.WORD, font=("Arial", 12), bg="white", fg="black")
        widget_huffman.insert(tk.END, f"Texto codificado con Huffman:\n\n{codificado_huffman}")
        widget_huffman.pack(fill=tk.X, pady=5)


def mostrar_opciones():
    global ventana_opciones

    if ventana_opciones is not None and ventana_opciones.winfo_exists():
        ventana_opciones.destroy()

    ventana_opciones = tk.Toplevel(ventana_principal)
    ventana_opciones.title("Elegí un Algoritmo")
    ventana_opciones.configure(bg="black")
    ventana_opciones.geometry("300x150")

    ventana_opciones.attributes('-topmost', True)

    tk.Label(ventana_opciones, text="Elegí un Algoritmo para Decodificar", bg="black", fg="white").pack(pady=10)

    tk.Button(ventana_opciones, text="Huffman", width=20, command=lambda:decodificar("huffman", ventana_opciones)).pack(pady=5)

    tk.Button(ventana_opciones, text="Shannon-Fano", width=20, command=lambda:decodificar("shannon", ventana_opciones)).pack(pady=5)

def decodificar(algoritmo, ventana_popup):
    global widget_huffman, widget_shannon, codigos_shannon, codigos_huffman, codificado_huffman, codificado_shannon, alto, ancho, json, ventana_json

    ventana_popup.destroy()

    if algoritmo == "huffman":
        if not codigos_huffman:
            messagebox.showerror("Error", "No hay códigos Huffman disponibles", parent=ventana_texto_codificado)
            return
        texto_decodificado = decodificar_huffman(codificado_huffman, codigos_huffman)
        if not imagen_cargada and not json:
            widget_huffman.delete("1.0", tk.END)
            widget_huffman.insert(tk.END, texto_decodificado)
        if json:
            ventana_json = tk.Toplevel(ventana_principal)
            ventana_json.title("Texto Decodificado")
            ventana_json.configure(bg="white")
            ventana_json.geometry("600x300")

            ventana_json.attributes('-topmost', True)

            contenedor = tk.Frame(ventana_json, bg="black")
            contenedor.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

            widget_huffman = tk.Text(contenedor, height=15, wrap=tk.WORD, font=("Arial", 12), bg="white", fg="black")
            widget_huffman.insert(tk.END, f"Texto decodificado con Huffman:\n\n{texto_decodificado}")
            widget_huffman.pack(fill=tk.X, pady=5)
    elif algoritmo == "shannon":
        if not codigos_shannon:
            messagebox.showerror("Error", "No hay códigos Shannon-Fano disponibles", parent=ventana_texto_codificado)
            return
        texto_decodificado = decodificar_shannon_fano(codificado_shannon, codigos_shannon)
        if not imagen_cargada and not json:
            widget_shannon.delete("1.0", tk.END)
            widget_shannon.insert(tk.END, texto_decodificado)
        if json:
            ventana_json = tk.Toplevel(ventana_principal)
            ventana_json.title("Texto Decodificado")
            ventana_json.configure(bg="white")
            ventana_json.geometry("600x300")

            ventana_json.attributes('-topmost', True)

            contenedor = tk.Frame(ventana_json, bg="black")
            contenedor.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

            widget_shannon = tk.Text(contenedor, height=15, wrap=tk.WORD, font=("Arial", 12), bg="white", fg="black")
            widget_shannon.insert(tk.END, f"Texto decodificado con Shannon:\n\n{codificado_shannon}")
            widget_shannon.pack(fill=tk.X, pady=5)
    
    if imagen_cargada:
        ruta = filedialog.asksaveasfilename(
            parent=ventana_principal,
            defaultextension=".png", filetypes=[("Imagen PNG", "*.png")], title="Guardar imagen reconstruida como..."
        )
        try:
            reconstruir_imagen_desde_texto(texto_decodificado, ancho, alto, ruta)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar la imagen:\n{e}")

def manejar_archivo_json():
    global codigos_huffman, codificado_huffman, json
    
    if not json:
        json = True

        boton_huffman.config(state=tk.DISABLED)
        boton_shannon.config(state=tk.DISABLED)

        ruta =  filedialog.askopenfilename(filetypes=[("Archivos JSON", "*.json")])

        boton_cargar_json.config(text="Quitar Códigos")
        info_codigos = cargar_codigos_codificacion(ruta)
        algoritmo = info_codigos["Algoritmo"]
        codigosJSON = info_codigos["Códigos"]

        # Texto codificado desde el Text
        texto_codificado = cuadro_texto.get("1.0", tk.END).strip()
        if algoritmo == "Huffman":
            codigos_huffman = codigosJSON
            codificado_huffman = texto_codificado
        elif algoritmo == "Shannon-Fano":
            codigos_shannon = codigosJSON
            codificado_shannon = texto_codificado

        boton_decodificar.config(state=tk.NORMAL)
    elif json:
        json = False
        boton_cargar_json.config(text="Cargar Códigos")
        codigos_huffman = {}
        codificado_huffman = {}
        codigos_shannon = {}
        codificado_shannon = {}
        boton_huffman.config(state=tk.NORMAL)
        boton_shannon.config(state=tk.NORMAL)
        if ventana_json and ventana_json.winfo_exists():
            ventana_json.destroy()
        boton_decodificar.config(state=tk.DISABLED)
#-------------------------------------------------------------

# Mostrar Gráficos #
#-------------------------------------------------------------
def mostrar_grafico_frecuencias():
    global ventana_grafico_frecuencias, texto_original, datos_codificacion

    texto_original = cuadro_texto.get("1.0", tk.END).strip()

    if not texto_original:
        messagebox.showwarning("Advertencia", "No hay texto para analizar")
        return
    
    # Obtener Frecuencias
    frecuencias = {simbolo["Caracter"]: simbolo["Cantidad"] for simbolo in datos_codificacion["ListaSimbolos"]}

    simbolos = list(frecuencias.keys())
    valores = list(frecuencias.values())

    # Crear ventana emergente
    ventana_grafico_frecuencias = tk.Toplevel(ventana_principal)
    ventana_grafico_frecuencias.title("Gráfico de Frecuencias")
    ventana_grafico_frecuencias.geometry("600x400")
    ventana_grafico_frecuencias.config(bg="white")

    ventana_grafico_frecuencias.attributes('-topmost', True)

    # Frame con Scroll
    frame_canvas = tk.Frame(ventana_grafico_frecuencias)
    frame_canvas.pack(fill="both", expand=True)

    canvas_tk = tk.Canvas(frame_canvas, bg="white")
    h_scroll = tk.Scrollbar(frame_canvas, orient="horizontal", command=canvas_tk.xview)

    canvas_tk.config(xscrollcommand=h_scroll.set)

    h_scroll.pack(side="bottom", fill="x")
    canvas_tk.pack(side="left", fill="both", expand=True, padx=0, pady=0)

    frame_grafico = tk.Frame(canvas_tk)
    canvas_tk.create_window((0, 0), window=frame_grafico, anchor="nw")
    
    # Crear figura matplotlib (ancho dinámico según cantidad de símbolos)
    ancho_grafico = max(10, len(simbolos) * 0.25)
    figura = Figure(figsize=(ancho_grafico, 6.5), dpi=100, tight_layout=False)
    ejes = figura.add_subplot(111)
    ejes.bar(simbolos, valores, color="skyblue")
    ejes.set_title("Frecuencia de Símbolos")
    ejes.set_xlabel("Símbolo")
    ejes.set_ylabel("Frecuencia")
    ejes.set_xlim(-1, len(simbolos) - 0.25)
    figura.subplots_adjust(
    left=0.1, 
    right=0.95,
    top=0.9,
    bottom=0.005
    )
    ejes.tick_params(axis='x', labelrotation=0)

    # Integrar con Tkinter
    canvas = FigureCanvasTkAgg(figura, master=frame_grafico)
    canvas.get_tk_widget().pack(fill="both", expand=True)
    canvas.draw()
    canvas.get_tk_widget().update_idletasks()

    frame_grafico.update_idletasks()

    canvas_tk.config(scrollregion=canvas_tk.bbox("all"))

def mostrar_tabla_codigos():
    global ventana_tabla_codigos

    if ventana_tabla_codigos is not None and ventana_tabla_codigos.winfo_exists():
        ventana_tabla_codigos.destroy()

    if not codigos_huffman and not codigos_shannon:
        messagebox.showinfo("Sin datos", "No hay códigos disponibles")
        return

    ventana_tabla_codigos = tk.Toplevel(ventana_principal)
    ventana_tabla_codigos.title("Tabla de Códigos")
    ventana_tabla_codigos.configure(bg="black")
    ventana_tabla_codigos.geometry("800x400")

    ventana_tabla_codigos.attributes('-topmost', True)

    frame_tablas = tk.Frame(ventana_tabla_codigos, bg="black")
    frame_tablas.pack(padx=20, pady=20)

    if codigos_huffman:
        frame_huffman = tk.Frame(frame_tablas, bg="black")
        frame_huffman.pack(side=tk.LEFT, padx=10)
        tk.Label(frame_huffman, text="Huffman", fg="white", bg="#333333", font=("Arial", 12, "bold")).pack()
        crear_treeview(frame_huffman, codigos_huffman)

    if codigos_shannon:
        frame_shannon = tk.Frame(frame_tablas, bg="black")
        frame_shannon.pack(side=tk.LEFT, padx=10)
        tk.Label(frame_shannon, text="Shannon", fg="white", bg="#333333", font=("Arial", 12, "bold")).pack()
        crear_treeview(frame_shannon, codigos_shannon)

# Esta función crea la tabla de símbolos y códigos
def crear_treeview(parent, codigos):

    texto = cuadro_texto.get("1.0", tk.END).strip()

    tree = ttk.Treeview(parent, columns=("Símbolo", "Código"), show="headings", height=len(set(texto)))
    tree.heading("Símbolo", text="Símbolo")
    tree.heading("Código", text="Código")
    tree.column("Símbolo", anchor="center", width=100)
    tree.column("Código", anchor="center", width="200")

    for simbolo, codigo in codigos.items():
        tree.insert("", tk.END, values=(repr(simbolo), (codigo)))
    tree.pack(padx=10, pady=5)
#-------------------------------------------------------------

# Compresión de Imagen #
#-------------------------------------------------------------
def cargar_imagen():
    global imagen_cargada, datos_codificacion, ancho, alto

    if not imagen_cargada:
        imagen = filedialog.askopenfilename(filetypes=[("Archivos de Imagen", "*.png")])
        
        boton_cargar_imagen.config(text="Quitar Imagen")
        boton_cargar_archivo.config(state=tk.DISABLED)
        
        ruta_gris, ancho, alto = convertir_a_grises_y_mostrar(imagen)
        textoImagen, _, _ = cargar_pixeles_como_texto(ruta_gris)
        cuadro_texto.insert("1.0", textoImagen)
        cuadro_texto.config(state=tk.DISABLED)
        imagen_cargada = True

        cuadro_texto.unbind("<KeyRelease>")

        datos_codificacion = cargar_datos_simbolos(textoImagen)
    elif imagen_cargada:
        boton_cargar_imagen.config(text="Cargar Imagen")
        imagen_cargada = False
        datos_codificacion = {}
        alto = None
        ancho = None
        textoImagen = None
        verificar_contenido()
        boton_cargar_archivo.config(state=tk.NORMAL)
        cuadro_texto.config(state=tk.NORMAL)
        cuadro_texto.bind("<KeyRelease>", controlar_cuadro_texto)
        cuadro_texto.delete("1.0", tk.END)

#-------------------------------------------------------------

# Comparación #
#-------------------------------------------------------------
def obtener_metricas(algoritmo, texto_original, datos_codificacion, texto_codificado):

    # Tasa de compresión
    tam_original = len(texto_original) * 8
    tam_codificado = len(texto_codificado)
    tasa_compresion = tam_codificado / tam_original if tam_original > 0 else 0

    longitud_promedio = datos_codificacion["Codificaciones"][algoritmo]["LongitudPromedio"]
    eficiencia = datos_codificacion["Codificaciones"][algoritmo]["Eficiencia"]

    return tasa_compresion, longitud_promedio, eficiencia

def mostrar_comparacion():
    global ventana_comparacion, codificado_huffman, codificado_shannon, texto_original, datos_codificacion

    if ventana_comparacion is not None and ventana_comparacion.winfo_exists():
        ventana_comparacion.destroy()

    ventana_comparacion = tk.Toplevel(ventana_principal)
    ventana_comparacion.title("Comparación de Algoritmos")
    ventana_comparacion.config(bg="black")
    ventana_comparacion.geometry("800x400")

    ventana_comparacion.attributes('-topmost', True)
    
    # Obtener Métricas
    tasa_h, longitud_h, eficiencia_h = obtener_metricas("Huffman", texto_original, datos_codificacion, codificado_huffman)
    tasa_s, longitud_s, eficiencia_s = obtener_metricas("Shannon-Fano", texto_original, datos_codificacion, codificado_shannon)

    # Mostrar resultados
    label = tk.Label(ventana_comparacion, text="Comparación entre Huffman y Shannon-Fano", font=("Arial", 14, "bold"), fg="white", bg="black")
    label.pack(pady=10)

    frame_tabla = tk.Frame(ventana_comparacion, bg="white")
    frame_tabla.pack(padx=20, pady=10)

    tabla = ttk.Treeview(frame_tabla, columns=("Métrica", "Huffman", "Shannon-Fano"), show="headings", height=3)
    tabla.heading("Métrica", text="Métrica")
    tabla.heading("Huffman", text="Huffman")
    tabla.heading("Shannon-Fano", text="Shannon-Fano")
    tabla.insert("", tk.END, values=("Tasa de compresión", f"{tasa_h:.3f}", f"{tasa_s:.3f}"))
    tabla.insert("", tk.END, values=("Longitud promedio", f"{longitud_h:.3f}", f"{longitud_s:.3f}"))
    tabla.insert("", tk.END, values=("Eficiencia", f"{eficiencia_h:.3f}", f"{eficiencia_s:.3f}"))
    tabla.pack(padx=10, pady=10)
#-------------------------------------------------------------

def salir():
    ventana_principal.destroy()


# Ventana principal #
ventana_principal = tk.Tk()
ventana_principal.title("Codificador de texto")
ventana_principal.state('zoomed')
ventana_principal.config(bg="black")

archivo_cargado = False
imagen_cargada = False

# Cuadro de texto #
cuadro_texto = tk.Text(ventana_principal, height=15, width=60, font=("Arial", 12))
cuadro_texto.grid(row=0, column=0, padx=20, pady=20, sticky="nw", columnspan=2)
cuadro_texto.bind("<KeyRelease>", controlar_cuadro_texto)

#----------------------------------------------------------
# Marco para los botones de cargar archivo y ver texto codificado
marco_botones = tk.Frame(ventana_principal, bg="black")
marco_botones.grid(row=1, column=0, columnspan=2, pady=(0, 20))

# Botón para cargar y quitar archivo
boton_cargar_archivo = tk.Button(marco_botones, text="Cargar Archivo", command=manejar_boton_archivo, font=("Arial", 11), fg="white", bg="#003187", activebackground="white", bd="4", activeforeground="black", relief="sunken", cursor="hand2", highlightbackground="#333333")
boton_cargar_archivo.pack(side=tk.LEFT, padx=10)

# Botón para cargar JSON
boton_cargar_json = tk.Button(ventana_principal, text="Cargar Códigos", command=manejar_archivo_json, font=("Arial", 11), fg="white", bg="#003187", activebackground="white", bd="4", state=tk.DISABLED, activeforeground="black", relief="sunken", cursor="hand2", highlightbackground="#333333")
boton_cargar_json.place(relx=1.0, rely=1.0, x=-580, y=-600, anchor="se")

# Botón para ver el texto codificado
boton_ver_texto_codificado = tk.Button(marco_botones, text="Ver Texto Codificado", command=ver_texto_codificado, state=tk.DISABLED, font=("Arial", 11), fg="white", bg="#333333", activebackground="#555555", bd="4", activeforeground="black", relief="sunken", cursor="hand2", highlightbackground="#333333")
boton_ver_texto_codificado.pack(side=tk.LEFT, padx=10) 
#----------------------------------------------------------

#----------------------------------------------------------
# Frame para el bloque de codificación
frame_codificacion = tk.Frame(ventana_principal, bg="black")
frame_codificacion.grid(row=2, column=0, columnspan=2, pady=(10, 20))

# Marco visual del bloque de codificación
marco_codificacion = tk.LabelFrame(frame_codificacion, text="CODIFICAR MENSAJE", font=("Arial", 12, "bold"), fg="white", bg="#001122", bd=4, relief="sunken", labelanchor="n", padx=35, pady=15)
marco_codificacion.pack()

# Etiqueta de instrucción
etiqueta_algoritmo = tk.Label(marco_codificacion, text="Elija el Algoritmo a Utilizar", font=("Arial", 11), fg="white", bg="#001122")
etiqueta_algoritmo.pack(pady=(0, 10)) 

# Botones de algoritmo
frame_botones_algoritmo = tk.Frame(marco_codificacion, bg="#001122")
frame_botones_algoritmo.pack()

boton_huffman = tk.Button(frame_botones_algoritmo, text="Huffman", command=lambda: codificar_texto("huffman"), width=12, font=("Arial", 10), cursor="hand2", activebackground="#333333", activeforeground="white", bd="4", highlightbackground="#333333", relief="sunken") 
boton_huffman.pack(side=tk.LEFT, padx=5)

boton_shannon = tk.Button(frame_botones_algoritmo, text="Shannon-Fano", command=lambda: codificar_texto("shannon"), width=12, font=("Arial", 10), cursor="hand2", relief="sunken", activebackground="#333333", activeforeground="white", highlightbackground="#333333", bd="4")
boton_shannon.pack(side=tk.LEFT, padx=5)

# Botón para decodificar
boton_decodificar = tk.Button(ventana_principal, text="DECODIFICAR", command=mostrar_opciones, state=tk.DISABLED, bg="#333333", fg="white", activebackground="#555555", activeforeground="white", cursor="hand2", relief="sunken", bd="4", height=2, width=20)
boton_decodificar.place(relx=1.0, rely=1.0, x=-915, y=-140, anchor="se")
#----------------------------------------------------------

#----------------------------------------------------------
# Botón cargar imagen
boton_cargar_imagen = tk.Button(text="Cargar Imagen", command=cargar_imagen, font=("Arial", 11), fg="white", bg="#003187", activebackground="white", bd="4", activeforeground="black", relief="sunken", cursor="hand2", highlightbackground="#333333")
boton_cargar_imagen.place(relx=1.0, rely=1.0, x=-585, y=-645, anchor="se")
#----------------------------------------------------------

#----------------------------------------------------------
# Botón de tabla de códigos
boton_tabla_codigos = tk.Button(ventana_principal, text="Mostrar Tabla de Códigos", state=tk.DISABLED, command=mostrar_tabla_codigos, bg="#333333", fg="white", activebackground="#555555", cursor="hand2", font=("Arial", 11), activeforeground="white", bd="4", relief="sunken")
boton_tabla_codigos.place(relx=1.0, rely=0.0, x=-20, y=70, anchor="ne")

# Botón para mostrar el gráfico de frecuencias
boton_grafico_frecuencias = tk.Button(ventana_principal, text="Ver Gráfico de Frecuencias", command=mostrar_grafico_frecuencias, bg="#333333", font=("Arial", 11), fg="white", cursor="hand2", activebackground="#555555", activeforeground="white", relief="sunken", bd="4")
boton_grafico_frecuencias.place(relx=1.0, rely=0.0, x=-20, y=20, anchor="ne")
#----------------------------------------------------------

#----------------------------------------------------------
# Botón para realizar la comparación
boton_comparar_resultados = tk.Button(ventana_principal, text="Comparar Resultados de Huffman y Shannon-Fano", command=mostrar_comparacion, bg="#333333", fg="white", font=("Arial", 11, "bold"), activebackground="#555555", activeforeground="white", relief="sunken", cursor="hand2", bd="4", state=tk.DISABLED)
boton_comparar_resultados.place(relx=1.0, rely=1.0, x=-800, y=-50, anchor="se")

# Botón de salir de la aplicación
boton_salir = tk.Button(ventana_principal, text="Salir", font=("Arial", 11), fg="white", bg="darkred", command=salir, bd="4", cursor="hand2", relief="sunken", highlightbackground="#333333")
boton_salir.place(relx=1.0, rely=1.0, x=-20, y=-20, anchor="se")
#----------------------------------------------------------

def main():
    ventana_principal.mainloop()

if __name__ == "__main__":
        main()