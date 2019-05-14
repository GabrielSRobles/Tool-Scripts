import sys
import os
import base64
import binascii
import requests

base_url = "http://35.196.135.216/daa1793873/?post=%s"

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

def decipher_me(cipher_text):
	cipher_texts = chunks(cipher_text,16)
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
 	return ''.join(result)

def cipher_me(plain_text):
	plain_texts = chunks(plain_text,16)
	known_ciphers = ['\x00' * 16 ]			
	for idx, text in enumerate(reversed(plain_texts)):
		if idx == len(plain_texts):
			continue
		known_values = []
		while len(known_values) < len(text):
 			known_values = find_me_the_imv(known_ciphers[0],known_values)
 			print known_values
		known_ciphers.insert(0,xor_me(known_values,map(lambda x: ord(x), text)));
		print known_ciphers 
	return known_ciphers


plain_text = '{"flag": "^FLAG^b8c2e8ad43fe55ac737d4d3b41a7c0d284b7b771a86889b90255151d63fa9275$FLAG$", "id": "1", "key": "iOAGDTTk1YTochGAvnDPvg~~"}\n\n\n\n\n\n\n\n\n\n'
cipher_blocks = cipher_me(plain_text)
print b64e(''.join(cipher_blocks))