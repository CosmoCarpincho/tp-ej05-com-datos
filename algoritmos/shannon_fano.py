from collections import Counter

def calcular_frecuencias(texto):
    """Calcula la frecuencia de cada carácter en el texto"""
    frecuencias = Counter(texto)
    total = sum(frecuencias.values())
    return sorted([(char, freq / total) for char, freq in frecuencias.items()],
                  key=lambda x: x[1], reverse=True)

def dividir_simbolos(simbolos):
    """Divide la lista de símbolos en dos partes con suma de probabilidades lo más equilibrada posible"""
    total = sum(freq for _, freq in simbolos)
    acumulado = 0
    for i in range(len(simbolos)):
        acumulado += simbolos[i][1]
        if acumulado >= total / 2:
            return simbolos[:i+1], simbolos[i+1:]
    return simbolos, []

def asignar_codigos(simbolos, prefijo='', codigos=None):
    """Asigna códigos binarios a cada símbolo utilizando el algoritmo de Shannon-Fano"""
    if codigos is None:
        codigos = {}
    if len(simbolos) == 1:
        codigos[simbolos[0][0]] = prefijo or '0'
        return codigos
    izquierda, derecha = dividir_simbolos(simbolos)
    asignar_codigos(izquierda, prefijo + '0', codigos)
    asignar_codigos(derecha, prefijo + '1', codigos)
    return codigos

def codificar_shannon_fano(texto):
    """Devuelve el texto codificado y los códigos binarios por carácter"""
    simbolos = calcular_frecuencias(texto)
    codigos = asignar_codigos(simbolos)
    texto_codificado = ''.join(codigos[char] for char in texto)
    return texto_codificado, codigos

def decodificar_shannon_fano(texto_codificado, codigos):
    """Decodifica el texto binario utilizando los códigos de Shannon-Fano"""
    codigos_invertidos = {v: k for k, v in codigos.items()}
    codigo_actual = ''
    texto_decodificado = ''
    for bit in texto_codificado:
        codigo_actual += bit
        if codigo_actual in codigos_invertidos:
            texto_decodificado += codigos_invertidos[codigo_actual]
            codigo_actual = ''
    return texto_decodificado
