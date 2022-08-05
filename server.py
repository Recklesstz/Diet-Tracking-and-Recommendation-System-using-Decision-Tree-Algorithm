from flask import Flask, redirect, url_for, render_template, request, flash, session
import re
import os
import sqlite3
import hashlib
from base64 import decode
import requests
import json
from nutritionix import Nutritionix
from decimal import Decimal
from datetime import date, datetime,timedelta 
import time
import pandas as pd
import numpy as np
import pickle
from sklearn.tree import DecisionTreeClassifier # Import Decision Tree Classifier
from sklearn.model_selection import train_test_split # Import train_test_split function
from sklearn import metrics #Import scikit-learn metrics module for accuracy calculation
from sklearn.preprocessing import LabelEncoder 
import random


app = Flask(__name__)
app.secret_key='honsproject'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.jinja_env.globals.update(zip=zip)

bf_meal = []
onefood = []
lunch_meal = []
dinner_meal = []
snack_meal = []



@app.route("/delete_food", methods =['GET','POST'])
def delete_food():
	if request.method == 'GET':
		return redirect(url_for('add_successful'))

	else:
		mealtime = request.form['mealtime']
		item = request.form['fname']

		uid = session['uid']
		track_date = str(datetime.today().strftime ('%Y-%m-%d'))
		
		bf_list = []
		lunch_list = []
		dinner_list = []
		snack_list = []
		# for i in session['bf_numbers']:

			
		# 	print(float(i))
		# 	session.modified = True
		# 	print(type(i))
		if mealtime == "Breakfast":
			
			for i in bf_meal:
				if item == i[0]:
					bf_meal.remove(i)

			for i in session['bf_meal']:
				if item == i[0]:
					session['bf_meal'].remove(i)
					session.modified = True

			
					

				
					for j in session['bf_numbers']:
						j = round(Decimal(j), 2)
						bf_list.append(j)
					
				
					bf_list[0]-=round(Decimal(i[3]), 2)
					bf_list[1]-=round(Decimal(i[4]), 2)
					bf_list[2]-=round(Decimal(i[5]), 2)
					bf_list[3]-=round(Decimal(i[6]), 2)

					try:
						with get_connection() as conn:
							cur = conn.cursor()
						
							cur.execute("select * from tracking where track_date=? and u_id=?",(track_date,uid,))
							track_info= cur.fetchall()
				
							calorie = round(Decimal(track_info[0][6]), 2)-round(Decimal(i[3]), 2)
							protein = round(Decimal(track_info[0][7]), 2)-round(Decimal(i[4]), 2)
							carb = round(Decimal(track_info[0][8]), 2)-round(Decimal(i[5]), 2)
							fat = round(Decimal(track_info[0][9]), 2)-round(Decimal(i[6]), 2)
						
							cur2 = conn.cursor()
							cur2.execute("select * from tracking where track_date=? and u_id=?",(track_date,uid,))
							u_data = cur2.fetchone()

							item_in_db = u_data[2].split(",")[:-1]
							item_to_db = ""

							for i in item_in_db:
								if item == i:
									item_in_db.remove(i)

							item_to_db = ",".join(item_in_db)+","

							cur2.execute("update tracking set track_breakfast=?,track_calorie=?,track_protein=?,track_carb=?,track_fat=? where track_date=? and u_id=?", (item_to_db,float(calorie),float(protein),float(carb),float(fat),track_date,uid))
							conn.commit()

					except sqlite3.Error as e:
						return (f'{e}')
					finally:
						conn.close()


					session['bf_numbers'].clear()

					[x for x in session['bf_numbers'] if x]

					session.modified = True
					for i in bf_list:
						session['bf_numbers'].append(i)	
						session.modified = True

					

					
					
					

		
		if mealtime == "Lunch":
			foodlist = session['lunch_meal']

			for i in lunch_meal:
				if item == i[0]:
					lunch_meal.remove(i)

			for i in foodlist:
				if item == i[0]:
					foodlist.remove(i)
				
			
					for j in session['lunch_numbers']:
						j = round(Decimal(j), 2)
						lunch_list.append(j)
					
				
					lunch_list[0]-=round(Decimal(i[3]), 2)
					lunch_list[1]-=round(Decimal(i[4]), 2)
					lunch_list[2]-=round(Decimal(i[5]), 2)
					lunch_list[3]-=round(Decimal(i[6]), 2)

					try:
						with get_connection() as conn:
							cur = conn.cursor()
						
							cur.execute("select * from tracking where track_date=? and u_id=?",(track_date,uid,))
							track_info= cur.fetchall()
				
							calorie = round(Decimal(track_info[0][6]), 2)-round(Decimal(i[3]), 2)
							protein = round(Decimal(track_info[0][7]), 2)-round(Decimal(i[4]), 2)
							carb = round(Decimal(track_info[0][8]), 2)-round(Decimal(i[5]), 2)
							fat = round(Decimal(track_info[0][9]), 2)-round(Decimal(i[6]), 2)
						
							cur2 = conn.cursor()
							cur2.execute("select * from tracking where track_date=? and u_id=?",(track_date,uid,))
							u_data = cur2.fetchone()

							item_in_db = u_data[3].split(",")[:-1]
							item_to_db = ""

							for i in item_in_db:
								if item == i:
									item_in_db.remove(i)

							item_to_db = ",".join(item_in_db)+","
							
							cur2.execute("update tracking set track_lunch=?,track_calorie=?,track_protein=?,track_carb=?,track_fat=? where track_date=? and u_id=?", (item_to_db,float(calorie),float(protein),float(carb),float(fat),track_date,uid))
							conn.commit()

					except sqlite3.Error as e:
						return (f'{e}')
					finally:
						conn.close()

					session['lunch_numbers'].clear()

					[x for x in session['lunch_numbers'] if x]

					session.modified = True
					for i in lunch_list:
						session['lunch_numbers'].append(i)	
						session.modified = True


		if mealtime == "Snack":
			foodlist = session['snack_meal']

			for i in snack_meal:
				if item == i[0]:
					snack_meal.remove(i)

			for i in foodlist:
				if item == i[0]:
					foodlist.remove(i)
				
			
					for j in session['snack_numbers']:
						j = round(Decimal(j), 2)
						snack_list.append(j)
					
				
					snack_list[0]-=round(Decimal(i[3]), 2)
					snack_list[1]-=round(Decimal(i[4]), 2)
					snack_list[2]-=round(Decimal(i[5]), 2)
					snack_list[3]-=round(Decimal(i[6]), 2)

					try:
						with get_connection() as conn:
							cur = conn.cursor()
						
							cur.execute("select * from tracking where track_date=? and u_id=?",(track_date,uid,))
							track_info= cur.fetchall()
				
							calorie = round(Decimal(track_info[0][6]), 2)-round(Decimal(i[3]), 2)
							protein = round(Decimal(track_info[0][7]), 2)-round(Decimal(i[4]), 2)
							carb = round(Decimal(track_info[0][8]), 2)-round(Decimal(i[5]), 2)
							fat = round(Decimal(track_info[0][9]), 2)-round(Decimal(i[6]), 2)
						
							cur2 = conn.cursor()
							cur2.execute("select * from tracking where track_date=? and u_id=?",(track_date,uid,))
							u_data = cur2.fetchone()

							item_in_db = u_data[4].split(",")[:-1]
							item_to_db = ""

							for i in item_in_db:
								if item == i:
									item_in_db.remove(i)

							item_to_db = ",".join(item_in_db)+","
				
							cur2.execute("update tracking set track_snack=?,track_calorie=?,track_protein=?,track_carb=?,track_fat=? where track_date=? and u_id=?", (item_to_db,float(calorie),float(protein),float(carb),float(fat),track_date,uid))
							conn.commit()

					except sqlite3.Error as e:
						return (f'{e}')
					finally:
						conn.close()

					session['snack_numbers'].clear()

					[x for x in session['snack_numbers'] if x]

					session.modified = True
					for i in snack_list:
						session['snack_numbers'].append(i)	
						session.modified = True

					

		if mealtime == "Dinner":
			foodlist = session['dinner_meal']
			for i in dinner_meal:
				if item == i[0]:
					dinner_meal.remove(i)

			for i in foodlist:
				if item == i[0]:
					foodlist.remove(i)
				
			
					for j in session['dinner_numbers']:
						j = round(Decimal(j), 2)
						dinner_list.append(j)
					
				
					dinner_list[0]-=round(Decimal(i[3]), 2)
					dinner_list[1]-=round(Decimal(i[4]), 2)
					dinner_list[2]-=round(Decimal(i[5]), 2)
					dinner_list[3]-=round(Decimal(i[6]), 2)

					try:
						with get_connection() as conn:
							cur = conn.cursor()
						
							cur.execute("select * from tracking where track_date=? and u_id=?",(track_date,uid,))
							track_info= cur.fetchall()
				
							calorie = round(Decimal(track_info[0][6]), 2)-round(Decimal(i[3]), 2)
							protein = round(Decimal(track_info[0][7]), 2)-round(Decimal(i[4]), 2)
							carb = round(Decimal(track_info[0][8]), 2)-round(Decimal(i[5]), 2)
							fat = round(Decimal(track_info[0][9]), 2)-round(Decimal(i[6]), 2)
						
							cur2 = conn.cursor()
							cur2.execute("select * from tracking where track_date=? and u_id=?",(track_date,uid,))
							u_data = cur2.fetchone()

							item_in_db = u_data[5].split(",")[:-1]
							item_to_db = ""

							for i in item_in_db:
								if item == i:
									item_in_db.remove(i)

							item_to_db = ",".join(item_in_db)+","
							cur2.execute("update tracking set track_dinner=?,track_calorie=?,track_protein=?,track_carb=?,track_fat=? where track_date=? and u_id=?", (item_to_db,float(calorie),float(protein),float(carb),float(fat),track_date,uid))
							conn.commit()

					except sqlite3.Error as e:
						return (f'{e}')
					finally:
						conn.close()

					session['dinner_numbers'].clear()

					[x for x in session['dinner_numbers'] if x]

					session.modified = True
					for i in dinner_list:
						session['dinner_numbers'].append(i)	
						session.modified = True

					
				
								
		return render_template('add_food.html',mealtime=mealtime)
	


