import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import time

def buscar_en_lamudi(caracteristicas):
    # Inicializar navegador
    options = uc.ChromeOptions()
    #options.add_argument("--headless")  # Opcional: para que no se abra el navegador
    browser = uc.Chrome(options=options)

    # Construir URL de búsqueda en base a ubicación
    base_url = "https://www.lamudi.com.mx/"
    ubicacion = caracteristicas["ubicacion"].replace(" ", "-")
    url_busqueda = f"{base_url}{ubicacion}/terreno/?sorting=desc-date"  # Ejemplo básico

    print(f"🔗 Abriendo URL: {url_busqueda}")
    browser.get(url_busqueda)
    time.sleep(5)  # Esperar a que cargue el contenido

    terrenos = []

    try:
        resultados = browser.find_elements(By.CSS_SELECTOR, ".ListingCell-AllInfo")
        for r in resultados:
            try:
                titulo = r.find_element(By.CSS_SELECTOR, "a").text
                precio = r.find_element(By.CSS_SELECTOR, ".PriceSection-FirstPrice").text
                link = r.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
                descripcion = r.text

                terrenos.append({
                    "titulo": titulo,
                    "precio": precio,
                    "descripcion": descripcion,
                    "link": link
                })
            except Exception:
                continue

    except Exception as e:
        print("⚠️ Error al procesar resultados:", e)
    finally:
        browser.quit()

    print(f"\n✅ Se encontraron {len(terrenos)} terrenos en Lamudi.\n")
    return terrenos

def pedir_datos_terreno():
    print("🔍 Ingreso de características del terreno que buscas:\n")

    try:
        min_m2 = int(input("Tamaño mínimo en m²: "))
        max_m2 = int(input("Tamaño máximo en m²: "))
        min_precio = int(input("Precio mínimo en pesos: "))
        max_precio = int(input("Precio máximo en pesos: "))
    except ValueError:
        print("⚠️ Por favor, ingresa solo números para tamaño y precio.")
        return None

    ubicacion = input("Ubicación deseada (ciudad o colonia): ").strip().lower()
    tipo = input("Tipo de terreno (urbano, rústico, comercial, etc.): ").strip().lower()

    caracteristicas = {
        "min_m2": min_m2,
        "max_m2": max_m2,
        "min_precio": min_precio,
        "max_precio": max_precio,
        "ubicacion": ubicacion,
        "tipo": tipo
    }

    print("\n✅ Características capturadas con éxito:")
    for k, v in caracteristicas.items():
        print(f"{k}: {v}")

    return caracteristicas

if __name__ == "__main__":
    datos_terreno = pedir_datos_terreno()
    if datos_terreno:
        resultados = buscar_en_lamudi(datos_terreno)
        for i, r in enumerate(resultados[:5], start=1):
            print(f"\n{i}. {r['titulo']}")
            print(f"   Precio: {r['precio']}")
            print(f"   Link: {r['link']}")

# Ejemplo de uso
if __name__ == "__main__":
    datos_terreno = pedir_datos_terreno()
