#from subprocess import Popen, PIPE
import subprocess
import sys
from parser import TestParser

def usage():
    print("""
        python runner.py <location_of_rvs_binary>
        """)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        usage()
        sys.exit()
    parser = TestParser("gst")
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
    parser.parse(testcases)
    print("output file: "+parser.output_file)
    f = open(parser.output_file, "w")
    rvs = sys.argv[1]
    ret = subprocess.call([rvs, '-c', str(parser.conf_file)], stdout=f)


