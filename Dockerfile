FROM python:3.9-alpine3.19

#Debian aktualisieren
RUN apk update && apk upgrade

#Ordner erstellen
RUN mkdir /opt/scripts

#PIP update & Python Pakete installieren
RUN pip install --upgrade pip
RUN pip install datetime requests pytz

#Environment variables
ENV DEST_URL="https://<<FE2SERVER:PORT>>/rest/external/http/alarm/v2"
ENV THRESHOLD="15"
ENV AUTH="MY_SECRET"

#Dateien kopieren
COPY main.py /opt/scripts/

VOLUME /opt/scripts/

ENTRYPOINT python3 /opt/scripts/main.py
