from algoritmos import (
    codificar_huffman, decodificar_huffman,
    codificar_shannon_fano, decodificar_shannon_fano
)

def menu():
    while True:
        print("\n--- Menú de Compresión ---")
        print("1. Ingresar texto para codificar (Huffman)")
        print("2. Ingresar texto para codificar (Shannon-Fano)")
        print("3. Comprimir archivo de texto (Huffman)")
        print("4. Comprimir archivo de texto (Shannon-Fano)")
        print("5. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            texto = input("Ingrese el texto a codificar: ")
            codificado, codigos = codificar_huffman(texto)
            decodificado = decodificar_huffman(codificado, codigos)
            print(f"\nTexto codificado (Huffman):\n{codificado}")
            print(f"\nTexto decodificado:\n{decodificado}")
            print(f"\nCódigos asignados:\n{codigos}")

        elif opcion == "2":
            texto = input("Ingrese el texto a codificar: ")
            codificado, codigos = codificar_shannon_fano(texto)
            decodificado = decodificar_shannon_fano(codificado, codigos)
            print(f"\nTexto codificado (Shannon-Fano):\n{codificado}")
            print(f"\nTexto decodificado:\n{decodificado}")
            print(f"\nCódigos asignados:\n{codigos}")

        elif opcion == "3":
            ruta = input("Ingrese la ruta del archivo de texto: ")
            try:
                with open(ruta, "r", encoding="utf-8") as archivo:
                    texto = archivo.read()
                codificado, codigos = codificar_huffman(texto)
                decodificado = decodificar_huffman(codificado, codigos)
                print(f"\nArchivo codificado (Huffman, primeros 500 bits):\n{codificado[:500]}")
                print(f"\nTexto decodificado:\n{decodificado[:500]}")
                print(f"\nCódigos asignados:\n{codigos}")
            except FileNotFoundError:
                print("Archivo no encontrado. Intente nuevamente.")
            except Exception as e:
                print(f"Error al leer el archivo: {e}")

        elif opcion == "4":
            ruta = input("Ingrese la ruta del archivo de texto: ")
            try:
                with open(ruta, "r", encoding="utf-8") as archivo:
                    texto = archivo.read()
                codificado, codigos = codificar_shannon_fano(texto)
                decodificado = decodificar_shannon_fano(codificado, codigos)
                print(f"\nArchivo codificado (Shannon-Fano, primeros 500 bits):\n{codificado[:500]}")
                print(f"\nTexto decodificado:\n{decodificado[:500]}")
                print(f"\nCódigos asignados:\n{codigos}")
            except FileNotFoundError:
                print("Archivo no encontrado. Intente nuevamente.")
            except Exception as e:
                print(f"Error al leer el archivo: {e}")

        elif opcion == "5":
            print("Saliendo...")
            break

        else:
            print("Opción inválida. Intente nuevamente.")

if __name__ == "__main__":
    menu()
