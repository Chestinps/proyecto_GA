## Scripts
rutas.py obtiene el geojson con las rutas de los buses
rutas_a_gtfs transforma este geojson resultante en los archivos necesatios para el formato GTFS

## Descargar archivos requeridos
```sh
bash requirements.sh
```

## Directorio final
```
otp_data/
├── otp-2.6.0-shaded.jar
└── graphs/
    └── default/
        ├── archivo_mapa.osm.pbf
        ├── routes.txt
        ├── trips.txt
        ├── stops.txt
        └── (otros archivos GTFS)
```
## Comandos OTP
```
java -Xmx8G -jar otp-2.6.0-shaded.jar --build graphs/default --save
```
```
java -Xmx8G -jar otp-2.6.0-shaded.jar --build graphs/default --serve
```
