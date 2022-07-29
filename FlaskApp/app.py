from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
#from flask_sqlalchemy import relationship
#from sqlalchemy import false

app=Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///test.db'
db = SQLAlchemy(app)


#helper table as given https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/
#For this helper table it is strongly recommended to NOT use a model but an actual table:
FeatureTest = db.Table('FeatureTest',
    db.Column('Test_id', db.Integer, db.ForeignKey('test.TestID'), primary_key=True),
    db.Column('Feature_id', db.Integer, db.ForeignKey('feature.FID'), primary_key=True)
    #learning while specifying use the same name as the model name but only in small chars to denote a table
)

ModuleTest = db.Table('ModuleTest',
    db.Column('Test_id', db.Integer, db.ForeignKey('test.TestID'), primary_key=True),
    db.Column('Module_id', db.Integer, db.ForeignKey('module.FID'), primary_key=True)
)


class Test(db.Model):
    TestID = db.Column(db.Integer, primary_key=True)
    TestName = db.Column(db.String(250),unique=True, nullable=False)
    ToBeExecuted = db.Column(db.Boolean,default=False)
    MoudulPartOf = db.relationship('Module', secondary=ModuleTest, backref='allmodules')
    FeaturesPartOf = db.relationship('Feature', secondary=FeatureTest, backref='allfeatures')

    def __repr__(self) -> str:
        return f'<Tests: {self.TestID}>'


class Feature(db.Model):
    FID = db.Column(db.Integer, primary_key=True)
    Fname=db.Column(db.String(250),unique=True, nullable=False)
    ComprisesofTests = db.relationship('Test', secondary=FeatureTest, backref='Tests_under_This_feature')
    #ComprisesofTests = db.relationship('Test', secondary=FeatureTest, lazy='subquery', backref=db.backref('Tests_under_This_feature', lazy=True))

    def __repr__(self) -> str:
        return f'<Feature: {self.FID}>'

#even for features we need to decide which tests to be ran first. logically the HW features should be first and then building on top of them
#This model helps us in choosing all the test which need to be executed.
#Something like : Select all from Module where The MID=1 and ( for all TestID in TestsUnderThismodule where ToBeExecuted = 1)
#Something like : Select all from Module where The MID=2 and ( for all TestID in TestsUnderThismodule where ToBeExecuted = 1)
#here the MID 1 is lower to hardware
class Module(db.Model):
    MID = db.Column(db.Integer, primary_key=True)
    MouduleName = db.Column(db.String(250),nullable=False)
    TestsUnderThismodule = db.relationship('Test', secondary=ModuleTest, backref='Tests_under_This_module')




if __name__ == "__main__":
    app.run(debug=True)

