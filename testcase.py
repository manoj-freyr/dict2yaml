class TestCase:
    cnt = 0
    def __init__(self,modname):
        self.testDict = {}
        self.enabled = False
        self.moduleName = modname
        TestCase.cnt += 1
        self.testID = TestCase.cnt
        self.feature = "Default"
        self.moduleID = 0

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
