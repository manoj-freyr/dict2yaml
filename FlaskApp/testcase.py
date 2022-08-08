import copy
import json


class TestCase:
    cnt = 0
    def __init__(self,modname, pdict, fname, id=-1,mid=0,enb=False):
        ## Kidly do not change the order of the member vars
        ## json gets destroyed, if new member add at the end
        if id < 0 :
           TestCase.cnt += 1
           self.testID = TestCase.cnt
        else:
           self.testID = id

        self.enabled = enb
        self.moduleName = modname
        self.feature = fname
        self.moduleID = mid
        self.testDict = copy.deepcopy(pdict)


    def update_dict(self,tdict):
        self.testDict = tdict

    def enabled(self):
        return self.enabled

    def enable(self, val):
        self.enabled = val

    def feature_name(self):
        return self.feature

    def update_feature(self, fname):
        self.feature = fname

    def module_id(self):
        return self.moduleID 
    
    def update_moduleid(self,modid):
        self.moduleID = modid

    def run(self):
        pass
  
    def stringify(self):
        modstr=""
        for k in self.testDict:
            modstr += k + " : " + self.testDict[k] + ","

        return modstr

        
    def __str__(self):
        lstr=self.stringify()
        return "TestCase object with fields: " + "testID: " +str(self.testID) + " ,feature: " + self.feature + " ,moduleId: " +str(self.moduleID) + ", Test Name : " + self.testDict["name"] + " \n and test parameters are :\n" + lstr
        




class TestCaseJsonEncoder(json.JSONEncoder):
    def default(self,obj):
        if isinstance(obj,TestCase):
            return [obj.testID, obj.enabled, obj.moduleName, obj.feature, obj.moduleID, obj.testDict ]
            #return [{"testID", obj.testID}, {"enabled", obj.enabled}, {"moduleName", obj.moduleName}, {"feature", obj.feature}, {"moduleID", obj.moduleID}, obj.testDict ]
        
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)


