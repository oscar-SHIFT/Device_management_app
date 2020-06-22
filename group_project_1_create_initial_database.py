#Group_Project1 update

import os
import sqlite3
import pandas as pd

# Checking if i have a Databases  "Group_Project1.db", with I have a File iqual it going to delete
if os.path.exists("Group_Project1.db"):
	os.remove("Group_Project1.db")

    #Creating a new DataBase
db_filename = "Group_Project1.db"
db_connector = sqlite3.connect(db_filename,check_same_thread=False)
cur = db_connector.cursor()

#******************************************************************************************************************************************************************
# Useing the db_connector I am Creating the tables that i need (Staff)
cur.execute("CREATE TABLE Staff\
(email varchar(256) PRIMARY KEY NOT NULL, \
FirstName varchar(50) DEFAULT NULL, \
LastName varchar(50) DEFAULT NULL, \
Admin varchar(50) DEFAULT NULL, \
Active varchar(50) DEFAULT NULL, \
Office_Location varchar (50),\
Deleted INTEGER DEFAULT 0);")

  #populating my DB_ Staff
cur.execute("INSERT INTO Staff (email, FirstName, LastName,Admin, Active,  Office_Location) VALUES ('kcontatos12@gmail.com','Harrison','Buckley','True','True','Office II')")
cur.execute("INSERT INTO Staff (email, FirstName, LastName,Admin,Active, Office_Location) VALUES ('calor_de_verao@gmail.com','Aquila','Robinson', 'False','True', 'Office I')")
cur.execute("INSERT INTO Staff (email, FirstName, LastName,Admin,Active, Office_Location) VALUES ('meu_amor@gmail.com','Rhona','Kirk','False','True','Office II')")
cur.execute("INSERT INTO Staff (email, FirstName, LastName,Admin, Active,Office_Location) VALUES ('Familia_ideal@gmail.com','Brennan','Chavez','False','True', 'Office II')")
cur.execute("INSERT INTO Staff (email, FirstName, LastName,Admin,Active, Office_Location) VALUES ('Tempo_de_qualidade@gmail.com','Lani','Carrillo', 'False','True' ,'Office I')")

#******************************************************************************************************************************************************************
# Useing the db_connector I am Creating the tables that i need (Device)

cur.execute("CREATE TABLE Device\
(Device_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, \
Device_Type varchar(50), \
Device_Name varchar(50), \
Device_Model varchar(50),\
OS_Type varchar(50),\
OS_Version varchar(50), \
Device_RAM varchar(50), \
Device_CPU_GPU varchar(50),\
Device_Bit varchar(50),\
Device_Screen_Resolution varchar(50),\
Device_Screen_PPI Integer,\
Device_Grade varchar(50),\
Device_UUID varchar(50),\
Device_Location varchar(50));")

	#populating my DB_Register

current_file = os.path.abspath(os.path.dirname(__file__))
data_url = 'data/Devices.csv'
csv_filename = os.path.join(current_file, data_url)
data_table = pd.read_csv(csv_filename, header=0)
data_table.to_sql('Device', db_connector, if_exists='append', index = False)

#******************************************************************************************************************************************************************
# Useing the db_connector I am Creating the tables that i need (Register)
cur.execute("CREATE TABLE Register\
(Register_Number INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,\
email varchar(256) NOT NULL,\
Device_ID INTEGER NOT NULL,\
When_Checkedout char,\
When_Checkedback char,\
Returned boolean,\
foreign key (email) references Staff (email),\
foreign key (Device_ID) references Device (Device_ID));")

  #populating my DB_Register
cur.execute("INSERT INTO Register (email, Device_ID, When_Checkedout, When_Checkedback, Returned ) VALUES ('kcontatos12@gmail.com','001', '2018-09-10', '2018-09-14', False)")
cur.execute("INSERT INTO Register (email, Device_ID, When_Checkedout, When_Checkedback, Returned ) VALUES ('calor_de_verao@gmail.com','002', '2018-09-10', '2018-09-10', False)")
cur.execute("INSERT INTO Register (email, Device_ID, When_Checkedout, When_Checkedback, Returned ) VALUES ('meu_amor@gmail.com','003', '2018-09-10', '2018-09-14', True)")
cur.execute("INSERT INTO Register (email, Device_ID, When_Checkedout, When_Checkedback, Returned ) VALUES ('Familia_ideal@gmail.com','004', '2018-09-09', '2018-09-11', False)")
cur.execute("INSERT INTO Register (email, Device_ID, When_Checkedout, When_Checkedback, Returned ) VALUES ('Tempo_de_qualidade@gmail.com','005', '2018-09-09', '2018-09-11', True)")

db_connector.commit()
db_connector.close()
