#Group_Project1
from itertools import groupby
from flask import Flask, session, redirect, url_for, escape, request, render_template, make_response

app = Flask(__name__)

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5#y2L"F4Q8z\njjjl\xec]/'

# This is the landing page of the website
@app.route('/', methods = ['POST', 'GET'])
def device_list():

    # To start we import sqlquery.py, so we can access the functions we need.
	from functions.sqlquery import getAllDevices, getBookedDevicesForUser, getAllStaffEmails, adminCheck, getStaffDetails,deleteStaff, getAllActiveStaffEmails
	from datetime import date, timedelta

    # Get the info on all the devices
	dresults = getAllDevices()

    # Get a list of all the emails in the database
	#	semails = getAllStaffEmails()
	# only return staff emails of users that are active (not deleted)
	semails = getAllActiveStaffEmails()

	# get todays date
# 	oneday = date.today() + timedelta(4)
# 	today = oneday.strftime("%Y-%m-%d")

	# see if there is a msg
	if request.args.get('msg'):
		msg = request.args.get('msg')
	else:
		msg = ' '

	today = date.today().strftime("%Y-%m-%d")


	# if email is found in cookie then dont need post
	if request.cookies.get('email'):
		emailSelected = request.cookies.get('email')
		hasCookie = 'True'
		sdetails = getStaffDetails(emailSelected)
		bresults = getBookedDevicesForUser(emailSelected)
		sdetails = getStaffDetails(emailSelected)
		isAdmins = adminCheck(emailSelected)
		if isAdmins[0]["Admin"] == 'True':
			session["username"] = 'admin'
		else:
			session.pop('username', None)
		return render_template('devices_homepage.html', dresults=dresults, semails=semails, bresults=bresults, emailSelected=emailSelected, hasCookie=hasCookie, isAdmins=isAdmins, sdetails=sdetails, today=today, msg=msg)
	elif request.args.get('email'):
		if request.cookies.get('email'):
			hasCookie = 'True'
		else:
			hasCookie = ''
		# if there is no cookie, check if there is a email passed into the url
		emailSelected = request.args.get('email')
		if emailSelected != "none":
			sdetails = getStaffDetails(emailSelected)
			bresults = getBookedDevicesForUser(emailSelected)
			isAdmins = adminCheck(emailSelected)
			if isAdmins[0]["Admin"] == 'True':
				session["username"] = 'admin'
			else:
				session.pop('username', None)
			return render_template('devices_homepage.html', dresults=dresults, semails=semails, bresults=bresults, emailSelected=emailSelected, isAdmins=isAdmins, today=today, sdetails=sdetails, msg=msg, hasCookie=hasCookie)
		else:
			return render_template('devices_homepage.html', dresults=dresults, semails=semails, today=today, msg=msg)
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
			response.set_cookie('email',emailSelected)
		# if not save email to cookie
		except:
			response.set_cookie('email','')
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
		redirect_to_index = redirect(url_for('editstaff', email=current_user_email,msg=msg))
		response = make_response(redirect_to_index)
		return response

@app.route('/editStafffp', methods = ['POST', 'GET'])
def editStafffp():
    # To start we import sqlquery.py, so we can access the functions we need.
	from functions.sqlquery import editStaff
	if 'username' in session:
		# get data from form
		if request.method == 'POST':
			current_user_email = request.form['email']
			firstName = request.form['FirstName']
			lastName = request.form['LastName']
			admin = request.form['Admin']
			officeLocation = request.form['Office_Location'] 
			msg = "Edited user: {}".format(current_user_email)		
			editStaff(current_user_email,firstName,lastName,admin,officeLocation)
			redirect_to_index = redirect(url_for('device_list', email=current_user_email,msg=msg))
			response = make_response(redirect_to_index)
			return response
	else:
		redirect_to_index = redirect(url_for('device_list'))
		response = make_response(redirect_to_index)
		return response

@app.route('/deleteStaffMember', methods = ['POST', 'GET'])
def deleteStaffMember():
    # To start we import sqlquery.py, so we can access the functions we need.
	from functions.sqlquery import deleteStaff, getBookedDevicesForUser, isStaffActive

	# get data from form
	if request.method == 'POST':
		current_user_email = request.form['email']

	if getBookedDevicesForUser(current_user_email)== [] and isStaffActive(current_user_email) :

		deleteStaff(current_user_email)
		msg= "Deleted user: {}".format(current_user_email)
	else:
		msg= "Can't delete user: {} because they have one or more devices checked out".format(current_user_email)
	redirect_to_index = redirect(url_for('editstaff', email=current_user_email,msg=msg))
	response = make_response(redirect_to_index)
	return response


@app.route('/addStaff', methods = ['POST', 'GET'])
def addStaff():
    # To start we import sqlquery.py, so we can access the functions we need.
	from functions.sqlquery import addStaff, sql_query

	# get data from form
	if request.method == 'POST':
		current_user_email = request.form['email']
		firstName = request.form['FirstName']
		lastName = request.form['LastName']
		admin = request.form['Admin']
		officeLocation = request.form['Office_Location']	
		if sql_query((''' Select email from Staff where email = '{}' ''').format(current_user_email)):
			msg = "Email already exist for user: {}".format(current_user_email)
		else:
			addStaff(current_user_email,firstName,lastName,admin,officeLocation)
			msg = "Added new user: {}".format(current_user_email)
		redirect_to_index = redirect(url_for('editstaff', email=current_user_email,msg=msg))
		response = make_response(redirect_to_index)
		return response

