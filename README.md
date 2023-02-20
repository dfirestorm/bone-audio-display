# bone-audio-display
takes audio input and displays it using an adafruit display



## audio input

for this project I used a MAX9418 on a breakout from Adafruit linked [here](https://www.adafruit.com/product/1713) 

 you could also use the MAX4466 linked [here](https://www.adafruit.com/product/1063) or any other single pin analog input source.

### wiring

**IMPORTANT NOTE** the analog input pins are 1.8v tolerant, not 3.3. most microphones including those above will be capable of more than that. use a voltage divider as necessary, I wired through a 1.5 with a 1.8 to ground. 

## display 
this should explain how this whole thing goes together
### wiring
use jumpers direct to pins. requires HDMI off since it uses those pins
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

### pin names and descriptions
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
