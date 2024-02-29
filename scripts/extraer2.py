import pandas as pd
import os
import re

# Crea el directorio data si no existe
directorio_data = 'data_nueva'
if not os.path.exists(directorio_data):
    os.makedirs(directorio_data)

# Ruta al archivo Excel
archivo_excel = 'C:/Users/mason/OneDrive/Documentos/Trabajo pasantias/Scripts/progresivas/docs/Copia de 02.Planilla de tendido de postacion y ferreteria OLT Villa Busch 070224.xlsx'

# Carga el archivo de Excel
xls = pd.ExcelFile(archivo_excel)

# Lista para almacenar los datos extraídos
datos = []

# Expresión regular para validar datos numéricos o '-'
patron_numerico = re.compile(r'^-?\d*\.?\d*$')

for nombre_hoja in xls.sheet_names:
    if nombre_hoja.startswith("R-") and nombre_hoja != "R-1.1":
        df = pd.read_excel(xls, sheet_name=nombre_hoja, header=None, skiprows=3)
        
        if df.shape[1] > 42:
            for _, fila in df.iterrows():
                valor_numero_poste = str(fila[1]).strip()
                if patron_numerico.match(valor_numero_poste):
                    numero_poste = valor_numero_poste
                else:
                    continue
                
                longitudes = []
                for indice in [41, 42]:  # Ajuste en los índices según tu estructura de datos
                    valor = fila[indice]
                    if pd.notnull(valor) and (isinstance(valor, int) or isinstance(valor, float)):
                        valor = int(valor) if valor.is_integer() else valor  # Convertir a int si es posible
                        longitudes.append(str(valor))
                    elif valor == ' ':
                        longitudes.append(valor)
                
                               # Comprobar si las longitudes son iguales y tomar solo una si es el caso
                if len(longitudes) == 2 and longitudes[0] == longitudes[1]:
                    longitudes = [longitudes[0]]

                datos.append([numero_poste] + longitudes)

# Escribe los datos en un archivo de texto dentro del directorio 'data_nueva'
ruta_archivo_salida = os.path.join(directorio_data, 'datos_postes_nuevos.txt')
with open(ruta_archivo_salida, 'w') as archivo:
    archivo.write("Numero poste, Longitud 1, Longitud 2\n")
    for fila in datos:
        archivo.write(', '.join(fila) + '\n')

print(f"Datos extraídos y escritos en '{ruta_archivo_salida}'")
