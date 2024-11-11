#!bin/bash

# Descargar OTP
wget https://repo1.maven.org/maven2/org/opentripplanner/otp/2.6.0/otp-2.6.0-shaded.jar -O "otp_data/otp-2.6.0-shaded.jar"

# Descargar osm.pbf
wget https://download.geofabrik.de/south-america/chile-latest.osm.pbf -O "otp_data/graphs/default/chile-latest.osm.pbf"
 
echo "Done..."
