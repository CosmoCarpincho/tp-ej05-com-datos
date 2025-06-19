import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog, messagebox
import math
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from algoritmos.shannon_fano import codificar_shannon_fano, decodificar_shannon_fano, calcular_probabilidad # Importo Shannon-Fano
from algoritmos.huffman import codificar_huffman, decodificar_huffman # Importo Huffman
from collections import Counter

codigos_huffman = {}
codigos_shannon = {}
texto_original = ""
codificado_huffman = ""
codificado_shannon = ""
probabilidades = {}

ventana_texto_codificado = None
ventana_tabla_codigos = None
ventana_opciones = None
ventana_comp = None
ventana_grafico_frecuencias = None

widget_huffman = None
widget_shannon = None

# Función para actualizar el estado del botón de texto
def actualizar_estado_boton_texto(event=None):
    contenido = text_widget.get("1.0", tk.END).strip()

    if not archivo_cargado and contenido:
        boton_cargar_archivo.config(state=tk.DISABLED)
    else:
        if not archivo_cargado:
            boton_cargar_archivo.config(state=tk.NORMAL)

# Función para cargar o quitar archivo
def manejar_archivo():
    global archivo_cargado

    if not archivo_cargado:
        archivo = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt")])
        if archivo:
            with open(archivo, "r", encoding="utf-8") as f:
                contenido = f.read()
                text_widget.delete("1.0", tk.END)
                text_widget.insert("1.0", contenido)
                text_widget.config(state=tk.DISABLED)
                archivo_cargado = True
                boton_cargar_archivo.config(text="Quitar archivo")
    else:
        text_widget.config(state=tk.NORMAL)
        text_widget.delete("1.0", tk.END)
        archivo_cargado = False
        boton_cargar_archivo.config(text="Cargar archivo")
        actualizar_estado_boton_texto()
        verificar_contenido()

# Función para codificar el texto
def codificar_texto(algoritmo):
    global codigos_huffman, codigos_shannon, codificado_shannon, codificado_huffman, probabilidades, texto_original

    texto_original = text_widget.get("1.0", tk.END).strip()
    if not texto_original:
        messagebox.showwarning("Aviso", "No hay texto para codificar.")
        return
    
    if algoritmo == "shannon":
        texto_codificado, codigos, frecuecias = codificar_shannon_fano(texto_original)
        codigos_shannon = codigos
        diccionario_codigos = codigos_shannon
        codificado_shannon = texto_codificado
        lista = calcular_probabilidad(frecuecias) # Uso Shannon-Fano para obtener la probabilidad
        probabilidades = dict(lista)
    elif algoritmo == "huffman":
        texto_codificado, codigos, frecuecias = codificar_huffman(texto_original)
        codigos_huffman = codigos
        diccionario_codigos = codigos_huffman
        codificado_huffman = texto_codificado

    resultado = f"Texto codificado:\n{texto_codificado}\n\nCódigos:\n"
    for simbolo, codigo in codigos.items():
        resultado += f"'{simbolo}': {codigo}\n"

    if codigos_huffman or codigos_shannon:
        boton_tabla_codigos.config(state=tk.NORMAL)

    if codificado_huffman and codificado_shannon:
        boton_comparar.config(state=tk.NORMAL)

    boton_ver_texto_codificado.config(state=tk.NORMAL)

# Ventana que me permite elegir cuál algoritmo voy a usar para decodificar
def mostrar_opciones(opcion):
    global ventana_opciones

    if ventana_opciones is not None and ventana_opciones.winfo_exists():
        ventana_opciones.destroy()

    ventana_opciones = tk.Toplevel(ventana)
    ventana_opciones.title("Elegí un algoritmo")
    ventana_opciones.configure(bg="black")
    ventana_opciones.geometry("300x150")

    ventana_opciones.attributes('-topmost', True)

    tk.Label(ventana_opciones, text="Elegí un algoritmo para decodificar", bg="black", fg="white").pack(pady=10)

    tk.Button(ventana_opciones, text="Huffman", width=20, command=lambda:decodificar_con_algoritmo("huffman", ventana_opciones)).pack(pady=5)

    tk.Button(ventana_opciones, text="Shannon-Fano", width=20, command=lambda:decodificar_con_algoritmo("shannon", ventana_opciones)).pack(pady=5)

