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

## System Update und Installation von Ansible

Auf der Konsole führ man nun nacheinander die nachfolgenden Befehle aus.

1. `sudo apt-get update` Um die Paketlisten zu aktualisieren
2. `sudo apt-get upgrade` Um die Pakete zu aktualisieren
3. `sudo apt-get install ansible` Um Ansible zu installieren

Nun hat man das System auf den aktuellsten Stand gebracht und [Ansible](https://docs.ansible.com/ansible/latest/index.html), ein Tool zum automatischen provisionieren von Systemen, installiert.

## AlarmPi Git Repositiory clonen

TBD
