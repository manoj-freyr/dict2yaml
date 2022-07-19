from parser import TestParser

if __name__ == "__main__":
	print("hello")
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
			'matrix_size_a' : '10000',
			'matrix_size_b' : '10000',
			'matrix_size_c' : '10000',
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
			'matrix_size_a' : '10000',
			'matrix_size_b' : '10000',
			'matrix_size_c' : '10000',
			'lda' : '8640',
			'ldb' : '8640',
			'ldc' : '8640'
		}
		]
	parser.parse(testcases)
	print("done")

