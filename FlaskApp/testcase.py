import copy
class TestCase:
    cnt = 0
    def __init__(self,modname, pdict, fname):
        self.testDict = copy.deepcopy(pdict)
        self.enabled = False
        self.moduleName = modname
        self.feature = fname
        self.moduleID = 0
        self.modstr = ""
        TestCase.cnt += 1
        self.testID = TestCase.cnt


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
        for k in self.testDict:
            self.modstr += k + " : " + self.testDict[k] + ","
        
    def __str__(self):
        self.stringify()
        return "TestCase object with fields: " + "testID: " +str(self.testID) + " ,feature: " + self.feature + " ,moduleId: " +str(self.moduleID) + ", Test Name : " + self.testDict["name"] + " \n and test parameters are :\n" + self.modstr
            
