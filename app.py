from flask import Flask, render_template, url_for
import os
import json
from QuantitiesToJSON import CreateJSON
from LCAbygJSONtoAPI import JSONtoAPI
from ShowResultsPy import ShowResult
from WelcomePy import welcomeSite

app = Flask(__name__)

@app.route('/')
def Welcome():
    return welcomeSite()

@app.route('/UpdateData')
def UpdateData():
    return CreateJSON()
    
@app.route('/RunLCA')
def RunLCA(): 
    return JSONtoAPI()
    
@app.route('/ShowResult')
def ShowResults(): 
    return ShowResult()

if __name__ == "__main__":
    app.run(debug=True)

# %https://www.youtube.com/watch?v=GHvj1ivQ7ms