def get_connection():
	conn = sqlite3.connect('diet_recommendation.db')
	conn.row_factory=sqlite3.Row # to be able to reference by column name
	return conn

def pwd_security(passwd):
	"""A strong password must be at least 8 characters long
	   and must contain a lower case letter, an upper case letter,
	   and at least 3 digits.
	   Returns True if passwd meets these criteria, otherwise returns False.
	   """
	# check password length
	# check password for uppercase, lowercase and numeric chars
	hasupper = False	
	haslower = False
	digitcount = 0
	digit= False
	strong = False
	length = True
	special = False
	for c in passwd:
		if (c.isupper()==True):
			hasupper= True
		elif (c.islower()==True):
			haslower=True
		elif (c.isdigit()==True):
			digitcount+=1
			digit = True
		elif re.findall('[^A-Za-z0-9]',c):
			special = True
	if hasupper == True and haslower == True and digit == True and special == True:
		strong = True
	if len(passwd) <8:
		length = False
	return strong,haslower,hasupper,digit,length, special

def pwd_encode(pwd):
	secure_pwd =hashlib.md5(pwd.encode()).hexdigest()
	return secure_pwd



@app.route("/update_profile", methods =['GET','POST'] )
def edit_weight():
	if request.method == 'GET':

		try:
			with get_connection() as conn:
				cur = conn.cursor()
				cur.execute("select * from user where u_id=?",(session['uid'],))
				u_data = cur.fetchone()
				name = u_data[1]
				age = u_data[4]
				weight = u_data[6]
				email = u_data[5]
				password = session['u_pass']
				gender = u_data[3]
				ft = u_data[7]
				inch = u_data[8]
				vegan = u_data[12]
				allergy = u_data[13]

		except sqlite3.Error as e:
			return (f'{e}')
		finally:
			conn.close()
		

		return render_template('edit_profile.html', name= name,
													age = age,
													weight = weight,
													email = email,
													password = password,
													gender = gender,
													ft = ft,
													inch = inch,
													vegan = vegan,
													allergy = allergy)
	else:
		# name = u_data[1]
		# age = u_data[4]
		# weight = u_data[6]
		# email = u_data[5]
		# password = session['u_pass']
		# gender = u_data[3]
		# ft = u_data[7]
		# inch = u_data[8]
		# vegan = u_data[12]
		# allergy = u_data[13]

		return redirect(url_for('profile'))

@app.route("/add_food", methods =['GET','POST'] )
def add_food():
	if request.method == 'GET':
		
		return render_template('add_food.html')

	else:
		mealtime = request.form['mealtime']
		
		
		return render_template('add_food.html',mealtime=mealtime)

def food_list(meal,item):
	
	meal.append(item)

	return meal

def one_food(item,portion,p_type):
	
	meal = [item,portion,p_type]

	return meal

@app.route("/add_successful", methods =['GET','POST'] )

