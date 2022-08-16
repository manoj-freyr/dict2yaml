from collections import defaultdict
import sys
import copy

def dprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

class SelectedTest:
    COUNTERIDX = 0
    def __init__(self,masteridx, Masterlist):
        SelectedTest.COUNTERIDX += 1
        self.IDx='S_'+ str(SelectedTest.COUNTERIDX)
        self.mid=Masterlist[int(masteridx)].moduleID
        self.fid=Masterlist[int(masteridx)].feature
        self.Mname=Masterlist[int(masteridx)].moduleName
        self.Fname=Masterlist[int(masteridx)].feature
        self.TestParams = copy.deepcopy(Masterlist[int(masteridx)].testDict)
        #self.testname=self.TestParams["name"]
        self.status="Not Started"
        self.Result="Unknown"
        self.LogFile="NA"

    def GetTestidx(self):
        return self.IDx

    def GetModuleID(self):
        return self.mid

    def GetFeatureID(self):
        return self.fid

    def GetStatus(self):
        return self.status

    def SetStatus(self,status):
        self.status=status

    def GetResult(self):
        return self.Result

    def SetResult(self,result):
        self.Result=result

    def GetLogFile(self):
        return self.LogFile

    def SetLogFile(self,logfile):
        self.LogFile=logfile

    def GetModuleName(self):
        return self.Mname

    def GetFeatureName(self):
        return self.Fname

    def GetTestParams(self):
        return self.TestParams
    
    def SetTestParams(self,ParamsDict):
        self.TestParams = copy.deepcopy(ParamsDict)
    
    def PrintThisItem(self):
        dprint(f"Idx = {self.IDx}, MID={self.mid} & name = {self.Mname}, FID={self.fid} & name = {self.Fname}")
        dprint(f"Status = {self.status}, Result={self.Result}, LogFile={self.LogFile}")
        dprint(f"Params of this item : {self.TestParams}")
        #self.testname=self.TestParams["name"]


class Controller:
    def __init__(self,mlist):
        #Data Structures

        #This Masterlist is obtained from utils.py
        self.Masterlist=mlist

        #A list of strigs to populate the features
        self.FeatureNames=[]

        #A list of strigs to populate the modules
        self.ModuleNames=[]

        #A dictionary of string:IndexList[] which points to the test objects of Masterlist
        self.ModuleDict=defaultdict(list)

        #A dictionary of string:IndexList[] which points to the test objects of Masterlist
        self.FeatureDict=defaultdict(list)

        #This is a list of Selected Tests
        self.Selectedlist=[]

        #if the list starts increasing the then 'in' functionality becomes slow
        #https://stackoverflow.com/a/40963434/672480  ;  we should be using sets in that case
        for item in self.Masterlist:
            #caluculate the index of this item in the parent list
            idx=self.Masterlist.index(item)
            #dprint(f" processing for index {idx} of the testcaselist ")

            #If this feature does not exists in the feature list then only add it
            if item.feature not in self.FeatureNames:
                self.FeatureNames.append(item.feature)

            #same with module ID
            if item.moduleName not in self.ModuleNames:
                self.ModuleNames.append(item.moduleName)
                #print(f"ModuleNames=  {self.ModuleNames}")

            #add this idx of the parent list to this dictionary
            self.ModuleDict[item.moduleName].append(idx)
            self.FeatureDict[item.feature].append(idx)
           # print(f"Initialized Object with Master list :  {self.Masterlist}")


    def GetSelectedTestList(self):
        return self.Selectedlist

    def GetFeatureNames(self):
        return self.FeatureNames

    def GetModuleNames(self):
        return self.ModuleNames

    #This list populates the 2 part (#Box 1)
    def GetWholeTestListBasedOnModuleOrFeature(self,Moduleorfeature, name):
        tmplist=[]
        returlist=[]
        #true means module
        if Moduleorfeature is True:
            tmplist=self.ModuleDict[name]
        else:
            tmplist=self.FeatureDict[name]

        for idx in tmplist:
            returlist.append([idx,self.Masterlist[idx].testDict["name"]])

        return returlist

    #API for adding test to selected list
    def AddToSelectedList(self,listofmasterids):
        DisplayList=[]
        for idx in listofmasterids:
            #Each test would be new Selected test, hence just create one
            selectedobj=SelectedTest(idx,self.Masterlist)
            self.Selectedlist.append(selectedobj)
            DisplayList.append([selectedobj.GetTestidx(),selectedobj.GetTestParams()["name"]])
        
        return DisplayList


    #API for removing a test from the selected list
    def RemoveFromSelectedList(self,ListOfIDXOfSelectedTest):
        for idx in ListOfIDXOfSelectedTest:
            for obj in self.Selectedlist:
                if obj.GetTestidx() == idx:
                    dprint(f" removing : {idx}")
                    self.Selectedlist.remove(obj)
                    break

    #API for getting the test params of a selected test (#box : 3)
    def GetParamsOfSelectedItem(self,idx):
        dprint(f" GettingDataOf : {idx}")
        for obj in self.Selectedlist:
            if obj.GetTestidx() == idx:
                dprint(f" ObjFound for : {idx}")
                return obj.GetTestParams()

    #API for updating the modified params from the User (#box :3 updated data)
    def SetParamsOfSelectedItem(self,idx,dict):
        dprint(f" SettingDataOf : {idx}")
        for obj in self.Selectedlist:
            if obj.GetTestidx() == idx:
                dprint(f" ObjFound for : {idx}")
                obj.SetTestParams(dict)


    #I want to use this in observer faishon. Need to figure out how to do it in Python
    def ExecuteTest(self,selectedlist):
        for obj in selectedlist:
            self.Masterlist[obj.GetMasteridx()].enable()




'''# below APIs will not be good hence we have discareded these afert discussion
def GetNextItem(moduleorfeature, currentidx):

def GetPreviousItem(moduleorfeature, currentidx):
'''

