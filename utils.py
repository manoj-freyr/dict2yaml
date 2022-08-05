import re
import sys
import testcase
import os.path 
#rvsloc = "/opt/rocm/share/rocm-validation-suite/conf/"
rvsloc = "/home/taccuser/PRs/RVS/ROCmValidationSuite/rvs/conf/"
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

def get_kv(line):
    line = line.strip('-')
    kv = line.split(':')
    return kv[0].strip(), kv[1].strip()

def parse_configline(line, testlist, paramdict):
    line = line.strip()
    #print(line)
    if line == "" or line.startswith('#') or line.startswith('actions:'):
        return  
    if line == '\n':
        return  
    if(line.startswith('-')):
        if(len(paramdict) != 0):
            mod = paramdict['module']
            # handle error here if module not present
            t = testcase.TestCase(mod,paramdict,"DefaultFeature")
            #print(paramdict)
            #t.update_dict(paramdict)
            #print(t)
            testlist.append(t)
            paramdict.clear()
    k,v = get_kv(line)
    paramdict[k] = v

def parse_cfile(fname):
    tlist = []
    pdict = {}
    fname = rvsloc+fname
    if not os.path.isfile(fname):
        return tlist 
    with open(fname) as f:
        for line in f:
            parse_configline(line,tlist,pdict)
    if(len(pdict) != 0):
        t = testcase.TestCase(pdict['module'], pdict,"DefaultFeature")
        tlist.append(t)
    return tlist

def testcase_list():
    testlist = []
    with open("modules.txt") as f:
        for line in f:
            lst = parse_cfile(line.strip())
            if(len(lst) != 0):
                testlist.extend(lst)
    return testlist

if __name__ == "__main__":
	#if len(sys.argv) != 2:
	#	usage()
	#	sys.exit()
	#conf2dict(sys.argv[1])
  tt = testcase_list()
  print(len(tt))
  print("the list is as below")
  for item in tt:
      print(item)	
