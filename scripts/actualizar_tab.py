from woocommerce import API
import pandas as pd
from config import woo_url, consumer_key, consumer_secret

# Configura tu API de WooCommerce
wcapi = API(
    url=woo_url,
    consumer_key=consumer_key,
    consumer_secret=consumer_secret,
    version="wc/v3"
)

# Función para actualizar el producto con el enlace a la ficha
def actualizar_ficha_producto(product_id, enlace_ficha):
    # Obtener el producto
    response = wcapi.get(f"products/{product_id}")
    
    if response.status_code == 200:
        producto = response.json()
        
        # Buscar las pestañas personalizadas existentes
        custom_tabs = producto.get("meta_data", [])
        updated = False
                
        # Verificar y añadir la pestaña "Documentación"
        for tab in custom_tabs:
            if tab["key"] == "_woodmart_product_custom_tab_title":
                tab["value"] = "Documentación"
                updated = True
            if tab["key"] == "_woodmart_product_custom_tab_content":
                tab["value"] = f"<a href='{enlace_ficha}' target='_blank'>Ficha del Producto</a>"
                updated = True

        if not updated:
            custom_tabs.append({
                "key": "_woodmart_product_custom_tab_title",
                "value": "Documentación"
            })
            custom_tabs.append({
                "key": "_woodmart_product_custom_tab_content",
                "value": f"<a href='{enlace_ficha}' target='_blank'>Ficha del Producto</a>"
            })
            print(f"Pestaña Documentación creada para el producto {product_id}")


        # Actualizar el producto con la nueva pestaña si hay cambios
        update_response = wcapi.put(f"products/{product_id}", {
            "meta_data": custom_tabs
        })
        if update_response.status_code == 200:
            print(f"Pestaña Documentación actualizada para el producto {product_id}")
        else:
            print(f"Error al actualizar el producto {product_id}: {update_response.status_code}, {update_response.json()}")
    else:
        print(f"Producto {product_id} no encontrado. Código de estado: {response.status_code}")

