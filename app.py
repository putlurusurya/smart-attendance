from os import access
import pyrebase
config = {
  "apiKey": "AIzaSyCiXgPde47Im1KsMqsORSm2hNPf2kGk8LA",
  "authDomain": "iotproject-7e71f.firebaseapp.com",
  "databaseURL": "https://iotproject-7e71f-default-rtdb.firebaseio.com",
  "projectId": "iotproject-7e71f",
  "storageBucket": "iotproject-7e71f.appspot.com",
  "messagingSenderId": "340854926149",
  "appId": "1:340854926149:web:f7792bf803d516ba67ac2c",
  "measurementId": "G-QJLFVLJTQS"
}
firebase = pyrebase.initialize_app(config)

db = firebase.database()
auth=firebase.auth()
person = {"is_logged_in": False, "name": "", "email": "", "uid": ""}
from flask import *

app = Flask(__name__)

app.secret_key = "ThisIsNotASecret:p"

@app.route('/', methods=['GET'])
def index():
    if session.get('logged_in'):
        return redirect('/welcome')
    else:
        return redirect('/login')

@app.route("/welcome",methods=['GET','POST'])
def welcome():
    if session["logged_in"] == True:
      date=db.child("date").get().val()
      tag=db.child("tag").get().val()
      temp=db.child("temperature").get().val()
      acc=db.child("access").get().val()
      dates=[]
      tags=[]
      temps=[]
      accs=[]
      for i in date:
        dates.append(date[i])
      for i in tag:
        tags.append(tag[i])
      for i in temp:
        temps.append(temp[i])
      for i in acc:
        accs.append(acc[i])
      data=[]
      for i in range(0,min(len(dates),min(len(tags),min(len(accs),len(temps)))):
        t=[]
        t.append(tags[i])
        t.append(temps[i])
        t.append(dates[i])
        t.append(accs[i])
        data.append(t)

      return render_template("welcome.html",data=data)
    else:
        return redirect('/')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session['logged_in'] = False
    return redirect('/')

@app.route("/login", methods = ["POST", "GET"])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        u = request.form['login']
        p = request.form['password']
        if u=="admin@gmail.com" and p=="admin":
            print("success")
            session['logged_in'] = True
            return redirect('/welcome')
        return redirect('/login')
if __name__ == '__main__':
  
  app.run(debug=True)

