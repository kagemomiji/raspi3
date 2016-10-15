#ir script description
*test_file: test json file for json2signal.py
*aircon.sh
script for ir signal generate and send signal by lirc
**json2signal.py
generator for ir_signal from setting and format json
usage sudo python json2signal.py <setting json file>
dependency:rev_git.py
caution:it will overwrite /etc/lirc/lircd.conf
*decode_ir.py
script for decode signal from lirc's script 'mode2' format file
dependency:rev_git.py
