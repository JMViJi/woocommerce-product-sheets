import requests
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.graphics import renderPDF
from svglib.svglib import svg2rlg
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.colors import HexColor
from bs4 import BeautifulSoup
from PIL import Image
import os
from io import BytesIO

# Registrar la fuente Montserrat
pdfmetrics.registerFont(TTFont('Montserrat-Medium', 'fonts/Montserrat-Medium.ttf'))
pdfmetrics.registerFont(TTFont('Montserrat-Bold', 'fonts/Montserrat-Bold.ttf'))
pdfmetrics.registerFont(TTFont('Montserrat-Light', 'fonts/Montserrat-Light.ttf'))

def download_and_resize_image(image_url, output_path, max_size):
    response = requests.get(image_url)
    if response.status_code == 200:
        img = Image.open(BytesIO(response.content))
        larger_size = (max_size[0] * 3, max_size[1] * 3)  
        img.thumbnail(larger_size, Image.LANCZOS)  
        img.save(output_path, format="JPEG", quality=85)
        return output_path
    return None

def download_image(url, save_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, 'wb') as f:
            f.write(response.content)
        return save_path
    return None

def draw_table(c, data, y, col_widths, row_height, font_name, font_size, page_width):
    c.setFont(font_name, font_size)
    table_width = sum(col_widths)
    x = (page_width - table_width) / 2  # Calcular el x para centrar la tabla

    for row in data:
        for i, cell in enumerate(row):
            c.drawString(x + sum(col_widths[:i]), y, cell)
        y -= row_height

def clean_html(html_content, omit_first_paragraph=False):
    soup = BeautifulSoup(html_content, "html.parser")

    # Reemplazar listas con guiones
    for ul in soup.find_all('ul'):
        new_content = ''
        list_items = ul.find_all('li')
        for li in list_items:
            new_content += '- ' + li.text + '\n'
        ul.replace_with(BeautifulSoup(new_content, "html.parser"))

    paragraphs = soup.find_all('p')
    if omit_first_paragraph and paragraphs:
        paragraphs[0].decompose()

    text = "\n".join(p.get_text() for p in soup.find_all(text=True) if p.strip() != '')
    return text

def draw_text_with_spacing(c, text, x, y, width, font_name, font_size, line_spacing=14, paragraph_spacing=20):
    c.setFont(font_name, font_size)
    lines = text.split('\n')
    for line in lines:
        if line.startswith('- '):
            # Ajustar el espacio adicional para listas
            y -= paragraph_spacing
        if line.strip() == "":
            y -= paragraph_spacing  # Espacio adicional entre párrafos
        else:
            words = line.split()
            current_line = ""
            for word in words:
                if c.stringWidth(current_line + " " + word, font_name, font_size) <= width:
                    if current_line:
                        current_line += " " + word
                    else:
                        current_line = word
                else:
                    c.drawString(x, y, current_line)
                    current_line = word
                    y -= line_spacing
            if current_line:
                c.drawString(x, y, current_line)
                y -= line_spacing

def clean_html_long(html_content, omit_first_paragraph=False):
    soup = BeautifulSoup(html_content, "html.parser")

    # Reemplazar listas con guiones
    for ul in soup.find_all('ul'):
        new_content = ''
        list_items = ul.find_all('li')
        for li in list_items:
            new_content += '- ' + li.text + '\n'
        ul.replace_with(BeautifulSoup(new_content, "html.parser"))

    paragraphs = soup.find_all('p')
    if omit_first_paragraph and paragraphs:
        paragraphs[0].decompose()

    text = "\n\n".join(p.get_text(strip=True) for p in soup.find_all(['p', 'li']) if p.text.strip())
    return text

def draw_text_with_spacing_long(c, text, x, y, width, font_name, font_size, line_spacing=14, paragraph_spacing=20):
    c.setFont(font_name, font_size)
    paragraphs = text.split('\n\n')  # Separar texto por párrafos dobles

    for paragraph in paragraphs:
        lines = paragraph.split('\n')
        for line in lines:
            words = line.split()
            current_line = ""
            for word in words:
                if c.stringWidth(current_line + " " + word, font_name, font_size) <= width:
                    if current_line:
                        current_line += " " + word
                    else:
                        current_line = word
                else:
                    c.drawString(x, y, current_line)
                    current_line = word
                    y -= line_spacing
            if current_line:
                c.drawString(x, y, current_line)
                y -= line_spacing
        y -= paragraph_spacing  # Aplicar espacio entre párrafos después de cada párrafo

def create_product_pdf(data, template_svg_path):
    pdf_file = f"pdfs/{data['name'].replace(' ', '_')}.pdf"
    c = canvas.Canvas(pdf_file, pagesize=A4)
    width, height = A4

    drawing = svg2rlg(template_svg_path)
    renderPDF.draw(drawing, c, 0, 0)

    title_x = width - 50
    title_y = height - 60
    title_text = data['name']
    title_width = c.stringWidth(title_text, "Montserrat-Bold", 12)

    c.setFont("Montserrat-Bold", 12)
    c.setFillColor(HexColor('#333333'))  

    c.drawString(title_x - title_width, title_y, title_text)

    category_text = data['category']
    c.setFont("Montserrat-Light", 10)
    c.setFillColor(HexColor('#333333'))  
    category_width = c.stringWidth(category_text, "Montserrat-Light", 10)
    c.drawString(title_x - category_width, title_y - 15, category_text)

    c.setFont("Montserrat-Medium", 11)
    short_description = clean_html(data.get('short_description', ''), True)
    long_description = clean_html_long(data.get('description', ''))

    # Descargar y redimensionar la imagen
    size=(190, 190)
    images = eval(data.get('images', '[]'))
    if images:
        first_image_url = images[0]['src']
        image_path = download_and_resize_image(first_image_url, 'temp_image.jpg', size)
        if image_path:
            c.drawImage(image_path, 40, height - 290, width=size[0], height=size[1])  # Ajustar la posición y tamaño de la imagen
            os.remove(image_path)  # Eliminar la imagen temporal después de usarla

    draw_text_with_spacing(c, short_description, 250, height - 100, width - 300, "Montserrat-Medium", 11, 14, 5)
    draw_text_with_spacing_long(c, long_description, 40, height - 310, width - 100, "Montserrat-Medium", 11, 14, 10)

    # Dibujar la tabla de atributos
    attributes = eval(data.get('attributes', '[]'))  # Convertir la cadena de atributos en una lista de diccionarios
    table_data = [["Atributo", "Valor"]]  # Encabezados de la tabla
    for attr in attributes:
        name = attr['name']
        options = ', '.join(attr['options'])
        table_data.append([name, options])

    draw_table(c, table_data, height - 650, [140, 200], 20, "Montserrat-Medium", 10, width)

    c.showPage()
    c.save()

