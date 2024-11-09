FROM ghcr.io/project-osrm/osrm-backend

WORKDIR /data
RUN apt update && apt install -y wget
RUN wget https://download.geofabrik.de/europe/italy/nord-est-latest.osm.pbf

COPY profile.lua /opt
RUN osrm-extract -p /opt/profile.lua nord-est-latest.osm.pbf
RUN osrm-partition /data/nord-est-latest.osrm
RUN osrm-customize /data/nord-est-latest.osrm

ENTRYPOINT ["osrm-routed", "--algorithm", "mld", "/data/nord-est-latest.osrm"]
