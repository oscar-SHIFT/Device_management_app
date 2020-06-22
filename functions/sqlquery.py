import os
import sqlite3
from datetime import date, timedelta


database = "Group_Project1.db"

if os.path.exists(database):
	print('DB Found')
else:
	print('No DB error')

def execute_this_query(query):
	conn = sqlite3.connect(database)
	conn.row_factory = sqlite3.Row
	cur = conn.cursor()
	cur.execute(query)
	rows = cur.fetchall()
	conn.commit()
	conn.close()
	return rows

def getAllDevices():
	query = ''' SELECT Device.*, Staff.*, Register.When_Checkedback, min(Register.returned) as returned, (Device.OS_Type || ' ' || Device.OS_Version) as os, (Device.Device_Name || ' - ' || Device.Device_Model) as nameModel
	From Device
	Left Join Register on Device.Device_ID = Register.Device_ID
	left Join Staff on Staff.email = Register.email
	GROUP BY Device.Device_ID
	Order by Device.Device_Type, Device.Device_Name '''
	conn = sqlite3.connect(database)
	conn.row_factory = sqlite3.Row
	cur = conn.cursor()
	cur.execute(query)
	rows = cur.fetchall()
	conn.commit()
	conn.close()
	return rows

def getSortedDeviceID():
	query = '''SELECT *, (Device.OS_Type || ' ' || Device.OS_Version) as os, (Device.Device_Name || ' - ' || Device.Device_Model) as nameModel, (Device.Device_Screen_Resolution || ' ' || Device.Device_Screen_PPI) as screenSpecs
	FROM Device ORDER BY Device.Device_ID DESC'''
	conn = sqlite3.connect(database)
	conn.row_factory = sqlite3.Row
	cur = conn.cursor()
	cur.execute(query)
	rows = cur.fetchall()
	conn.commit()
	conn.close()
	return rows

def bookDevice(email, Device_ID):
	duraton = 3
	currentDate = date.today()
	returnDate = date.today() + timedelta(duraton)
	query ='''INSERT INTO Register (email, Device_ID, When_Checkedout, When_Checkedback, Returned) Values('{}','{}', '{}', '{}' , '0')'''.format(email,Device_ID, currentDate, returnDate)
	conn = sqlite3.connect(database)
	conn.row_factory = sqlite3.Row
	cur = conn.cursor()
	cur.execute(query)
	conn.commit()
	conn.close()
	stafflocation = getStaffLocation(email)
	addDeviceLocation(stafflocation,Device_ID)
	conn.close()


def getStaffLocation(email):
	query = ('''SELECT Office_Location from Staff where email = '{}' ''').format(email)
	conn = sqlite3.connect(database)
	conn.text_factory = str
	cur = conn.cursor()
	fetch = cur.execute(query).fetchall()
	location = fetch[0][0]
	conn.close()
	return location

def addDeviceLocation(location, deviceID):
	query =(''' UPDATE Device
	SET Device_Location = '{}'
	WHERE Device_ID = '{}' ''').format(location, deviceID)
	conn = sqlite3.connect(database)
	conn.row_factory = sqlite3.Row
	cur = conn.cursor()
	cur.execute(query)
	conn.commit()

def addStaff(email, FirstName, LastName, Admin,Office_Location):
	query ='''INSERT INTO Staff (email, FirstName, LastName, Admin,Office_Location) Values('{}','{}','{}', '{}','{}')'''.format(email, FirstName, LastName, Admin,Office_Location)
	conn = sqlite3.connect(database)
	conn.row_factory = sqlite3.Row
	cur = conn.cursor()
	cur.execute(query)
	conn.commit()
	conn.close()

def editStaff(email, FirstName, LastName, Admin,Office_Location):
	query ='''UPDATE Staff set FirstName = '{}', LastName = '{}', Admin = '{}', Office_Location = '{}' WHERE email = '{}' '''.format(FirstName, LastName, Admin,Office_Location, email)
	conn = sqlite3.connect(database)
	conn.row_factory = sqlite3.Row
	cur = conn.cursor()
	cur.execute(query)
	conn.commit()
	conn.close()

def deleteStaff(email):
	query ='''UPDATE Staff set Deleted = '{}' WHERE email = '{}' '''.format('1', email)
	conn = sqlite3.connect(database)
	conn.row_factory = sqlite3.Row
	cur = conn.cursor()
	cur.execute(query)
	conn.commit()
	conn.close()

def isStaffActive(email):
	query ='''SELECT email from Staff WHERE email = '{}' and Deleted = 0  '''.format(email)
	conn = sqlite3.connect(database)
	conn.row_factory = sqlite3.Row
	cur = conn.cursor()
	cur.execute(query)
	rows = cur.fetchall()
	conn.commit()
	conn.close()
	# if the user is not deleted return true
	if rows != []:
		return True
	else:
		return False

def getAllAvailableDevices():
	query = ''' SELECT  d.Device_ID, d.Device_Type, d.Device_Name, d.Device_Model, d.OS_Type ,d.OS_Version, d.Device_RAM , d.Device_CPU_GPU,d.Device_Bit ,d.Device_Screen_Resolution, (Device.OS_Type || ' ' || Device.OS_Version) as os, (Device.Device_Name || ' - ' || Device.Device_Model) as nameModel
	FROM Device d
	LEFT JOIN Register r ON r.Device_ID = d.Device_ID
	WHERE r.Device_ID IS NULL or r.Returned = 1'''

	conn = sqlite3.connect(database)
	conn.row_factory = sqlite3.Row
	cur = conn.cursor()
	cur.execute(query)
	rows = cur.fetchall()
	conn.commit()
	conn.close()
	return rows

