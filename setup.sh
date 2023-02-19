#!/bin/bash

# enable scan
echo 1 > /sys/bus/iio/devices/iio\:device0/scan_elements/in_voltage0_en
# set buffer size
echo 512 > /sys/bus/iio/devices/iio\:device0/buffer/length
# enable buffer
echo 1 > /sys/bus/iio/devices/iio\:device0/buffer/enable