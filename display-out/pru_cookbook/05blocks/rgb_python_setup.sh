#!/bin/bash
# Setup for 64x32 RGB Matrix
export TARGET=rgb1.pru0
echo TARGET=$TARGET

# Configure the PRU pins based on which Beagle is running
machine=$(awk '{print $NF}' /proc/device-tree/model)
echo -n $machine
if [ $machine = "Black" ]; then
    echo " Found"
    gpiopins="P8_41 P8_42 P8_43 P8_44 P8_45 P8_46"
    prupins="P9_28 P9_92 P9_27 P9_91 P9_29 P9_30 P9_31"
    gpionums="70 71 72 73 74 75 113 114 115 116 111 110 112"
elif [ $machine = "Blue" ]; then
    echo " Found"
    pins=""
elif [ $machine = "PocketBeagle" ]; then
    echo " Found"
    prupins="P2_32 P1_31 P1_33 P1_29 P2_30 P2_34 P1_36"
    gpiopins="P2_10 P2_06 P2_04 P2_01 P2_08 P2_02"
    # Uncomment for J2
    # gpiopins="$gpiopins P2_27 P2_25 P2_05 P2_24 P2_22 P2_18"
else
    echo " Not Found"
    pins=""
fi

for pin in $prupins
do
    echo $pin
    # config-pin $pin pruout
    config-pin $pin gpio
    config-pin -q $pin
done

for pin in $gpiopins
do
    echo $pin
    config-pin $pin gpio
    config-pin -q $pin
done
for number in $gpionums
do 
    echo $number
    echo out > /sys/class/gpio/gpio$number/direction
done