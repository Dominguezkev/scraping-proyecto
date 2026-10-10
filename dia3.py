import requests
from bs4 import BeautifulSoup

r = requests.get("https://books.toscrape.com", timeout=10)
r.encoding = "utf-8"  # le decimos cómo leer los caracteres
sopa = BeautifulSoup(r.text, "html.parser")

# Buscamos TODOS los libros de la página
libros = sopa.select("article.product_pod")
print(f"Encontré {len(libros)} libros")

# Recorremos los 20 libros y mostramos título y precio de cada uno
for libro in libros:
    # El título está en el atributo "title" del enlace dentro del h3
    titulo = libro.h3.a["title"]

    # El precio está en un <p> con la clase price_color
    precio = libro.select_one("p.price_color").text

    print("Título:", titulo)
    print("Precio:", precio)