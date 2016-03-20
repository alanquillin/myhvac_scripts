#!/usr/bin/python

import sys
sys.path.append('./lib')
from Adafruit_CharLCD import Adafruit_CharLCD
import pcf8574gpio as PCF

GPIO = PCF.Pcf8574Gpio(1, 0x38)

# Define PCF pins connected to the LCD.
lcd_rs        = 0
lcd_en        = 2
pins_db       = [4, 5, 6, 7]

# Instantiate LCD Display
lcd = Adafruit_CharLCD(lcd_rs, lcd_en, pins_db, GPIO=GPIO)
lcd.clear()

lcd.message('  Raspberry Pi\n  I2C LCD 0x20')

GPIO.cleanup()         # clean up
