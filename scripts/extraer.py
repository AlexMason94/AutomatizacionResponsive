import pandas as pd
import os
import re

# Crea el directorio data si no existe
directorio_data = 'data_nueva'
if not os.path.exists(directorio_data):
    os.makedirs(directorio_data)

# Ruta al archivo Excel
archivo_excel = 'C:/Users/mason/OneDrive/Documentos/Trabajo pasantias/Scripts/progresivas/docs/02. Formulario de control de postacion ODN alborada 10_02.xlsx'

# Carga el archivo de Excel
xls = pd.ExcelFile(archivo_excel)

# Lista para almacenar los datos extraídos
datos = []

# Expresión regular para validar datos numéricos o '-'
patron_numerico = re.compile(r'^-?\d*\.?\d*$')

# Itera sobre cada hoja del archivo Excel que comience con "R-" y no sea "R-1.1"
# Itera sobre cada hoja del archivo Excel que comience con "R-" y no sea "R-1.1"
for nombre_hoja in xls.sheet_names:
    if nombre_hoja.startswith("R-") or nombre_hoja != "R-1.1":
        df = pd.read_excel(xls, sheet_name=nombre_hoja, header=None, skiprows=3)
        
        # Asegurarse de que el DataFrame tenga al menos 42 columnas
        if df.shape[1] > 42:
            for _, fila in df.iterrows():
                # Extrae el número de poste y verifica si es un número válido
                valor_numero_poste = str(fila[1]).strip()
                if patron_numerico.match(valor_numero_poste):
                    numero_poste = valor_numero_poste
                else:
                    continue  # Salta esta fila si el número de poste no es válido
                
                # Depura los datos de longitud
                longitudes = []
                for indice in [41, 42]:
                    valor = str(fila[indice])
                    if patron_numerico.match(valor) or valor == '-':
                        longitudes.append(valor)
                    else:
                        longitudes.append('')  # Asume '-' si el dato no es válido o no está presente
                
                datos.append([numero_poste] + longitudes)

# Escribe los datos en un archivo de texto dentro del directorio 'data_nueva'
ruta_archivo_salida = os.path.join(directorio_data, 'datos_postes_nuevos.txt')
with open(ruta_archivo_salida, 'w') as archivo:
    archivo.write("Numero poste, Longitud 1, Longitud 2\n")
    for fila in datos:
        archivo.write(', '.join(fila) + '\n')

print(f"Datos extraídos y escritos en '{ruta_archivo_salida}'")
