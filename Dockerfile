FROM python:3.9-alpine3.19

#Debian aktualisieren
RUN apk update && apk upgrade

#Ordner erstellen
RUN mkdir /opt/scripts

#PIP update & Python Pakete installieren
RUN pip install --upgrade pip
RUN pip install datetime requests pytz

#Environment variables
ENV DEST_URL="https://alamos.mauchle.net"
ENV THRESHOLD="15"
ENV AUTH=""

#Dateien kopieren
COPY main.py /opt/scripts/

VOLUME /opt/scripts/ --name abflussalarm

ENTRYPOINT python3 /opt/scripts/main.py