@app.route('/admin', methods = ['POST', 'GET'])
def admin():
	from functions.sqlquery import getAllDevices,getAllActiveStaffEmails,getSortedDeviceID
	if 'username' in session:
		dresults = getSortedDeviceID()	
		return render_template('admin.html', dresults=dresults)
	else: 
		redirect_to_index = redirect(url_for('device_list'))
		response = make_response(redirect_to_index)
		return response

@app.route('/editstaff', methods = ['POST', 'GET'])
def editstaff():
    # To start we import sqlquery.py, so we can access the functions we need.
	from functions.sqlquery import getAllActiveStaffEmails, getStaffDetails
	from datetime import date, timedelta

	# only return staff emails of users that are active (not deleted)
	semails = getAllActiveStaffEmails()

	if request.args.get('msg'):
		msg = request.args.get('msg')
	else:
		msg = ' '

	if request.args.get('email'):
		emailSelected = request.args.get('email')
		sdetails = getStaffDetails(emailSelected)
		return render_template('staff.html', semails=semails,emailSelected=emailSelected, sdetails=sdetails, msg=msg)

	return render_template('staff.html', semails=semails, msg=msg)


@app.route('/addDevice', methods = ['POST', 'GET'])
def addDevice():
	from functions.sqlquery import sql_edit_insert, getAllDevices, getSortedDeviceID
	if 'username' in session: 
	
		# get data from HTML form
		if request.method == 'POST':
			Device_type = request.form ["Device_type"]
			Device_name = request.form ["Device_name"]
			model = request.form ["model"]
			OS_type = request.form ["OS_type"]
			OS_version = request.form ["OS_version"]
			ram = request.form ["ram"]
			CPU_GPU = request.form ["CPU_GPU"]
			bit = request.form ["bit"]
			reso = request.form ["reso"]
			PPI = request.form ["PPI"]
			grade = request.form ["grade"]
			UUID = request.form ["UUID"]
			Location = "Library"
			
			if Device_type and Device_name:
				sql_edit_insert(('''INSERT INTO Device (Device_Type, Device_Name, Device_Model, OS_Type,\
					OS_Version, Device_RAM, Device_CPU_GPU, Device_Bit, Device_Screen_Resolution, Device_Screen_PPI,\
					Device_Grade, Device_UUID, Device_Location)
					VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)'''), (Device_type, Device_name, model, OS_type, OS_version, ram, CPU_GPU, bit, reso, PPI, grade, UUID, Location ))

   		# Get the info on all the devices
		dresults = getSortedDeviceID()
	
		return render_template('admin.html', dresults=dresults)
	
	else:
		redirect_to_index = redirect(url_for('device_list'))
		response = make_response(redirect_to_index)
		return response	


@app.route('/updateSelectedRow', methods = ['POST', 'GET'])
def selected_Row():

	from functions.sqlquery import sql_edit_insert, getAllDevices, getSortedDeviceID

	if request.method == 'POST':
		Device_ID = request.form ["Device_ID"]
		Device_Type     = request.form ["Device_Type"]
		Device_Name     = request.form ["Device_Name"]
		Device_Model    = request.form ["Device_Model"]
		OS_Type         = request.form ["OS_Type"]
		OS_Version      = request.form ["OS_Version"]
		Device_RAM      = request.form ["Device_RAM"]
		Device_CPU_GPU  = request.form ["Device_CPU_GPU"]
		Device_Bit      = request.form ["Device_Bit"]
		Device_Screen_Resolution = request.form ["Device_Screen_Resolution"]
		Device_Screen_PPI        = request.form ["Device_Screen_PPI"]
		Device_Grade    = request.form ["Device_Grade"]
		Device_UUID     = request.form ["Device_UUID"]

		sql_edit_insert('''UPDATE Device SET Device_Type = ?, Device_Name = ?, Device_Model = ?,\
		OS_Type = ?, OS_Version = ?, Device_RAM = ?, Device_CPU_GPU = ?, Device_Bit = ?,\
            Device_Screen_Resolution = ?, Device_Screen_PPI = ?, Device_Grade = ?, Device_UUID = ? \
			WHERE Device_ID = ? ''',(Device_Type, Device_Name, Device_Model, OS_Type, OS_Version, Device_RAM, Device_CPU_GPU, Device_Bit, Device_Screen_Resolution, Device_Screen_PPI, Device_Grade, Device_UUID, Device_ID))

		dresults = getSortedDeviceID()

		return render_template('admin.html', dresults=dresults)

@app.route('/query_edit', methods = ['POST', 'GET'])
def query_Selected_Row():
	from functions.sqlquery import getAllDevices, sql_query2, getSortedDeviceID
	if request.method == 'GET':
		Selected_Device_ID = request.args.get('Selected_Device_ID')
		eresults = sql_query2('''select * from Device where device_ID = ? ''',(Selected_Device_ID,))
		dresults = getSortedDeviceID()
		return render_template('admin.html', eresults=eresults, dresults=dresults)

# If flask is being started from the command line, run the app and set debug to true.
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
