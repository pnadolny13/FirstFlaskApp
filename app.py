# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
#from flask.ext.cqlalchemy import CQLAlchemy
import csv
import datetime
import subprocess
import git
# test

app = Flask(__name__)
bootstrap = Bootstrap(app)

warning = ""
file = "C:\\Users\\pnadolny\\Documents\\Personal_Development\\GitHub\\100-days-of-code\\log.md"
date = datetime.datetime.now().strftime("%B %d, %Y")
lastDay = ""
recent = ""
recentLine = 0




############ CQL AlCHEMY #######################
#app.config['CASSANDRA_HOSTS'] = ['127.0.0.1']
#app.config['CASSANDRA_KEYSPACE'] = "logsDB"
#db = CQLAlchemy(app)


#class User(db.Model):
#    day = db.columns.Text(primary_key=True)
#    log = db.columns.Text(required=False)


###############   SQL AlCHEMY   ##################
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dbs\\log.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

class Logs(db.Model):
    day = db.Column(db.String, primary_key=True)
    logContent = db.Column(db.String)  
    
    def __repr__(self):
        return '%r' % self.logContent


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
    # hit github and check if theres a diff on the file
    repo = git.Repo( 'C:/Users/pnadolny/Documents/Personal_Development/GitHub/100-days-of-code/' )
    gitOutput = repo.git.status()
#    if "Untracked files" in gitOutput or "modified" in gitOutput:
        # do nothing
    return render_template('github.html', gitOutput = gitOutput ) 


###########   ACTIONS  ################

@app.route('/delete', methods = ['POST'])
def delete():
    prepForInputPage()
    # call input with no inputs to load in variables if needed
    global recent       
    if date in recent:
        logsR = open(file,"r")
        lines = logsR.readlines()
        logsR.close()
        
        with open(file, 'w') as outfile:
            writer = csv.writer(outfile)        
        
        logsW = open(file,"w", newline= '')          
        count = 1;
        for line in lines:
            if count == (recentLine - 2) or count == (recentLine - 1) or count >= recentLine:
                #deleteLine
                print("Delete: " + str(line))
            else:
                writer.writerow(line)
                logsW.write(line)
            count += 1
        recent = ""
        logsW.close()
        
        # delete from sql db
#        log = Logs(day=str(today), logContent=today)
#        db.session.delete(Logs.delete())
#        db.session.commit()
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
    # logContent = "### Day " + str(day) + ": " + str(date) + "**Today\'s Progress**: " + str(today)
    # + "**Thoughts** " + thoughts + "**Link(s) to work:** " + links;
    # day doesnt exist, go ahead and update now
    content = open (file, "a")
    content.write("\n\n\n### Day " + str(day) + ": " + date + "\n\n")
    content.write("**Today\'s Progress**: " + today + "\n\n")    
    content.write("**Thoughts** " + thoughts + "\n\n")
    content.write("**Link(s) to work:** " + links)
    content.close()
    
    # write to sql db
#    log = Logs(day=str(day), logContent=today)
#    db.session.add(log)
#    db.session.commit()

    
    return redirect('/')

@app.route('/pushToGitHub', methods = ['POST'])
def pushToGit():
    repo = git.Repo( 'C:/Users/pnadolny/Documents/Personal_Development/GitHub/100-days-of-code/' )
    repo.remotes.origin.push();
    print("pushed")
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
