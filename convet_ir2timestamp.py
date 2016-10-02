#coding: utf-8
import csv
import sys

#import module
import csv

#get argv
param = sys.argv

# csv
reader = csv.reader(open(param[1],'r'),delimiter=' ')
writer = csv.writer(open(param[1]+'_timestamp.csv','wb'))

time=0
for data in reader:
	if data[0] == 'space':
	 bit = 0
	else:
	 bit = 1
	writer.writerow([time+1,bit])
	time = time + int(data[1])
	writer.writerow([time,bit])
	