# Función para crear la ventana que me permite ver el texto codificado por los algoritmos
# < La decodificación solo estará disponible si esta ventana está abierta, ya que acá se mostrará
# el texto decodificado >
def ver_texto_codificado():
    global ventana_texto_codificado, widget_huffman, widget_shannon, codificado_huffman, codificado_shannon

    boton_decodificar.config(state=tk.NORMAL)

    if ventana_texto_codificado is not None and ventana_texto_codificado.winfo_exists():
        ventana_texto_codificado.destroy()

    ventana_texto_codificado = tk.Toplevel(ventana)
    ventana_texto_codificado.title("Texto codificado")
    ventana_texto_codificado.configure(bg="white")
    
    ventana_texto_codificado.attributes('-topmost', True)
    ventana_texto_codificado.rowconfigure(0, weight=1)
    ventana_texto_codificado.columnconfigure(0, weight=1)

    ventana_texto_codificado.protocol("WM_DELETE_WINDOW", lambda: (boton_decodificar.config(state="disabled"), ventana_texto_codificado.destroy()))

    frame_contenedor = tk.Frame(ventana_texto_codificado, bg="black")
    frame_contenedor.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    # Reemplazar contenido del widget con el texto codificado 
    if codificado_huffman: 
        widget_huffman = tk.Text(frame_contenedor, height=5, wrap=tk.WORD, font=("Arial", 12), bg="white", fg="black")
        # widget_huffman.grid(row=0, column=0, padx=10, pady=10, sticky="nsew", columnspan=2)
        widget_huffman.insert(tk.END, f"Texto codificado con Huffman:\n\n{codificado_huffman}")
        widget_huffman.pack(fill=tk.X, pady=5)
    if codificado_shannon:
        widget_shannon = tk.Text(frame_contenedor, height=5, wrap=tk.WORD, font=("Arial", 12), bg="white", fg="black")
        # widget_shannon.grid(row=0, column=0, padx=10, pady=10, sticky="nsew", columnspan=2)
        widget_shannon.insert(tk.END, f"Texto codificado con Shannon:\n\n{codificado_shannon}")
        widget_shannon.pack(fill=tk.X, pady=5)

# Función para decodificar el mensaje
def decodificar_con_algoritmo(algoritmo, ventana_popup):
    global widget_huffman, widget_shannon
    ventana_popup.destroy() # Cierra la ventana emergente

    if algoritmo == "huffman": 
        if not codigos_huffman:
            # raise ValueError("No hay códigos Huffman disponibles")
            messagebox.showerror("Error", "No hay códigos Huffman disponibles", parent=ventana_texto_codificado)
        texto_decodificado = decodificar_huffman(codificado_huffman, codigos_huffman)
        widget_huffman.delete("1.0", tk.END)
        widget_huffman.insert(tk.END, texto_decodificado)
    elif algoritmo == "shannon":
        if not codigos_shannon:
            # raise ValueError("No hay códigos Shannon-Fano disponibles")
            messagebox.showerror("Error", "No hay códigos Shannon-Fano disponibles", parent=ventana_texto_codificado)
        texto_decodificado = decodificar_shannon_fano(codificado_shannon, codigos_shannon)
        widget_shannon.delete("1.0", tk.END)
        widget_shannon.insert(tk.END, texto_decodificado)

# Función para mostrar el gráfico de frecuencias
def mostrar_grafico_frecuencias():
    global ventana_grafico_frecuencias

    texto = text_widget.get("1.0", tk.END).strip()

    if not texto:
        messagebox.showwarning("Advertencia", "No hay texto para analizar")
        return
    
    # Calcular frecuencias
    frecuencias = Counter(texto)
    simbolos = list(frecuencias.keys())
    valores = list(frecuencias.values())

    # Crear ventana emergente
    ventana_grafico_frecuencias = tk.Toplevel(ventana)
    ventana_grafico_frecuencias.title("Gráfico de Frecuencias")
    ventana_grafico_frecuencias.geometry("600x400")
    ventana_grafico_frecuencias.config(bg="white")

    ventana_grafico_frecuencias.attributes('-topmost', True)

    # Crear figura matplotlib
    figura = Figure(figsize=(6, 4), dpi=100)
    ejes = figura.add_subplot(111)
    ejes.bar(simbolos, valores, color="skyblue")
    ejes.set_title("Frecuencia de Símbolos")
    ejes.set_xlabel("Símbolo")
    ejes.set_ylabel("Frecuencia")

    # Integrar con Tkinter
    canvas = FigureCanvasTkAgg(figura, master=ventana_grafico_frecuencias)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

