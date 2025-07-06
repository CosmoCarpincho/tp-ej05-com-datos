from algoritmos_nuevos import (
    cargar_datos_simbolos,
    codificar_shannon_fano,
    codificar_huffman,
    comparar_codificaciones,
    obtener_codigos_ordenados,
    decodificar_shannon_fano,
    decodificar_huffman
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

