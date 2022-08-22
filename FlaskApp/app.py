import py_compile
from typing import List
from flask import Flask, render_template, request, url_for, redirect
from processor import Controller
from utils import testcase_list, JSON_FILE_FOR_DUMPING_OBJS
import sys
import json
from testcase import TestCase
#from types import SimpleNamespace

RUNNIN_IN_WINDOWS=True


app=Flask(__name__)

#####################################################################
# Support Functions
#####################################################################
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def GetMasterListFromRVS():
    ListFromRVS=testcase_list()
    return ListFromRVS

def GetMasterListFromFile():
    eprint(f" This is starting of the function : GetMasterListFromFile()  ")
    ListFromfile=[]
    fd=open(JSON_FILE_FOR_DUMPING_OBJS,'r')
    #fd=open("C:\work\MLSE-SDT\RVS-Enhancement\dict2yaml\FlaskApp\ObjValsDumps.txt", 'r')
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

#####################################################################
# View Functions
#####################################################################

#--------------------------------------------------------------------
# RVT Home Screen View
#--------------------------------------------------------------------
# Keys mapped to columns as Header row
# Values are mapped to data for each cell
# table is assumed to be a List of dictionaries.

@app.route('/', methods=['GET', 'POST'])
def home():

    tbl_dict=[]
    selected_tests = AppController.GetSelectedTestList()

    for test in selected_tests:
        tbl_dict.append({'test_id':test.GetTestidx(), 'module_id':test.GetModuleName(),
                         'test_name':test.GetTestParams()["name"], 'test_status':test.GetStatus(),
                         'test_log':test.GetLogFile()})

    if len(selected_tests) == 0:
        btn_disable_add = ''
        btn_disable_run = 'disabled'
    else:
        btn_disable_add = ''
        btn_disable_run = ''

    run_status = AppController.ExecutionStarted
    if  run_status== True:
        btn_disable_add = 'disabled'


    return render_template('home.html', tbl_dict=tbl_dict,
                            btn_disable_add = btn_disable_add,
                            btn_disable_run = btn_disable_run,
                            run_status=run_status)


#--------------------------------------------------------------------
# RVT Add Remove Test Screen View
#--------------------------------------------------------------------


# mod_selected = "Select the module"
@app.route('/add-remove-test', methods=['GET', 'POST'])
def add_remove_test():
    print ("request = ", request)
    print ("request.args = ", request.args)
    print ("request.form = ", request.form)


    modules = AppController.GetModuleNames()
    selected_tests = AppController.GetSelectedTestListForDisplay()

    if request.method == 'POST':
        module_id=request.form.get('mod-list')
        mod_selected = module_id
        print ( "module-id = ", module_id)

        # get the list of testcases for the selected module/feature
        tests = AppController.GetWholeTestListBasedOnModuleOrFeature(True, module_id)
        #the tests list obtained above is of the format [[]] (list of list) of the type [[idx,testname]]
        print("tests [] = ", tests)

        # get the selected tests  and update it to right list as selected
        test_tobe_added = request.form.getlist('test-list')
        print( "test-list selected = ", test_tobe_added)
        if test_tobe_added != "":
            # add the user selected test in to SelectedList and update the selected test list display
            selected_tests = AppController.AddToSelectedList(test_tobe_added)

    else:
        mod_selected = "Select the module"
        tests =[]

    return render_template('add-remove-test.html', modules=modules, mod_selected=mod_selected, tests=tests, selected_tests=selected_tests)

#--------------------------------------------------------------------
# RVT Add Test
#--------------------------------------------------------------------
@app.route('/addtest', methods=['GET', 'POST'])
def addtest():
    print("addtest() Post req = ", request.form)
    print("addtest() tests to be added = ", request.form.getlist('test-list'))

    # get the selected tests  and update it to right list as selected
    # test_tobe_added = request.form.getlist('test-list')
    # print( "test-list selected = ", test_tobe_added)

    # AppController.AddToSelectedList(test_tobe_added)

    return redirect('/add-remove-test')

#--------------------------------------------------------------------
# RVT Remove Test 
#--------------------------------------------------------------------
@app.route('/removetest/<test_id>', methods=['GET', 'POST'])
def removetest(test_id):
    print("Post req = ", request.form)
    print("Test id to be removed from selected test = ", test_id)

    # remove selected tests in to the active test list
    AppController.RemoveFromSelectedList([test_id])

    return redirect('/add-remove-test')
#--------------------------------------------------------------------
# RVT Modify Test parameters
#--------------------------------------------------------------------
@app.route('/modifytest/<test_id>', methods=['GET', 'POST'])
def modifytest(test_id):
    print("Post req = ", request.form)

    if request.method == 'POST':
        # Gather the updated parameter values and call the API if there is change in the parameter values.
        newparams = request.form.to_dict()
        print ("new params = ", newparams)
        oldparams = AppController.GetParamsOfSelectedItem(test_id)
        print ("old params = ", oldparams)

        if newparams != oldparams:
            # update/modify the params of the selected test_id
            AppController.SetParamsOfSelectedItem(test_id, newparams)

        return redirect('/add-remove-test')
    else:
        print("Test id to be modified from selected test = ", test_id)
        # update/modify the params of the selected test_id
        params = AppController.GetParamsOfSelectedItem(test_id)
        # params_type = AppController.GetParamsTypeOfSelectedItem(test_id)

        print("params = ", params)
        # return redirect('/add-remove-test')
        return render_template('modify-test.html', test_id=test_id, params=params)

#--------------------------------------------------------------------
# execute_tests Screen View
#--------------------------------------------------------------------

@app.route('/run', methods=['GET', 'POST'])
def execute_tests():

    # Open a uds socket and pass it on to runner

    AppController.ExecuteTests()

    return redirect('/')

#--------------------------------------------------------------------
# execute_tests Screen View
#--------------------------------------------------------------------

@app.route('/stop', methods=['GET', 'POST'])
def stop_tests():

    print("Stop_test_called. Reloading Home page.")
    AppController.ExecutionStarted = False

    return redirect('/')



#####################################################################
# Callback function
#####################################################################
def callback_refresh():

    print("Callback fn called. Reload Home page.")

    return redirect('/')

#####################################################################
# Main
#####################################################################

#App Start
Mlist=[] #Master Tests List
if RUNNIN_IN_WINDOWS:
    Mlist = GetMasterListFromFile()
else:
    Mlist = GetMasterListFromRVS()

#Create Controller now
AppController=Controller(Mlist)
AppController.SetCallback( callback_refresh )

if __name__ == "__main__":


    eprint(f" The module names are :  {AppController.GetModuleNames() }")
    eprint(f" The Feature names are :  {AppController.GetFeatureNames() }")

    app.run(debug=True)


