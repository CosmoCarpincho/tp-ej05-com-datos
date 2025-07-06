def comparar_codificaciones(datos_codificacion: dict, imprimir=True, encoding='utf-8'):
    """
    Compara codificaciones aplicadas y guarda métricas en el diccionario.
    También identifica el mejor algoritmo por eficiencia y por compresión.
    """

    texto_original = datos_codificacion['TextoOriginal']
    try:
        bits_originales = len(texto_original.encode(encoding)) * 8
    except UnicodeEncodeError:
        raise ValueError(f"El texto contiene caracteres que no se pueden representar en '{encoding}'.")

    comparaciones = {}
    mejor_eficiencia = -1
    mejor_eficiencia_alg = None

    menor_bits = float('inf')
    mejor_compresion_alg = None

    for nombre_alg, info in datos_codificacion["Codificaciones"].items():
        longitud_cod = info["LongitudPromedio"]
        eficiencia = info["Eficiencia"]
        bits_totales = info["CantidadBits"]
        tasa_compresion = bits_totales / bits_originales if bits_originales else 0

        comparaciones[nombre_alg] = {
            "LongitudPromedio": longitud_cod,
            "Eficiencia": eficiencia,
            "BitsTotales": bits_totales,
            "TasaCompresion": tasa_compresion,
            "BitsOriginales": bits_originales
        }

        if eficiencia > mejor_eficiencia:
            mejor_eficiencia = eficiencia
            mejor_eficiencia_alg = nombre_alg

        if bits_totales < menor_bits:
            menor_bits = bits_totales
            mejor_compresion_alg = nombre_alg

        if imprimir:
            print(f"\nAlgoritmo: {nombre_alg}")
            print(f"  Longitud promedio de código: {longitud_cod:.4f}")
            print(f"  Eficiencia: {eficiencia:.4f}")
            print(f"  Bits totales codificados: {bits_totales}")
            print(f"  Tasa de compresión: {tasa_compresion:.4f} ({tasa_compresion * 100:.2f}%)")
            print(f"  Bits originales ({encoding}): {bits_originales}")

    datos_codificacion['Comparaciones'] = comparaciones
    datos_codificacion['ResumenComparacion'] = {
        "MejorEficiencia": mejor_eficiencia_alg,
        "MejorCompresion": mejor_compresion_alg
    }

    if imprimir:
        print("\n===== MEJORES RESULTADOS =====")
        print(f"  Mejor eficiencia: {mejor_eficiencia_alg}")
        print(f"  Mejor compresión (menos bits): {mejor_compresion_alg}")

    return datos_codificacion


def obtener_codigos_ordenados(datos_codificacion: dict, algoritmo: str) -> dict:
    """
    Devuelve los códigos de un algoritmo ordenados por frecuencia descendente.
    Ideal para mostrarlos en una tabla de interfaz gráfica.
    
    Parámetros:
        datos_codificacion: dict con resultados de codificación
        algoritmo: 'Huffman' o 'Shannon-Fano'

    Retorna:
        dict {caracter: codigo}, ordenado por frecuencia descendente
    """
    if algoritmo not in datos_codificacion["Codificaciones"]:
        raise ValueError(f"Algoritmo '{algoritmo}' no encontrado en los resultados.")

    codigos = datos_codificacion["Codificaciones"][algoritmo]["Codigos"]
    simbolos_ordenados = sorted(
        datos_codificacion["ListaSimbolos"],
        key=lambda s: s["Cantidad"],
        reverse=True
    )

    codigos_ordenados = {}
    for simbolo in simbolos_ordenados:
        char = simbolo["Caracter"]
        if char in codigos:
            codigos_ordenados[char] = codigos[char]

    return codigos_ordenados
