from collections import Counter

def calcular_probabilidad(frecuencias):
    total = sum(frecuencias.values())
    return sorted([(char, freq / total) for char, freq in frecuencias.items()],
                  key=lambda x: x[1], reverse=True)

def dividir_simbolos(simbolos):
    """Divide la lista de símbolos en dos partes con suma de probabilidades lo más equilibrada posible"""
    total = sum(freq for _, freq in simbolos)
    mitad = total / 2
    mejor_id = 0
    mejor_diferencia = float('inf')
    acumulado = 0

    for i in range(len(simbolos) - 1):  # evitar que una parte quede vacía
        acumulado += simbolos[i][1]
        diferencia = abs(mitad - acumulado)
        if diferencia < mejor_diferencia:
            mejor_diferencia = diferencia
            mejor_id = i
        else:
            # una vez que empieza a empeorar la diferencia, se corta
            break

    return simbolos[:mejor_id + 1], simbolos[mejor_id + 1:]


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
    frecuencia_simbolos = Counter(texto)
    prob_simbolos = calcular_probabilidad(frecuencia_simbolos)
    codigos = asignar_codigos(prob_simbolos)
    texto_codificado = ''.join(codigos[char] for char in texto)
    return texto_codificado, codigos, frecuencia_simbolos

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
