# bone-audio-display
takes audio input and displays it using an adafruit display. 

## install and operation
install.sh will install smbus and numpy, which are required to run the code. The main code is in main.py, with some other files that may help troubleshoot issues in the other folders. 
to run, just run ./main.py , and use ctrl-c to stop. 

The way it works is by using the industrial io system on the beaglebone to generate a 96kHz audio signal, making a 481-point FFT of it with numpy, then splitting that FFT into a number of buckets according to the display width. The relative magnitude of the highest point in each bucket to the minimum and maximum determines its height, and that height relative to the display maximum height determines its color. 

## other sites
This project is also on hackster.io as [audio spectrum display](https://www.hackster.io/donald-hau/beagleboard-audio-spectrum-display-6a0568) and elinux.org as [audio spectrum display](https://elinux.org/ECE434_Project_-_Audio_Spectrum_Display). Check those out for more info.

## audio input

for this project I used a MAX9418 on a breakout from Adafruit linked [here](https://www.adafruit.com/product/1713) 

 you could also use the MAX4466 linked [here](https://www.adafruit.com/product/1063) or any other single pin analog input source. 

### wiring

**IMPORTANT NOTE** the analog input pins are 1.8v tolerant, not 3.3. most microphones including those above will be capable of more than that. use a voltage divider as necessary, I wired through a 1.5k with a 1.8k to ground as I was running my microphones on 3.3V. 

It should be connected to AIN 1, on P9_40, with the AIN GND on pin 34 connected across whatever output it has. 

## display 
I initially wanted this to work with the 64x32 LED matrix linked [here](https://www.adafruit.com/product/2278) but it was not working well. The code relating to that display is in the display-out folder, with modified versions of Dr. Mark Yoder's PRU code in display-out/pru-cookbook/05blocks. 

Instead, what I used was the 8x8 bicolor LED matrix available from adafruit, found [here](https://www.adafruit.com/product/902). This is wired to i2c bus 2 on P9_19 and P9_20. This is easily modifiable by going into main.py and changing the variables at the top of the code. 

If one was to get the other display working, the code is set up to output an array with hex values for each column, one bit for each LED in the column and two hex values per column. The first hex value is green and the second is red, combining to make yellow between 50 and 75% of the maximum volume. The integration would need to send this array to the display to be output in the correct order.  It assumes the 0,0 is in the bottom right of the display so that may be a desired change for a future user. As well, the setup of the display would need to be updated if the array size would be different as the initial array is hard coded and it only gets modified as the code runs. 

### wiring of 64x32 matrix
use jumpers direct to pins. requires HDMI off since it uses those pins. If you get this working, note it does require a connection between the bone ground and its own 5V supply (the bone's 5V is 1A limited and this requires closer to 4A)

| bone pin | display pin | display pin | bone pin |
| -------- | ----------- | ----------- | -------- |
| P8_44 | R1 | G1 | P8_46 |
| P8_43 | B1 | GND | GND | 
| P8_44 | R2 | G2 | P8_41 |
| P8_42 | B2 | GND | GND |
| P9_28 | A | B | P9_42B |
| P9_27 | C | D | P9_41B |
| P9_30 | CLK | LAT | P9_29 |
| P9_31 | OE | GND | GND |

#### pin names and descriptions
| Pin Group | Display pin | Bone Pin | Bone GPIO | Bone GPIO number | R30 number |
| --------- | ----------- | -------- | --------- | ---------------- | ---------- |
| Upper RGB Data | R1 | P8_45 | gpio2[6] | 70 | - |
| Upper RGB Data | G1 | P8_46 | gpio2[7] | 71 | - |
| Upper RGB Data | B1 | P8_43 | gpio2[8] | 72 | - |
| Lower RGB Data | R2 | P8_44 | gpio2[9] | 73 | - |
| Lower RGB Data | G2 | P8_41 | gpio2[10] | 74 | - |
| Lower RGB Data | B2 | P8_42 | gpio2[11] | 75 | - |
| Row Select Lines | A | P9_28 | gpio3[17] | 113 | 3 |
| Row Select Lines | B | P9_42B | gpio3[18] | 114 | 4 |
| Row Select Lines | C | P9_27 | gpio3[19] | 115 | 5 |
| Row Select Lines | D | P9_41B | gpio3[20] | 116 | 6 |
| Latch | LAT | P9_29 | gpio3[15] | 111 | 1 |
| Output Enable | OE | P9_31 | gpio3[14] | 110 | 0 |
| Clock | CLK | P9_30 | gpio3[16] | 112 | 2 |
