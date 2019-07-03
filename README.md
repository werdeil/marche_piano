# Marche Piano
Project to turn stair steps into a piano

This project was made as an animation for the Forum des Images during the festival "Tout-petits cinéma" in February 2015.

## Introduction

This project is aimed to be a simple device, easy to user allowing to make a piano from stairs. This device will them be plugged to a sound system through a standard jack interface in order to play the sounds.


## Requirements of the project
To limit the development, here are the requirements taken into account:
- 16 steps of the stair will be equiped, each step being 2,5 m of width,
- The device shall work without interruption during a whole day and should need minimum maintenance,
- At least 6 types of sounds shall be included and it shall be possible to add more easily,
- The user interface shall be easy.

## Building

The project is separated in 3 parts: the sensors, the computer and the software.

### The sensors

The sensors are made of IR LED and sensors. They are made of 2 PCB to be inserted in 2 boxes of the same size positioned on each side of the step. On one side, the emitter is emitting the IR signal to the receiver. On the other side the receiver is constantly analysing IR beam. When the IR level decreases it means that something is on the step and the info is send to the computer.

### The computer

All sensors are plugged to each other on a I2C bus, and linked to a Raspberry Pi computer. The Raspberry Pi is placed in case with 2 push buttons with integrated LED. One of the button is allowing to start and stop the system, the other one is allowing to switch between sounds. The behavior will be detailled later.

The Rapsbeery Pi have a micro SD card which contains the operating system and the project's program. This card will also be the mean to change some part of the project (add new sounds, change the period of automatic switch).

### The software

The software is developped in Python.

#### Operating

As soon as the Raspberry Pi is booting the program shall start automatically, avoiding any extra action. To each sensor is linked a sound, this sound is played when there is something between the sensor and the emitter.

Two operating modes are planned, the manual and the automatic switch. In the automatic switch mode, the sounds family is changed automatically after a defined time (written in a configuration file on the SD card). This mode allows to have multiple sounds without needing an action from the team.
In the manual mode the push button is used to switch between each sound family. At each press the sound family is changed (there shall be at least 1s between each press).
The switch between automatic and manual mode is also done through the push button, the automatic mode being considered as one of the sound family (the light on the button is always on in this mode).

#### Sounds

All of the sounds of a family are grouped in a folder, ideally the folder name starts with a number to allow an easier ordering of the program. All of the sound folders are stored on the SD card.
For each sounds family, the sound shall be numbered in the desired order, if there are more sounds than sensors, only the first one will be used.
Most of the sound used in this project have been extracted from http://www.freesound.org/ which is a collabrative database giving a multitude of sound on free license.
Specific sounds could be added afterward, the software using the folder and file names to know which sound to play. Moreover the sounds can be changed easily.
The project is delivered with 8 sound families: piano, guitar, glockenspiel (small xylophone), drums, car horns, farm animals, wild animals and water drops.

## Installation and run

### Packages

 `pygame` shall be installed (on debian `python-pygame` package)

### Run program at startup

Add the python program to be ran at startup of the Raspberry Pi

/etc/rc.local is a script on the Raspberry Pi which runs when Linux first boots. To edit it, you will need root privileges:

    sudo nano /etc/rc.local

Then add this to the end of rc.local:

    python marche_piano.py
