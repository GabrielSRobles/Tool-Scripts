import sys

def write_val(val):
	sys.stdout.write(val)
	sys.stdout.flush()
	
def overwrite(value,prev_value):
	erase_value(prev_value)
	write_val("%s" % value)

def clean(value):
	erase_value(value)
	write_val(" " * len(str(value)))

def erase_value(value):
	write_val("%s" % "\b"*len(str(value)))
	write_val("%s" % " "*len(str(value)))
	write_val("%s" % "\b"*len(str(value)))	