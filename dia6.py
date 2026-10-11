import re
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urljoin

URL_PAGINA = "https://books.toscrape.com/catalogue/page-{}.html"
PAGINAS = 2      # para probar. El sitio tiene 50.
PAUSA = 0.5      # segundos entre pedidos, para no saturar el sitio

ESTRELLAS = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}


def descargar(url):
    """Descarga una página. Reintenta 3 veces. Devuelve la 'sopa' o None."""
    for intento in range(1, 4):
        try:
            r = requests.get(url, timeout=10)
            r.raise_for_status()      # lanza error si el código no es 2xx
            r.encoding = "utf-8"
            return BeautifulSoup(r.text, "html.parser")
        except requests.RequestException as e:
            print(f"  Intento {intento} falló en {url}: {e}")
            time.sleep(2)
    return None


def obtener_detalle(url_libro):
    """Entra a la página del libro y devuelve (stock, categoria)."""
    sopa = descargar(url_libro)
    if sopa is None:
        return None, None
    texto = sopa.select_one("p.availability").text   # "In stock (19 available)"
    numero = re.search(r"\d+", texto)                 # buscamos los dígitos
    stock = int(numero.group()) if numero else 0
    # Migas de pan: Home > Books > Categoría > Título
    links = sopa.select("ul.breadcrumb li a")
    categoria = links[2].get_text(strip=True) if len(links) >= 3 else None
    return stock, categoria


libros = []

for n in range(1, PAGINAS + 1):
    url = URL_PAGINA.format(n)
    print(f"Página {n}...")
    sopa = descargar(url)
    if sopa is None:
        print(f"  Salteo la página {n}")
        continue

    for item in sopa.select("article.product_pod"):
        titulo = item.h3.a["title"]
        precio = float(item.select_one("p.price_color").text.replace("£", ""))
        clase = item.select_one("p.star-rating")["class"][1]

        # urljoin arma la URL completa del libro a partir del enlace relativo
        url_libro = urljoin(url, item.h3.a["href"])
        stock, categoria = obtener_detalle(url_libro)

        libros.append({
            "titulo": titulo,
            "precio": precio,
            "calificacion": ESTRELLAS[clase],
            "stock": stock,
            "categoria": categoria,
        })
        time.sleep(PAUSA)

tabla = pd.DataFrame(libros).sort_values("precio")
print(tabla["categoria"].value_counts())
tabla.to_excel("libros.xlsx", index=False)
print(f"Listo: {len(tabla)} libros guardados en libros.xlsx")
