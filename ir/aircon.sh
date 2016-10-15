#!/bin/sh
SCRIPT_DIR=/home/pi/system/app/ir
sudo python $SCRIPT_DIR/json2signal.py $1
sudo service lirc stop
sudo service lirc start
irsend SEND_ONCE aircon json
