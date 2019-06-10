# Marche Piano
Project to turn stair steps into a piano

This project was made as an animation for the Forum des Images during the festival "Tout-petits cinéma" in February 2015.

## Hardware setting

I will describe later how the whole project was set up

## Installation and run

### Packages

 `pygame` shall be installed (on debian `python-pygame` package)

### Run program at startup

Add the python program to be ran at startup of the Raspberry Pi

/etc/rc.local is a script on the Raspberry Pi which runs when Linux first boots. To edit it, you will need root privileges:

    sudo nano /etc/rc.local

Then add this to the end of rc.local:

    python marche_piano.py
