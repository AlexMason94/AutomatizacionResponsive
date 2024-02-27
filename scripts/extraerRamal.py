import pandas as pd
import os

# Crea el directorio data si no existe
directorio_data = 'data'
if not os.path.exists(directorio_data):
    os.makedirs(directorio_data)

# Ruta al archivo Excel y nombre de la hoja de interés
archivo_excel = 'C:/Users/mason/OneDrive/Documentos/Trabajo pasantias/Scripts/progresivas/docs/02. Formulario de control de postacion ODN alborada 10_02.xlsx'
nombre_hoja = 'R-1.1'

# Intenta leer la hoja especificada
try:
    # Lee la hoja sin asumir encabezados; ajusta 'skiprows' según sea necesario
    df = pd.read_excel(archivo_excel, sheet_name=nombre_hoja, header=None, skiprows=3)  # Ajusta 'skiprows' según sea necesario
    
    # Asumiendo que has identificado las columnas por inspección
    indice_numero_poste = 1  # Ajusta esto al índice correcto de la columna 'N° Poste'
    indice_longitud_fo_1 = 41 # Ajusta esto al índice correcto de la primera columna de longitud
    indice_longitud_fo_2 =  42 # Ajusta esto al índice correcto de la segunda columna de longitud
    # Filtra las columnas de interés
    

    # Escribe los datos en un archivo de texto dentro del directorio 'data'
    ruta_archivo_salida = os.path.join(directorio_data, 'datos_postes.txt')
    with open(ruta_archivo_salida, 'w') as archivo:
        for _, fila in df.iterrows():
            numero_poste = fila[indice_numero_poste]
            longitud_fo_1 = fila[indice_longitud_fo_1]
            longitud_fo_2 = fila[indice_longitud_fo_2]
            # Escribe el número de poste seguido de las dos longitudes separadas por comas
            archivo.write(f'{numero_poste}, {longitud_fo_1}, {longitud_fo_2}\n')

    print(f"Datos extraídos y escritos en '{ruta_archivo_salida}'")

except Exception as e:
    print(f"Error al leer el archivo Excel: {e}")
