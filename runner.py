#from subprocess import Popen, PIPE
import subprocess
import sys
from collections import defaultdict
from parser import TestParser
import asyncio
import itertools as it

def usage():
    print("""
        python runner.py <location_of_rvs_binary>
        """)

if __name__ == "__main__":
    asyncio.run(mainfun())

async def taskgenerator(listdict,queue):
    for lst in listdict:
         await queue.put(lst)
    
async def mainfun():
    if len(sys.argv) == 1:
        usage()
        sys.exit()
    testcases = [
        { 
            'name' : 'gpustress-9000-sgemm-false',
            'device' : 'all',
            'module' : 'gst',
            'parallel' : 'false',
            'duration' : '10000',
            'ops_type' : 'sgemm',
            'target_stress' : '9000',
            'matrix_size_a' : '8640',
            'matrix_size_b' : '8640',
            'matrix_size_c' : '8640',
            'lda' : '8640',
            'ldb' : '8640',
            'ldc' : '8640'
        },
        { 
            'name' : 'gpustress-9000-sgemm-true',
            'device' : 'all',
            'module' : 'gst',
            'parallel' : 'true',
            'duration' : '10000',
            'ops_type' : 'sgemm',
            'target_stress' : '9000',
            'matrix_size_a' : '8640',
            'matrix_size_b' : '8640',
            'matrix_size_c' : '8640',
            'lda' : '8640',
            'ldb' : '8640',
            'ldc' : '8640'
        }
        ]
    print("ok")
    mod_dict = defaultdict(list)
    for item in testcases:
        mod_dict[item['module']].append(item)
    q = asyncio.Queue()
    prod = asyncio.create_task(taskgenerator(mod_dict,q)
    consumers =[asyncio.create_task(consumertask(module, q) for a in range(7))]
    await asyncio.gather(prod)
    await q.join()
    for c in consumers:
        c.cancel()
    #parser.parse(testcases)
    print("output file: "+parser.output_file)
    #f = open(parser.output_file, "w")
    #rvs = sys.argv[1]
    #ret = subprocess.call([rvs, '-c', str(parser.conf_file)], stdout=f)


async def consumertask(modulename, queue):
    while True:
        testcases = await queue.get() #list of dicts
        parser = TestParser("gst")
        parser.parse(testcases) #ensure return cfile,opfile explicitly
        print("output file: "+parser.output_file)
        f = open(parser.output_file, "w")
        proc = await asyncio.create_subprocess_exec(rvs,'-c',parser.conf_file,stdout=f)
        ret = await proc.wait()#wait for can help in timeout
        f.close()
        queue.task_done()
        return ret, opfile
