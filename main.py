import os
import csv
from scripts.subida_archivos import subir_archivo_wordpress
from scripts.actualizar_tab import actualizar_ficha_producto
from scripts.utils import create_product_pdf

# Rutas de archivos
CSV_FILE_PATH = 'data/products.csv'
TEMPLATE_SVG_PATH = 'templates/template.svg'
PDF_DIRECTORY = 'pdfs'

# Crear directorio para PDFs si no existe
if not os.path.exists(PDF_DIRECTORY):
    os.makedirs(PDF_DIRECTORY)

# Leer y procesar cada fila del archivo CSV
output_rows = []
prev_id = None

with open(CSV_FILE_PATH, mode='r', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=',')
    fieldnames = reader.fieldnames
    
    # Añadir nueva columna si falta
    if 'sheet_file' not in fieldnames:
        fieldnames.append('sheet_file')
    
    for row in reader:
        if row['id'] != prev_id:
            # Crear y subir PDF si es una nueva ID
            filename = f"{row['name'].replace(' ', '_')}.pdf"
            pdf_file_path = os.path.join(PDF_DIRECTORY, filename)
            create_product_pdf(row, TEMPLATE_SVG_PATH)
            media_url = subir_archivo_wordpress(pdf_file_path)
            actualizar_ficha_producto(row['id'], media_url)
            row['sheet_file'] = media_url
        else:
            # Evitar procesamiento duplicado para la misma ID
            row['sheet_file'] = ''
        prev_id = row['id']
        output_rows.append(row)

# Guardar el CSV actualizado con la nueva información
with open(CSV_FILE_PATH, mode='w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(output_rows)