def addStaff(email, FirstName, LastName, Admin,Office_Location):
	query ='''INSERT INTO Staff (email, FirstName, LastName, Admin,Office_Location) Values('{}','{}','{}', '{}','{}') '''.format(email, FirstName, LastName, Admin,Office_Location)
	conn = sqlite3.connect(database)
	conn.row_factory = sqlite3.Row
	cur = conn.cursor()
	cur.execute(query)
	conn.commit()
	conn.close()

def editStaff(email, FirstName, LastName, Admin,Office_Location):
	query ='''UPDATE Staff set FirstName = '{}', LastName = '{}', Admin = '{}', Office_Location = '{}' WHERE email = '{}' '''.format(FirstName, LastName, Admin,Office_Location, email)
	conn = sqlite3.connect(database)
	conn.row_factory = sqlite3.Row
	cur = conn.cursor()
	cur.execute(query)
	conn.commit()
	conn.close()


def getAllStaffEmails():
	query = '''select email, Admin from Staff  where Deleted = '0' order by email asc '''
	conn = sqlite3.connect(database)
	conn.row_factory = sqlite3.Row
	cur = conn.cursor()
	cur.execute(query)
	rows = cur.fetchall()
	conn.commit()
	conn.close()
	return rows

def getStaffDetails(email):
	query = '''select email, FirstName, LastName, Admin, Office_Location from Staff where email = '{}' '''.format(email)
	conn = sqlite3.connect(database)
	conn.row_factory = sqlite3.Row
	cur = conn.cursor()
	cur.execute(query)
	rows = cur.fetchall()
	conn.commit()
	conn.close()
	return rows

def getAllActiveStaffEmails():
	query = '''select email, Admin from Staff WHERE Deleted = 0 order by email asc'''

	conn = sqlite3.connect(database)
	conn.row_factory = sqlite3.Row
	cur = conn.cursor()
	cur.execute(query)
	rows = cur.fetchall()
	conn.commit()
	conn.close()
	return rows

def getStaffDetails(email):
	query = '''select email, FirstName, LastName, Admin, Office_Location from Staff where email = '{}' '''.format(email)
	conn = sqlite3.connect(database)
	conn.row_factory = sqlite3.Row
	cur = conn.cursor()
	cur.execute(query)
	rows = cur.fetchall()
	conn.commit()
	conn.close()
	return rows


def adminCheck(current_user_email):
	query = ('''select Admin from Staff where email = '{}' ''').format(current_user_email)
	conn = sqlite3.connect(database)
	conn.row_factory = sqlite3.Row
	cur = conn.cursor()
	cur.execute(query)
	rows = cur.fetchall()
	conn.close()
	return rows

def returnDevice(registerNumber):
	query = ('''update Register set Returned = '1' where Register_Number = '{}' ''').format(registerNumber)
	conn = sqlite3.connect(database)
	conn.row_factory = sqlite3.Row
	cur = conn.cursor()
	cur.execute(query)
	conn.commit()
	deviceID = getDeviceID(registerNumber)
	location = "Library"
	addDeviceLocation(location,deviceID)
	conn.close()

def getDeviceID(registerNumber):
	query = ('''SELECT Device_ID from Register where Register_Number = '{}' ''').format(registerNumber)
	conn = sqlite3.connect(database)
	conn.text_factory = str
	cur = conn.cursor()
	fetch = cur.execute(query).fetchall()
	deviceID = fetch[0][0]
	conn.close()
	return deviceID

def getBookedDevicesForUser(current_user_email):
	query = '''SELECT Device.Device_ID,Device.Device_Name, Device.Device_Model,
	Device.Device_Location, Device.Device_Type, date(Register.When_Checkedback) as When_Checkedback, Register.Register_Number,
	(Device.OS_Type || ' ' || Device.OS_Version) as os, (Device.Device_Name || ' - ' || Device.Device_Model) as nameModel
	from Register
	inner join Device on Register.Device_ID = Device.Device_ID
	WHERE Register.email = '{}' and Register.Returned = 0
	Order by Device.Device_Type, Device.Device_Name  '''.format(current_user_email)
	conn = sqlite3.connect(database)
	conn.row_factory = sqlite3.Row
	cur = conn.cursor()
	cur.execute(query)
	rows = cur.fetchall()
	conn.commit()
	conn.close()
	return rows

def sql_edit_insert(query,var):
	conn = sqlite3.connect(database)
	conn.row_factory = sqlite3.Row
	cur = conn.cursor()
	cur.execute(query,var)
	conn.commit()
	conn.close()

def sql_delete(query,var):
	conn = sqlite3.connect(database)
	conn.row_factory = sqlite3.Row
	cur = conn.cursor()
	cur.execute(query,var)
	conn.commit()
	conn.close()

def sql_query2(query,var):
	conn = sqlite3.connect(database)
	conn.row_factory = sqlite3.Row
	cur = conn.cursor()
	cur.execute(query,var)
	rows = cur.fetchall()
	conn.commit()
	conn.close()
	return rows

def sql_query(query):
	conn = sqlite3.connect(database)
	conn.row_factory = sqlite3.Row
	cur = conn.cursor()
	cur.execute(query)
	rows = cur.fetchall()
	conn.commit()
	conn.close()
	return rows
