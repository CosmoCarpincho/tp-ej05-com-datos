import os
from algoritmos_nuevos import (
    cargar_datos_simbolos,
    codificar_shannon_fano,
    codificar_huffman,
    comparar_codificaciones,
    obtener_codigos_ordenados,
    decodificar_shannon_fano,
    decodificar_huffman,
    guardar_codigos_codificacion,
    cargar_codigos_codificacion
)

# ====== EJEMPLO DE USO ======
texto = "EL CENTRO DE ESTUDIOS DESARROLLO Y TERRITORIO Y LA FACULTAD REGIONAL LA PLATA - UNIVERSIDAD TECNOLÓGICA NACIONAL, DE COMÚN ACUERDO, SUSCRIBEN ESTA CARTA DE INTENCIÓN, SOBRE LA BASE DE LAS CONSIDERACIONES Y PROPÓSITOS QUE SE EXPONEN A CONTINUACIÓN:"

# Paso 1: Analizar símbolos
datos_codificacion = cargar_datos_simbolos(texto)

# Paso 2: Aplicar codificaciones
codificar_shannon_fano(datos_codificacion)
codificar_huffman(datos_codificacion)

# Paso 3: Mostrar códigos generados (no ordenados)
print("===== CÓDIGOS GENERADOS =====\n")
for alg in datos_codificacion['Codificaciones']:
    print(f"Algoritmo: {alg}")
    codigos = datos_codificacion['Codificaciones'][alg]['Codigos']
    for char, code in codigos.items():
        print(f"  {repr(char)}: {code}")
    print()

# Paso 4: Comparar codificaciones
comparar_codificaciones(datos_codificacion, encoding='utf-8')

# Paso 5: Ver una muestra del texto codificado
print("\n===== MUESTRA DE CODIFICACIÓN =====")
for alg in datos_codificacion['Codificaciones']:
    texto_cod = datos_codificacion['Codificaciones'][alg]['TextoCodificado']
    print(f"{alg}: {texto_cod[:80]}...")  # Mostrar primeros 80 bits

# Paso 6: Mostrar resumen de comparación
print("\n===== MEJOR ALGORITMO SEGÚN COMPARACIÓN =====")
mejor_eficiencia = datos_codificacion["ResumenComparacion"]["MejorEficiencia"]
mejor_compresion = datos_codificacion["ResumenComparacion"]["MejorCompresion"]
print(f"  Mejor eficiencia: {mejor_eficiencia}")
print(f"  Mejor compresión (menos bits): {mejor_compresion}")

# Paso 7: Preparar códigos ordenados para la interfaz gráfica
codigos_huffman = obtener_codigos_ordenados(datos_codificacion, "Huffman")
codigos_shannon = obtener_codigos_ordenados(datos_codificacion, "Shannon-Fano")

# (Opcional) Mostrar ordenados
print("\n===== CÓDIGOS ORDENADOS (para GUI) =====")
print("Huffman:")
for char, code in codigos_huffman.items():
    print(f"  {repr(char)}: {code}")
print("Shannon-Fano:")
for char, code in codigos_shannon.items():
    print(f"  {repr(char)}: {code}")

import os

# Crear carpeta de salida si no existe
carpeta_salida = "salida_codificacion"
os.makedirs(carpeta_salida, exist_ok=True)

# Paso 8: Decodificar, verificar y mostrar el texto decodificado
print("\n===== DECODIFICACIÓN Y VERIFICACIÓN =====")

for alg in datos_codificacion['Codificaciones']:
    codigos = datos_codificacion['Codificaciones'][alg]['Codigos']
    texto_codificado = datos_codificacion['Codificaciones'][alg]['TextoCodificado']

    if alg == "Shannon-Fano":
        texto_decodificado = decodificar_shannon_fano(texto_codificado, codigos)
    elif alg == "Huffman":
        texto_decodificado = decodificar_huffman(texto_codificado, codigos)
    else:
        print(f"No hay decodificador implementado para {alg}")
        continue

    es_correcto = texto_decodificado == texto
    estado = "✅ Correcto" if es_correcto else "❌ Incorrecto"
    print(f"{alg}: {estado}")
    print(f"\nTexto decodificado ({alg}):\n")
    print(texto_decodificado)
    print("-" * 80)

# Paso 9: Guardar códigos como JSON y textos codificados como archivos planos
guardar_codigos_codificacion(datos_codificacion, "Huffman", os.path.join(carpeta_salida, "huffman_codificado.json"))
guardar_codigos_codificacion(datos_codificacion, "Shannon-Fano", os.path.join(carpeta_salida, "shannon_codificado.json"))

with open(os.path.join(carpeta_salida, "texto_comprimido.huffman"), "w", encoding="utf-8") as f:
    f.write(datos_codificacion["Codificaciones"]["Huffman"]["TextoCodificado"])

with open(os.path.join(carpeta_salida, "texto_comprimido.shannon"), "w", encoding="utf-8") as f:
    f.write(datos_codificacion["Codificaciones"]["Shannon-Fano"]["TextoCodificado"])

# Paso 10: Cargar códigos desde JSON y texto desde archivo .huffman/.shannon y decodificar
print("\n===== PRUEBA DE CARGA Y DECODIFICACIÓN DESDE JSON + TEXTO CODIFICADO =====")

rutas = [
    (
        os.path.join(carpeta_salida, "huffman_codificado.json"),
        os.path.join(carpeta_salida, "texto_comprimido.huffman"),
        decodificar_huffman
    ),
    (
        os.path.join(carpeta_salida, "shannon_codificado.json"),
        os.path.join(carpeta_salida, "texto_comprimido.shannon"),
        decodificar_shannon_fano
    ),
]

for archivo_json, archivo_texto, funcion_decodificar in rutas:
    datos = cargar_codigos_codificacion(archivo_json)
    algoritmo = datos["Algoritmo"]
    codigos = datos["Codigos"]

    with open(archivo_texto, "r", encoding="utf-8") as f:
        texto_codificado = f.read()

    texto_decodificado = funcion_decodificar(texto_codificado, codigos)

    print(f"\n{algoritmo} (cargado desde JSON + texto):")
    print(texto_decodificado)
    print("-" * 80)
