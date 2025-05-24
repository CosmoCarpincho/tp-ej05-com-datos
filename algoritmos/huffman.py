from .monticulo_minimo import MonticuloMinimo, Nodo
from collections import Counter

"""
Algoritmo de Huffman:

1. Contar la frecuencia de aparición de cada carácter en el texto.
2. Crear un nodo hoja para cada carácter con su frecuencia.
3. Insertar todos los nodos en un montículo mínimo (min-heap).
4. Mientras haya más de un nodo en el montículo:
    a. Extraer los dos nodos con menor frecuencia.
    b. Crear un nuevo nodo padre con la suma de las frecuencias de estos nodos.
    c. Asignar los nodos extraídos como hijos izquierdo y derecho del nodo padre.
    d. Insertar el nodo padre de nuevo en el montículo.
5. El nodo restante en el montículo es la raíz del árbol de Huffman.
6. Recorrer el árbol para asignar códigos binarios a cada carácter:
    - Asignar '0' al recorrer hacia la izquierda.
    - Asignar '1' al recorrer hacia la derecha.
7. Codificar el texto reemplazando cada carácter por su código binario asignado.
8. Decodificar el texto reconstruyendo los caracteres a partir de los códigos binarios y el árbol.

(Pág 145 libro)
"""
def construir_arbol_huffman(frecuencias_simbolos):

    monticulo = MonticuloMinimo() # es un arbol binario con dos restricciones
    # estructura: todos los niveles del árbol deben estar completos, a excepción del último que se completa desde izq
    # orden: el arbol debe estar ordenado por niveles asc o desc. En este caso es de orden mínimo. Padre menor que sus hijos.
    # Pagina del libro 187. LEER!!!

    # Crea un nodo por caracter y lo inserta en el montículo
    for caracter, frecuencia in frecuencias_simbolos.items():
        monticulo.insertar(Nodo(caracter, frecuencia))

    # Combina los nodos de menor frecuencia hasta construir el árbol completo
    # ESTE ES LA PARTE IMPORTANTE DEL ALGORITMO HUFFMAN
    
    while len(monticulo) > 1:
        nodo1 = monticulo.extraer_minimo()
        nodo2 = monticulo.extraer_minimo()
        nodo_combinado = Nodo(frecuencia=nodo1.frecuencia + nodo2.frecuencia)
        nodo_combinado.izquierda = nodo1
        nodo_combinado.derecha = nodo2
        monticulo.insertar(nodo_combinado)

    return monticulo.extraer_minimo() if len(monticulo) == 1 else None

# Parte 6 del algoritmo de huffman ->
def construir_codigos(raiz):
    # Recorre el árbol en profundidad para asignar códigos binarios a cada caracter
    codigos = {}
    def _construir_codigos(nodo, codigo_actual):
        if nodo is None:
            return
        if nodo.caracter is not None:
            codigos[nodo.caracter] = codigo_actual
        _construir_codigos(nodo.izquierda, codigo_actual + "0")
        _construir_codigos(nodo.derecha, codigo_actual + "1")

    _construir_codigos(raiz, "")
    return codigos

def codificar_huffman(texto):
     # Cuenta la frecuencia de cada caracter en el texto y devuelve un dic ej: {'a':5, 'b': 10}
    frecuencias_simbolos = Counter(texto)
    # Construye el árbol de Huffman y genera el texto codificado
    raiz = construir_arbol_huffman(frecuencias_simbolos)
    codigos = construir_codigos(raiz)
    texto_codificado = ''.join(codigos[caracter] for caracter in texto)
    return texto_codificado, codigos, frecuencias_simbolos

def decodificar_huffman(texto_codificado, codigos):
    # Decodifica el texto binario usando los códigos generados
    codigos_invertidos = {v: k for k, v in codigos.items()}
    codigo_actual = ""
    texto_decodificado = ""
    for bit in texto_codificado:
        codigo_actual += bit
        if codigo_actual in codigos_invertidos:
            texto_decodificado += codigos_invertidos[codigo_actual]
            codigo_actual = ""
    return texto_decodificado