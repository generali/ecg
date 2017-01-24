# ElderyCare/Guard

In diesem Repository werden alle projektrelevanten Dateien der mitwirkenden Kollegen zentrale verwaltet.

---

Dokumentation:
=======================
Sensoren:
- https://www.sunfounder.com/learn/category/Sensor-Kit-v1-0-for-Raspberry-Pi.html

Schaltpläne, Belegungspläne:
- https://www.bitblokes.de/wp-content/uploads/2016/01/raspberry_pi_gpio-shutdown-pins.png

Tipps:
- (...)

Anleitung:
=======================
1. Github clonen
  - cd ~
  - git clone git:://github.com/generali/ecg
  - cd ecg
  
  Done :)
  
2. für eine Standardinstallation,die alle Treiber und Hilfsprogramme für die Sensorik mitbringt, kann das Skript *init.sh* ausgeführt werden.

2. Die Konfiguration des Systems ist durchzuführen
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

# MERKER
Ab der Konfiguration (und dem Reboot) ist der Raspberry unter "ssh -p 22 pi@<Name des Systems>" im lokalen Netzwerk erreichbar (hierfür idealerweise DHCP im Router aktivieren und den Raspebrry per Netzwerkkabel anschließen)