def add_successful():
	
	if request.method == 'GET':
		
		return render_template('add_food.html')

	else:
		mealtime = request.form['mealtime']
		
		item_name = request.form['food']
		foodPortion = int(request.form['portion'])
		portion_type = request.form['portion_type']

		app_id = "88ae9566"
		app_key = "7c955adc27b276ef3f07ca3c0501e4ee	—"

		nix = Nutritionix(app_id, app_key)

		item = nix.search().nxql(
    		fields = [
    					"item_name",
    					"nf_calories",
    					"nf_protein",
    					"nf_total_carbohydrate",
    					"nf_total_fat",
    					"nf_serving_size_qty",
    					"nf_serving_size_unit"
  								],
  			offset= 0,
  			limit= 1,
  
  			query= item_name,
  			filters = {
      					"nf_serving_size_unit": portion_type
      					
  						}

					).json()
		
		name = item['hits'][0].get("fields").get('item_name')
		calories = item['hits'][0].get("fields").get('nf_calories')
		protein = item['hits'][0].get("fields").get('nf_protein')
		carb = item['hits'][0].get("fields").get('nf_total_carbohydrate')
		fat = item['hits'][0].get("fields").get('nf_total_fat')
		quantity = foodPortion
		unit = item['hits'][0].get("fields").get('nf_serving_size_unit')

		finalCalorie = (calories*foodPortion)/quantity
		finalProtein = (protein*foodPortion)/quantity
		finalCarb = (carb*foodPortion)/quantity
		finalFat = (fat*foodPortion)/quantity

		food = [item_name,quantity,unit,finalCalorie,finalProtein,finalCarb,finalFat]
		uid = session['uid']
		track_date = str(datetime.today().strftime ('%Y-%m-%d'))

		try:
			with get_connection() as conn:
				cur = conn.cursor()
						
				cur.execute("select * from tracking where track_date=? and u_id=?",(track_date,uid,))
				track_info= cur.fetchall()
				

				calorie = round(Decimal(track_info[0][6]), 2)+round(Decimal(food[3]), 2)
				protein = round(Decimal(track_info[0][7]), 2)+round(Decimal(food[4]), 2)
				carb = round(Decimal(track_info[0][8]), 2)+round(Decimal(food[5]), 2)
				fat = round(Decimal(track_info[0][9]), 2)+round(Decimal(food[6]), 2)
						
				cur2 = conn.cursor()
				
				if mealtime == "Breakfast":
					meal_input = track_info[0][2] + food[0] +","
					
					cur2.execute("update tracking set track_breakfast=?,track_calorie=?,track_protein=?,track_carb=?,track_fat=? where track_date=? and u_id=?", (meal_input,float(calorie),float(protein),float(carb),float(fat),track_date,uid))
					conn.commit()


				if mealtime == "Lunch":
					meal_input = track_info[0][3] + food[0] +","
					
					
					cur2.execute("update tracking set track_lunch=?,track_calorie=?,track_protein=?,track_carb=?,track_fat=? where track_date=? and u_id=?", (meal_input,float(calorie),float(protein),float(carb),float(fat),track_date,uid))
					conn.commit()

				if mealtime == "Snack":
					meal_input = track_info[0][4] + food[0] +","
					
					cur2.execute("update tracking set track_snack=?,track_calorie=?,track_protein=?,track_carb=?,track_fat=? where track_date=? and u_id=?", (meal_input,float(calorie),float(protein),float(carb),float(fat),track_date,uid))
					conn.commit()

				if mealtime == "Dinner":
					meal_input = track_info[0][5] + food[0] +","
					
					cur2.execute("update tracking set track_dinner=?,track_calorie=?,track_protein=?,track_carb=?,track_fat=? where track_date=? and u_id=?", (meal_input,float(calorie),float(protein),float(carb),float(fat),track_date,uid))
					conn.commit()
				

		except sqlite3.Error as e:
			return (f'{e}')
		finally:
			conn.close()

		
		if mealtime == "Breakfast":
			
			session['bf_numbers'] = [0,0,0,0]
			session['bf_meal'] = food_list(bf_meal,food)
			
			for i in session['bf_meal']:
						
				session['bf_numbers'][0]+=round(Decimal(i[3]), 2)
				session['bf_numbers'][1]+=round(Decimal(i[4]), 2)
				session['bf_numbers'][2]+=round(Decimal(i[5]), 2)
				session['bf_numbers'][3]+=round(Decimal(i[6]), 2)
			print(session['bf_meal'])
					

		if mealtime == "Lunch":
			session['lunch_numbers'] = [0,0,0,0]
			session['lunch_meal'] = food_list(lunch_meal,food)

			for i in session['lunch_meal']:			
				session['lunch_numbers'][0]+=round(Decimal(i[3]), 2)
				session['lunch_numbers'][1]+=round(Decimal(i[4]), 2)
				session['lunch_numbers'][2]+=round(Decimal(i[5]), 2)
				session['lunch_numbers'][3]+=round(Decimal(i[6]), 2)
				
		
		if mealtime == "Snack":
			session['snack_numbers'] = [0,0,0,0]
			session['snack_meal'] = food_list(snack_meal,food)

			for i in session['snack_meal']:
						
				session['snack_numbers'][0]+=round(Decimal(i[3]), 2)
				session['snack_numbers'][1]+=round(Decimal(i[4]), 2)
				session['snack_numbers'][2]+=round(Decimal(i[5]), 2)
				session['snack_numbers'][3]+=round(Decimal(i[6]), 2)

		if mealtime == "Dinner":
			session['dinner_numbers'] = [0,0,0,0]
			session['dinner_meal'] = food_list(dinner_meal,food)

			for i in session['dinner_meal']:
						
				session['dinner_numbers'][0]+=round(Decimal(i[3]), 2)
				session['dinner_numbers'][1]+=round(Decimal(i[4]), 2)
				session['dinner_numbers'][2]+=round(Decimal(i[5]), 2)
				session['dinner_numbers'][3]+=round(Decimal(i[6]), 2)
		

		return render_template('add_food.html',mealtime=mealtime)

