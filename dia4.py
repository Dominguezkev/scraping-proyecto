import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd

URL = "https://books.toscrape.com"

r = requests.get(URL, timeout=30)
r.encoding = "utf-8"  # para que el símbolo £ salga bien
sopa = BeautifulSoup(r.text, "html.parser")

# Traducimos la calificación de texto a número
ESTRELLAS = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}

libros = []  # lista de diccionarios: cada uno es una fila

for item in sopa.select("article.product_pod"):
    titulo = item.h3.a["title"]

    # Sacamos el £ y convertimos el precio a número
    precio_texto = item.select_one("p.price_color").text
    precio = float(precio_texto.replace("£", ""))

    # La clase es ["star-rating", "Three"]: tomamos la segunda
    clase_estrellas = item.select_one("p.star-rating")["class"][1]
    calificacion = ESTRELLAS[clase_estrellas]

    # La disponibilidad está en la página de cada libro: entramos al detalle
    href = item.h3.a["href"]
    url_libro = urljoin(URL + "/", href)
    rd = requests.get(url_libro, timeout=30)
    rd.encoding = "utf-8"
    sopa_detalle = BeautifulSoup(rd.text, "html.parser")
    disponibilidad = sopa_detalle.select_one("p.instock.availability").get_text(strip=True)

    libros.append({
        "titulo": titulo,
        "precio": precio,
        "calificacion": calificacion,
        "disponibilidad": disponibilidad,
    })

# Armamos la tabla, ordenamos por precio y guardamos en Excel
tabla = pd.DataFrame(libros)
tabla = tabla.sort_values("precio")
tabla.to_excel("libros.xlsx", index=False)

print(f"Listo: {len(tabla)} libros guardados en libros.xlsx")