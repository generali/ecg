#!/bin/bash
echo "Starte ngrok:5000"
sudo ~/ngrok http 5000 &
echo "Starte Flask Server"
python gpio_control.py & 
