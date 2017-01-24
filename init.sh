#!/bin/bash
THISHOST="ecg1"
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

# Bluetooth
sudo apt-get -y install bluetooth bluez
# Python
sudo apt-get -y install python-gobject python-gobject-2 python-bluez python-dev python-rpi.gpio python-requests python-smbus i2c-tools
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

# Abschluss
sudo apt-get -y autoremove

# #####################################################
# 2. WiringPi installieren (für SensorPack)
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
# 3. Git
git config --global push.default simple
git config --global user.name "$THISHOST"
git config --global user.email "$THISHOST@discard.email"
