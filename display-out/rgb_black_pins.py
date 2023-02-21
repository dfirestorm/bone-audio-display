#Black - Not tested
# These are from https:#github.com/FalconChristmas/fpp/blob/master/src/pru/PocketScrollerV1.hp
# _gpio tells which gpio port and _pin tells which bit in the port
# The first 1 in r11 is for the J1 connector
# See the githuub file for the other connectors

d_r11 = (0x1<<6)
d_g11 = (0x1<<7)
d_b11 = (0x1<<8)
d_r12 = (0x1<<9)
d_g12 = (0x1<<10)
d_b12 = (0x1<<11)

d_latch = (0x1<<15)	# These are the bit positions in gpio3
d_oe = (0x1<<14)
d_clock = (0x1<<16)

# Control pins are all in GPIO3
# The pocket has these on R0, the code needs to be changed for this work work
d_selA = (0x1<<17) # must be sequential with sel1 and sel2 
d_selB = (0x1<<18)
d_selC = (0x1<<19)
d_selD = (0x1<<20)