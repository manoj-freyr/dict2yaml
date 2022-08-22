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

async def taskgenerator(listdict,queue):
    for key in listdict:
         queue.put_nowait(listdict[key])
         print("taskgenerator put a testcase",listdict[key])
    
async def mainfun(testcases):
    #if len(sys.argv) == 1:
    #    usage()
    #    sys.exit()
    #print("ok")
    mod_dict = defaultdict(list)
    testcase_dict = defaultdict(list)
    for item in testcases:
        mod_dict[item.TestParams['module']].append(item.TestParams)
        testcase_dict[item.TestParams['module']].append(item)
    print("size of dict is ",len(mod_dict))
    q = asyncio.Queue()
    loop = asyncio.get_event_loop()
    
    prod = loop.create_task(taskgenerator(mod_dict,q))
    consumers = []
    await prod
    for a in range(2):
        consumers.append(loop.create_task(consumertask(q, a, testcase_dict)))
    await q.join()
    for c in consumers:
        print("before cancelling consumer")
        ret, ofile = await c
        c.cancel()
        print("output file: "+ ofile)
        print("result: "+ str(ret))
    print("ALL done")

def notifier(tclist, opfile):
    if len(tclist) == 0:
        return
    for tc in tclist:
        tc.SetLogFile(opfile)
        tc.SetStatus("Executed")
    tclist[0].Notify()

async def consumertask(queue, idx, tcdict):
    while True:
        print("consumer idx", idx)
        try:
            #testcases = await queue.get_nowait() #list of dicts
            testcases = queue.get_nowait() #list of dicts
            mod_name = testcases[0]['module']
            print("got a testcase consumer ",mod_name) 
            parser = TestParser(mod_name)
            testIdList = parser.parse(testcases) #ensure return cfile,opfile explicitly
            print("output file: "+parser.output_file)
            rvs = sys.argv[1]
            proc = await asyncio.create_subprocess_exec(rvs,'-c',parser.conf_file,'-l',parser.output_file)
            ret = await proc.wait()#wait for can help in timeout
            queue.task_done()
            notifier(tcdict[mod_name], parser.output_file)
            return ret, parser.output_file

        except asyncio.CancelledError:
            print("coro cancelled from caller, all assigned tasks completed")
            return -1, ""
        except asyncio.QueueEmpty:
            return -1, "empty queue of tasks"

if __name__ == "__main__":
    testcases = [
        {
            'name' : 'gpustress-9000-sgemm-false',
            'device' : '6059',
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
            'name': 'action_1',
            'device': 'all',
            'module': 'iet',
            'parallel': 'true',
            'count': '1',
            'duration': '50000',
            'ramp_interval': '5000',
            'sample_interval': '700',
            'log_interval': '700',
            'max_violations': '1',
            'target_power': '180',
            'tolerance': '0.06',
            'matrix_size': '8640',
            'ops_type': 'dgemm'
        }
        ]

    loop = asyncio.get_event_loop()
    # server address id the UDS
    loop.run_until_complete(mainfun(testcases))

def execute_main(testcases):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(mainfun(testcases))
