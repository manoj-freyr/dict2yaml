import re
import sys
def usage():
	print("""
		python utils.py <conf filename>
		""")

def is_num_list(line):
	nlist = line.split()
	for num in nlist:
		if not num.isdecimal():
			return False
	return True

def is_float(numval):
	try:
		float(numval)
		return True
	except ValueError:
		return False

def alnum_parse(k,v, params):
	if v  == "all":
		params[k] = "all_or_list"
	elif v == "true" or v == "false":
		params[k] = "boolean"
	elif v.isalnum():
		params[k] = "alphanum"
	elif is_num_list(v):
			params[kv[0]] = "list"
	else:
		m = re.match(r"^[a-zA-Z]([\w -]*[a-zA-Z])?$", v)
		if m:
			params[k] = "alphanum"
		else:
			params[k] = "others"
		
def parse_line(line, params):
	line = line.strip('-')
	if line == "" or line.startswith('#') or line.startswith('actions:'):
		return
	if line == '\n':
		return
	kv = line.split(':')
	#print(kv)
	k = kv[0].strip()
	v = kv[1].strip()
	if v.isdecimal():
		params[k] = "number"
	elif is_float(v):
		params[k] = "float"
	else:
		alnum_parse(k, v, params)

def conf2dict(filename):
	with open(filename) as f:
		params = {}
		for line in f:
			parse_line(line, params)
	for key in params:
		print(key + ":" + params[key])

if __name__ == "__main__":
	if len(sys.argv) != 2:
		usage()
		sys.exit()
	conf2dict(sys.argv[1])
	
