from os import listdir
from os.path import isfile, join
import sys
import re


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

mypath = sys.argv[1]
print mypath

onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]


baseline = ''
with open(mypath  + '../' + 'baseline.eml') as baseline:
	baseline = baseline.read()
for idx,file in enumerate(onlyfiles):
	print 'Working with file %s' % file
	with open(mypath + '/' + file) as check_file: 
		for line, base in zip(check_file, baseline.split('\n')):
			line =  line.strip().replace('\n','')
			base = base.strip().replace('\n','')
			if line != base:
 				print bcolors.FAIL +  line + bcolors.ENDC
 				print bcolors.OKGREEN + base + bcolors.ENDC
 		print 'Displaying file %i/%i' % (idx+1,len(onlyfiles))
 		comand = raw_input('Press Enter to continue, o to open file. Can add regex after the o\n')
 		
 		# --PROOFPOINT_BOUNDARY_2(.*)--PROOFPOINT_BOUNDARY_2--
 		if len(comand) and comand[0] == 'o':
 			comand = comand[1:].strip()
 			check_file.seek(0,0)
 			text = check_file.read() 
 			if comand:
 				r = re.compile(comand,re.DOTALL)
 				print r.search(text).group(1)
 			else:
 				print text
 			raw_input('Press Enter to continue\n')
 	print('\n' * 50)