@app.route("/track", methods = ['GET','POST'])
def track():
	if request.method == 'GET':
		uid = session['uid']
		
		track_date = str(datetime.today().strftime ('%Y-%m-%d'))

		try:
			with get_connection() as conn:
				cur = conn.cursor()
				cur.execute("select * from tracking where track_date=? and u_id=?",(track_date,uid))
				track_info= cur.fetchall()


				if track_info:
					pass
				else:
					try:
						with get_connection() as conn:
							cur = conn.cursor()
							breakfast=""
							lunch = ""
							dinner = ""
							snack = ""
							cur.execute("insert into tracking (track_date,u_id,track_calorie,track_protein,track_fat,track_carb,track_breakfast,track_lunch,track_snack,track_dinner) values (?,?,0,0,0,0,?,?,?,?)",(track_date,uid,breakfast,lunch,snack,dinner))
							conn.commit()

							cur.execute("select * from tracking where track_date=? and u_id=?",(track_date,uid))
							track_info= cur.fetchall()
							if track_info[0][2] == ",":
								cur.execute("update tracking set track_breakfast=?",("",))
								conn.commit()
					except sqlite3.Error as e:
						return (f'{e}')
					finally:
						conn.close()

				cur.execute("select * from tracking where track_date=? and u_id=?",(track_date,uid))
				track_info= cur.fetchall()

				protein_goal = session['u_info'][14]
				carb_goal = session['u_info'][15]
				fat_goal = session['u_info'][16]
				breakfast = track_info[0][2]
				lunch = track_info[0][3]
				snack = track_info[0][4]
				dinner = track_info[0][5]

					
				protein_consumed = track_info[0][7]
				carb_consumed = track_info[0][8]
				fat_consumed = track_info[0][9]

				calorie_goal = session['u_info'][17]
				calorie_consumed = track_info[0][6]

				protein_percent = "{:.2f}".format((protein_consumed/protein_goal) * 100)
				carb_percent = "{:.2f}".format((carb_consumed/carb_goal) * 100)
				fat_percent = "{:.2f}".format((fat_consumed/fat_goal) * 100)
				calorie_percent = "{:.2f}".format((calorie_consumed/calorie_goal) * 100)
					
				try:
					with get_connection() as conn:
						cur = conn.cursor()
						cur.execute("update tracking set track_calorie=?,track_protein=?,track_carb=?,track_fat=? where track_date=? and u_id=?", (calorie_consumed,protein_consumed,carb_consumed,fat_consumed,track_date,uid,))
						conn.commit()

				except sqlite3.Error as e:
					return (f'{e}')
				finally:
					conn.close()
					
				return render_template('track.html',p_goal=protein_goal,
											c_goal = carb_goal,
											f_goal=fat_goal,
											p_consumed = protein_consumed,
											c_consumed=carb_consumed,
											f_consumed = fat_consumed,
											p_percent = protein_percent,
											c_percent = carb_percent,
											f_percent = fat_percent,
											cal_percent = calorie_percent,
											cal_goal = calorie_goal,
											cal_consumed = calorie_consumed,
											breakfast = breakfast,
											lunch = lunch,
											snack = snack,
											dinner = dinner,
											)
						
		except sqlite3.Error as e:
			return (f'{e}')
		finally:
			conn.close()
		
	else:
		return render_template('track.html')


@app.route("/register", methods = ['GET','POST'])
def citizen_register():
	if request.method == 'GET':
		return render_template('register.html')
	else:
		name = request.form['name']
		
		email = request.form['email']
		password = request.form['password']
		
		return render_template('profilesetup.html',name=name,email=email,password=password)

@app.route("/login", methods = ['GET','POST'])
def login():
	if request.method == 'GET':
		return render_template('login.html')
	else:
		
		session['uid'] = 0
		email = request.form['email']
		password = request.form['password']
		secure_pwd = pwd_encode(password)
		msg=''
		try:
			with get_connection() as conn:
				cur = conn.cursor()
				cur.execute("select * from user where u_email=?",(email,))
				u_info= cur.fetchall()
				if not u_info:
					flash(f'The email address ({email}) that you entered does not exist in our database.')
					return redirect(url_for('login'))
				else:
					for row in u_info:
						session['uid'] = row[0]
						u_pass = row[2] 
						u_name = row[1]
						u_date = row[-1]
					
					if secure_pwd == u_pass:
						days = []
						flash(f'Your have successfully logged in as {u_name}')
						session['u_logged'] = True
						session['u_info'] = []
						session['u_pass'] = password 

						track_date = datetime.today().strftime ('%Y-%m-%d')
						sdate = datetime.strptime(u_date, '%Y-%m-%d').date()
						edate = datetime.strptime(track_date, '%Y-%m-%d').date()
						delta = edate - sdate     

						for i in range(delta.days + 1):
							day = sdate + timedelta(days=i)
							days.append(str(day))
							journey = len(days)

						try:
							with get_connection() as conn:
								cur = conn.cursor()
								cur2 = conn.cursor()
								cur2.execute("update user set u_journey=? where u_id=?", (journey,session['uid'],))
								conn.commit()

								cur.execute("select * from user where u_id=?",(session['uid'],))
								u_info = cur.fetchone()
				
								for row in u_info:
									session['u_info'].append(row)

						except sqlite3.Error as e:
							return (f'{e}')
						finally:
							conn.close()

						return redirect(url_for('index'))
					else:
						session.pop('uid',None)
						flash('Sorry the credentails you are using are invalid')
						return redirect(url_for('login'))

		except sqlite3.Error as e:
			return (f'{e}')
		finally:
			conn.close()

