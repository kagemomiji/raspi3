#coding: utf-8
def reverse_bit8(x):
	x = ((x & 0x55) << 1) | ((x & 0xAA) >> 1)
	x = ((x & 0x33) << 2) | ((x & 0xCC) >> 2)
	return ((x & 0x0F) <<4 | x >> 4)

def reverse_bit4(x):
	x = ((x & 0x5) << 1) | ((x & 0xA) >> 1)
	x = ((x & 0x3) << 2) | ((x & 0xC) >> 2)
	return x

