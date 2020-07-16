from flask import Flask, redirect, url_for, request, render_template,flash
import numpy as np
import pandas as pd
import db
import os
import random
from datetime import date
app = Flask(__name__)
app.secret_key="secret key"
app.config["IMAGE_UPLOADS"] = "/home/ankita/dbms1/static"
day={0:'Idli',1:'Pongal',2:'Dosa',3:'Puliyogare',4:'Upma',5:'Lemon rice',6:'Tomato rice'}
alert=dict()
info=[]
info1=[]
d=0
c=0
c1=0
cnt=6
@app.route('/')
def session():
	return render_template('dbms_login_signup.html')
@app.route('/logout')
def logout():
	return render_template('dbms_login_signup.html')
@app.route('/backp')
def backp():
	return render_template('profile.html')
@app.route('/backs/<uid>',methods=['POST','GET'])
def backs(uid):
	info=db.Student.load_from_db(uid)
	return render_template('student.html',info=info,uid=uid)
@app.route('/sdetails',methods=['POST','GET'])
def sdetails():
	info=db.Student.load_all()
	return render_template('sdetails.html',info=info)
@app.route('/sattendance',methods=['POST','GET'])
def sattendance():
	global info
	global c
	j=0
	if c==0:
		info=db.Student.load_all()
		c=1
	info1=db.Student.load_all()
	for i in info:
			k=info.index(i)
			if i in info1:
				j=info1.index(i)
				info[k]=info1[j]
	return render_template('sattendance.html',info=info)

@app.route('/satt',methods=['POST','GET'])
def satt():
	global info
	if request.method == 'POST':
		att = list(request.form.keys())
		for i in info:
			if(str(i[0])==str(att[0])):
				db.Student.att(i[0])
				info.remove(i)
	return redirect('/sattendance')
@app.route('/eattendance',methods=['POST','GET'])
def eattendance():
	global info1
	global c1
	if c1==0:
		info1=db.Employee.load_all()
		c1=1
	return render_template('eattendance.html',info=info1)

@app.route('/eatt',methods=['POST','GET'])
def eatt():
	global info1
	if request.method == 'POST':
		att = list(request.form.keys())
		for i in info1:
			if(str(i[0])==str(att[0])):
				db.Employee.att(i[0])
				info1.remove(i)
	if len(info1)!=0:
		return redirect('/eattendance')
	return redirect('/backp')

@app.route('/edetails',methods=['POST','GET'])
def edetails():
	info=db.Employee.load_all()
	if len(info)!=0:
		return render_template('edetails.html',info=info)
	else:
		return redirect('/backp')
@app.route('/fdetails')
def fdetails():
	info=db.Food.load_all()
	return render_template('fdetails.html',info=info)
@app.route('/rdetails')
def rdetails():
	info=db.Room.load_all()
	return render_template('rdetails.html',info=info)
@app.route('/feedback',methods=['POST','GET'])
def feedback():
	info=db.Feedback.load_from_db()
	return render_template('feedback.html',info=info)
@app.route('/schedule',methods=['POST','GET'])
def schedule():
	info=day
	return render_template('schedule.html',info=info)

@app.route('/add',methods=['POST','GET'])
def add():
	return render_template('add.html')
@app.route('/bdetails',methods=['POST','GET'])
def bdetails():
	info=db.Bill.load_from_db()
	if len(info)!=0:
		return render_template('bdetails.html',info=info)
	return redirect('/backp')
@app.route('/sadd',methods=['POST','GET'])
def sadd():
	if request.method == 'POST':
		name = request.form['name']
		type1 = request.form['type']
		db.Food.save_to_db(name,type1)
	return redirect('/add')

@app.route('/codes/<uid>',methods=['POST','GET'])
def codes(uid):
	c=0
	l=[]
	for i in list(alert):
		if alert[i][0]==uid:
				l.append([i,alert[i][1]])
				c=1
	print('l=',l)
	if len(l)!=0:
		return render_template('request.html',l=l,uid=uid)
	return redirect('/backs/'+uid)
@app.route('/rooms/<uid>',methods=['POST','GET'])
def rooms(uid):
	return render_template('form.html',uid=uid)
@app.route('/roomc/<uid>',methods=['POST','GET'])
def roomc(uid):
	return render_template('room.html',uid=uid)
@app.route('/swap/<uid>',methods=['POST'])
def swap(uid):
	global alert
	if request.method == 'POST':
		uid1 = request.form['id']
		for i in list(alert):
			if i==uid:
				alert.pop(i)
		try:
			alert[uid]=[uid1,random.randrange(0,1000)]
		except:
			print('Error')
		return render_template('code.html',uid=uid,uid1=uid1)
@app.route('/success/<uid>/<uid1>',methods=['POST','GET'])
def success(uid,uid1):
	global alert
	if request.method == 'POST':
		code = request.form['code']
		for i in list(alert):
			if str(i==str(uid)):
				print('Hi')
				if str(code) == str(alert[i][1]):
					print('Success')
					db.Room.swap(uid,uid1)
					for i in list(alert):
						if alert[i][0]==uid1:
							alert.pop(i)
	return redirect('/backs/'+uid)
@app.route('/rrequest/<uid>',methods=['POST'])
def rrequest(uid):
	if request.method == 'POST':
		uid1 = request.form['id']
		db.Room.equest(uid1,uid)
		return redirect('/rooms/'+uid)
	return redirect('/backs/'+uid)
