import os
import requests
from bs4 import BeautifulSoup
import json
import urllib3

# Suprimir advertencias de SSL
def get_images(url):
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    # Crear el directorio para guardar las imágenes si no existe
    if not os.path.exists('images'):
        os.makedirs('images')

    # Solicitud HTTP
    res = requests.get(url, verify=False)
    res.raise_for_status()  # Verificar si la solicitud fue exitosa

    # Parsear el contenido HTML
    soup = BeautifulSoup(res.text, 'html.parser')

    # Obtener todas las etiquetas img
    results = soup.find_all('img')

    array = []

    for result in results:
        src = result.get('src', '')
        if src and src.startswith(('http://', 'https://')):
            try:
                # Descargar las imágenes
                response = requests.get(src, verify=False)
                response.raise_for_status()
                # Guardar la imagen
                image_name = src.split('/')[-1]
                with open(os.path.join('images', image_name), 'wb') as f:
                    f.write(response.content)
                array.append(src)
            except requests.RequestException as e:
                print(f"Error al acceder a {src}: {e}")
            except Exception as e:
                print(f"Error al procesar {src}: {e}")

    # Guardar el array en un archivo JSON
    with open('images.json', 'w') as f:
        json.dump(array, f)
        print("""Imágenes descargadas con éxito, puede ver el archivo images.json para ver las imagenes 
              descargadas.
              Luego puede ver el directorio images para ver las imagenes descargadas.
              """)

