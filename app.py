# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, redirect
from flask_bootstrap import Bootstrap

import datetime
app = Flask(__name__)
Bootstrap(app)

warning = ""
file = "C:\\Users\\pnadolny\\Documents\\Personal_Development\\GitHub\\100-days-of-code\\log.md"
date = datetime.datetime.now().strftime("%B %d, %Y")
lastDay = ""
recent = ""
recentLine = 0


#######    VIEWS  ################

@app.route("/")
def homeView():
    prepForInputPage()
    log = open(file,"r")
    return render_template('index.html', warning=warning, log=log )

@app.route('/input')
def inputView():
    prepForInputPage()
    return render_template('input.html', warning="", lastDay=lastDay)    


@app.route('/currentLogs')
def currentLogsView():
    ## here just render the whole log file
    prepForInputPage()
    log = open(file,"r")
    return render_template('currentLogs.html', log=log)
    
@app.route('/delete')
def deleteView():
    prepForInputPage()
    log = open(file,"r")
    toDelete = []
    deleteBool = False
    for line in log:
        if date in line:
            deleteBool = True
        if deleteBool:
            toDelete.append(line)
    deleteBool = False
    return render_template('delete.html', toDelete=toDelete) 


@app.route('/github')
def pushToGithubView():
    prepForInputPage()
    return render_template('github.html') 


###########   ACTIONS  ################

@app.route('/delete', methods = ['POST'])
def delete():
    prepForInputPage()
    # call input with no inputs to load in variables if needed
    global recent       
    if date in recent:
        logsR = open(file,"rb")
        lines = logsR.readlines()
        logsR.close()
        logsW = open(file,"wb")            
        count = 1;
        for line in lines:
            if count == (recentLine - 2) or count == (recentLine - 1) or count >= recentLine:
                #deleteLine
                print("Delete: " + str(line))
            else:
                logsW.write(line)
            count += 1
        recent = ""
        logsW.close()
    return redirect('/')


@app.route('/inputData', methods = ['POST'])
def inputs():
    global warning
    warning = ""
    day = int(lastDay) + 1
    global today
    today = request.form['today']
    global thoughts
    thoughts = request.form['thoughts']
    global links
    links = request.form['links']        
    #open log file and write to it
    content = open(file,"r")
    for line in content:
        if (date) in line:
            warning = "ENTRY FOR TODAY ALREADY EXISTS!!!"
            return render_template('input.html', warning=warning, recent=recent)
    content.close()

    # day doesnt exist, go ahead and update now
    content = open (file, "a")
    content.write("\n\n\n### Day " + str(day) + ": " + date + "\n\n")
    content.write("**Today\'s Progress**: " + today + "\n\n")    
    content.write("**Thoughts** " + thoughts + "\n\n")
    content.write("**Link(s) to work:** " + links)
    content.close()
    
    return redirect('/')    




########### METHODS ################

def prepForInputPage():
    logs = open(file,"r")
    global recent
    recent = ""
    count = 0
    for line in logs:
        count += 1
        if line.startswith("### Day"):
            global lastDay
            lastDay = line[7:].split(":")[0]
            global recentLine
            recentLine = count
            recent = "Day " + lastDay + ": " + date;
    logs.close();
    print (recentLine)

if __name__ == "__main__":
    app.run()