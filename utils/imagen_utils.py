from PIL import Image
import os

def convertir_a_grises_y_mostrar(nombre_archivo, carpeta="image"):
    ruta_original = os.path.join(carpeta, nombre_archivo)
    ruta_gris = os.path.join(carpeta, nombre_archivo.replace(".png", "_gris.png"))

    imagen_color = Image.open(ruta_original)
    imagen_gris = imagen_color.convert("L")
    imagen_gris.save(ruta_gris)
    print(f"Imagen guardada en escala de grises: {ruta_gris}")

    # Mostrar mapa de bits
    pixeles = list(imagen_gris.getdata())
    ancho, alto = imagen_gris.size
    matriz_pixeles = [pixeles[i * ancho:(i + 1) * ancho] for i in range(alto)]

    print(f"\nMapa de bits (grises) para {nombre_archivo}:")
    for fila in matriz_pixeles:
        print(fila)

    return ruta_gris, ancho, alto

def cargar_pixeles_como_texto(path_imagen):
    imagen = Image.open(path_imagen).convert("L")
    pixels = list(imagen.getdata())
    ancho, alto = imagen.size
    texto = ''.join(chr(p) for p in pixels)
    return texto, ancho, alto

def reconstruir_imagen_desde_texto(texto, ancho, alto, path_salida):
    pixels = [ord(c) for c in texto]
    imagen = Image.new("L", (ancho, alto))
    imagen.putdata(pixels)
    imagen.save(path_salida)
