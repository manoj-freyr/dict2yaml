import py_compile
from flask import Flask, render_template
from processor import Controller
from utils import testcase_list


app=Flask(__name__)

@app.route('/')
def index():

    AppController=Controller(testcase_list())

    print(f" The module names are :  {AppController.GetModuleNames() }")

    print(f" The module names are :  {AppController.GetFeatureNames() }")

    return render_template('index.html')





if __name__ == "__main__":
    app.run(debug=True)

