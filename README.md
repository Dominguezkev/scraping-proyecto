# Comparador de precios de librería

Programa que compara precios y stock del catálogo de la competencia
(`books.toscrape.com`, sitio de prueba) y genera un Excel prolijo
con un resumen arriba.

## Qué recibe el cliente

Un archivo Excel (por defecto `catalogo.xlsx`) con 2 hojas:

- **Resumen**: cantidad de libros, precio promedio/mínimo/máximo,
  calificación promedio, libros sin categoría real, filas con datos
  faltantes (y precio promedio en ARS si se pasa cotización).
- **Catalogo**: una fila por libro con `titulo`, `precio_gbp`,
  `calificacion`, `stock`, `categoria`, `url`
  (y `precio_ars` si se pasa cotización).

## Requisitos

- Python 3.10 o superior.
- Conexión a internet.

## Instalación (paso a paso)

1. Descargue o clone este proyecto y entre a la carpeta:
   `cd scraping-proyecto`
2. Cree un entorno virtual (recomendado):
   `python3 -m venv venv`
3. Actívelo:
   `source venv/bin/activate` (Linux/Mac) o
   `venv\Scripts\activate` (Windows).
4. Instale las dependencias:
   `pip install requests beautifulsoup4 pandas openpyxl`

## Uso

Ejemplo básico (2 páginas de prueba):

```bash
python scraper.py --paginas 2 --salida catalogo.xlsx
```

Ejemplo con precios en pesos (cotización de la libra):

```bash
python scraper.py --paginas 2 --cotizacion 1500 --salida catalogo.xlsx
```

Opciones:

- `--paginas`: cuántas páginas traer (máximo 50). Empiece con 2.
- `--pausa`: segundos de espera entre pedidos (por defecto 0.5).
- `--salida`: nombre del Excel de salida.
- `--cotizacion`: número para calcular `precio_ars = precio_gbp * cotizacion`.
  Si no se pasa, no se crea esa columna.

## Ejemplo de salida

```text
Página 1/2...
Página 2/2...
  categoria
Fiction         15
Poetry          10
...
Listo: 40 libros en catalogo.xlsx (45 s)
```

## Buenas prácticas

- El programa espera `PAUSA` segundos entre pedidos para no saturar el sitio.
- Es un sitio de prueba. En sitios reales, revise el archivo `robots.txt`
  y los términos de uso antes de scrapear.
