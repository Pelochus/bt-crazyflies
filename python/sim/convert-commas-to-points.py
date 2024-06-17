# Thanks to ChatGPT for doing this in case your numbers have commas instead of points
def convert_commas_to_points(input_file, output_file=None):
    # Abrir el archivo de entrada en modo lectura
    with open(input_file, 'r') as file:
        # Leer todo el contenido del archivo
        content = file.read()

    # Reemplazar comas por puntos
    modified_content = content.replace(',', '.')

    # Si se proporciona un archivo de salida, escribir el contenido modificado en él
    if output_file:
        with open(output_file, 'w') as file:
            file.write(modified_content)
        print(f"Se ha creado el archivo '{output_file}' con comas convertidas a puntos.")
    else:
        # Si no se proporciona un archivo de salida, imprimir el contenido modificado en consola
        print("Contenido con comas convertidas a puntos:")
        print(modified_content)

# Ejemplo de uso
input_file = 'log.txt'
output_file = 'log-new.txt'  # Opcional: si se desea guardar el resultado en otro archivo

convert_commas_to_points(input_file, output_file)

