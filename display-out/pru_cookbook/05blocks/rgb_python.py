#!/usr/bin/env python3
import Adafruit_BBIO.GPIO as GPIO

# Define which functions are connect to which pins
OE="P9_31"      # Output Enable, active low
LAT="P9_29"     # Latch, toggle after clocking in a row of pixels
CLK="P9_30"     # Clock, toggle after each pixel

# Input data pins 
R1="P8_45"  # R1, G1, B1 are for the top rows (1-16) of pixels
G1="P8_46"
B1="P8_43"

R2="P8_44"   # R2, G2, B2 are for the bottom rows (17-32) of pixels
G2="P8_41"
B2="P8_42"

LA="P9_28"  # Address lines for which row (1-16 or 17-32) to update
LB="P9_42"
LC="P9_27"
LD="P9_41"

# Set everything as output ports
GPIO.setup(OE,  GPIO.OUT)
GPIO.setup(LAT, GPIO.OUT)
GPIO.setup(CLK, GPIO.OUT)

GPIO.setup(R1, GPIO.OUT)
GPIO.setup(G1, GPIO.OUT)
GPIO.setup(B1, GPIO.OUT)
GPIO.setup(R2, GPIO.OUT)
GPIO.setup(G2, GPIO.OUT)
GPIO.setup(B2, GPIO.OUT)

GPIO.setup(LA, GPIO.OUT)
GPIO.setup(LB, GPIO.OUT)
GPIO.setup(LC, GPIO.OUT)
GPIO.setup(LD, GPIO.OUT)

GPIO.output(OE,  0)     # Enable the display
GPIO.output(LAT, 0)     # Set latch to low

while True:
    for bank in range(64):
        GPIO.output(LA, bank>>0&0x1)    # Select rows
        GPIO.output(LB, bank>>1&0x1)
        GPIO.output(LC, bank>>2&0x1)
        GPIO.output(LD, bank>>3&0x1)
        
        # Shift the colors out.  Here we only have four different 
        # colors to keep things simple.
        for i in range(16):
            GPIO.output(R1,  1)     # Top row, white
            GPIO.output(G1,  1)
            GPIO.output(B1,  1)
            
            GPIO.output(R2,  1)     # Bottom row, red
            GPIO.output(G2,  0)
            GPIO.output(B2,  0)

            GPIO.output(CLK, 0)     # Toggle clock
            GPIO.output(CLK, 1)
    
            GPIO.output(R1,  0)     # Top row, black
            GPIO.output(G1,  0)
            GPIO.output(B1,  0)

            GPIO.output(R2,  0)     # Bottom row, green
            GPIO.output(G2,  1)
            GPIO.output(B2,  0)
    
            GPIO.output(CLK, 0)     # Toggle clock
            GPIO.output(CLK, 1)
    
        GPIO.output(OE,  1)     # Disable display while updating
        GPIO.output(LAT, 1)     # Toggle latch
        GPIO.output(LAT, 0)
        GPIO.output(OE,  0)     # Enable display
