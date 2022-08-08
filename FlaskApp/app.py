import py_compile
from flask import Flask, render_template
from processor import Controller
from utils import testcase_list
import sys

app=Flask(__name__)

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


@app.route('/')
def index():

    fd=open(JSON_FILE_FOR_DUMPING_OBJS,'r')

    ListFromfile= json.load(fd)

    fd.close()

    eprint(f"Read : {len(ListFromfile)} Objs")

    for item in ListFromfile:
        eprint(item)
        

    AppController=Controller(testcase_list())

    eprint(f" The module names are :  {AppController.GetModuleNames() }")

    eprint(f" The module names are :  {AppController.GetFeatureNames() }")

    return render_template('index.html')





if __name__ == "__main__":
    app.run(debug=True)