# Mostrar tabla de códigos
def mostrar_tabla_codigos():
    global ventana_tabla_codigos

    if ventana_tabla_codigos is not None and ventana_tabla_codigos.winfo_exists():
        ventana_tabla_codigos.destroy()

    if not codigos_huffman and not codigos_shannon:
        messagebox.showinfo("Sin datos", "No hay códigos disponibles")
        return

    ventana_tabla_codigos = tk.Toplevel(ventana)
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

    texto = text_widget.get("1.0", tk.END).strip()

    tree = ttk.Treeview(parent, columns=("Símbolo", "Código"), show="headings", height=len(set(texto)))
    tree.heading("Símbolo", text="Símbolo")
    tree.heading("Código", text="Código")
    tree.column("Símbolo", anchor="center", width=100)
    tree.column("Código", anchor="center", width="200")

    for simbolo, codigo in codigos.items():
        tree.insert("", tk.END, values=(repr(simbolo), (codigo)))
    tree.pack(padx=10, pady=5)

# Función para calcular eficiencia, tasa de compresión y logitud promedio
def calcular_metricas(texto_original, texto_codificado, codigos, probabilidades):

    # Tasa de compresión
    tam_original = len(texto_original) * 8
    tam_codificado = len(texto_codificado)
    tasa_compresion = tam_codificado / tam_original if tam_original > 0 else 0

    # Longitud promedio
    longitud_prom = sum(probabilidades[simb] * len(codigos[simb]) for simb in codigos)

    # Entropía
    entropia = -sum(prob * math.log2(prob) for prob in probabilidades.values() if prob > 0)

    # Eficiencia
    eficiencia = entropia / longitud_prom if longitud_prom > 0 else 0

    return tasa_compresion, longitud_prom, eficiencia

# Esta función va a mostrar la comparación entre los algoritmos
def mostrar_comparacion():
    global codificado_shannon, codificado_huffman, codigos_huffman, codigos_shannon, probabilidades, texto_original, ventana_comp

    if ventana_comp is not None and ventana_comp.winfo_exists():
        ventana_comp.destroy()

    ventana_comp = tk.Toplevel(ventana)
    ventana_comp.title("Comparación de Algoritmos")
    ventana_comp.config(bg="black")
    ventana_comp.geometry("800x400")

    ventana_comp.attributes('-topmost', True)

    # Calcular métricas
    tasa_h, longitud_h, efic_h = calcular_metricas(texto_original, codificado_huffman, codigos_huffman, probabilidades)
    tasa_s, longitud_s, efic_s = calcular_metricas(texto_original, codificado_shannon, codigos_shannon, probabilidades)

    # Mostrar resultados
    label = tk.Label(ventana_comp, text="Comparación entre Huffman y Shannon-Fano", font=("Arial", 14, "bold"), fg="white", bg="black")
    label.pack(pady=10)

    frame_tabla = tk.Frame(ventana_comp, bg="white")
    frame_tabla.pack(padx=20, pady=10)

    tabla = ttk.Treeview(frame_tabla, columns=("Métrica", "Huffman", "Shannon-Fano"), show="headings", height=3)
    tabla.heading("Métrica", text="Métrica")
    tabla.heading("Huffman", text="Huffman")
    tabla.heading("Shannon-Fano", text="Shannon-Fano")
    tabla.insert("", tk.END, values=("Tasa de compresión", f"{tasa_h:.3f}", f"{tasa_s:.3f}"))
    tabla.insert("", tk.END, values=("Longitud promedio", f"{longitud_h:.3f}", f"{longitud_s:.3f}"))
    tabla.insert("", tk.END, values=("Eficiencia", f"{efic_h:.3f}", f"{efic_s:.3f}"))
    tabla.pack(padx=10, pady=10)

# Esta función actualizará el estado de la aplicación cuando se modifique el contenido del Text
# Si se modifica el texto original ingresado, se deshabilitan algunos botones y se cierran las ventanas abiertas
def verificar_contenido(event=None):

    if archivo_cargado:
        return
        
    global codigos_huffman, codigos_shannon, codificado_shannon, codificado_huffman, ventana_texto_codificado, ventana_tabla_codigos, widget_huffman, widget_shannon, ventana_comp, ventana_grafico_frecuencias

    # Limpio las variables que guardan los símbolos y los códigos e inhabilito los botones
    codigos_huffman = None
    codigos_shannon = None
    codificado_shannon = None
    codificado_huffman = None
    if ventana_texto_codificado and ventana_texto_codificado.winfo_exists():
        ventana_texto_codificado.destroy()
    if ventana_tabla_codigos and ventana_tabla_codigos.winfo_exists():
        ventana_tabla_codigos.destroy()
    if widget_huffman:
        widget_huffman.destroy()
    if widget_shannon:
        widget_shannon.destroy()
    boton_ver_texto_codificado.config(state=tk.DISABLED)
    boton_tabla_codigos.config(state=tk.DISABLED)
    boton_decodificar.config(state=tk.DISABLED)
    if ventana_comp and ventana_comp.winfo_exists():
        ventana_comp.destroy()
    boton_comparar.config(state=tk.DISABLED)
    if ventana_grafico_frecuencias and ventana_grafico_frecuencias.winfo_exists():
        ventana_grafico_frecuencias.destroy()

