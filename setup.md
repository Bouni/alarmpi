# Setup

Es wird von einem raspberryPi 4 B ausgegangen, aber die Schritte sollten auch mit einem RaspberryPi 3 B funktionieren.
Desweiteren wird davon ausgegangen das das Setup von einem Windows PC aus erfolgt.

Es wird kein Bildschirm am RaspberryPi benötigt um dieses Setup durchzuführen. Es werden lediglich Strom und Netzwerk benötigt, hierbei muss das RPi im selben Netzwerk sein wie der PC von dem aus das Setup durchgeführt wird.

## Grundlegendes RaspberryPi Setup

1. Raspbian Buster Lite image [herunterladen](https://www.raspberrypi.org/downloads/raspbian/)
2. Etcher [herunterladen](https://www.balena.io/etcher/) und installieren.
3. Das Raspbian image mit Hilfe von Etcher auf die SD Karte des RaspberryPi schreiben (weitere infos finden sich [hier](https://www.raspberrypi.org/documentation/installation/installing-images/README.md)). Hierfür wird am Windows PC ein SD Karten Leser (MicroSD) benötigt.
4. Nach dem das Image auf der SD Karte ist, wird diese als `Boot` unter Windows angezeigt. Nun öffnet man die SD karte und erstellt eine leere Datei Namens `ssh.txt` um den SSH Server zu aktivieren.
5. Nun SD Karte ins RaspberryPi stecken und dieses anschliessend mit Strom versorgen.
6. Das RPi bootet und bekommt vom Router (z.B. der FritzBox) eine IP Adresse per DHCP zugewiesen. Diese lässt sich über das Webinterface des Routers herausfinden.
7. kitty.exe [herunterladen](https://github.com/cyd01/KiTTY/releases).
8. Per SSH (kitty) mit dem RaspberryPi verbinden, hierzu die eben ausfindig gemachte IP in das Feld Host name eintragen und auf Open klicken.

## Installation des eigentlichen Systems

Auf der Konsole führt man nun den nachfolgenden Befehle aus:

`curl -sSL https://raw.githubusercontent.com/Bouni/alarmpi/alarmpi-docker/install.sh | sudo bash`

Dies updatet das System, installiert die notwendigen Pakete und klont das Git repo

Danach sollte das system einmal neu gestartet werden, hierzu `sudo reboot` eingeben und Enter drücken.

## Config File anpassen

Nun muss ein config file erstellt werden, hierzu kopiert man das Beispiel:

`cp ~/alarmpi/config/config.yaml.example ~/alarmpi/config/config.yaml`

Nun öffnet man das config file mit z.B. nano und passt dieses an.

Hier ein Beispiel:

```
accounts:
  - name: Musterstadt
    mail:
        host: imap.mailprovider.de
        user: alarm@ffw-musterstadt.de
        password: Feuer!
        subject: "Einsatzmeldung"
    connect:
        token: >- 
            E-pzIiYlxxTdFu8w9a-KWNVHv-4jIqRdg5UKyiwRE24soOJNDHyFi9MHXDzHICJUQ9O
            AQryScOihl5F2ZVsFeOEvy1bhOU5Vr33ocLRteQhTL4uTHr76wV4BLkaOYvJGOpzVBx
            YyQoQr88o9DgarO3V3tU2wGWghmWcSHYQzZcCu1SVDkvPJk3qs6Uz6uLGsERzSQIOnd
            pPagCKpBt8p9flM_dax-10oWhqXjhTXzCnOO512R1-0i1S9N7OEjUFr1NIesrhCjrl9
            K_nwPwWHoHHXaSpaddouk_9_EKDcXVqBXFLJwYRB9mQ-pxMhm--Gy-iKqzBeky-pPpG
            i4_v9XDzDpS4xPlpL3N1NGuAmQsgVWbEjWa-rdRu9Af8k9Bb4XvogCQJ5--TRlnGzDo
            04g3Xi2obBBpwBmZRXdddYpwRKHBTyl96ERDZadnD2c70QpFfOA2pduLBM1RHUpeqiw
            GABXfs-FQ5eZ8fMPX7RYiutzourY3K_tFsCvaB0w6jXqTzQsfqjSceJyPh8erf6OiTS
            LA_C65GHJY3v6c3sCToIIuoplDHB7Havy0XI0S4_NNvfIQ

parser:
  - var: start
    regex: 'LS RTK: (.*)\n'
  - var: number
    regex: 'EINSATZNUMMER: (.*)\n'
  - var: keyword
    regex: 'STICHWORT: (.*)\n'
  - var: city
    regex: 'Ort: (.*)\n'
  - var: district
    regex: 'Ortsteil: (.*)\n'
  - var: object
    regex: 'Objekt: (.*)\n'
  - var: street
    regex: 'Strasse: (.*)\n'
  - var: housenumber
    regex: 'Hausnummer: (.*)\n'
  - var: comment
    regex: 'Bemerkung: (.*)\n'
  - var: siren
    regex: 'Sondersignal: (.*)\n'
  - var: assigned
    regex: 'Zugeteilt: (.*)\n'

```

Beim config File handelt es sich um ein [YAML](https://de.wikipedia.org/wiki/YAML) file, bei diesem ist die Tiefe der einrückung entscheidend!

Es können quasi beliebig viele Mail Accounts für die Überwachung angegeben werden, hierzu wird einfach ein weiter Block `-name: ...` unter dem ersten angelegt.
Auch hier wieder auf die Einrückungstiefe achten.

## Docker container starten

Ist das File angepasst startet man den Docker container:

```
cd ~/alarmpi
docker-compose up -d
```

Um zu sehen ob der Container erfolgreich gestartet ist, gibt man `docker ps -a` ein, der output sieht ungefähr so aus:

```
CONTAINER ID        IMAGE                                 COMMAND                  CREATED             STATUS                    PORTS               NAMES
d2d03145f6b5        alarmpi_alarmpi                       "python alarmpi conf…"   23 minutes ago      Up 23 minutes                                 alarmpi
```

Wenn man die logs begutachten möchte, dann kann man die mit dem Befehl `docker logs alarmpi -f`, der output wird ungefähr so aussehen:

```
2020-02-04 13:57:44.236 - mailcheck - INFO - Successfully connected to IMAP server <mailserveradresse>
2020-02-04 13:57:44.251 - mailcheck - INFO - Successfully logged in to IMAP server as <mailaccount>
2020-02-04 13:57:44.265 - mailcheck - INFO - Successfully selected mailbox INBOX
2020-02-04 13:57:44.278 - mailcheck - INFO - Keine neuen E-Mails
```

Um den container zu stoppen gibt man `docker-compose down` ein.
