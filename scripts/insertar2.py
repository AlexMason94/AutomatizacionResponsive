import xml.etree.ElementTree as ET
import os
import re

def normalizar_nombre_poste(nombre_poste):
    """Extrae y normaliza el nombre del poste para comparación."""
    match = re.match(r'(P(Ma|Me|C|M)?-\d+)', nombre_poste)
    if match:
        return match.group(1)  # Retorna la parte normalizada del nombre
    else:
        return None  # O manejar de otra manera

def leer_datos(archivo_datos):
    datos_postes = {}
    with open(archivo_datos, 'r', encoding='ISO-8859-1') as archivo:
        for linea in archivo:
            partes = linea.strip().split(',')
            if partes[0].strip() == '' or partes[0].strip() == '':
                continue
            numero_poste = partes[0].strip()
            longitudes = [parte.strip() for parte in partes[1:] if parte.strip() != '']
            longitud_combinada = '-'.join(longitudes)  # Unir longitudes con ' / ' si hay más de una
            if numero_poste in datos_postes:
                datos_postes[numero_poste] += f" {longitud_combinada}" if longitud_combinada else ''
            else:
                datos_postes[numero_poste] = longitud_combinada
    return datos_postes


def leer_kml_y_extraer_datos(archivo_kml_existente):
    datos_leidos = []
    tree = ET.parse(archivo_kml_existente)
    root = tree.getroot()

    ns = {'kml': 'http://www.opengis.net/kml/2.2'}
    patron_poste = re.compile(r'P(Ma|Me|C|M)?-(\d+)')

    for placemark in root.findall('.//kml:Placemark', ns):
        nombre_poste_element = placemark.find('.//kml:name', ns)
        if nombre_poste_element is not None:
            nombre_poste = nombre_poste_element.text
            match = patron_poste.match(nombre_poste)
            if match:
                numero_poste = match.group(2)  # Convertir el número del poste a entero para ordenar
                datos_leidos.append((numero_poste, nombre_poste))
    #print(f"Datos leídos del KML: {datos_leidos}") 
    return datos_leidos

def combinar_datos_y_escribir_txt(datos_leidos, datos_postes, archivo_salida_txt):
    datos_ordenados = sorted(datos_leidos, key=lambda x: int(x[0]))

    with open(archivo_salida_txt, 'w') as archivo:
        archivo.write("Nombre del Placemark, Longitudes\n")
        for numero_poste, nombre_poste in datos_ordenados:
            longitudes = datos_postes.get(str(numero_poste), "Sin Longitud")
            archivo.write(f"{nombre_poste}, {longitudes}\n")

def actualizar_kml_con_datos(archivo_kml_existente, datos_postes, archivo_kml_salida):
    tree = ET.parse(archivo_kml_existente)
    root = tree.getroot()
    ns = {'kml': 'http://www.opengis.net/kml/2.2'}

    for placemark in root.findall('.//kml:Placemark', ns):
        nombre_poste_element = placemark.find('.//kml:name', ns)
        if nombre_poste_element is not None:
            nombre_poste_original = nombre_poste_element.text
            match = re.search(r'P(Ma|Me|C|M)?-(\d+)', nombre_poste_original)
            if match:
                numero_poste = match.group(2)
                # Verificar si el número de poste está en los datos y actualizar el nombre
                if numero_poste in datos_postes:
                    longitudes = datos_postes[numero_poste]
                    if '' in longitudes:  # Presencia de múltiples longitudes
                        nombre_poste_actualizado = f"{nombre_poste_original} {longitudes}"
                    else:  # Solo una longitud
                        nombre_poste_actualizado = f"{nombre_poste_original} {longitudes}"  # Ajusta según necesidad
                    nombre_poste_element.text = nombre_poste_actualizado
                    #print(f"Actualizando {nombre_poste_original} con {longitudes}")
                else:
                    print(f"No se encontraron datos para actualizar el poste {nombre_poste_original}")

    tree.write(archivo_kml_salida, encoding='utf-8', xml_declaration=True)

def imprimir_datos_leidos(archivo_datos):
    datos_postes = leer_datos(archivo_datos)
    for nombre_poste, longitudes in datos_postes.items():
        print(f"Poste: {nombre_poste} Longitudes: {longitudes}")

def escribir_resultados_txt(datos_postes, datos_leidos, archivo_resultados):
    with open(archivo_resultados, 'w') as archivo:
        archivo.write("Nombre del Placemark Actualizado\n")
        for numero_poste, nombre_poste in datos_leidos:
            if numero_poste in datos_postes:
                # Construir el nombre completo con longitudes
                nombre_completo = f"{nombre_poste} {datos_postes[numero_poste]}"
                archivo.write(f"{nombre_completo}\n")

def escribir_lectura_kml_a_txt(datos_leidos, archivo_salida_txt):
    # Ordenar los datos por el número del poste (primer elemento de la tupla)
    datos_ordenados = sorted(datos_leidos, key=lambda x: x[0])
    
    with open(archivo_salida_txt, 'w') as archivo:
        archivo.write("Número de Poste, Nombre del Placemark\n")
        for numero_poste, nombre_poste in datos_ordenados:
            archivo.write(f"{nombre_poste}\n")

def main():
    archivo_datos = 'data_nueva/datos_postes_nuevos.txt'
    archivo_kml_existente = 'C:/Users/mason/OneDrive/Documentos/Trabajo pasantias/Scripts/progresivas/docs/01. Diseño Final ODN ALBORADA 23-2-24.kml'
    archivo_kml_salida = 'data_nueva/postes_actualizados.kml'
    archivo_resultados_txt = 'data_nueva/resultados_modificaciones.txt'
    archivo_lectura_txt = 'data_nueva/lectura_kml.txt'
    # Llamar a la función con el path del archivo de datos
    
    imprimir_datos_leidos(archivo_datos)
    datos_postes = leer_datos(archivo_datos)
    datos_leidos = leer_kml_y_extraer_datos(archivo_kml_existente)

    actualizar_kml_con_datos(archivo_kml_existente, datos_postes, archivo_kml_salida)
    combinar_datos_y_escribir_txt(datos_leidos, datos_postes, archivo_resultados_txt)  # Asegúrate de definir correctamente esta función para reflejar la lógica de combinación deseada
    escribir_lectura_kml_a_txt(datos_leidos, archivo_lectura_txt)
    escribir_resultados_txt(datos_postes, datos_leidos, archivo_resultados_txt)

    print(f"Archivo KML actualizado generado en: {archivo_kml_salida}")
    print(f"Resultados de modificaciones escritos en: {archivo_resultados_txt}")
    print(f"Lectura del archivo KML escrita en: {archivo_lectura_txt}")

if __name__ == "__main__":
    main()

