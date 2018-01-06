# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, redirect
import datetime
import os
app = Flask(__name__)

@app.route("/")
def hello():
    thisAuthor = "Pat"
    thisName = "everyone"    
    return render_template('index.html', author=thisAuthor, name=thisName)
 
@app.route('/signup', methods = ['POST'])
def signup():
    global day
    day = request.form['day']
    global today
    today = request.form['today']
    global thoughts
    thoughts = request.form['thoughts']
    global links
    links = request.form['links']    
    global date
    date = datetime.datetime.now().strftime("%m %B, %Y")
    print(day + today + thoughts + links + date)
    
    #open log file and write to it
    file = "C:\\Users\\pnadolny\\Documents\\Personal_Development\\GitHub\\100-days-of-code\\log - Copy.md"
    content = open(file,"r")
    for line in content:
        print (line)    
    content.close()
    content = open (file, "a")
    content.write("\n \n \n ### Day " + day + ": " + date + "\n \n")
    content.write("**Today\'s Progress**: " + today + "\n \n")    
    content.write("**Thoughts** " + thoughts + "\n \n")
    content.write("**Link(s) to work:** " + links + "\n")
    content.close() 
    
    return redirect('/')    

@app.route('/logs.html')
def logs():
    print(day)
    return render_template('logs.html', author='Pat', day=day , date=date , today=today , thoughts=thoughts , links=links)


if __name__ == "__main__":
    app.run()