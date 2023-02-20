//Black - Not tested
// These are from https://github.com/FalconChristmas/fpp/blob/master/src/pru/PocketScrollerV1.hp
// _gpio tells which gpio port and _pin tells which bit in the port
// The first 1 in r11 is for the J1 connector
// See the githuub file for the other connectors

#define r11_gpio 2
#define r11_pin (0x1<<6)
#define g11_gpio 2
#define g11_pin (0x1<<7)
#define b11_gpio 2
#define b11_pin (0x1<<8)

#define r12_gpio 2
#define r12_pin (0x1<<9)
#define g12_gpio 2
#define g12_pin (0x1<<10)
#define b12_gpio 2
#define b12_pin (0x1<<11)

#define pru_latch (0x1<<1)	// These are the bit positions in R30
#define pru_oe    (0x1)
#define pru_clock (0x1<<2)

// Control pins are all in GPIO2
// The pocket has these on R0, the code needs to be changed for this work work
#define pru_sel0 3 /* must be sequential with sel1 and sel2 */
#define pru_sel1 4
#define pru_sel2 5
#define pru_sel3 6
#define pru_sel4 7
