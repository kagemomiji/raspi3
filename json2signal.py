# coding:utf-8
		
#import mod
import json
import sys
import rev_bit

##################################
#initialize
##################################
	

#check argvs
argvs = sys.argv
argc = len(argvs)
if(argc !=2):
	print 'Usage: #python %s filename' % argvs[0]
	quit()

#set local value
SIGNAL_LIB_DIR = "./lib/"

##################################
#load setting
##################################
try:
	s = open(argvs[1],'r')
	set_data = json.load(s)
	data = set_data["data"]
except ValueError:
	print 'setting json format error'
	s.close()
	quit()
except IOError:
	print 'No Such File or Directory %s' %(argvs[1])
	quit()
except NameError:
	print 'Unknown format of setting %s' %(argvs[1])
	s.close()
	quit()
except :
	print 'Unexpected error:',sys.exc_info()[0]
	quit()
#print json.dumps(set_data,sort_keys = True, indent = 4)

##################################
#load format
##################################
format_file = set_data["format_id"] + ".json"
f = open(SIGNAL_LIB_DIR + format_file,'r') 
format = json.load(f)

# print json.dumps(format,sort_keys = True, indent = 4)

##################################
#convert setting to binary signal
##################################

#initialize
signal = format["signal"]
rule = signal["rule"]
format_type = format["type"]
bin_signal = ''

#convert setting to binary signal
for frame in signal["frame"]:
	bin_signal = bin_signal+'L'
	bitmap = frame["bitmap"]
	raw_signal = []
	for i in xrange(len(bitmap)):
		val = frame["value"][i].split("+")	
		sig = 0
		for j in xrange(len(val)):
			#append fixed_bit
			if '0x' in val[j]:
				sig = sig + int(val[j],16) << bitmap[i][j]
			#append setting_bit
			elif val[j] in rule.keys():
				sig = sig + int(rule[val[j]][data[val[j]]],16)<<bitmap[i][j]				
			#append error_check_bit
			elif val[j] == 'sum':
				sig = reduce(lambda x,y:x+y,raw_signal) & 0x0ff				
			else:
				sig = sig + data[val[j]] << bitmap[i][j]	

		#append new signal
		raw_signal.append(sig)
		bin_signal = bin_signal + bin(rev_bit.reverse_bit8(sig)).replace('0b','').zfill(8)
		
	if format_type == 'AEHA':
		#append tracer tag 
		bin_signal = bin_signal + 'T'

	#debug
	#print map(hex,raw_signal)
		
#print bin_signal

###################################
#convert binary signal to ir_signal
###################################

#initialize 
T = signal["T"]
ir_signal = ''

#AEHA format setting
if format_type == 'AEHA':
	trailer_t = signal["trailer_t"]

	for i in xrange(len(bin_signal)):
		#append 0
		if bin_signal[i] == '0':
			ir_signal = ir_signal + 'pulse ' + str(T) + '\nspace ' + str(T) + '\n'
		#append 1
		elif bin_signal[i] == '1':
			ir_signal = ir_signal + 'pulse ' + str(T) + '\nspace ' + str(3*T)+ '\n'
		#append Leader 
		elif bin_signal[i] == 'L':
			ir_signal = ir_signal + 'pulse ' + str(8*T) + '\nspace ' + str(4*T)+ '\n'
		#append Trailer
		elif bin_signal[i] == 'T':
			ir_signal = ir_signal + 'pulse ' + str(T) + '\nspace ' + str(trailer_t) + '\n'
print ir_signal

##################################
# finish
##################################
s.close()
f.close()
