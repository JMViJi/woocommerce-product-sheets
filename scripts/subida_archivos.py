import requests
from requests.auth import HTTPBasicAuth
from unidecode import unidecode
from config import wordpress_user, wordpress_password, wordpress_url

def normalizar_nombre(nombre):
    return unidecode(nombre)

def buscar_y_eliminar_archivo(file_name):
    # Normalizar el nombre del archivo
    file_name_normalizado = normalizar_nombre(file_name)

    # Crear una sesión HTTP para manejar la autenticación básica
    session = requests.Session()
    session.auth = HTTPBasicAuth(wordpress_user, wordpress_password)

    # Buscar el archivo por nombre (sin extensión)
    search_url = f"{wordpress_url}?search={file_name_normalizado}"
    response = session.get(search_url)

    if response.status_code == 200:
        media_items = response.json()
        for item in media_items:
            # Comparar sin extensión y normalizar
            if normalizar_nombre(item['title']['rendered']) == file_name_normalizado:
                delete_url = f"{wordpress_url}/{item['id']}"
                delete_response = session.delete(delete_url, params={'force': True})
                if delete_response.status_code == 200:
                    print(f"Archivo {file_name} eliminado con éxito")
                else:
                    print(f"Error al eliminar el archivo {file_name}: {delete_response.status_code}")
    else:
        print(f"Error al buscar el archivo {file_name}: {response.status_code}")

def subir_archivo_wordpress(file_path):
    # Crear una sesión HTTP para manejar la autenticación básica
    session = requests.Session()
    session.auth = HTTPBasicAuth(wordpress_user, wordpress_password)

    # Nombre del archivo sin extensión y normalizado
    file_name = file_path.split("/")[-1].rsplit('.', 1)[0]
    file_name_normalizado = normalizar_nombre(file_name)

    # Buscar y eliminar el archivo existente si lo hay
    buscar_y_eliminar_archivo(file_name_normalizado)

    # Subir el archivo
    with open(file_path, 'rb') as file:
        files = {
            'file': (f"{file_name}.pdf", file, 'application/pdf')
        }
        headers = {
            'Content-Disposition': f'attachment; filename={file_name}.pdf',
            'Content-Type': 'application/pdf'
        }
        response = session.post(wordpress_url, files=files, headers=headers)

    # Verificar la respuesta
    if response.status_code == 201:
        media_data = response.json()
        media_url = media_data['source_url']
        return media_url
    else:
        print("Error al subir el archivo:", response.status_code, response.json())
        return None
