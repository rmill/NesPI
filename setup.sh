#!/bin/bash

# Configure the raspberry pi. Need to expand the file system
sudo raspi-config

# Update Apt Repositories
sudo apt-get update -y

# Install Git
sudo apt-get install -y --force-yes git dialog

# Install RetroArch and EmulationStaion
sudo git clone --depth=0 git://github.com/petrockblog/RetroPie-Setup.git /var/RetroPie
sudo chmod +x /var/RetroPie/retropie_setup.sh
sudo /var/RetroPie/retropie_setup.sh
sudo mkdir /var/RetroPie/roms
sudo ln -s /RetroPie /var/RetroPie
sudo mkdir /.emulationstation
sudo cp assets/es_systems.cfg /.emulationstation/es_systems.cfg
sudo cp assets/es_input.cfg /.emulationstation/es_input.cfg

# Hide the Kernel Logging
sudo cp assets/cmdline.txt /boot/cmdline.txt

# Setup Boot
sudo cp assets/inittab /etc/inittab

# Add Splash Screen
sudo apt-get install mplayer

# Copy over Splash Screen
sudo mkdir /.nespi
sudo cp /assets/splashscreen /.nespi/splashscreen

# Add Init Scripts
sudo cp daemons/emulation-station /etc/init.d/emulation-station
sudo cp daemons/nes-keypress /etc/init.d/nes-keypress
sudo chmod 775 /etc/init.d/emulation-station
sudo chmod 775 /etc/init.d/nes-keypress
sudo update-rc.d emulation-station defaults
sudo update-rc.d nes-keypress defaults

# Install Python Libraries
sudo apt-get install python-rpi.gpio python3-rpi.gpio libudev-dev

# Setup NES controller driver
sudo git clone https://github.com/rmill/nes-keypress.git /var/nes-keypress
sudo cp /var/nes-keypress/nes-keypress.py /usr/bin/nes-keypress.py
sudo mkdir /.nes-keypress
sudo cp assets/controller1.json /.nes-keypress/controller1.json
sudo cp assets/controller2.json /.nes-keypress/controller2.json

# Install the uinput library
cd lib/python-uinput-0.9
sudo python setup.py install --prefix=/usr/local
sudo python modprobe uinput

# Reboot the Pi
echo "******** INSTALLATION COMPLETE ********"
echo "******* PRESS ANY KEY TO REBOOT *******"
read ANY_KEY
sudo reboot
