# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, redirect
app = Flask(__name__)
 
email_addresses = []
@app.route("/")
def hello():
    thisAuthor = "Pat"
    thisName = "everyone"    
    return render_template('index.html', author=thisAuthor, name=thisName)
 
@app.route('/signup', methods = ['POST'])
def signup():
    email = request.form['email']
    email_addresses.append(email)
    print(emails)
    return redirect('/')    

@app.route('/emails.html')
def emails():
    return render_template('emails.html', author='Pat', emails=email_addresses)


if __name__ == "__main__":
    app.run()