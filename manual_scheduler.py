import datetime
import time
import MySQLdb
import sys
import smtplib

from email.mime.text import MIMEText
#Retrieve The Name Data from the Main Database
    
def retrieveNameData():
    """Takes Name from Database and Returns it"""
    # open a database connection
    # be sure to change the host IP address, username, password and database name to match your own
    connection = MySQLdb.connect (host = "localhost", user = "root", passwd = "zwfkc2msyfx7", db = "Scheduler_Database")
    # prepare a cursor object using cursor() method
    cursor = connection.cursor ()

    # execute the SQL query using execute() method.
    cursor.execute ("select name_first from user_information")

    # fetch all of the rows from the query
    name = cursor.fetchall ()

    # print the rows

    # close the cursor object
    cursor.close ()

    # close the connection
    connection.close ()

    return name

#Retrieve the Phone Number from the Database

def retrievePhoneData():
    """Takes Name from Database and Returns it"""
    # open a database connection
    # be sure to change the host IP address, username, password and database name to match your own
    connection = MySQLdb.connect (host = "localhost", user = "root", passwd = "zwfkc2msyfx7", db = "Scheduler_Database")
    # prepare a cursor object using cursor() method
    cursor = connection.cursor ()

    # execute the SQL query using execute() method.
    cursor.execute ("select phone_number from user_information")

    # fetch all of the rows from the query
    phone = cursor.fetchall ()

    # print the rows

    # close the cursor object
    cursor.close ()

    # close the connection
    connection.close ()

    return phone

#Retrieve the Carrier from the Database and parse accordingly

def retrieveCarrierData():
    """Takes Name from Database and Returns it"""
    # open a database connection
    # be sure to change the host IP address, username, password and database name to match your own
    connection = MySQLdb.connect (host = "localhost", user = "root", passwd = "zwfkc2msyfx7", db = "Scheduler_Database")
    # prepare a cursor object using cursor() method
    cursor = connection.cursor ()

    # execute the SQL query using execute() method.
    cursor.execute ("select carrier from user_information")

    # fetch all of the rows from the query
    data = cursor.fetchall ()
    return data
    # close the cursor object
    cursor.close ()

    # close the connection
    connection.close ()

def Manual_Compile(period1, period2, period3, period4, period5, period6, period7):
    """In case of Failure, This is a Manual Backup for the Scheduler, It will send the 7 Periods entered above
    """
    print "Manually Compiling Schedule" + "\n"
    dayOfWeek = str(datetime.date.today().strftime("%A")) #Finds the Current Day of the Week

    #Asks for Verification
    print Date + "==================" + "\n" + period1 + "\n" + period2 + "\n" + period3 + "\n" + period4 + "\n" + period5 + "\n" + period6 + "\n" + period7
    userYesOrNo = raw_input("\n" + "Is that Correct? (Yes/No): ")
    #Checks If the Input is Correct
    if userYesOrNo == "Yes":
        sendEmail(Date + "==================" + "\n" + period1 + "\n" + period2 + "\n" + period3 + "\n" + period4 + "\n" + period5 + "\n" + period6 + "\n" + period7)
    else:
        print "Re-run the Function with the Periods, Please try Again" 
        
def sendEmail(msg):
    print "Starting Send Text Function" + "\n"

    #Define Variables
    userPhone = retrievePhoneData()
    userCarrier = retrieveCarrierData()
    userName = retrieveNameData()
    Carrier = ""

    #Login Information
    username = 'benjaminscheduler'  
    password = 'benjaminschool'

    #Open a Server Connection
    server = smtplib.SMTP('smtp.gmail.com:587')  
    server.starttls()  
    server.login(username,password)
 
    for x in range(len(userName)):
        if " ".join(userCarrier[x])  == "Verizon":
            Carrier = "@vtext.com"
        elif " ".join(userCarrier[x]) == "ATT":
            Carrier =  "@txt.att.net"
        elif " ".join(userCarrier[x]) == "T-Mobile":
            Carrier = "@tmomail.net"
        elif " ".join(userCarrier[x]) == "Sprint":
            Carrier = "@pm.sprint.com"
        elif " ".join(userCarrier[x]) == "Virgin-Mobile":
            Carrier = "@vmobl.com"
        elif " ".join(userCarrier[x]) == "MetroPCS":
            Carrier = "@mymetropcs.com"
        
        sendUserName = " ".join(userName[x])
        sendPhone = " ".join(userPhone[x])
        fromaddr = 'benjaminscheduler@gmail.com'
        toaddrs  = str(sendPhone) + str(Carrier) 
        print "Sending Schedule to: " + str(sendUserName) + "\n" + "Phone Number: " + str(sendPhone)
      
    #Send Mail
        server.sendmail(fromaddr, toaddrs, msg)
        time.sleep(5)
        print "Succesfully Sent to: " + str(sendUserName) + "\n"

    #Close Connection After Loop
    server.quit()
