import py_compile
from flask import Flask, render_template
from processor import Controller
from utils import testcase_list, JSON_FILE_FOR_DUMPING_OBJS
import sys
import json
from testcase import TestCase
#from types import SimpleNamespace

app=Flask(__name__)

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def BeforeLaunch():
    eprint(f" This is starting of the function : BeforeLaunch()  ")
    ListFromfile=[]
    fd=open(JSON_FILE_FOR_DUMPING_OBJS,'r')
    file_in=fd.readlines()
    for line in file_in:
        line.rstrip()
        tobj=json.loads(line)
        #eprint(tobj)
        tele=TestCase(tobj[2],tobj[5],tobj[3],tobj[0],tobj[4],tobj[1])
        #eprint(tele)
        ListFromfile.append(tele)
         
    eprint(f"Read : {len(ListFromfile)} Objs")

    #for item in ListFromfile:
    #    eprint(item)


    AppController=Controller(ListFromfile)

    eprint(f" The module names are :  {AppController.GetModuleNames() }")

    eprint(f" The module names are :  {AppController.GetFeatureNames() }")




@app.route('/')
def index():

    return render_template('index.html')




if __name__ == "__main__":
    BeforeLaunch()
    app.run(debug=True)


