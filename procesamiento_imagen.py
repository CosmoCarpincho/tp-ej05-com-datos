import os
from algoritmos_nuevos import (
    cargar_datos_simbolos,
    codificar_shannon_fano,
    codificar_huffman,
    decodificar_shannon_fano,
    decodificar_huffman
)
from utils.imagen_utils import (
    convertir_a_grises_y_mostrar,
    cargar_pixeles_como_texto,
    reconstruir_imagen_desde_texto
)


# Crear carpetas
os.makedirs("image", exist_ok=True)
os.makedirs("salida_codificacion_imagen", exist_ok=True)

# Imágenes a procesar
imagenes = ["gato01.png", "gato02.png"]

for imagen_nombre in imagenes:
    print(f"\n============================")
    print(f"Procesando {imagen_nombre}")
    print(f"============================")

    # Paso 1: Convertir a gris y mostrar matriz
    ruta_gris, ancho, alto = convertir_a_grises_y_mostrar(imagen_nombre)

    # Paso 2: Cargar como texto (píxeles a caracteres)
    texto, _, _ = cargar_pixeles_como_texto(ruta_gris)
    datos_codificacion = cargar_datos_simbolos(texto)

    # Paso 3: Codificar
    codificar_shannon_fano(datos_codificacion)
    codificar_huffman(datos_codificacion)

    # Paso 4: Verificar decodificación y reconstruir imagen
    print("\n===== VERIFICACIÓN DE DECODIFICACIÓN =====")
    for alg in datos_codificacion['Codificaciones']:
        codigos = datos_codificacion['Codificaciones'][alg]['Codigos']
        texto_codificado = datos_codificacion['Codificaciones'][alg]['TextoCodificado']

        if alg == "Shannon-Fano":
            texto_decodificado = decodificar_shannon_fano(texto_codificado, codigos)
        elif alg == "Huffman":
            texto_decodificado = decodificar_huffman(texto_codificado, codigos)
        else:
            continue

        es_correcto = texto_decodificado == texto
        estado = "✅ Correcto" if es_correcto else "❌ Incorrecto"
        print(f"{alg}: {estado}")

        salida_img = os.path.join(
            "salida_codificacion_imagen",
            f"{imagen_nombre.replace('.png', '')}_reconstruida_{alg}.png"
        )
        reconstruir_imagen_desde_texto(texto_decodificado, ancho, alto, salida_img)
        print(f"Imagen reconstruida guardada en: {salida_img}")