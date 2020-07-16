import psycopg2 as pg
visited=[]
s=0
g=0
l={}

class Student:
	def __init__(self,name, uid, ph,city,dob,pwd,fees,room,days):
		self.uid=int(uid)
		self.pwd=pwd
		self.name=name
		self.ph=ph
		self.city=city
		self.dob=dob
		self.fees=fees
		self.room=room
		self.days=days
	@classmethod
	def load_from_db_by_sid(self,sid):
		with pg.connect(user='postgres', password='123', database='postgres',host='localhost') as connection:
			with connection.cursor() as cursor:
				cursor.execute('select sid from student')
				res=cursor.fetchall()
				for i in res:
					if str(i[0])==str(sid):
						cursor.execute('delete from feedback where sid=%s',(sid))
						cursor.execute('delete from poll where sid=%s',(sid))
						cursor.execute('delete from request where sid=%s',(sid))
						cursor.execute('delete from student where sid=%s',(sid))
						return 1
		return 0
	

	@classmethod
	def load_all(self):
		with pg.connect(user='postgres', password='123', database='postgres',host='localhost') as connection:
			with connection.cursor() as cursor:
				cursor.execute('SELECT sid,sname,room,ph,days,fee from student order by sid')
				info=cursor.fetchall()
				return info


	@classmethod		
	def load_from_db(self,uid):
		with pg.connect(user='postgres', password='123', database='postgres',host='localhost') as connection:
			with connection.cursor() as cursor:
				try:
					cursor.execute('SELECT pwd,sname,room,ph,dob,addr from student where sid=%s',uid)
					pwd=cursor.fetchone()
					return pwd
				except:
					return
    
	def save_to_db(self):
        	with pg.connect(user='postgres', password='123', database='postgres',host='localhost') as connection:
            		with connection.cursor() as cursor:
                		try:
	                		cursor.execute('INSERT into student values (%s,%s,%s,%s,%s,%s,%s,%s,%s)',(self.uid,self.name,self.city,self.ph,self.days,self.pwd,self.dob,self.fees,self.room))
                			#cursor.execute('UPDATE room set vacancy=vacancy-1 where roomid=%s',self.room)
                			return 0
                		except:
                        		return -1
	@classmethod	
	def setpwd(self,uid,pwd):
		with pg.connect(user='postgres', password='123', database='postgres',host='localhost') as connection:
			with connection.cursor() as cursor:
				try:
					cursor.execute('UPDATE student set pwd=%s where sid=%s',(pwd,uid))
				except:
					return
	@classmethod
	def att(self,uid):
		with pg.connect(user='postgres', password='123', database='postgres',host='localhost') as connection:
			with connection.cursor() as cursor:
				cursor.execute('UPDATE student set days=days+1 where sid=%s',(str(uid)))
		
class Feedback:
	def __init__(self,uid,content):
		self.uid=uid
		self.content=content
	def save_to_db(self):
		with pg.connect(user='postgres', password='123', database='postgres',host='localhost') as connection:
			with connection.cursor() as cursor:
				cursor.execute('INSERT into feedback (sid,content) values (%s,%s)',(self.uid,self.content))
	@classmethod
	def load_from_db(self):
		with pg.connect(user='postgres', password='123', database='postgres',host='localhost') as connection:
			with connection.cursor() as cursor:
				cursor.execute('SELECT sid,content from feedback')
				info=cursor.fetchall()
				return info

class Food:
	def load_from_db():
		with pg.connect(user='postgres', password='123', database='postgres',host='localhost') as connection:
			with connection.cursor() as cursor:
				cursor.execute("SELECT name from food where type='Breakfast'")
				info=cursor.fetchall()	
				return info
	def poll(name,uid):
		with pg.connect(user='postgres', password='123', database='postgres',host='localhost') as connection:
			with connection.cursor() as cursor:
				try:
					for i in name:
						cursor.execute('INSERT into poll values (%s,%s)',(i,uid))
				except:
					return
	def count(uid):
		with pg.connect(user='postgres', password='123', database='postgres',host='localhost') as connection:
			with connection.cursor() as cursor:
				try:
					cursor.execute('SELECT count(*) from poll where sid=%s',(uid))
					return cursor.fetchall()
				except:
					return 0
	def result():
		with pg.connect(user='postgres', password='123', database='postgres',host='localhost') as connection:
			with connection.cursor() as cursor:
					cursor.execute('SELECT name,count(*) from poll group by name order by count(*) desc')
					info=cursor.fetchall()
					print(info)	
					return info	
	def delete():
		with pg.connect(user='postgres', password='123', database='postgres',host='localhost') as connection:
			with connection.cursor() as cursor:
				cursor.execute("DELETE from poll")
					
	
	@classmethod			
	def load_all(self):
		with pg.connect(user='postgres', password='123', database='postgres',host='localhost') as connection:
			with connection.cursor() as cursor:
					cursor.execute('SELECT * from food')
					info=cursor.fetchall()
					return info
	def load_from_db_by_rname(rname):
		with pg.connect(user='postgres', password='123', database='postgres',host='localhost') as connection:
			with connection.cursor() as cursor:
				cursor.execute('select name from food')
				res=cursor.fetchall()
				for i in res:
					print(i[0],rname)
					if i[0]==rname:
						try:
							cursor.execute('delete from poll where name=%s',(rname,))
							cursor.execute('delete from food where name=%s',(rname,))
						except:
							cursor.execute('delete from food where name=%s',(rname,))
						return 1
		return 0
	def save_to_db(name,typ):
		with pg.connect(user='postgres', password='123', database='postgres',host='localhost') as connection:
			with connection.cursor() as cursor:
				try:
					cursor.execute('INSERT into food values(%s,%s)',(name,typ))
				except:
					return
				

