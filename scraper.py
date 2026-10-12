import argparse
import re
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urljoin

URL_PAGINA = "https://books.toscrape.com/catalogue/page-{}.html"
ESTRELLAS = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}


def descargar(url):
    """Descarga una página con 3 reintentos. Devuelve la 'sopa' o None."""
    for intento in range(1, 4):
        try:
            r = requests.get(url, timeout=10)
            r.raise_for_status()
            r.encoding = "utf-8"
            return BeautifulSoup(r.text, "html.parser")
        except requests.RequestException as e:
            print(f"  Intento {intento} falló en {url}: {e}")
            time.sleep(2)
    return None


def extraer_detalle(url_libro):
    """Entra a la página del libro: devuelve (stock, categoria)."""
    sopa = descargar(url_libro)
    if sopa is None:
        return None, None
    texto = sopa.select_one("p.availability").text
    numero = re.search(r"\d+", texto)
    stock = int(numero.group()) if numero else 0
    categoria = sopa.select("ul.breadcrumb li")[2].text.strip()
    return stock, categoria


def extraer_libro(item, url_pagina):
    """Convierte un <article> del listado en un diccionario (una fila)."""
    url_libro = urljoin(url_pagina, item.h3.a["href"])
    stock, categoria = extraer_detalle(url_libro)
    clase = item.select_one("p.star-rating")["class"][1]
    return {
        "titulo": item.h3.a["title"],
        "precio_gbp": float(item.select_one("p.price_color").text.replace("£", "")),
        "calificacion": ESTRELLAS[clase],
        "stock": stock,
        "categoria": categoria,
        "url": url_libro,
    }


def scrapear(paginas, pausa):
    """Recorre las páginas y devuelve una lista de libros."""
    libros = []
    for n in range(1, paginas + 1):
        url = URL_PAGINA.format(n)
        print(f"Página {n}/{paginas}...")
        sopa = descargar(url)
        if sopa is None:
            print(f"  Salteo la página {n}")
            continue
        for item in sopa.select("article.product_pod"):
            libros.append(extraer_libro(item, url))
            time.sleep(pausa)
    return libros


def armar_resumen(tabla):
    """Tabla chica con los números clave para el cliente."""
    datos = {
        "Libros analizados": len(tabla),
        "Precio promedio (GBP)": round(tabla["precio_gbp"].mean(), 2),
        "Precio mínimo (GBP)": tabla["precio_gbp"].min(),
        "Precio máximo (GBP)": tabla["precio_gbp"].max(),
        "Calificación promedio": round(tabla["calificacion"].mean(), 2),
        "Sin categoría asignada": int((tabla["categoria"] == "Default").sum()),
        "Filas con datos faltantes": int(tabla.isna().any(axis=1).sum()),
    }
    return pd.DataFrame(list(datos.items()), columns=["Indicador", "Valor"])


def exportar(tabla, archivo):
    """Guarda el Excel con dos hojas: Resumen y Catalogo."""
    with pd.ExcelWriter(archivo) as writer:
        armar_resumen(tabla).to_excel(writer, sheet_name="Resumen", index=False)
        tabla.to_excel(writer, sheet_name="Catalogo", index=False)


def main():
    parser = argparse.ArgumentParser(description="Scraper de catálogo de libros")
    parser.add_argument("--paginas", type=int, default=2, help="cuántas páginas (máx. 50)")
    parser.add_argument("--pausa", type=float, default=0.5, help="segundos entre pedidos")
    parser.add_argument("--salida", default="catalogo.xlsx", help="nombre del Excel")
    args = parser.parse_args()

    inicio = time.time()
    libros = scrapear(args.paginas, args.pausa)
    if not libros:
        print("No se obtuvo ningún dato. Revisá tu conexión.")
        return

    tabla = pd.DataFrame(libros).sort_values("precio_gbp")
    exportar(tabla, args.salida)
    print(f"Listo: {len(tabla)} libros en {args.salida} ({time.time() - inicio:.0f} s)")


if __name__ == "__main__":
    main()