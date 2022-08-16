import py_compile
from typing import List
from flask import Flask, render_template, request, url_for, redirect
from processor import Controller
from utils import testcase_list, JSON_FILE_FOR_DUMPING_OBJS
import sys
import json
from testcase import TestCase
#from types import SimpleNamespace

app=Flask(__name__)

#####################################################################
# Support Functions
#####################################################################
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def BeforeLaunch():
    eprint(f" This is starting of the function : BeforeLaunch()  ")
    ListFromfile=[]
    #fd=open(JSON_FILE_FOR_DUMPING_OBJS,'r')
    fd=open("C:\work\MLSE-SDT\RVS-Enhancement\dict2yaml\FlaskApp\ObjValsDumps.txt", 'r')
    file_in=fd.readlines()
    for line in file_in:
        line.rstrip()
        tobj=json.loads(line)
        #eprint(tobj)
        
        tele=TestCase(tobj[2],tobj[5],tobj[3],tobj[0],tobj[4],tobj[1])  # (modname, pdict, fname, id=-1,mid=0,enb=False)
        
        #eprint(tele)
        ListFromfile.append(tele)
         
    #eprint(f"Read : {len(ListFromfile)} Objs")

    #for item in ListFromfile:
    #    eprint(item)


    #AppController=Controller(ListFromfile)

    #eprint(f" The module names are :  {AppController.GetModuleNames() }")

    #eprint(f" The Feature names are :  {AppController.GetFeatureNames() }")

    return ListFromfile

mlist = BeforeLaunch()
AppController=Controller(mlist)

#####################################################################
# View Functions
#####################################################################

#--------------------------------------------------------------------
# RVT Home Screen View
#--------------------------------------------------------------------
# Keys mapped to columns as Header row
# Values are mapped to data for each cell
# table is assumed to be a List of dictionaries. 
tbl_dict = [ 
         {'test_id':1, 'module_id':'gst', 'test_name':"test1", 'test_status':"Pass ",'test_log':"This log file is clickable "},
         {'test_id':2, 'module_id':'gst', 'test_name':"test1", 'test_status':"Fail",'test_log':"output.txt"},
         {'test_id':3, 'module_id':'gst', 'test_name':"test1", 'test_status':"Running..",'test_log':"testlog.txt"},
         {'test_id':4, 'module_id':'gst', 'test_name':"test1", 'test_status':"",'test_log':"testlog.txt"},
         {'test_id':5, 'module_id':'gst', 'test_name':"test1", 'test_status':"",'test_log':"testlog.txt"},
         {'test_id':6, 'module_id':'gst', 'test_name':"test1", 'test_status':"",'test_log':"testlog.txt"},
         {'test_id':7, 'module_id':'gst', 'test_name':"test1", 'test_status':"",'test_log':"testlog.txt"},
         {'test_id':8, 'module_id':'gst', 'test_name':"test1", 'test_status':"",'test_log':"testlog.txt"},
         {'test_id':9, 'module_id':'gst', 'test_name':"test1", 'test_status':"",'test_log':"testlog.txt"},
         {'test_id':10,'module_id':'gst',  'test_name':"test1", 'test_status':"",'test_log':"testlog.txt"},
        ]

btn_disable_add = ''
btn_disable_run = ''

@app.route('/', methods=['GET', 'POST'])
def home():

    btn_disable_add = ''
    btn_disable_run = 'disabled'
    return render_template('home.html', tbl_dict=tbl_dict,
                            btn_disable_add = btn_disable_add,
                            btn_disable_run = btn_disable_run)


#--------------------------------------------------------------------
# RVT Add Remove Test Screen View
#--------------------------------------------------------------------


mod_selected = "Select the module"
@app.route('/add-remove-test', methods=['GET', 'POST'])
def add_remove_test():
    print ("request = ", request)
    print ("request.args = ", request.args)
    print ("request.form = ", request.form)

    tests =[]
    #modules = [ "mod1", "mod2", "mod3", "mod4"]
    modules = AppController.GetModuleNames()

    selected_tests = []
    mod_selected = "Select the module"
    if request.method == 'POST':
        module_id=request.form.get('mod-list')
        mod_selected = module_id
        print ( "module-id = ", module_id)
        
        """
        if module_id == 'mod1':
            # get the test list for the selected module/feature
            tests = [ "test11", "test12", "test13", "test14"]
        elif module_id == 'mod2':
            # get the test list for the selected module/feature
            tests = [ "test21", "test22", "test23", "test24"]
        else:
            tests = [ "test31", "test32", "test33", "test34"]
        """
        # get the list of testcases for the selected module/feature
        tests = AppController.GetWholeTestListBasedOnModuleOrFeature(True, module_id)
        print("tests [] = ", tests)

        ## get the selected tests  and update it to right list as selected
        test_list = request.form.getlist('test-list')


        print( "test-list selected = ", test_list)
        selected_tests = test_list
    return render_template('add-remove-test.html', modules=modules, mod_selected=mod_selected, tests=tests, selected_tests=selected_tests)

#--------------------------------------------------------------------
# RVT Add Test 
#--------------------------------------------------------------------
@app.route('/addtest', methods=['GET', 'POST'])
def addtest():
    print("addtest() Post req = ", request.form)
    print("addtest() tests to be added = ", request.form.getlist('test-list'))
    test_tobe_added = request.form.getlist('test-list')

    # Add selected tests in to the active test list
    # AppController.addTest(test_tobe_added)


    return redirect('/add-remove-test')

#--------------------------------------------------------------------
# RVT Remove Test 
#--------------------------------------------------------------------
@app.route('/removetest/<test_id>', methods=['GET', 'POST'])
def removetest(test_id):
    print("Post req = ", request.form)
    print("Test id to be removed from selected test = ", test_id)

    # remove selected tests in to the active test list
    # AppController.removeTest(test_id)

    return redirect('/add-remove-test')
#--------------------------------------------------------------------
# RVT Modify Test parameters
#--------------------------------------------------------------------
@app.route('/modifytest/<test_id>', methods=['GET', 'POST'])
def modifytest(test_id):
    print("Post req = ", request.form)
    print("Test id to be modified from selected test = ", test_id)

    # Gather the updated parameter values and call the API if there is update in the parameter values.
    # params

    # update/modify the params of the selected test_id
    # AppController.modifyTest(test_id)

    return redirect('/add-remove-test')


#####################################################################
# Main
#####################################################################

if __name__ == "__main__":


    eprint(f" The module names are :  {AppController.GetModuleNames() }")
    eprint(f" The Feature names are :  {AppController.GetFeatureNames() }")

    app.run(debug=True)