class Bill:
	def save_to_db(url):
		with pg.connect(user='postgres', password='123', database='postgres',host='localhost') as connection:
			with connection.cursor() as cursor:
				cursor.execute('INSERT into bill (expense) values(%s)',(url,))
	def load_from_db():
		with pg.connect(user='postgres', password='123', database='postgres',host='localhost') as connection:
			with connection.cursor() as cursor:
				cursor.execute('SELECT * from bill')
				info=cursor.fetchall()
				return info			
class Room:
	def equest(rid,uid):
		global s
		with pg.connect(user='postgres', password='123', database='postgres',host='localhost') as connection:
			with connection.cursor() as cursor:
				try:
					cursor.execute('INSERT into request values (%s,%s)',(uid,rid))
					cursor.execute('SELECT vacancy from room where roomid=%s',rid)
					info=cursor.fetchone()
					print(info[0])
					if str(info[0])!=str(0):
						cursor.execute('UPDATE room set vacancy=vacancy+1 where roomid=(select room from student where sid=%s)',uid)
						cursor.execute('UPDATE room set vacancy=vacancy-1 where roomid=%s',rid)
						cursor.execute('UPDATE student set room=%s where sid=%s',(rid,uid))
						return
				except:
					print('exception')
					return
	def swap(uid,uid1):
		with pg.connect(user='postgres', password='123', database='postgres',host='localhost') as connection:
			with connection.cursor() as cursor:
				cursor.execute('SELECT room from student where sid=%s',(uid))
				info=cursor.fetchone()
				cursor.execute('SELECT room from student where sid=%s',(uid1))
				info1=cursor.fetchone()
				print(info1[0])
				cursor.execute('UPDATE student set room=%s where sid=%s',(info1[0],uid))
				cursor.execute('UPDATE student set room=%s where sid=%s',(info[0],uid1))
	@classmethod			
	def load_all(self):
		with pg.connect(user='postgres', password='123', database='postgres',host='localhost') as connection:
			with connection.cursor() as cursor:
					cursor.execute('SELECT * from room order by roomid')
					info=cursor.fetchall()
					return info
		
								
		

class Employee:
	def __init__(self,name, uid, ph,city,dob,gen,salary,days):
            self.uid=int(uid)
            self.gen=gen
            self.name=name
            self.ph=ph
            self.city=city
            self.dob=dob
            self.salary=salary
            self.days=days

	@classmethod
	def load_from_db_by_eid(self,eid):
		with pg.connect(user='postgres', password='123', database='postgres',host='localhost') as connection:
			with connection.cursor() as cursor:
				cursor.execute('select eid from employee')
				res=cursor.fetchall()
				for i in res:
					if str(i[0])==str(eid):
						cursor.execute('delete from employee where eid=%s',(eid,))
						return 1
		return 0

	def save_to_db(self):
        	with pg.connect(user='postgres', password='123', database='postgres',host='localhost') as connection:
            		with connection.cursor() as cursor:
                             try:
                                  cursor.execute('INSERT into employee values (%s,%s,%s,%s,%s,%s,%s,%s)',
(self.uid,self.name,self.city,self.ph,self.salary,self.days,self.dob,self.gen))
                                  return 0
                             except:
                                  return -1
	@classmethod
	def load_all(self):
		with pg.connect(user='postgres', password='123', database='postgres',host='localhost') as connection:
			with connection.cursor() as cursor:
				cursor.execute('SELECT eid,ename,ph,days,salary from employee order by eid')
				info=cursor.fetchall()
				print(info)
				return info
	@classmethod
	def att(self,uid):
		with pg.connect(user='postgres', password='123', database='postgres',host='localhost') as connection:
			with connection.cursor() as cursor:
				cursor.execute('UPDATE employee set days=days+1 where eid=%s',(str(uid)))
