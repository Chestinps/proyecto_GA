import requests
import json

# Define URLs
LISTADO_BUSES_URL = "https://www.red.cl/restservice_v2/rest/getservicios/all"
RUTAS_BUS_URL_TEMPLATE = "https://www.red.cl/restservice_v2/rest/conocerecorrido?codsint={bus_code}"

# Archivo final de salida para todas las rutas
OUTPUT_FILE = "rutas_buses.geojson"

# Función para obtener el listado de servicios de buses
def obtener_lista_buses():
    response = requests.get(LISTADO_BUSES_URL)
    if response.status_code == 200:
        return response.json()  # Retorna el listado en formato JSON
    else:
        print("Error al obtener el listado de buses:", response.status_code)
        return []

# Función para obtener la ruta de un bus específico
def obtener_ruta_bus(bus_code):
    url = RUTAS_BUS_URL_TEMPLATE.format(bus_code=bus_code)
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()  # Datos de la ruta en formato JSON
    else:
        print(f"Error al obtener la ruta del bus {bus_code}: {response.status_code}")
        return None

# Función principal para consolidar todas las rutas en un solo archivo geojson
def main():
    # Paso 1: Obtén la lista de buses
    lista_buses = obtener_lista_buses()
    
    # Inicializa la estructura de GeoJSON para el archivo consolidado
    geojson_data = {
        "type": "FeatureCollection",
        "features": []
    }
    
    # Paso 2: Para cada bus en la lista, obtén su ruta y agrégala al FeatureCollection
    for bus_code in lista_buses:
        ruta_data = obtener_ruta_bus(bus_code)
        if ruta_data:
            # Extraer los paths de ida y regreso si están disponibles
            ida_path = ruta_data.get("ida", {}).get("path", [])
            regreso_path = ruta_data.get("regreso", {}).get("path", [])
            
            # Invertir el orden de las coordenadas en los paths
            ida_path = [[coord[1], coord[0]] for coord in ida_path]
            regreso_path = [[coord[1], coord[0]] for coord in regreso_path]
            
            # Convertir los paths a formato GeoJSON (asumiendo que los paths son listas de coordenadas)
            if ida_path:
                ida_feature = {
                    "type": "Feature",
                    "properties": {
                        "bus_code": bus_code,
                        "direction": "ida"
                    },
                    "geometry": {
                        "type": "LineString",
                        "coordinates": ida_path  # Asumiendo que es una lista de [lat, lon]
                    }
                }
                geojson_data["features"].append(ida_feature)
                print(f"Ruta de ida de {bus_code} añadida.")
                
            if regreso_path:
                regreso_feature = {
                    "type": "Feature",
                    "properties": {
                        "bus_code": bus_code,
                        "direction": "regreso"
                    },
                    "geometry": {
                        "type": "LineString",
                        "coordinates": regreso_path  # Asumiendo que es una lista de [lat, lon]
                    }
                }
                geojson_data["features"].append(regreso_feature)
                print(f"Ruta de regreso de {bus_code} añadida.")
    
    # Paso 3: Guarda toda la colección en un archivo geojson único
    with open(OUTPUT_FILE, "w") as geojson_file:
        json.dump(geojson_data, geojson_file)
    print(f"Todas las rutas guardadas exitosamente en {OUTPUT_FILE}")

# Ejecuta el script
if __name__ == "__main__":
    main()