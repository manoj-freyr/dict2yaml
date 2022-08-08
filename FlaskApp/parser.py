import time
class TestParser:
    def __init__(self, modulename):
        time_stamp = time.time()
        self.mod_name = modulename
        self.conf_file= "/tmp/manoj/"+self.mod_name+str(time_stamp)+".conf"
        self.output_file= "/tmp/manoj/"+self.mod_name+str(time_stamp)+".txt"
        try:
            self.fileobj = open(self.conf_file, 'a')
        except OSError as e:
            print("error")
            raise Exception(" error opening file" + self.conf_file) from e
        self.add_init()

    def add_init(self):
            self.fileobj.write("actions:\n")

    def parse(self, testlist):
        for testcase in testlist:
            self.parse_dict(testcase)
        self.fileobj.close()

    def parse_dict(self, test):
        delimit = " "
        self.fileobj.write("-"+delimit)
        delimit += " "
        for param in test:
            self.fileobj.write(param + ": " + test[param] + "\n" +delimit)
        self.fileobj.write("\n") 
        
    def __del__(self):
        self.fileobj.close()
    