# Función para manejar el KeyRelease del widget Text (el cuadro para escribir texto directamente)
def manejar_keyrelease(event=None):
    actualizar_estado_boton_texto(event)
    verificar_contenido(event)

# Función para salir de la interfaz
def salir():
    ventana.destroy()

# Crear ventana principal
ventana = tk.Tk()
ventana.title("Codificador")
ventana.state('zoomed')
ventana.config(bg="black")

archivo_cargado = False

# Cuadro de texto
text_widget = tk.Text(ventana, height=15, width=60, font=("Arial", 12))
text_widget.grid(row=0, column=0, padx=20, pady=20, sticky="nw", columnspan=2)
text_widget.bind("<KeyRelease>", manejar_keyrelease)
# -------------------------------------------------------------------------------
# Frame para los botones de cargar archivo y ver el texto codificado
frame_botones = tk.Frame(ventana, bg="black")
frame_botones.grid(row=1, column=0, columnspan=2, pady=(0, 20))

# Botón para cargar o quitar archivo
boton_cargar_archivo = tk.Button(frame_botones, text="Cargar archivo", command=manejar_archivo, font=("Arial", 11), fg="white", bg="darkblue", activebackground="white", bd="4", activeforeground="black", relief="sunken", highlightbackground="#333333")
boton_cargar_archivo.pack(side=tk.LEFT, padx=10)

# Botón para ver el texto codificado
boton_ver_texto_codificado = tk.Button(frame_botones, text="Ver texto codificado", command=ver_texto_codificado, state=tk.DISABLED, font=("Arial", 11), fg="white", bg="#333333", activebackground="#555555", bd="4", activeforeground="black", relief="sunken", highlightbackground="#333333")
boton_ver_texto_codificado.pack(side=tk.LEFT, padx=10) 
# -------------------------------------------------------------------------------
# Frame para el bloque de codificación
frame_codificacion = tk.Frame(ventana, bg="black")
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
boton_decodificar = tk.Button(ventana, text="DECODIFICAR", command=lambda: mostrar_opciones("decodificar"), state=tk.DISABLED, bg="#333333", fg="white", activebackground="#555555", activeforeground="white", relief="sunken", bd="4", height=2, width=20)
boton_decodificar.place(relx=1.0, rely=1.0, x=-915, y=-140, anchor="se")
# -------------------------------------------------------------------------------
# Botón de tabla de códigos
boton_tabla_codigos = tk.Button(ventana, text="Mostrar tabla de códigos", state=tk.DISABLED, command=mostrar_tabla_codigos, bg="#333333", fg="white", activebackground="#555555", activeforeground="white", bd="4", relief="sunken")
boton_tabla_codigos.place(relx=1.0, rely=0.0, x=-20, y=70, anchor="ne")

# Botón para mostrar el gráfico de frecuencias
boton_grafico_frecuencias = tk.Button(ventana, text="Ver gráfico de frecuencias", command=mostrar_grafico_frecuencias, bg="#333333", fg="white", cursor="hand2", activebackground="#555555", activeforeground="white", relief="sunken", bd="4")
boton_grafico_frecuencias.place(relx=1.0, rely=0.0, x=-20, y=20, anchor="ne")

# Botón para realizar la comparación
boton_comparar = tk.Button(ventana, text="Comparar Resultados de Huffman y Shannon-Fano", command=mostrar_comparacion, bg="#333333", fg="white", font=("Arial", 10, "bold"), activebackground="#555555", activeforeground="white", relief="sunken", bd="4", state=tk.DISABLED)
boton_comparar.place(relx=1.0, rely=1.0, x=-825, y=-50, anchor="se")

# Botón de salir de la aplicación
boton_salir = tk.Button(ventana, text="Salir", font=("Arial", 11), fg="white", bg="darkred", command=salir, bd="4", relief="sunken", highlightbackground="#333333")
boton_salir.place(relx=1.0, rely=1.0, x=-20, y=-20, anchor="se")

def main():
    ventana.mainloop()

if __name__ == "__main__":
        main()