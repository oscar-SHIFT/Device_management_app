#Group_Project1
from itertools import groupby
from flask import Flask, session, redirect, url_for, escape, request, render_template, make_response

app = Flask(__name__)

# This is the landing page of the website
@app.route('/', methods = ['POST', 'GET'])
def device_list():

    # To start we import sqlquery.py, so we can access the functions we need.
	from functions.sqlquery import getAllDevices, getBookedDevicesForUser, getAllStaffEmails, adminCheck, getStaffDetails
	from datetime import date, timedelta
	
    # Get the info on all the devices
	dresults = getAllDevices()
	    
    # Get a list of all the emails in the database
	semails = getAllStaffEmails()
	
	# get todays date
# 	oneday = date.today() + timedelta(4)
# 	today = oneday.strftime("%Y-%m-%d")

	# see if there is a msg
	try: 
		msg = request.args.get('msg')
	except:
		msg = 'got here'
	
	today = date.today().strftime("%Y-%m-%d")
	
	# if email is found in cookie then dont need post
	if request.cookies.get('email'):
		emailSelected = request.cookies.get('email')
		hasCookie = 'True' 
		bresults = getBookedDevicesForUser(emailSelected)
		sdetails = getStaffDetails(emailSelected)
		isAdmins = adminCheck(emailSelected)
		return render_template('devices_homepage.html', dresults=dresults, semails=semails, bresults=bresults, emailSelected=emailSelected, hasCookie=hasCookie, isAdmins=isAdmins, today=today, msg=msg)
	elif request.args.get('email'):
		# if there is no cookie, check if there is a email passed into the url
		emailSelected = request.args.get('email')
		bresults = getBookedDevicesForUser(emailSelected)
		sdetails = getStaffDetails(emailSelected)
		isAdmins = adminCheck(emailSelected)
		return render_template('devices_homepage.html', dresults=dresults, semails=semails, bresults=bresults, emailSelected=emailSelected, isAdmins=isAdmins, today=today, msg=msg)	
	else:	
		# If no cookies or emails just render the page wiht a list of devices
		return render_template('devices_homepage.html', dresults=dresults, semails=semails, today=today, msg=msg)	

@app.route('/set_cookie', methods = ['POST', 'GET'])
def cookie_insertion():
	# get data from form
	if request.method == 'POST':
		emailSelected = request.form['email']		
		# set up redirect 	
		redirect_to_index = redirect(url_for('device_list', email=emailSelected))
		response = make_response(redirect_to_index)  
		# see if public was chosen, is so cookie is nul
		try:
			isPublic = request.form['public']
			response.set_cookie('email','')
		# if not save email to cookie
		except:
			response.set_cookie('email',emailSelected)
		# redirect to home, sending email in cookie or get
		finally:
			return response
			
@app.route('/book', methods = ['POST', 'GET'])
def book():
    # To start we import sqlquery.py, so we can access the functions we need.
	from functions.sqlquery import bookDevice

	# get data from form
	if request.method == 'POST':
		select_Device_ID = request.form['Device_ID']
		current_user_email = request.form['Staff_Email']	
		bookDevice(current_user_email, select_Device_ID)
		redirect_to_index = redirect(url_for('device_list', email=current_user_email))
		response = make_response(redirect_to_index)  
		return response

@app.route('/checkBack', methods = ['POST', 'GET'])
def checkBack():
    # To start we import sqlquery.py, so we can access the functions we need.
	from functions.sqlquery import returnDevice

	# get data from form
	if request.method == 'POST':
		registerNumber = request.form['Register_Number']
		current_user_email = request.form['Staff_Email']	
		returnDevice(registerNumber)
		redirect_to_index = redirect(url_for('device_list', email=current_user_email))
		response = make_response(redirect_to_index)  
		return response

@app.route('/editStaff', methods = ['POST', 'GET'])
def editStaff():
    # To start we import sqlquery.py, so we can access the functions we need.
	from functions.sqlquery import editStaff

	# get data from form
	if request.method == 'POST':
		current_user_email = request.form['email']
		firstName = request.form['FirstName']
		lastName = request.form['LastName']
		admin = request.form['Admin']
		officeLocation = request.form['Office_Location'] 
		msg = "Eddited user: {}".format(current_user_email)		
		editStaff(current_user_email,firstName,lastName,admin,officeLocation)
		redirect_to_index = redirect(url_for('device_list', email=current_user_email,msg=msg))
		response = make_response(redirect_to_index)
		return response
		
@app.route('/addStaff', methods = ['POST', 'GET'])
def addStaff():
    # To start we import sqlquery.py, so we can access the functions we need.
	from functions.sqlquery import addStaff

	# get data from form
	if request.method == 'POST':
		current_user_email = request.form['email']
		firstName = request.form['FirstName']
		lastName = request.form['LastName']
		admin = request.form['Admin']
		officeLocation = request.form['Office_Location']	
		msg = "Ádded new user: {}".format(current_user_email)	
		addStaff(current_user_email,firstName,lastName,admin,officeLocation)
		redirect_to_index = redirect(url_for('device_list', email=current_user_email,msg=msg))
		response = make_response(redirect_to_index)  
		return response

# If flask is beeing started from the comand line, run the app and set debug to true.
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
