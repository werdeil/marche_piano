#!/usr/bin/env python
# -*- coding: utf8 -*-

import os
import time
import pygame
import RPi.GPIO as GPIO

pygame.mixer.pre_init(channels=2, buffer=1024)
pygame.mixer.init()

class Piano:
    def __init__(self, ports, switch_time = 3600):
        self.auto_change = True
        self.switch_time = switch_time
        self.sound_sets = os.listdir("sounds")
        self.current_sound_set_index = 0
        self.prepare_notes()
        #GPIO ports
        GPIO.setmode(GPIO.BCM)
        self.push_button = ports[0]
        GPIO.setup(self.push_button, GPIO.IN)
        self.LED_button = ports[1]
        GPIO.setup(self.LED_button, GPIO.OUT, initial=1)
        self.step_ports = ports[2:]
        for port in self.step_ports:
            GPIO.setup(port, GPIO.IN)

    def prepare_notes(self):
        # Empty the note variable
        self.notes = []
        # List the file of the directory corresponding to the current index
        folder = self.sound_sets[self.current_sound_set_index]
        notefile_list = os.listdir(folder)
        # Load all the sounds in the class variable
        for note in notefile_list:
            if note.endswith(".wav"):
                self.notes.append(pygame.mixer.Sound(os.path.join(folder, note)))
        self.last_changed_time = time.time()
            
    def handle_sound_set_change(self):
        current_time = time.time()
        if self.auto_change and current_time-self.last_changed_time >= self.switch_time:
            self.current_sound_set_index = (self.current_sound_set_index + 1)%len(self.sound_sets)
            self.prepare_notes()

    def handle_buttons(self):
        if GPIO.input(self.push_button):
            if self.auto_change:
                self.auto_change = False
                self.current_sound_set_index = 0
                self.prepare_notes()
            else:
                self.current_sound_set_index = (self.current_sound_set_index + 1)%len(self.sound_sets)
                self.prepare_notes()
                if self.current_sound_set_index == 0: # Case all the sets have been done, reactivate the auto switch
                    self.auto_change = True

    def main(self):
        while True:
            # Part for switching between sounds sets
            self.handle_sound_set_change()
            self.handle_buttons()

            # Part for the GPIO inputs
            for port in self.step_ports:
                if GPIO.input(port):
                    self.notes[self.step_ports.index(port)].play()
            
            # Part for the LED
            GPIO.output(self.LED_button, self.auto_change)
    
class PianoEdge(Piano):
    def __init__(self, ports, switch_time=3600):
        super().__init__(ports, switch_time=switch_time)
        for port in self.step_ports:
            GPIO.add_event_detect(port, GPIO.RISING, callback=self.play_channel)

    def play_channel(self, channel):
        self.notes[self.step_ports.index(channel)].play()
        
    def main(self):
        while True:
            # Part for switching between sounds sets
            self.handle_sound_set_change()
            self.handle_buttons()
                        
            # Part for the LED
            GPIO.output(self.LED_button, self.auto_change)
            time.sleep(0.5) # to avoid too many loops
    
if __name__ == "__main__":
    PORTS = []
    try:
        PIANO = PianoEdge(PORTS)
        PIANO.main()
    except KeyboardInterrupt:
        GPIO.cleanup()       # clean up GPIO on CTRL+C exit
    GPIO.cleanup()           # clean up GPIO on normal exit
