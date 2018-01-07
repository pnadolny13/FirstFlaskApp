# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, redirect
import datetime
app = Flask(__name__)

warning = ""
file = "C:\\Users\\pnadolny\\Documents\\Personal_Development\\GitHub\\100-days-of-code\\log.md"
thisAuthor = "Pat"
thisName = "everyone"
date = datetime.datetime.now().strftime("%B %d, %Y")
lastDay = ""
recent = ""
recentLine = 0

@app.route("/")
def home():
    return render_template('index.html', author=thisAuthor, name=thisName, warning=warning )

@app.route('/action', methods = ['POST'])
def action():
    # if action is log or input redirect, if not then send back to homepage
    action = request.form['action']
    global recent
    if action == "view":
        prepForInputPage()
        return redirect('/currentLogs')
    elif action == "input":
        prepForInputPage()
        return render_template('input.html', author=thisAuthor, warning="", lastDay=lastDay)
    elif action == "delete":
        prepForInputPage()
        # call input with no inputs to load in variables if needed
        print ("date = " + date)
        print ("recent = " + recent)
        print ("recent = " + str(recentLine))        
        if date in recent:
            logsR = open(file,"r")
            lines = logsR.readlines()
            logsR.close()
            logsW = open(file,"w")            
            count = 1;
            for line in lines:
                if count == (recentLine - 2) or count == (recentLine - 1) or count >= recentLine:
                    #deleteLine
                    print("Delete: " + line)
                else:
                    logsW.write(line)
                count += 1
            recent = ""
            logsW.close()        
        return redirect('/currentLogs')

    print ("warning is :" + warning)

@app.route('/inputs', methods = ['POST'])
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
            return render_template('input.html', author=thisAuthor, warning=warning, recent=recent)
    content.close()

    # day doesnt exist, go ahead and update now
    content = open (file, "a")
    content.write("\n\n\n### Day " + str(day) + ": " + date + "\n\n")
    content.write("**Today\'s Progress**: " + today + "\n\n")    
    content.write("**Thoughts** " + thoughts + "\n\n")
    content.write("**Link(s) to work:** " + links)
    content.close()
    
    return redirect('/')    

@app.route('/currentLogs')
def currentLogs():
    ## here just render the whole log file
    log = open(file,"r")
    return render_template('currentLogs.html', author=thisAuthor, log=log)
    
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