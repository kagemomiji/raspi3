#coding: utf-8

#import module
import csv
import sys
import rev_bit

#get argv
param = sys.argv

# csv
reader = csv.reader(open(param[1],'r'),delimiter=' ')
writer = csv.writer(open(param[1]+'_format.csv','wb'))

#set local val
T = 436.0			#ir data length T(micro sec) 

#initialize
data_counter = 0		#data_number
leader_flag = 0			#leader flag 0:false 1:pulse detected 2:pulse+spacedetected

for row in reader:
	#detect pulse length
	length = int(round(int(row[1])/T))
	#detect leader
	if row[0] == 'pulse' and length == 8:
		leader_flag = 1	#8length pulse detect
	if row[0] == 'space' and length == 4 and leader_flag == 1:
		leader_flag = 2 #leader_detect
		data_counter = 0
		frame = []
		datum = 0
		pulse_flag = 0

	#detect frame
	if leader_flag == 2:
		if row[0] == 'pulse' and length == 1:
			data_counter = data_counter + 1
			pulse_flag = 1
		if row[0] == 'space' and pulse_flag:
		#	print "%d,%d" % (data_counter, length)
			#pulse_flag off
			pulse_flag = 0
			
			#detect bit on/off/tracer
			if length == 1:
				bit = 0
			elif length == 3:
				bit = 1
			elif length == 23:
				data_str = [hex(x) for x in frame]
				writer.writerow(data_str)
				writer.writerow(["tracer"])
			else:
				data_str = [hex(x) for x in frame]
				writer.writerow(data_str)

			datum = datum << 1 | bit
			 
			
			#detect 4bit datum(parity, data0)
			if data_counter == 20 or data_counter == 24:
				frame.append(rev_bit.reverse_bit4(datum))	
				datum = 0
			#detect 8bit datum(customer, data1~)	
			elif data_counter % 8 == 0:
				frame.append(rev_bit.reverse_bit8(datum))
				datum=0

	
			
data_str = [hex(x) for x in frame]
writer.writerow(data_str)
#	writer.writerow([time+1,bit])
#	time = time + int(data[1])
#	writer.writerow([time,bit])
	
	
