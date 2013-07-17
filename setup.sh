#!/bin/bash

# Become Root User
#sudo su

# Configure the raspberry pi
#raspi-config

# Update Apt Repositories
#apt-get update
#apt-get update -y

# Install Git
#apt-get install -y git dialog

# Install RetroArch and EmulationStaion
#git clone --depth=0 git://github.com/petrockblog/RetroPie-Setup.git /var/RetroPie
#chmod +x /var/RetroPie/retropie_setup.sh
#/var/RetroPie/retropie_setup.sh
#mkdir /home/pi/.emulationstation
#cp es_system.cfg /home/pi/.emulationstation
#ln -s /home/pi/.emulationstation /.emulationstation

# Hide the Kernel Logging
#cat cmdline.txt > /boot/cmdline.txt

# Setup Boot
#cat inittab > /etc/inittab

# Add Splash Screen
#cp splash /etc/init.d

# Add Init Scripts
#cp emulation-station /etc/init.d/
#cp nes-keypress /etc/init.d/
#update-rc.d /etc/init.d/emulation-station defaults
#update-rc.d /etc/init.d/nes-keypress defaults

# There is a bug in the install and libretro-fceu doesn't get moved
#mkdir /home/pi/RetroPie/emulatorcores/libretro-fceu
#cp /usr/lib/libretro-fceu.so /home/pi/RetroPie/emulators/libretro-fceu

# Install Python Libraries
#sudo apt-get install python-rpi.gpio python3-rpi.gpio
#cp nes-keypress.py /usr/bin/

# Reboot the Pi
echo "******** INSTALLATION COMPLETE ********"
echo "******* PRESS ANY KEY TO REBOOT *******"
read ANY_KEY
reboot
