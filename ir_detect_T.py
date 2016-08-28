#coding: utf-8

#import module
import csv
import sys

#get argv
param = sys.argv

reader = csv.reader(open(param[1], 'r'), delimiter=' ')

hist = [0] * 100
sum = [0] * 100
for row in reader:
	#make histgram
	length = int(row[1])
	if row[0] == 'pulse' and length <= 10000:
		hist[length/100] = hist[length/100] + 1
		sum[length/100] = sum[length/100] + length

# calc 1T
index = hist.index(max(hist))
T = sum[index]/hist[index]

# detect 8T
tmp_hist=[]
for x in range((index-1)*8,(index+1)*8+1):
	tmp_hist.append(hist[x])
tmp_index = tmp_hist.index(max(tmp_hist))
index = hist.index(tmp_hist[tmp_index])
T8 = sum[index]/hist[index]

#remove delay of rising up and falling
true_T = (T8-T)/7
print 'T= %d'%(true_T)
