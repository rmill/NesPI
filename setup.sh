#!/bin/bash

# Configure the raspberry pi
sudo raspi-config

# Update Apt Repositories
sudo apt-get update
sudo apt-get update -y

# Install Git
sudo apt-get install -y git dialog

# Install RetroArch and EmulationStaion
sudo git clone --depth=0 git://github.com/petrockblog/RetroPie-Setup.git /var/RetroPie
sudo chmod +x /var/RetroPie/retropie_setup.sh
sudo /var/RetroPie/retropie_setup.sh
sudo mkdir /home/pi/.emulationstation
#sudo cp es_system.cfg /home/pi/.emulationstation
sudo ln -s /home/pi/.emulationstation /.emulationstation

# Hide the Kernel Logging
#cat cmdline.txt > /boot/cmdline.txt

# Setup Boot
#cat inittab > /etc/inittab

# Add Splash Screen
#cp splash /etc/init.d

# Add Init Scripts
sudo cp emulation-station /etc/init.d/
sudo cp nes-keypress /etc/init.d/
sudo update-rc.d /etc/init.d/emulation-station defaults
sudo update-rc.d /etc/init.d/nes-keypress defaults

# Install Python Libraries
sudo apt-get install python-rpi.gpio python3-rpi.gpio
sudo cp nes-keypress.py /usr/bin/

# Install the uinput library
cd python-uinput-0.9
sudo python ./python-uinput-0.9/setup.py install --prefix=/usr/local
sudo python modprobe uinput

# Reboot the Pi
echo "******** INSTALLATION COMPLETE ********"
echo "******* PRESS ANY KEY TO REBOOT *******"
read ANY_KEY
sudo reboot
