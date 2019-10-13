#!/bin/sh -e
#
# rc.local
#
# This script is executed at the end of each multiuser runlevel.
# Make sure that the script will "exit 0" on success or any other
# value on error.
#
# In order to enable or disable this script just change the execution
# bits.
#
# By default this script does nothing.

#/usr/bin/wvdial &
sudo pppd call gprs &
sudo create_ap -n wlan0 pi raspberry &
sleep 30
sudo python /home/pi/quad/quad.py &
sudo python /home/pi/quad/quad_video.py &
 
#sudo route add -net 0.0.0.0 ppp0


exit 0