@app.route('/scheme/<uid>',methods=['POST','GET'])
def scheme(uid):
	global day
	cnt=0
	today=date.today()
	print(today.day)
	c=0
	if today.day==2:
		info=db.Food.result()
		for i in info:
			day[cnt]=i[0]
			cnt=cnt+1
		if cnt!=7:
			while cnt<7:
				info1=db.Food.load_all()
				for i in info1:
					k=0
					if i[1]=='Breakfast':
						for j in info:
							if i[0]==j[0]:
								k=1
						if k==0:
							day[cnt]=i[0]
							cnt=cnt+1
			
	return render_template('schedule.html',uid=uid,info=day)
@app.route('/poll/<uid>')
def poll(uid):	
	global cnt
	today=date.today()
	if today.day==2:
		cnt=6
		info=db.Food.load_from_db()
		return render_template('poll.html',uid=uid,info=info)
	else:
		return redirect('/backs/'+uid)

@app.route('/pollc/<uid>', methods=['POST','GET'])
def pollc(uid):
	global d
	if request.method == 'POST':
		name=request.form.keys()
		today=date.today()
		print('d',d)
		if d==0 and today.day==2:
			db.Food.delete()
			d=1
		print(name)
		count=db.Food.count(uid)
		print('count:',count[0])
		if count[0][0]<7:
			db.Food.poll(name,uid)
		url='/backs/'+uid
	return redirect(url)


@app.route('/slogin',methods=['POST'])
def slogin():
	if request.method == 'POST':
		uid = request.form['uid']
		pwd=request.form['pwd']
		url='/backs/'+uid
		info=db.Student.load_from_db(uid)
		if info!=None:
			if(pwd==info[0]):
				return redirect(url)
		return redirect('/')
		
@app.route('/wlogin',methods=['POST'])
def wlogin():
	if request.method == 'POST':
		user = request.form['uid']
		pwd=request.form['pwd']
		if user=="abcd" and pwd=="*****":
			return render_template("profile.html")
		else:
			return redirect("/")
@app.route('/signsuccess',methods=['POST'])
def signsuccess():
	if request.method == 'POST':
		uid = request.form['uid']
		name=request.form['name']
		pwd=request.form['pwd']
		ph = request.form['ph']
		city=request.form['city']
		dob = request.form['dob']
		fees=request.form['fees']
		room = request.form['room']
		d=db.Student(name,uid,ph,city,dob,pwd,fees,room,0)
		c=d.save_to_db()
		if(c==-1):
			return "Error"
		return redirect("/signup")
@app.route('/esignsuccess',methods=['POST'])
def esignsuccess():
	if request.method == 'POST':
		uid = request.form['uid']
		name=request.form['name']
		ph=request.form['ph']
		city=request.form['city']
		dob = request.form['dob']
		salary=request.form['salary']
		gen= request.form['gen']
		d=db.Employee(name,uid,ph,city,dob,gen,salary,0)
		c=d.save_to_db()
		if(c==-1):
			return "Error"
		return redirect("/esignup")
@app.route('/reset',methods=['POST'])
def reset():
	if request.method == 'POST':
		uid = request.form['uid']
		pwd=request.form['pwd']
		rpwd=request.form['rpwd']
		if pwd==rpwd:
			db.Student.setpwd(uid,pwd)
	return redirect('/')
@app.route('/send/<uid>',methods=['POST'])
def send(uid):
	if request.method == 'POST':
		content = request.form['content']
		d=db.Feedback(uid,content)
		d.save_to_db()
		url='/backs/'+uid
	return redirect(url)
@app.route('/signup')
def signup():
	return render_template("ssignup.html")
@app.route('/forgot')
def forgot():
	return render_template("reset_password.html")
@app.route('/esignup')
def esignup():
	return render_template("esignup.html")
@app.route('/bill')
def bill():
	return render_template("bill.html")

@app.route("/upload-image", methods=["GET", "POST"])
def upload_image():

	if request.method == "POST":

		if request.files:

			image = request.files["image"]
			image.save(os.path.join(app.config["IMAGE_UPLOADS"], image.filename))
			url='/static/'+image.filename
			db.Bill.save_to_db(url)
			print("Image saved")

	return redirect("/bill")

@app.route('/employee_remove',methods=["POST","GET"])
def eremove():
	if(request.method=='POST'):
		eid=request.form['eid']
		info=db.Employee.load_from_db_by_eid(eid)
		if info==1:
			flash("success")
		elif info==0:
			flash("Enter the correct id")
	return render_template("employee_remove.html")

@app.route('/student_remove',methods=["POST","GET"])
def sremove():
	if(request.method=='POST'):
		sid=request.form['sid']
		info=db.Student.load_from_db_by_sid(sid)
		if info==1:
			flash("success")
		elif info==0:
			flash("Enter the correct id")
	return render_template("student_remove.html")

@app.route('/recipe_remove',methods=["POST","GET"])
def rremove():
	if(request.method=='POST'):
		rname=request.form['rname']
		info=db.Food.load_from_db_by_rname(rname)
		if info==1:
			flash("success")
		elif info==0:
			flash("Enter the correct Recipe Name")
	return render_template("recipe_remove.html")

  
if __name__ == '__main__':
	app.run(debug=True)


"""d=db.Warden(name,uid,ph,city,dob,pwd)
		d.save_to_db()"""
