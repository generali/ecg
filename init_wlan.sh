#!/bin/bash
echo "Re-Initializing WLAN..."
echo "Setting WLAN0 down"
sudo ifdown  wlan0
echo "Setting WLAN0 up..."
sudo ifup wlan0
echo "Done."

echo "Setting WLAN1 down..."
sudo ifdown wlan1
echo "Setting WLAN1 up..."
sudo ifup wlan1
echo "Done."
