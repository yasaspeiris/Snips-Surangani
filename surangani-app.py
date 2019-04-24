#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from snipsTools import SnipsConfigParser
from hermes_python.hermes import Hermes
from hermes_python.ontology import *
import io

CONFIG_INI = "config.ini"

##MODBUS 
import minimalmodbus

instrument = minimalmodbus.Instrument('/dev/ttyS0', 1, mode = 'rtu') # port name, slave address - Use multiple objects to talk with multiple power meters
instrument.serial.baudrate = 9600

from threading import Thread

import RPi.GPIO as gpio
gpio.setmode(gpio.BCM)
gpio.setup(4, gpio.OUT)
gpio.output(4, gpio.HIGH)


# If this skill is supposed to run on the satellite,
# please get this mqtt connection info from <config.ini>
# Hint: MQTT server is always running on the master device
MQTT_IP_ADDR = "localhost"
MQTT_PORT = 1883
MQTT_ADDR = "{}:{}".format(MQTT_IP_ADDR, str(MQTT_PORT))

availableDevice = ('fan')

class Surangani_app(object):
    def __init__(self):
        # get the configuration if needed
        try:
            self.config = SnipsConfigParser.read_configuration_file(CONFIG_INI)
        except :
            self.config = None

        # start listening to MQTT
        self.start_blocking()
        
    # --> Sub callback function, one per intent
    def getVolts_callback(self, hermes, intent_message):
        # terminate the session first if not continue
        hermes.publish_end_session(intent_message.session_id, "")
        
        # action code goes here...
        print '[Received] intent: {}'.format(intent_message.intent.intent_name)

        device = None
        if intent_message.slots:
            device = intent_message.slots.deviceName.first().value
            # check if valid
            if device.encode("utf-8") not in availableDevice:
                device = None

        if device is None:
            reply = "No device specified"
        else:
            reply = "Voltage received by "+str(device) +" is " + str(self.get_volts()) + " Volts"

        hermes.publish_start_session_notification(intent_message.site_id, reply,"Surangani_app")
        hermes.publish_end_session(intent_message.session_id, reply)

    def getCurrent_callback(self, hermes, intent_message):
        # terminate the session first if not continue
        hermes.publish_end_session(intent_message.session_id, "")
        
        # action code goes here...
        print '[Received] intent: {}'.format(intent_message.intent.intent_name)

        device = None
        if intent_message.slots:
            device = intent_message.slots.deviceName.first().value
            # check if valid
            if device.encode("utf-8") not in availableDevice:
                device = None

        if device is None:
            reply = "No device specified"
        else:
            reply = "Current consumed by "+str(device) +" is " + str(self.get_current()) + " Amps"

        hermes.publish_start_session_notification(intent_message.site_id, reply,"Surangani_app")
        hermes.publish_end_session(intent_message.session_id, reply)

    def getPower_callback(self, hermes, intent_message):
        # terminate the session first if not continue
        hermes.publish_end_session(intent_message.session_id, "")
        
        # action code goes here...
        print '[Received] intent: {}'.format(intent_message.intent.intent_name)

        device = None
        if intent_message.slots:
            device = intent_message.slots.deviceName.first().value
            # check if valid
            if device.encode("utf-8") not in availableDevice:
                device = None

        if device is None:
            reply = "No device specified"
        else:
            reply = "Power consumed by "+str(device) +" is " + str(self.get_power()) + " Watts"

        hermes.publish_start_session_notification(intent_message.site_id, reply,"Surangani_app")
        hermes.publish_end_session(intent_message.session_id, reply)

    def getEnergy_callback(self, hermes, intent_message):
        # terminate the session first if not continue
        hermes.publish_end_session(intent_message.session_id, "")
        
        # action code goes here...
        print '[Received] intent: {}'.format(intent_message.intent.intent_name)

        device = None
        if intent_message.slots:
            device = intent_message.slots.deviceName.first().value
            # check if valid
            if device.encode("utf-8") not in availableDevice:
                device = None

        if device is None:
            reply = "No device specified"
        else:
            reply = "Total Energy consumed by "+str(device) +" is " + str(self.get_energy()) + " watt hours"

        hermes.publish_start_session_notification(intent_message.site_id, reply,"Surangani_app")
        hermes.publish_end_session(intent_message.session_id, reply)

    def turnOn_callback(self, hermes, intent_message):
        # terminate the session first if not continue
        hermes.publish_end_session(intent_message.session_id, "")
        
        # action code goes here...
        print '[Received] intent: {}'.format(intent_message.intent.intent_name)

        device = None
        if intent_message.slots:
            device = intent_message.slots.deviceName.first().value
            # check if valid
            if device.encode("utf-8") not in availableDevice:
                device = None

        if device is None:
            reply = "No device specified"
        else:
            reply = "Turning "+str(device) + " on"
            gpio.output(4, gpio.LOW)
        

        hermes.publish_start_session_notification(intent_message.site_id, reply,"Surangani_app")
        hermes.publish_end_session(intent_message.session_id, reply)

    def turnOff_callback(self, hermes, intent_message):
        # terminate the session first if not continue
        hermes.publish_end_session(intent_message.session_id, "")
        
        # action code goes here...
        print '[Received] intent: {}'.format(intent_message.intent.intent_name)

        device = None
        if intent_message.slots:
            device = intent_message.slots.deviceName.first().value
            # check if valid
            if device.encode("utf-8") not in availableDevice:
                device = None

        if device is None:
            reply = "No device specified"
        else:
            reply = "Turning "+str(device) + " off"
            gpio.output(4, gpio.HIGH)
        

        hermes.publish_start_session_notification(intent_message.site_id, reply,"Surangani_app")
        hermes.publish_end_session(intent_message.session_id, reply)

    def setMaxCurrent_callback(self, hermes, intent_message):
        # terminate the session first if not continue
        hermes.publish_end_session(intent_message.session_id, "")
        
        # action code goes here...
        print '[Received] intent: {}'.format(intent_message.intent.intent_name)

        device = None
        maxCurrent = None
        if intent_message.slots:
            device = intent_message.slots.deviceName.first().value
            # check if valid
            if device.encode("utf-8") not in availableDevice:
                device = None

            maxCurrent = intent_message.slots.maxCurrent.first().value

        if device is None:
            reply = "No device specified"
            hermes.publish_start_session_notification(intent_message.site_id, reply,"Surangani_app")
            hermes.publish_end_session(intent_message.session_id, reply)
        if maxCurrent is None:
            reply = "No current specified"
            hermes.publish_start_session_notification(intent_message.site_id, reply,"Surangani_app")
            hermes.publish_end_session(intent_message.session_id, reply)
        else:
            t1 = Thread(target=self.monitorCurrent, args=(intent_message,hermes,device,maxCurrent))
            t1.start()



    # --> Master callback function, triggered everytime an intent is recognized
    def master_intent_callback(self,hermes, intent_message):
        coming_intent = intent_message.intent.intent_name
        if coming_intent == '&3a8gr9ZbNyA4GVLEvw1nreV9Z3jMl1zn5dYBXWw2:getVoltage':
            self.getVolts_callback(hermes, intent_message)
        elif coming_intent == '&3a8gr9ZbNyA4GVLEvw1nreV9Z3jMl1zn5dYBXWw2:turnOn':
            self.turnOn_callback(hermes, intent_message)
        elif coming_intent == '&3a8gr9ZbNyA4GVLEvw1nreV9Z3jMl1zn5dYBXWw2:turnOff':
            self.turnOff_callback(hermes, intent_message)
        elif coming_intent == '&3a8gr9ZbNyA4GVLEvw1nreV9Z3jMl1zn5dYBXWw2:getCurrent':
            self.getCurrent_callback(hermes, intent_message)
        elif coming_intent == '&3a8gr9ZbNyA4GVLEvw1nreV9Z3jMl1zn5dYBXWw2:getPower':
            self.getPower_callback(hermes, intent_message)
        elif coming_intent == '&3a8gr9ZbNyA4GVLEvw1nreV9Z3jMl1zn5dYBXWw2:getEnergy':
            self.getEnergy_callback(hermes, intent_message)
        elif coming_intent == '&3a8gr9ZbNyA4GVLEvw1nreV9Z3jMl1zn5dYBXWw2:setMaxCurrent':
            self.setMaxCurrent_callback(hermes, intent_message)


        # more callback and if condition goes here...

    # --> Register callback function and start MQTT
    def start_blocking(self):
        with Hermes(MQTT_ADDR) as h:
            h.subscribe_intents(self.master_intent_callback).start()


    def get_volts(self):
        try:
            voltage = instrument.read_register(0x0000, numberOfDecimals=1, functioncode=4, signed=False)
            return voltage
        except ValueError:
            return self.get_voltage()
        except IOError:
            return 0

    def get_current(self):
        try:
            current_low = instrument.read_register(0x0001, numberOfDecimals=0, functioncode=4, signed=False)
            current_high = instrument.read_register(0x0002, numberOfDecimals=0, functioncode=4, signed=False)
            current = (current_high << 8 | current_low)/1000.0
            return current
        except ValueError:
            return self.get_current()
        except IOError:
            return 0

    def get_power(self):
        try:
            power_low = instrument.read_register(0x0003, numberOfDecimals=0, functioncode=4, signed=False)
            power_high = instrument.read_register(0x0004, numberOfDecimals=0, functioncode=4, signed=False)
            power = (power_high << 8 | power_low)/10.0
            return power
        except ValueError:
            return self.get_power()
        except IOError:
            return 0

    def get_energy(self):
        try:
            energy_low = instrument.read_register(0x0005, numberOfDecimals=0, functioncode=4, signed=False)
            energy_high = instrument.read_register(0x0006, numberOfDecimals=0, functioncode=4, signed=False)
            energy = (energy_high << 8 | energy_low)
            return energy
        except ValueError:
            return self.get_energy()
        except IOError:
            return 0
        
    def monitorCurrent(self,intent_message,hermes,device,maxCurrent):
        while True:
            try:
                current_low = instrument.read_register(0x0001, numberOfDecimals=0, functioncode=4, signed=False)
                current_high = instrument.read_register(0x0002, numberOfDecimals=0, functioncode=4, signed=False)
                current = (current_high << 8 | current_low)
                if current > maxCurrent :
                    reply = "Max Current Reached. Turning "+str(device) + " off"
                    gpio.output(4, gpio.HIGH)
                    hermes.publish_start_session_notification(intent_message.site_id, reply,"Surangani_app")
                    hermes.publish_end_session(intent_message.session_id, reply)
                    break


            except ValueError:
                pass
            except IOError:
                pass


    

if __name__ == "__main__":
    Surangani_app()
