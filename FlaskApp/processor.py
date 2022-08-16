from collections import defaultdict
import sys

def dprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

class SelectedTest:
    def __init__(self,masteridx, Masterlist):
        self.masterid=masteridx
        self.mid=Masterlist[self.masterid].moduleID
        self.fid=Masterlist[self.masterid].feature
        self.testID=Masterlist[masteridx].testID
        self.testname=Masterlist[masteridx].testDict["name"]
        self.status="Not Started"
        self.Result="Unknown"
        self.LogFile = ""

    def GetMasteridx(self):
        return self.masterid

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


    def GetFeatureNames(self):
        return self.FeatureNames

    def GetModuleNames(self):
        return self.ModuleNames

    #This list populates the 2 part
    def GetWholeTestListBasedOnModuleOrFeature(self,Moduleorfeature, name):
        tmplist=[]
        returlist=[]
        #true means module
        if Moduleorfeature is True:
            tmplist=self.ModuleDict[name]
        else:
            tmplist=self.FeatureDict[name]

        for idx in tmplist:
            returlist.append({self.Masterlist[idx].testDict["name"],idx})

        return returlist


    def AddToSelectedList(self,listofmasterids):
        for idx in listofmasterids:
            selectedobj=SelectedTest(idx,self.Masterlist)
            self.Selectedlist.append(selectedobj)

    def RemoveFromSelectedList(self,listofmasterids):
        for idx in listofmasterids:
            for obj in self.Selectedlist:
                if obj.GetMasteridx() == idx:
                    self.Selectedlist.remove(obj)
                    break

    def GetDictOfSelectedItem(self,idx):
        return self.Masterlist[idx].testDict

    def SetDictOfSelectedItem(self,idx,dict):
        self.Masterlist[idx].update_dict(dict)


    #I want to use this in observer faishon. Need to figure out how to do it in Python
    def ExecuteTest(self,selectedlist):
        for obj in selectedlist:
            self.Masterlist[obj.GetMasteridx()].enable()




'''# below APIs will not be good hence we have discareded these afert discussion
def GetNextItem(moduleorfeature, currentidx):

def GetPreviousItem(moduleorfeature, currentidx):
'''

