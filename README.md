# ElderyCare/Guard

In diesem Repository werden alle projektrelevanten Dateien der mitwirkenden Kollegen zentrale verwaltet. Weitere Informationen sind im Wiki unter https://github.com/generali/ecg/wiki dokumentiert.

---

Dokumentation:
=======================
Sensoren:
- https://www.sunfounder.com/learn/category/Sensor-Kit-v1-0-for-Raspberry-Pi.html (die korrekten Beispiele, die sich auf das Handbuch beziehen, sind unterhalb des Ordners ./docu/sunfounder/ in diesem Repository abgelegt)

Schaltpläne, Belegungspläne:
- https://www.bitblokes.de/wp-content/uploads/2016/01/raspberry_pi_gpio-shutdown-pins.png

Tipps:
- (...)

Anleitung Installation:
=======================
1. SD Karte installieren und in Betrieb nehmen
  - Empfohlen wird das Raspian-Image (https://www.raspberrypi.org/downloads/raspbian/) entweder in der vollen Ausstattung (mit Pixel als GUI) oder in der Lite-Variante (nur Console). 
  - Empfohlen ist weiterhin für den späteren Betrieb die Lite-Variante, da diese dazu führt, dass die Services bereits so eingerichtet werden, dass das System "headless" funktioniert. Eine Einrichtung von Diensten sollte bei der Nutzung der GUI immer so erfolgen, dass diese später auch im "headless mode" erfolgt (z.B. Autostart-Funktionalität). Die nachfolgenden 
  - alle nachfolgenden Befehle versuchensich auf die Consolen-Befehle zu beschränken, da dciese den kleinsten gemeinsamen Nenner darstellen, der auf jedem Raspian/Debian-System funktioniert.
    
2. Github clonen
Um im späteren Verlauf Ressourcen in dieses Repository übertragen zu könnnen, ist ein vorheriges Klonen des bestehenden Repository durchzuführen. Ausgehend von dem Benutzerverzeichnis (in der Regel 'pi') können folgende Schritte auf der Konsole durchgeführt werden:

  - cd ~
  - git clone https://github.com/generali/ecg.git
  - cd ecg
  
  Done :) Für eine spätere Übertragung der geänderten Dateien kann nach dem ersten Klonen dann im Verzeichnis ./ecg/ das Skript "./gitpush.sh" ausgeführt werden, welches die Änderungen akzeptiert, kommentiert und überträgt. Hierzu sind im Verlauf  Benutzername- und kennwort von Github anzugeben. Ggf. ist vorab das Skript "./gitpull.sh" aufzurufen, um zwischenzeitliche Änderungen in Github auf das lokale System zu übertragen ("local merge").
  
3. für eine Standardinstallation,die alle Treiber und Hilfsprogramme für die Sensorik mitbringt, kann das Skript *init.sh* ausgeführt werden.

4. Die Konfiguration des Systems ist durchzuführen
   - *sudo raspi-config* starten
   - deutsche Lokalisierung (4.I1 => de_DE.UTF-8 UTF-8 (per Space auswählen, Return zum bestätigen); Default=>de_DE.UTF-8)
   - deutsches Tastaturlayout (4.I3 => Other=>German=>German)
   - SSH aktivieren (5.P2 => yes)
   - VNC aktivieren (5.P3 => yes)
   - SPI Interface aktivieren (5.P4 => yes)
   - 1-wire aktivieren (5.P7 => yes)
   - Hostname konfigurieren (7.A2 => möglichst eindeutig)
        - verwendete Namen (jeder pflegt bitte):
          - Rene: ecg1
   - Reboot durchführen

MERKER
=======================
Ab der Konfiguration (und dem Reboot) ist der Raspberry unter "ssh -p 22 pi@_Name_des_Systems_" im lokalen Netzwerk erreichbar (hierfür idealerweise DHCP im Router aktivieren und den Raspebrry per Netzwerkkabel anschließen)

Wichtige Tipps
=======================
Die GPIO des Reaspberry sind unter unterschiedlichen Namen anzusprechen. In der Regel wird für die hier abgelegten Beispiele die  BCM-Nomenklatur genutzt.
