from collections import Counter


texto01 = "EL CENTRO DE ESTUDIOS DESARROLLO Y TERRITORIO Y LA FACULTAD REGIONAL LA PLATA - UNIVERSIDAD TECNOLÓGICA NACIONAL, DE COMÚN ACUERDO, SUSCRIBEN ESTA CARTA DE INTENCIÓN, SOBRE LA BASE DE LAS CONSIDERACIONES Y PROPÓSITOS QUE SE EXPONEN A CONTINUACIÓN:"

# Frecuencia
cod = {
    'Codificacion': 'Shannon-Fano',
    'Simbolos': None,
}

def crear_codificacion_vacia():
    return {
    'Codificacion' : None,
    'CantSimbolos': None,
    'EntropiaTotal': None,
    'LongPromedioTotal': None,
    'CantBitsTotal': None,
    'Simbolos' :  None,
}

def cargar_datos_simbolo(simbolo, cantidad):
    return { simbolo : {
                'Cantidad' : cantidad,
                'Probabilidad' : None,
                'IMutua': None,
                'Entropia': None,
                'Codificacion': None,
                'LongPromedio': None,
                'CantBits': None,
                    },
            }



def frecuencia_simbolos(cod: dict, texto):
    cod['Simbolos'] = Counter(texto)
    return cod

def calcular_probabilidad(cod_frec_simbolos: dict):
    for s in cod_frec_simbolos['Simbolos'].keys():
        s['Frecuencia']
        



# def crear_codificacion(tipo, texto):
#     cod = {}
#     frecuencias_simbolos = frecuencia_simbolos(texto)
#     if tipo == 'Shannon-Fano':
#         cod = 

# Ejemplo de datosShannon - Fano
cod_ppt = {
    'Codificación' : 'Shannon-Fano',
    'Simbolos' : {
        'A' : {
            'Frecuencia' : 15,
            'CodASCII': '00',
            'Mutua': 1.3777,
            'EntropiaMensaje': 0.52,
            'BitsMensaje': 30,
            'Prob': 0.3846,
            'LongPromedio': 0.7692
        },
    }
}

# Como en la hoja de calculo
cod_hc = {
    'Codificacion' : 'Shannon-Fano',
    'CantSimbolos': 247,
    'EntropiaTotal': 4.07,
    'LongPromedioTotal': 4.11,
    'CantBitsTotal': 1017,
    'Simbolos' :  {
        ' ' : {
            'Total' : 37,
            # 'Porcentaje' : 14.979757, # de mas es lo mismo que prob
            'Probabilidad' : 0.1498,
            #'1/Probabilidad': 6.67,
            'IMutua': 2.7389,
            'Entropia': 0.410,
            'Codificacion': '000',
            'LongPromedio': 0.44,
            'CantBits': 111,
        },
    },
}

print(frecuencia_simbolos(texto01))