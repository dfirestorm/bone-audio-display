#!/usr/bin/python3
#//////////////////////////////////////
#	analogInContinuous.py
# 	Read analog data via IIO continous mode and plots it.
#//////////////////////////////////////

# From: https://stackoverflow.com/questions/20295646/python-ascii-plots-in-terminal
# https://github.com/dkogan/gnuplotlib
# https://github.com/dkogan/gnuplotlib/blob/master/guide/guide.org
# sudo apt install gnuplot  (10 minute to install)
# pip3 install gnuplotlib
# This uses X11, so when connecting to the bone from the host use:  ssh -X bone

# See https://elinux.org/index.php?title=EBC_Exercise_10a_Analog_In#Analog_in_-_Continuous.2C_Change_the_sample_rate
# for instructions on changing the sampling rate.  Can go up to 200KHz.

import numpy      as np
import time,smbus

IIOPATH='/sys/bus/iio/devices/iio:device0'
IIODEV='/dev/iio:device0'
LEN = 960
SAMPLERATE=96000
AIN='1'
I2C_BUS = 2
I2C_ADDRESS = 0x70
DISP_WIDTH=8
DISP_HEIGHT=8

BUCKET_OFFSET = 1 # number of low-frequency buckets to ignore
SAMPLE_OFFSET = 11 # number of low-frequency samples to ignore when making buckets
MIC_OFFSET=20 # dB to increase raw input by
MIN_DB = -50 # below this should not display
MAX_DB = 5 # above this will be the full height of the display

# Setup IIO for Continous reading
# Enable AIN
try:
    file1 = open(IIOPATH+'/scan_elements/in_voltage'+AIN+'_en', 'w')
    file1.write('1') 
    file1.close()
except:     # carry on if it's already enabled
    pass
# Set buffer length
file1 = open(IIOPATH+'/buffer/length', 'w')
file1.write(str(2*LEN))     # I think LEN is in 16-bit values, but here we pass bytes
file1.close()
# Enable continous
file1 = open(IIOPATH+'/buffer/enable', 'w')
file1.write('1')
file1.close()

fd = open(IIODEV, "r")

# set up matrix 
# The first byte is GREEN, the second is RED.
output = [0x00, 0xFF, 0xFF, 0xFF, 0xFF, 0x00, 0x00, 0x00, 0x00,
0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
bus = smbus.SMBus(I2C_BUS)  # Use i2c bus 2
matrix = I2C_ADDRESS         # Use address 0x70

bus.write_byte_data(matrix, 0x21, 0)   # Start oscillator (p10)
bus.write_byte_data(matrix, 0x81, 0)   # Disp on, blink off (p11)
bus.write_byte_data(matrix, 0xe7, 0)   # Full brightness (page 15)
bus.write_i2c_block_data(matrix, 0, output)

print('Hit ^C to stop')

win = np.hamming(LEN)
vals = np.linspace(MIN_DB,MAX_DB,DISP_WIDTH)
try:
    while True:
        y = np.fromfile(fd, dtype='uint16', count=LEN)*1.8/4096
        sp = np.fft.rfft(y)
        # Scale the magnitude of FFT by window and factor of 2,
        # because we are using half of FFT spectrum.
        s_mag = np.abs(sp) * 2 / np.sum(win)

        # Convert to dBFS
        s_dB = 20 * np.log10(s_mag)
        s_dbfs = s_dB + MIC_OFFSET
        # generate buckets, one per display column
        buckets = []
        # 0hz bucket
        buckets.append(s_dB[0])
        # make buckets for the FFT values, take the highest value from the bucket
        bucket_indices = np.geomspace(SAMPLE_OFFSET,len(s_dbfs), DISP_WIDTH+1+BUCKET_OFFSET)
        for k in range(BUCKET_OFFSET,DISP_WIDTH+BUCKET_OFFSET):
            val = np.amax(s_dbfs[int(np.floor(bucket_indices[k])):int(np.ceil(bucket_indices[k+1]))])
            buckets.append(val) 
        # get rid of 0 Hz bucket
        display_val=buckets[1:DISP_WIDTH+1]
        # print(display_val) # bugfixing or display the dB values that the buckets are using
        # make matrix to be displayed
        for k in range(DISP_WIDTH):
            mag = display_val[k]
            # print(mag, vals[6],vals[4])
            if mag < vals[int(DISP_HEIGHT*0.75)]: # green side if under 75%
                for j in range(DISP_HEIGHT):
                    # print(vals[j],mag) # bugfixing - display the magnitude of the input vs the bucket being compared to
                    if mag < vals[0]: # no output for below min dB
                         output[2*k] = 0x0
                    if mag > vals[j]: # turn on highest value reached
                        output[2*k] = (2**(j+1))-1 
            else: # no output for below min dB
                output[2*k] = 0x0
            if mag > vals[int(DISP_HEIGHT*0.5)]: # red side if over 50% 
                for i in range(DISP_HEIGHT):
                    # print(vals[i],mag) # bugfixing - display the magnitude of the input vs the bucket being compared to
                    if mag > vals[i]: # turn on highest value reached
                        output[1+2*k] = (2**(i+1))-1
            else: # no output for below min dB
                output[1+2*k] = 0x0
                        
            
        # print(output) # bugfixing - display the magnitude of the input buckets
        bus.write_i2c_block_data(matrix, 0, output) # write to display
            



except KeyboardInterrupt:
    print("Turning off input.")
    # Disable continous
    file1 = open(IIOPATH+'/buffer/enable', 'w')
    file1.write('0')
    file1.close()
    
    file1 = open(IIOPATH+'/scan_elements/in_voltage'+AIN+'_en', 'w')
    file1.write('0') 
    file1.close()

# // Bone  | Pocket | AIN
# // ----- | ------ | --- 
# // P9_39 | P1_19  | 0
# // P9_40 | P1_21  | 1
# // P9_37 | P1_23  | 2
# // P9_38 | P1_25  | 3
# // P9_33 | P1_27  | 4
# // P9_36 | P2_35  | 5
# // P9_35 | P1_02  | 6