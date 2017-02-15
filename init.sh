#!/bin/bash

# Hostname (Default)
THISHOST="ecg1"
# Abfrage des Hostnamen
echo "Bitte geben Sie den Namen des Systems ein. Dieser sollte eindeutig sein:"
read THISHOST
echo ""
echo "Es wird der Hostname verwendet: $THISHOST"
read -r -p "Forfahren? [y/N] " response
case "$response" in
    [N][o]|[nN])
        echo "Abbruch durch Benutzer."
        exit 0
        ;;
    *)
        echo "OK, weitermachen..."
        echo ""
        ;;
esac
echo "hostename=$THISTHOST" > /home/pi/ecg/hostname.secret

# #####################################################
# 0. Identifizierung
sudo hostname $THISHOST
sudo sysctl kernel.hostname=$THISHOST

# #####################################################
# 1. Initialisierung
sudo apt-get -y update
sudo apt-get -y upgrade
sudo apt-get -y autoremove

# Tools
sudo apt-get -y install mc
sudo apt-get -y install htop
sudo apt-get -y install git-core
sudo apt-get -y install iftop

# WLAN Hotspot
sudo apt-get -y install hostapd
sudo apt-get -y install isc-dhcp-server

# Samba
sudo apt-get install samba samba-common-bin

# Bluetooth
sudo apt-get -y install bluetooth bluez
# Python
sudo apt-get -y install python-gobject python-gobject-2 python-bluez python-dev
sudo apt-get -y install python-rpi.gpio python-requests python-smbus i2c-tools
sudo apt-get -y install build-essential libbluetooth-dev
# Python Installer
sudo apt-get -y install python-pip python3-pip
# Python RRDtool
sudo apt-get -y install python-rrdtool rrdtool lighttpd php5-common php5-cgi php5 php5-cli python2.7-dev python-openssl
# Perl RRDtool
sudo apt-get install librrds-perl

# Dash Button
sudo apt-get -y install scapy tcpdump
sudo apt-get -y install dnsmasq

# Tools Systemmonitoring
sudo apt-get -y install ifstat

# Python Module
sudo pip install pybluez
sudo pip install gpiozero
sudo pip install requests
#sudo pip install pandas
sudo apt-get -y install python-pandas

# Suport USB
sudo apt-get -y install ntfs-3g hfsutils hfsprogs exfat-fuse
# mount with:
# 1. sudo mkdir /media/usbstick
# 2. sudo mount -t vfat -o utf8,uid=pi,gid=pi,noatime /dev/sda1 /media/usbstick

# Alexa->Script
sudo apt-get update && sudo apt-get upgrade -y
sudo apt-get install python2.7-dev python-dev python-pip
sudo pip install Flask flask-ask

cd ~
wget https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-arm.zip
unzip ngrok-stable-linux-arm.zip
sudo rm -rf ngrok-stable-linux-arm.zip


# Zeit-Synchro
#sudo dpkg-reconfigure tzdata
sudo apt-get -y purge ntp
sudo apt-get -y install ntpdate
sudo ntpdate -s 0.de.pool.ntp.org

#
# sudo crontab -e
# add -> @reboot ntpdate -s 0.de.pool.ntp.org
# add -> 0 */6 * * * ntpdate -s 0.de.pool.ntp.org
#

# Abschluss
sudo apt-get -y autoremove

# #####################################################
# 2. WLAN Konfiguration
network_ssid="wlan4eap"
echo "Welcher Benutzername soll für die SSID '${network_ssid} verwendet werden?"
read network_username
echo "Welches Kennwort soll für Benutzername '${network_username} für die SSID '${network_ssid} verwendet werden? (ACHTUNG: Eingabe sichtbar!)"
read network_passowrd

cat >>/etc/wpa_supplicant/wpa_supplicant.conf <<EOL
network={
     ssid="${network_ssid}"
     key_mgmt=WPA-EAP
     eap=PEAP
     identity="${network_username}"
     password="${network_password}"
}
EOL

# #####################################################
# 3. WiringPi installieren (für SensorPack)
cd ~
mkdir git
cd git
# Sensor-Beispiele installieren
git clone https://github.com/sunfounder/SunFounder_SensorKit_for_RPi2.git
# WiringPi installieren
git clone git://git.drogon.net/wiringPi
cd wiringPi
git pull origin
./build

# ####################################################
# 4. Git
echo "Git Konfiguration"
echo ""
echo "Welcher Benutzername soll fuer Git verwendet werden?"
read GIT_NAME
echo "Welches E-Mail-Adresse soll Fuer Git verwendet werden?"
read GIT_EMAIL
git config --global push.default simple
git config --global user.name "$GIT_NAME"
git config --global user.email "$GIT_EMAIL"
