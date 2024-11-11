import json
import csv
import os

# Archivos GTFS que se generarán
gtfs_files = {
    "stops": "stops.txt",
    "routes": "routes.txt",
    "trips": "trips.txt",
    "stop_times": "stop_times.txt",
    "shapes": "shapes.txt"
}

# Crear directorio para archivos GTFS
if not os.path.exists("gtfs_output"):
    os.makedirs("gtfs_output")

# Inicializar IDs para GTFS
route_id = 1
trip_id = 1
stop_id = 1
shape_id = 1

# Crear archivos GTFS con encabezados
with open(f"gtfs_output/{gtfs_files['stops']}", mode="w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["stop_id", "stop_name", "stop_lat", "stop_lon"])

with open(f"gtfs_output/{gtfs_files['routes']}", mode="w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["route_id", "route_short_name", "route_long_name", "route_type"])

with open(f"gtfs_output/{gtfs_files['trips']}", mode="w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["route_id", "service_id", "trip_id", "shape_id"])

with open(f"gtfs_output/{gtfs_files['stop_times']}", mode="w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["trip_id", "arrival_time", "departure_time", "stop_id", "stop_sequence"])

with open(f"gtfs_output/{gtfs_files['shapes']}", mode="w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["shape_id", "shape_pt_lat", "shape_pt_lon", "shape_pt_sequence"])

# Cargar el archivo GeoJSON
with open('rutas_buses.geojson') as f:
    geojson_data = json.load(f)

# Procesar cada ruta en el GeoJSON
for feature in geojson_data["features"]:
    bus_code = feature["properties"]["bus_code"]
    direction = feature["properties"]["direction"]
    coordinates = feature["geometry"]["coordinates"]

    # Escribir datos en routes.txt
    with open(f"gtfs_output/{gtfs_files['routes']}", mode="a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([route_id, bus_code, f"Ruta {bus_code} {direction}", 3])  # route_type 3: Bus

    # Escribir datos en trips.txt
    with open(f"gtfs_output/{gtfs_files['trips']}", mode="a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([route_id, "1", trip_id, shape_id])  # service_id is set to "1" for simplicity

    # Escribir datos en shapes.txt
    shape_sequence = 0
    for coord in coordinates:
        lat, lon = coord[1], coord[0]  # Intercambiar orden de lat y lon
        with open(f"gtfs_output/{gtfs_files['shapes']}", mode="a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([shape_id, lat, lon, shape_sequence])
        shape_sequence += 1

    # Escribir datos en stops.txt y stop_times.txt
    stop_sequence = 0
    for coord in coordinates:
        lat, lon = coord[1], coord[0]
        
        # Guardar paradas en stops.txt
        with open(f"gtfs_output/{gtfs_files['stops']}", mode="a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([stop_id, f"Parada {stop_id}", lat, lon])
        
        # Guardar tiempos en stop_times.txt (usando tiempos ficticios)
        arrival_time = f"{8 + stop_sequence // 60:02}:{stop_sequence % 60:02}:00"  # Ejemplo: "08:00:00"
        departure_time = arrival_time  # Para simplificar, misma hora de llegada y salida

        with open(f"gtfs_output/{gtfs_files['stop_times']}", mode="a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([trip_id, arrival_time, departure_time, stop_id, stop_sequence])

        stop_sequence += 1
        stop_id += 1

    # Incrementar IDs
    route_id += 1
    trip_id += 1
    shape_id += 1

print("Archivos GTFS generados en la carpeta 'gtfs_output'")