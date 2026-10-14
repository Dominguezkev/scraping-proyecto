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
   `git clone https://github.com/Dominguezkev/scraping-proyecto.git`
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
Listo: 40 libros en catalogo.xlsx (el tiempo depende de la conexión)
```

Después abra `catalogo.xlsx`: la hoja `Resumen` trae los totales
y la hoja `Catalogo` el listado completo.

## Ejecución en un servidor VPS

1. Instale Python y venv (Ubuntu/Debian):
   `sudo apt update && sudo apt install -y python3 python3-venv`
   Verifique con `python3 --version`.
2. Clone el repo e instale las dependencias:
   `git clone https://github.com/Dominguezkev/scraping-proyecto.git ~/scraping-proyecto`
   `cd ~/scraping-proyecto`
   `python3 -m venv venv`
   `venv/bin/pip install requests beautifulsoup4 pandas openpyxl`
3. Pruebe con una página:
   `venv/bin/python scraper.py --paginas 1 --salida catalogo.xlsx`
   Tiene que terminar con `Listo: 20 libros en catalogo.xlsx ...`.
4. Programe una ejecución diaria a las 8:00 con cron:
   `crontab -e` y agregue esta línea:
   `0 8 * * * cd ~/scraping-proyecto && ./venv/bin/python scraper.py --paginas 50 >> ~/scraping-proyecto/cron.log 2>&1`
   Verifique con `crontab -l` y revise `cron.log` al día siguiente.
   Nota: cron usa un entorno mínimo, por eso se usa la ruta del
   Python del venv en vez de activar el entorno con `source`.

## Buenas prácticas

- El programa espera los segundos de `--pausa` entre pedidos para no saturar el sitio.
- Es un sitio de prueba. En sitios reales, revise el archivo `robots.txt`
  y los términos de uso antes de scrapear.
