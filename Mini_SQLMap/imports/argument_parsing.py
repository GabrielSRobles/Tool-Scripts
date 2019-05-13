import argparse

def parameter_parsing():
	parser = argparse.ArgumentParser(description='Simple low level tool for mapping sql injections')
	parser.add_argument('--status_code','-sc', dest='status_code', default=200, type=int, help="Status code use to identify success requests")
	parser.add_argument('--base_url','-bu', dest='base_url', type=str, help="Base url from which include the SQLI payloads")
	parser.add_argument('--payload','-p', dest='payload', type=str, help='Payload to identify. Length is searched for and if found, its value is returned')
	parser.add_argument('--identify','-db_id', action='store_true', help='If set, identify whole database structure. Schemata, Tables and Columns')
	parser.add_argument('--value_length','-vl', dest='value_length', type=int, help='Set if the value of the payload to search is known')
	parser.add_argument('--known_start','-ks', dest='known_start', help='Set if the the initial section of the value to search is known')
	return parser.parse_args()