@app.route("/setup", methods = ['GET','POST'])
def profilesetup():
	if request.method == 'GET':
		return render_template('profilesetup.html')

	else:
		name = request.form['name']
		email = request.form['email']
		passwd = request.form['password']
		password = pwd_encode(passwd)
		age = int(request.form['age'])
		gender = request.form['gender']
		vegan = request.form['vegan']
		allergy = request.form['allergy']
		weight_lb = int(request.form['weight'])
		feet = int(request.form['feet'])
		inches = int(request.form['inches'])
		activity_level = request.form['activity']
		height_bmi = int((feet * 12) + inches)
		bmr = 0
		body_status = ""
		BMI =  weight_lb / (height_bmi*height_bmi) * 703
		bodyfat = 0

		if gender == "male":
			bmr = int((4.536 * weight_lb) + (15.88 * height_bmi) - (5 * age) + 5)
			bodyfat = int((1.20 * BMI) + (0.23 * age) - 16.2)
		else:
			bmr = int((4.536 * weight_lb) + (15.88 * height_bmi) - (5 * age) - 161)
			bodyfat = int((1.20 * BMI) + (0.23 * age) - 5.4)

		calorie = 0

		if activity_level == "sedentary":
			calorie = int(bmr*1.2)

		elif activity_level == "lightly active":
			calorie = int(bmr * 1.375)

		elif activity_level == "moderately active":
			calorie = int(bmr * 1.55)

		elif activity_level == "very active":
			calorie = int(bmr * 1.725)

		elif activity_level == "extra active":
			calorie = int(bmr * 1.9)

		if BMI < 18.5:
			body_status = "underweight"

		elif BMI >= 18.5 and BMI <= 24.9 :
			body_status = "healthy weight"

		elif BMI >= 25 and BMI <= 29.9 :
			body_status = "overweight"

		elif BMI >= 30 :
			body_status = "obese"

		protein = int(((calorie-500) * 0.30)/4)
		carb = int(((calorie-500)* 0.40)/4)
		fat = int(((calorie-500) * 0.30)/9)
		fiber = int(calorie/1000*14)
		journey = 1
		breakfast = int((calorie-500) * 0.30)
		snack = int((calorie-500)* 0.10)
		lunch = int((calorie-500)* 0.35)
		dinner = int((calorie-500)* 0.25)

		try:
			with get_connection() as conn:
				db = conn.cursor()
				db.execute("insert into user (u_username,u_email,u_password,u_age,u_gender,u_vegan,u_allergy,u_weight,u_feet,u_inches,u_bmi,u_activitylevel,u_protein,u_carb,u_fat,u_fiber,u_calories,u_journey,u_bodyfat,u_status,u_startdate) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(name,email,password,age,gender,vegan,allergy,weight_lb,feet,inches,int(BMI),activity_level,protein,carb,fat,fiber,calorie,journey,bodyfat,body_status,datetime.today().strftime ('%Y-%m-%d'),))
				conn.commit()
				flash('Successfully Registered')

		except sqlite3.Error as e:
			return (f'{e}')
		finally:
			conn.close()

	
		return redirect(url_for('login'))

@app.route("/profile", methods = ['GET','POST'])
def profile():
	if request.method == 'GET':
		uid = session['uid']
		try:
			with get_connection() as conn:
				db = conn.cursor()
				db.execute("select * from user where u_id=?",(uid,))
				u_info = db.fetchone()

				

				
		except sqlite3.Error as e:
			return (f'{e}')
		finally:
			conn.close()

		return render_template('profile.html',u_info = u_info)

	else:
		return render_template('profile.html')


@app.route("/recommendation", methods = ['GET','POST'])
def recommendation():
	if request.method == 'GET':
		return render_template('recommendation.html')

	else:
		dataset = pd.read_csv('dietdataset.csv')

		dataset = pd.DataFrame(data=dataset.iloc[:,0:10].values,columns = ['meal_name','carb','meat','vege','fruit', 'type','vegan','allergy','time'])
		le = LabelEncoder()
		dataset_encoded = dataset.iloc[:,0:10]
		for i in dataset_encoded:
			dataset_encoded[i] = le.fit_transform(dataset_encoded[i])
			
			model = pickle.load(open('model','rb'))

		bf_vege_input = []
		bf_meat_input = []
		bf_carb_input = []
		bf_fruit_input = []

		bf_vege = random.choice(request.form.getlist('vege'))
		bf_meat = random.choice(request.form.getlist('meat'))
		bf_carb = random.choice(request.form.getlist('carb'))
		bf_fruit = random.choice(request.form.getlist('fruit'))

		bf_vege_input.append(bf_vege)
		bf_meat_input.append(bf_meat)
		bf_carb_input.append(bf_carb)
		bf_fruit_input.append(bf_fruit)

		lunch_vege_input = []
		lunch_meat_input = []
		lunch_carb_input = []
		lunch_fruit_input = []

		lunch_vege = random.choice(request.form.getlist('vege'))
		lunch_meat = random.choice(request.form.getlist('meat'))
		lunch_carb = random.choice(request.form.getlist('carb'))
		lunch_fruit = random.choice(request.form.getlist('fruit'))

		lunch_vege_input.append(lunch_vege)
		lunch_meat_input.append(lunch_meat)
		lunch_carb_input.append(lunch_carb)
		lunch_fruit_input.append(lunch_fruit)

		snack_vege_input = []
		snack_meat_input = []
		snack_carb_input = []
		snack_fruit_input = []

		snack_vege = random.choice(request.form.getlist('vege'))
		snack_meat = random.choice(request.form.getlist('meat'))
		snack_carb = random.choice(request.form.getlist('carb'))
		snack_fruit = random.choice(request.form.getlist('fruit'))

		snack_vege_input.append(snack_vege)
		snack_meat_input.append(snack_meat)
		snack_carb_input.append(snack_carb)
		snack_fruit_input.append(snack_fruit)

		dinner_vege_input = []
		dinner_meat_input = []
		dinner_carb_input = []
		dinner_fruit_input = []

		dinner_vege = random.choice(request.form.getlist('vege'))
		dinner_meat = random.choice(request.form.getlist('meat'))
		dinner_carb = random.choice(request.form.getlist('carb'))
		dinner_fruit = random.choice(request.form.getlist('fruit'))

		dinner_vege_input.append(dinner_vege)
		dinner_meat_input.append(dinner_meat)
		dinner_carb_input.append(dinner_carb)
		dinner_fruit_input.append(dinner_fruit)
		
		type_breakfast = request.form.getlist('breakfast_dishes')
		type_lunch =  request.form.getlist('lunch_dishes')
		type_dinner = request.form.getlist('dinner_dishes')
		type_snack = request.form.getlist('snack_dishes')
		print(type_breakfast)
		allergy_input = []
		vegan_input = []
		allergy_input.append(session['u_info'][13])
		vegan_input.append(session['u_info'][12])

		print(type_breakfast,allergy_input,vegan_input)
		time_breakfast = ['Breakfast']
		time_snack = ['Snack']
		time_lunch = ['Lunch']
		time_dinner = ['Dinner']
    	
		def input_encode(entry,room): 
			meal = dataset.values.tolist()
			meal_encode = dataset_encoded.values.tolist()
			lists = []
			encode = []   
			for i in entry:
				for j in meal:
					if i==j[room]:
						lists.append(j)
						break
                 
			for j in lists: 
				encode.append(meal_encode[meal.index(j)][room])
        
			return encode
#         return meal_encode[meal.index(j)][room]

		def input_decode(entry,room): 
			meal = dataset.values.tolist()
			meal_encode = dataset_encoded.values.tolist()
			lists = []
			decode = []   
			for i in entry:
				for j in meal_encode:
					if i==j[room]:
						lists.append(j)
						break
                 
			for j in lists: 
				decode.append(meal[meal_encode.index(j)][room])
        
			return decode

		bf_carb_encode = input_encode(bf_carb_input,1)[0]
		bf_meat_encode = input_encode(bf_meat_input,2)[0]
		bf_vege_encode = input_encode(bf_vege_input,3)[0]
		bf_fruit_encode = input_encode(bf_fruit_input,4)[0]

		lunch_carb_encode = input_encode(lunch_carb_input,1)[0]
		lunch_meat_encode = input_encode(lunch_meat_input,2)[0]
		lunch_vege_encode = input_encode(lunch_vege_input,3)[0]
		lunch_fruit_encode = input_encode(lunch_fruit_input,4)[0]

		dinner_carb_encode = input_encode(dinner_carb_input,1)[0]
		dinner_meat_encode = input_encode(dinner_meat_input,2)[0]
		dinner_vege_encode = input_encode(dinner_vege_input,3)[0]
		dinner_fruit_encode = input_encode(dinner_fruit_input,4)[0]

		snack_carb_encode = input_encode(snack_carb_input,1)[0]
		snack_meat_encode = input_encode(snack_meat_input,2)[0]
		snack_vege_encode = input_encode(snack_vege_input,3)[0]
		snack_fruit_encode = input_encode(snack_fruit_input,4)[0]
				
		breakfast_encode = input_encode(type_breakfast,5)[0]
		lunch_encode = input_encode(type_lunch,5)[0]
		snack_encode = input_encode(type_snack,5)[0]
		dinner_encode = input_encode(type_dinner,5)[0]

		vegan_encode = input_encode(vegan_input,6)[0]
		allergy_encode = input_encode(allergy_input,7)[0]
		bf_time_encode = input_encode(time_breakfast,8)[0]
		lunch_time_encode = input_encode(time_lunch,8)[0]
		snack_time_encode = input_encode(time_snack,8)[0]
		dinner_time_encode = input_encode(time_dinner,8)[0]

		bf_input = [bf_carb_encode,bf_meat_encode,bf_vege_encode,bf_fruit_encode,breakfast_encode,vegan_encode,allergy_encode,bf_time_encode]
		
		bf_result = model.predict([bf_input])
		bf_prediction = input_decode(bf_result,0)	
			
		lunch_input = [lunch_carb_encode,lunch_meat_encode,lunch_vege_encode,lunch_fruit_encode,lunch_encode,vegan_encode,allergy_encode,lunch_time_encode]
		lunch_result = model.predict([lunch_input])
		lunch_prediction = input_decode(lunch_result,0)	
			
		snack_input = [snack_encode,snack_encode,snack_encode,snack_encode,snack_encode,vegan_encode,allergy_encode,snack_time_encode]
		snack_result = model.predict([snack_input])
		snack_prediction = input_decode(snack_result,0)	
						
		dinner_input = [dinner_encode,dinner_encode,dinner_encode,dinner_encode,dinner_encode,vegan_encode,allergy_encode,dinner_time_encode]
		dinner_result = model.predict([dinner_input])
		dinner_prediction = input_decode(dinner_result,0)	
		
		try:
			with get_connection() as conn:
				cur = conn.cursor()
				cur.execute("select * from user where u_id=?",(session['uid'],))
				data = cur.fetchone()
				calorie = data[17]
				protein = data[14]
				carb = data[15]
				fat = data[16]

		except sqlite3.Error as e:
			return (f'{e}')
		finally:
			conn.close()

		bf_cal = int(int(calorie)* 0.30)
		snack_cal = int(int(calorie)* 0.10)
		lunch_cal = int(int(calorie)* 0.35)
		dinner_cal = int(int(calorie)* 0.25)

		bf_protein = int(int(protein)* 0.30)
		snack_protein = int(int(protein)* 0.10)
		lunch_protein = int(int(protein)* 0.35)
		dinner_protein = int(int(protein)* 0.25)
		
		bf_carb = int(int(carb)* 0.30)
		snack_carb = int(int(carb)* 0.10)
		lunch_carb = int(int(carb)* 0.35)
		dinner_carb = int(int(carb)* 0.25)

		bf_fat = int(int(fat)* 0.30)
		snack_fat = int(int(fat)* 0.10)
		lunch_fat = int(int(fat)* 0.35)
		dinner_fat = int(int(fat)* 0.25)

		return render_template('recommendation.html',bf_prediction = bf_prediction[0],
													 lunch_prediction = lunch_prediction[0],
													 snack_prediction = snack_prediction[0],
													 dinner_prediction = dinner_prediction[0],
													 bf_cal = bf_cal,
													 snack_cal = snack_cal,
													 lunch_cal = lunch_cal,
													 dinner_cal = dinner_cal,
													 bf_protein = bf_protein,
													 snack_protein = snack_protein,
													 lunch_protein = lunch_protein,
													 dinner_protein = dinner_protein,
													 bf_carb = bf_carb,
													 snack_carb = snack_carb,
													 lunch_carb = lunch_carb,
													 dinner_carb = dinner_carb,
													 bf_fat = bf_fat,
													 snack_fat = snack_fat,
													 lunch_fat = lunch_fat,
													 dinner_fat = dinner_fat,

													 )




@app.route("/recommend_setup", methods = ['GET','POST'])
def recommend_setup():
	if request.method == 'GET':
		print(session['u_info'][12])
		return render_template('recommendsetup.html')

	else:
		
		return render_template('recommendsetup.html')

@app.route("/progress", methods = ['GET','POST'])
def progress():
	if request.method == 'GET':
		uid = session['uid']
		track_date = datetime.today().strftime ('%Y-%m-%d')
		days = []
		display_day = []
		weeks = []
		day_weight = []
		week_weight = []
		sdate = datetime.strptime(session['u_info'][-1], '%Y-%m-%d').date()
		edate = datetime.strptime(track_date, '%Y-%m-%d').date()
		delta = edate - sdate     

		for i in range(delta.days + 1):
			day = sdate + timedelta(days=i)
			days.append(str(day))

		
		
		split_list = [days[x:x+7] for x in range(0, len(days), 7)]
		weeknum = split_list.index(split_list[-1])+1
		pw_date = split_list[-1][-1]
		
		pw_weight =[]
		try:
			with get_connection() as conn:
				cur = conn.cursor()
				cur.execute("select * from progress where u_id=? and p_date=?",(uid,track_date))
				data = cur.fetchone()
				if not data:
					cur.execute("insert into progress (u_id,p_date,p_weight) values (?,?,?)",(session['u_info'][0],track_date,session['u_info'][6]))
					conn.commit()

				cur.execute("select * from progress where u_id=? and p_date=?",(uid,track_date))
				data2 = cur.fetchone()	
				for i in data2:
					pw_weight.append(data[2])
					

				cur.execute("select * from progress_week where u_id=? and pw_num=?",(uid,weeknum))
				week_exist = cur.fetchone()

				if not week_exist:
					
						
					cur.execute("insert into progress_week (u_id,pw_num,pw_weight) values (?,?,?)",(session['u_info'][0],weeknum,pw_weight[0]))
					conn.commit()



				
					
			cur.execute("select * from progress_week where u_id=?",(uid,))
			week_data = cur.fetchall()
			for i in week_data:
				weeks.append("Week"+str(i[1]))
				week_weight.append(i[2])
			for i in days:
				cur.execute("select * from progress where u_id=? and p_date=?",(uid,i))
				get_weight = cur.fetchall()
				for i in get_weight:
					day_weight.append(i[2])

		except sqlite3.Error as e:
			return (f'{e}')
		finally:
			conn.close()
		
		try:
			with get_connection() as conn:
				cur = conn.cursor()
				cur.execute("select * from progress where u_id=?",(uid,))
				dates = cur.fetchall()
				for i in dates:
					getdate = datetime.strptime(i[1], '%Y-%m-%d').date()
					dates = getdate.strftime("%B-%d")
			
					display_day.append(dates)

		except sqlite3.Error as e:
			return (f'{e}')
		finally:
			conn.close()

		
			

		return render_template('progress.html',days = display_day[-7:],weeks = weeks[-7:],d_weight = day_weight[-7:],w_weight = week_weight[-7:])
		

	else:
		return render_template('progress.html')

@app.route("/daily_detail", methods = ['GET','POST'])
def daily_detail():
	if request.method == 'GET':
		try:
			with get_connection() as conn:
				cur = conn.cursor()
				cur.execute("select * from tracking where u_id=? and track_date=?",(session['uid'],datetime.today().strftime ('%Y-%m-%d')))
				i = cur.fetchone()

				

				getdate = datetime.strptime(i[1], '%Y-%m-%d').date()
				date = getdate.strftime("%B-%d-%Y")
				breakfast = i[2]
				lunch = i[3]
				snack = i[4]
				dinner = i[5]
				calorie = session['u_info'][17]
				protein = i[7]
				carb = i[8]
				fat = i[9]
				consumed = i[6]
				deficit = round(Decimal(calorie - i[6]), 2)
				result = "Reduced "+ str(round(Decimal(consumed/3500),4))+"lb of bodyweight (in theory)"
				deficits = "Calorie Deficit: "+ str(deficit) +"kcal"

		except sqlite3.Error as e:
			return (f'{e}')
		finally:
			conn.close()
		return render_template('daily_detail.html',date = date,
												   breakfast = breakfast,
												   lunch = lunch,
												   snack = snack,
												   dinner = dinner,
												   calorie = calorie,
												   protein = protein,
												   carb = carb,
												   fat = fat,
												   consumed = consumed,
												   result = result,
												   deficit = deficits)

	else:
		getdate = request.form['date']
		weight = ""
		try:
			with get_connection() as conn:
				cur = conn.cursor()
				cur.execute("select * from tracking where u_id=? and track_date=?",(session['uid'],getdate,))
				i = cur.fetchone()
				
				
				print(i[1])
				


				
				getdate = datetime.strptime(i[1], '%Y-%m-%d').date()
				date = getdate.strftime("%B-%d-%Y")
				breakfast = i[2]
				lunch = i[3]
				snack = i[4]
				dinner = i[5]
				calorie = int(session['u_info'][17])
				protein = i[7]
				carb = i[8]
				fat = i[9]
				consumed = i[6]
				deficit = round(Decimal(calorie - i[6]), 2)
				result = "Reduced "+ str(round(Decimal(consumed/3500),4))+"lb of bodyweight (in theory)"
				deficits = "Calorie Deficit: "+ str(deficit) +"kcal"

				cur.execute("select * from progress where u_id=? and p_date=?",(session['uid'],getdate,))
				weights = cur.fetchone()
				if weights:
					for i in weights:
						weight = weights[2]
				else:
					weight = "undefined"
		except sqlite3.Error as e:
			return (f'{e}')
		finally:
			conn.close()
		return render_template('daily_detail.html',date = date,
												   breakfast = breakfast,
												   lunch = lunch,
												   snack = snack,
												   dinner = dinner,
												   calorie = calorie,
												   protein = protein,
												   carb = carb,
												   fat = fat,
												   consumed = consumed,
												   result = result,
												   deficit = deficits,
												   weight = weight)

@app.route("/weekly_detail", methods = ['GET','POST'])
def weekly_detail():
	if request.method == 'GET':
		try:
			with get_connection() as conn:
				cur = conn.cursor()
				cur.execute("select * from progress_week where u_id=?",(session['uid'],))
				u_week = cur.fetchall()
				weeks = []
				days = []
				track_date = datetime.today().strftime ('%Y-%m-%d')
				for i in u_week:
					weeks.append(i[1])

				sdate = datetime.strptime(session['u_info'][-1], '%Y-%m-%d').date()
				edate = datetime.strptime(track_date, '%Y-%m-%d').date()
				delta = edate - sdate     

				for i in range(delta.days + 1):
					day = sdate + timedelta(days=i)
					days.append(str(day))

		
				split_list = [days[x:x+7] for x in range(0, len(days), 7)]
				this_weeknum = split_list.index(split_list[-1])+1
				print(split_list[this_weeknum-1])
				
				calories = []
				proteins = []
				fats = []
				carbs = []
				
				try:
					with get_connection() as conn:
						cur = conn.cursor()
						cur.execute("select * from progress_week where u_id=? and pw_num=?",(session['uid'],this_weeknum,))
						wow = cur.fetchone()
						weight_of_week = wow[2]
						for i in split_list[this_weeknum-1]:
							cur.execute("select * from tracking where u_id=? and track_date=?",(session['uid'],i,))
							u_week = cur.fetchall()
							for i in u_week:
							
								calories.append(i[6])
								proteins.append(i[7])
								carbs.append(i[8])
								fats.append(i[9])


						calorie_consumed = sum(calories)
						
						required = float(session['u_info'][17])*len(calories)
						
						calorie_required = required

						deficit = calorie_required - calorie_consumed

						average_calorie = round(Decimal(sum(calories)/len(calories)),2)
						average_protein = round(Decimal(sum(proteins)/len(proteins)),2)
						average_carb = round(Decimal(sum(carbs)/len(carbs)),2)
						average_fat = round(Decimal(sum(fats)/len(fats)),2)
						average_deficit = round(Decimal(deficit/len(calories)),2)
						net_deficit = round(Decimal(deficit),2)
						loss_weight = round(Decimal(net_deficit/3500),2)
						result = "Reduced "+ str(loss_weight) +"lb of bodyweight in this whole week (in theory)"

				except sqlite3.Error as e:
					return (f'{e}')
				finally:
					conn.close()
				
				

		except sqlite3.Error as e:
			return (f'{e}')
		finally:
			conn.close()
		return render_template('weekly_detail.html',weeks = weeks,
													average_calorie = average_calorie,
													average_carb = average_carb,
													average_fat = average_fat,
													average_protein = average_protein,
													net_deficit = net_deficit,
													result = result,
													average_deficit = average_deficit,
													week = this_weeknum,
													weight_week = weight_of_week
												    )

	else:
		getweek = request.form['weeks']
		try:
			with get_connection() as conn:
				cur = conn.cursor()
				cur.execute("select * from progress_week where u_id=? and pw_num=?",(session['uid'],getweek))
				u_week = cur.fetchall()
				cur.execute("select * from progress_week where u_id=?",(session['uid'],))
				u_weeks = cur.fetchall()
				weeks = []
				days = []
				
				for i in u_weeks:
					weeks.append(i[1])

				track_date = datetime.today().strftime ('%Y-%m-%d')
				sdate = datetime.strptime(session['u_info'][-1], '%Y-%m-%d').date()
				edate = datetime.strptime(track_date, '%Y-%m-%d').date()
				delta = edate - sdate     

				for i in range(delta.days + 1):
					day = sdate + timedelta(days=i)
					days.append(str(day))

		
				split_list = [days[x:x+7] for x in range(0, len(days), 7)]
				this_weeknum = int(getweek)
				
				
				calories = []
				proteins = []
				fats = []
				carbs = []
				
				try:
					with get_connection() as conn:
						cur = conn.cursor()
						cur.execute("select * from progress_week where u_id=? and pw_num=?",(session['uid'],this_weeknum,))
						wow = cur.fetchone()
						weight_of_week = wow[2]
						for i in split_list[this_weeknum-1]:
							cur.execute("select * from tracking where u_id=? and track_date=? and track_calorie!=?",(session['uid'],i,0))
							u_week = cur.fetchall()
							for i in u_week:
							
								calories.append(i[6])
								proteins.append(i[7])
								carbs.append(i[8])
								fats.append(i[9])


						calorie_consumed = sum(calories)
						
						required = float(session['u_info'][17])*len(calories)
						
						calorie_required = required

						deficit = calorie_required - calorie_consumed

						average_calorie = round(Decimal(sum(calories)/len(calories)),2)
						average_protein = round(Decimal(sum(proteins)/len(proteins)),2)
						average_carb = round(Decimal(sum(carbs)/len(carbs)),2)
						average_fat = round(Decimal(sum(fats)/len(fats)),2)
						average_deficit = round(Decimal(deficit/len(calories)),2)
						net_deficit = round(Decimal(deficit),2)
						loss_weight = round(Decimal(net_deficit/3500),2)
						result = "Reduced "+ str(loss_weight) +"lb of bodyweight in this whole week (in theory)"

				except sqlite3.Error as e:
					return (f'{e}')
				finally:
					conn.close()
				
				

		except sqlite3.Error as e:
			return (f'{e}')
		finally:
			conn.close()
		return render_template('weekly_detail.html',weeks = weeks,
													average_calorie = average_calorie,
													average_carb = average_carb,
													average_fat = average_fat,
													average_protein = average_protein,
													net_deficit = net_deficit,
													result = result,
													average_deficit = average_deficit,
													week = getweek,
													weight_week = weight_of_week,
												    )


@app.route("/index", methods = ['GET','POST'])
def index():
	if request.method == 'GET':

		try:	
			with get_connection() as conn:
				cur = conn.cursor()
				cur.execute("select * from user where u_id=?",(session['uid'],))
				u_data = cur.fetchone()
				weight = u_data[6]


		except sqlite3.Error as e:
			return (f'{e}')
		finally:
			conn.close()
		return render_template('index.html', weight = weight)

	else:
		getweight = request.form['weight']
		try:
			with get_connection() as conn:
				cur = conn.cursor()
				cur.execute("update user set u_weight=? where u_id=?",(getweight,session['uid'],))
				conn.commit()

				cur.execute("update progress set p_weight=? where p_date=? and u_id=?",(getweight,datetime.today().strftime ('%Y-%m-%d'),session['uid'],))
				conn.commit()

				cur.execute("select * from user where u_id=?",(session['uid'],))
				u_data = cur.fetchone()
				weight = u_data[6]

				days = []
				weeks = []
				track_date = datetime.today().strftime ('%Y-%m-%d')
				sdate = datetime.strptime(session['u_info'][-1], '%Y-%m-%d').date()
				edate = datetime.strptime(track_date, '%Y-%m-%d').date()
				delta = edate - sdate     

				for i in range(delta.days + 1):
					day = sdate + timedelta(days=i)
					days.append(str(day))

				split_list = [days[x:x+7] for x in range(0, len(days), 7)]
				this_weeknum = split_list.index(split_list[-1])+1
				week_weights = []
				print(this_weeknum)
				try:
					with get_connection() as conn:
						cur = conn.cursor()
						for i in split_list[this_weeknum-1]:
							cur.execute("select * from progress where u_id=? and p_date=? ",(session['uid'],i,))
							u_week = cur.fetchall()
							for i in u_week:
								week_weights.append(i[2])
			
						week_weight = round(sum(week_weights)/len(week_weights))
						cur.execute("update progress_week set pw_weight=? where pw_num=? and u_id=?",(week_weight,this_weeknum,session['uid'],))
						conn.commit()
				except sqlite3.Error as e:
					return (f'{e}')
				finally:
					conn.close()

				

		except sqlite3.Error as e:
			return (f'{e}')
		finally:
			conn.close()
		return render_template('index.html',weight = weight)

@app.route("/about", methods = ['GET','POST'])
def about():
	if request.method == 'GET':
		return render_template('about.html')

	else:
		return render_template('about.html')

@app.route('/logout')
def logout():
	
	session.pop('uid',None)
	session.pop('u_pass',None)
	session.pop('u_info',None)
	session.pop('bf_meal',None)
	session.pop('bf_numbers',None)
	session.pop('lunch_meal',None)
	session.pop('lunch_numbers',None)
	session.pop('dinner_meal',None)
	session.pop('dinner_numbers',None)
	session.pop('snack_meal',None)
	session.pop('snack_numbers',None)
	bf_meal.clear()
	lunch_meal.clear()
	snack_meal.clear()
	dinner_meal.clear()
	flash('You have successfully logged out')
	return redirect(url_for('login'))

if __name__=="__main__":
	app.run(port=1234,debug="true")
