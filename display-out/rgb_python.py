#!/usr/bin/env python3

try:
  from mmap import mmap
except ImportError: 
  print("Must be run as root, try again with sudo")
import time,struct
from rgb_black_pins import *

GPIO1_offset = 0x4804c000
GPIO1_size = 0x4804cfff-GPIO1_offset
GPIO2_offset = 0x481A_C000
GPIO3_offset = 0x481A_E000
GPIO_OE = 0x134
GPIO_SETDATAOUT = 0x194
GPIO_CLEARDATAOUT = 0x190

with open("/dev/mem", "r+b" ) as f2:
    mem2 = mmap(f2.fileno(), GPIO1_size, offset=GPIO2_offset)
packed_reg2 = mem2[GPIO_OE:GPIO_OE+4]
reg_status2 = struct.unpack("<L", packed_reg2)[0]
reg_status2 &= ~(d_r11|d_g11|d_b11|d_r12|d_g12|d_b12)
mem2[GPIO_OE:GPIO_OE+4] = struct.pack("<L", reg_status2)

with open("/dev/mem", "r+b" ) as f3:
    mem3 = mmap(f3.fileno(), GPIO1_size, offset=GPIO3_offset)
packed_reg3 = mem3[GPIO_OE:GPIO_OE+4]
reg_status3 = struct.unpack("<L", packed_reg3)[0]
reg_status3 &= ~(d_latch|d_oe|d_clock|d_selA|d_selB|d_selC|d_selD)
mem3[GPIO_OE:GPIO_OE+4] = struct.pack("<L", reg_status3)
try:
    while True:
        for bank in range(64):
            load = bank%16
            mem3[GPIO_CLEARDATAOUT:GPIO_CLEARDATAOUT+4] = struct.pack("<L", 0xF<<17)
            mem3[GPIO_SETDATAOUT:GPIO_SETDATAOUT+4] = struct.pack("<L", load << 17)     # Select rows 
            
            # Shift the colors out.  Here we only have four different 
            # colors to keep things simple.
            for i in range(16):
                mem2[GPIO_SETDATAOUT:GPIO_SETDATAOUT+4] = struct.pack("<L", d_b11|d_g12) 
                mem2[GPIO_CLEARDATAOUT:GPIO_CLEARDATAOUT+4] = struct.pack("<L", d_r11|d_g11|d_r12|d_b12)

                mem3[GPIO_SETDATAOUT:GPIO_SETDATAOUT+4] = struct.pack("<L", d_clock)     # toggle clock
                mem3[GPIO_CLEARDATAOUT:GPIO_CLEARDATAOUT+4] = struct.pack("<L", d_clock)
        
        mem3[GPIO_SETDATAOUT:GPIO_SETDATAOUT+4] = struct.pack("<L", d_oe|d_latch)     # toggle latch and OE
        mem3[GPIO_CLEARDATAOUT:GPIO_CLEARDATAOUT+4] = struct.pack("<L", d_oe|d_latch)
except KeyboardInterrupt:
  mem2.close()
  mem3.close()
