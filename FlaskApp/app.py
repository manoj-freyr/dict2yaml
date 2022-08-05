import py_compile
from flask import Flask, render_template
from processor import  processtests


app=Flask(__name__)

@app.route('/')
def index():
    processtests() 
    return render_template('index.html')





if __name__ == "__main__":
    app.run(debug=True)

