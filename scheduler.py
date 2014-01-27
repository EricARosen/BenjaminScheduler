import pyPdf
import datetime
import time
import MySQLdb
import sys
import smtplib

from email.mime.text import MIMEText

def ScheduleWrite():
    now = datetime.datetime.now()
    cMonth = now.month
    cDay = now.day
    ################ Disect into a seperate binary function
    pdf = pyPdf.PdfFileReader(file("SchoolPlanner.pdf","rb"))
    currentPage = pdf.getNumPages()/2
    temp = scheduler(cMonth, cDay, pdf, currentPage)
    oneHalf = str(temp[0])
    currentPage = temp[1]

    content = ""
    if datetime.datetime.today().weekday() in range(3): #We need next page
        content += pdf.getPage(currentPage + 1).extractText()+"\n"
        content = content.split()
        weeklySchedule = allowedWords(content)

        finalSchedule = ""
        for day in weeklySchedule:
            pacer = ""
            for x in range(len(day[0])):
                pacer += "="
            finalSchedule += str(pacer + "\n")
            finalSchedule += str(day[0] + "\n")
            finalSchedule += str(pacer + "\n")
            for  period in range(1,len(day)):
                finalSchedule += str(day[period] + "\n")
                
        final = oneHalf + finalSchedule
    else:
        content += pdf.getPage(currentPage - 1).extractText()+"\n"
        content = content.split()
        weeklySchedule = allowedWords(content)

        finalSchedule = ""
        for day in weeklySchedule:
            pacer = ""
            for x in range(len(day[0])):
                pacer += "="
            finalSchedule += str(pacer + "\n")
            finalSchedule += str(day[0] + "\n")
            finalSchedule += str(pacer + "\n")
            for  period in range(1,len(day)):
                finalSchedule += str(day[period] + "\n")
        
        final = finalSchedule + oneHalf
    return final
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

def CompileSchedule():
    """Takes the Current Day and uses the information to find what the schedule
    for that day is.
    """
    print "Compiling Schedule" + "\n"
    dayOfWeek = str(datetime.date.today().strftime("%A")) #Finds the Current Day of the Week
    schedule = ScheduleWrite() #Runs the Main Function and Stores in Variable
    print schedule
    splitSchedule = schedule.split() #Splits the Schedule
    print splitSchedule
    UserInfo = retrieveNameData()
    Date = "Hi " + UserInfo + "," + "\nHere is the schedule for: " + "\n" + datetime.date.today().strftime("%B %d, %Y") + "\n"
    
    if splitSchedule[1] == dayOfWeek: #Monday
        Monday = "\n".join(splitSchedule[3:12])
        print str(Date + Monday) + "\n"
        sendEmail(Date + Monday)
    
    elif splitSchedule[13] == dayOfWeek: #Tuesday
        Tuesday = "\n".join(splitSchedule[16:24])
        print str(Date + Tuesday) + "\n"
        sendEmail(Date + Tuesday)

    elif splitSchedule[25] == dayOfWeek: #Wednesday
        Wednesday = "\n".join(splitSchedule[27:32])
        print str(Date + Wednesday) + "\n"
        sendEmail(Date + Wednesday)
    
    elif splitSchedule[34] == dayOfWeek: #Thursday
        Thursday = "\n".join(splitSchedule[37:42])
        print str(Date + Thursday) + "\n"
        sendEmail(Date + Thursday)
    
    elif splitSchedule[43] == dayOfWeek: #Friday
        Friday = "\n".join(splitSchedule[46:54])
        print str(Date + Friday) + "\n"
        sendEmail(Date + Friday)
        
        
def sendEmail(msg):
    print "Starting Send Text Function" + "\n"
    userPhone = retrievePhoneData()
    userCarrier = retrieveCarrierData()
    userName = retrieveNameData()
    Carrier = ""
 
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
            Carrier = "@metropcs.sms.us"
        
        sendUserName = " ".join(userName[x])
        sendPhone = " ".join(userPhone[x])
        fromaddr = 'benjaminscheduler@gmail.com'
        toaddrs  = str(sendPhone) + str(Carrier) 
        print "Sending Schedule to: " + str(sendUserName) + "\n" + "Phone Number: " + str(sendPhone)
    
        username = 'benjaminscheduler'  
        password = 'benjaminschool'
      
    #Send Mail
        server = smtplib.SMTP('smtp.gmail.com:587')  
        server.starttls()  
        server.login(username,password)  
        server.sendmail(fromaddr, toaddrs, msg)
        print "Succesfully Sent to: " + str(sendUserName) + "\n"
        server.quit()

def scheduler(cMonth, cDay, pdf, currentPage):
    exitLoop = False
    while (exitLoop != True):
        content = ""
        content += pdf.getPage(currentPage).extractText()+"\n"
        content = content.split()
        if len(content) == 0:
            currentPage -= 1
        elif changeMonth(content[1]) not in range(1,32):
            currentPage -= 1
        elif float(changeMonth(content[1])) > float(cMonth):
            currentPage -= 1
        elif float(changeMonth(content[1])) < float(cMonth):
            currentPage += 1
        elif float(changeMonth(content[1])) == float(cMonth):
            if float(cDay) in range(int(content[2]), int(content[2])+ 2):
                exitLoop = True
            elif float(cDay) < float(content[2]):
                currentPage -= 1
            else:
                currentPage += 1
    weeklySchedule = allowedWords(content)
    #Write to the file
    f = open("Schedule.txt","wb")

    finalSchedule = ""
    for day in weeklySchedule:
        pacer = ""
        for x in range(len(day[0])):
            pacer += "="
        finalSchedule += str(pacer + "\n")
        finalSchedule += str(day[0] + "\n")
        finalSchedule += str(pacer + "\n")
        for  period in range(1,len(day)):
            finalSchedule += str(day[period] + "\n")

    return [finalSchedule, currentPage]
    """
    fromaddr = 'benjaminscheduler@gmail.com'  
    toaddrs  = 'eric.rosen14@thebenjaminschool.org'  
    msg = finalSchedule  
      
      
    # Credentials (if needed)  
    username = 'benjaminscheduler'  
    password = 'benjaminschool'  
      
    # The actual mail send  
    server = smtplib.SMTP('smtp.gmail.com:587')  
    server.starttls()  
    server.login(username,password)  
    server.sendmail(fromaddr, toaddrs, msg)  
    server.quit()
    print "Done!"
    """
def changeMonth(month):
    if month == "January":
        return 1
    elif month == "February":
        return 2
    elif month == "March":
        return 3
    elif month == "April":
        return 4
    elif month == "May":
        return 5
    elif month == "June":
        return 6
    elif month == "July":
        return 7
    elif month == "August":
        return 8
    elif month == "September":
        return 9
    elif month == "October":
        return 10
    elif month == "November":
        return 11
    elif month == "December":
        return 12
    else:
        return 0
    
def allowedWords(text):
    desiredMonth = []
    desiredDay= []
    desiredWeekDay = []
    desiredActivity = []

    filteredMonth = []
    filteredDay = []
    filteredWeekDay = []
    filteredActivity = []
    
    #Days
    for i in range(1,32):
        desiredDay.append(str(i))
    #WeekDay        
    desiredWeekDay.append("Monday")
    desiredWeekDay.append("Tuesday")
    desiredWeekDay.append("Wednesday")
    desiredWeekDay.append("Thursday")
    desiredWeekDay.append("Friday")
    #Months
    desiredMonth.append("January")
    desiredMonth.append("February")
    desiredMonth.append("March")
    desiredMonth.append("April")
    desiredMonth.append("May")
    desiredMonth.append("June")
    desiredMonth.append("July")
    desiredMonth.append("August")
    desiredMonth.append("September")
    desiredMonth.append("October")
    desiredMonth.append("November")
    desiredMonth.append("December")
    #School
    desiredActivity.append("A")
    desiredActivity.append("B")
    desiredActivity.append("C")
    desiredActivity.append("D")
    desiredActivity.append("E")
    desiredActivity.append("F")
    desiredActivity.append("G")
    desiredActivity.append("A/split")
    desiredActivity.append("B/split")
    desiredActivity.append("C/split")
    desiredActivity.append("D/split")
    desiredActivity.append("E/split")
    desiredActivity.append("F/split")
    desiredActivity.append("G/split")
    #desiredActivity.append("Assembly")
    #desiredActivity.append("Lunch")
    #desiredActivity.append("Advisors")
    #desiredActivity.append("Activity")

    for word in range(len(text)):
        if text[word] in desiredDay:
            filteredDay.append(text[word])
        elif text[word] in desiredActivity:
            filteredActivity.append([text[word],text[word+1].replace('-',' ').replace(':',' ').split()])
        elif text[word] in desiredWeekDay:
            filteredWeekDay.append(text[word])
        elif text[word] in desiredMonth:
            filteredMonth.append(text[word])
    dates = []

    for i in range(len(filteredWeekDay)):
        dates.append(filteredWeekDay[i] + " " +filteredMonth[i] + " " + filteredDay[i])

    periods = []
    times = []
    for activity in filteredActivity:
        periods.append(activity[0])
        times.append(activity[1])
    return connectPeriods(dates, periods, times)

def connectPeriods(dates, periods, times):
    schedule = []
    leftOverPeriods = []
    if "Monday" in dates[0]: #It starts with Monday
        schedule.append([dates[0]])
        schedule.append([dates[1]])
        schedule.append([dates[2]])
    else:
        schedule.append([dates[0]])
        schedule.append([dates[1]
                         ])
    for index in range(len(periods)): #Looping through the indexes for all periods and times (They have the same amount of indexes)
        for temp in range(4): # Loops through all times to change them correctly
            if times[index][temp] == '1':
                times[index][temp] = '13'
            elif times[index][temp] == '2':
                times[index][temp] = '14'
        time1 = str(times[index][0]) + ":" + str(times[index][1]) + ":00"
        time2 = str(times[index][2]) + ":" + str(times[index][3]) + ":00"
        FMT = '%H:%M:%S'
        tdelta = datetime.datetime.strptime(time1, FMT)
        tdelta2 =  datetime.datetime.strptime(time2, FMT)
        totalTime = tdelta2 - tdelta
        totalTime = abs(totalTime.total_seconds() / 60)
        if "Monday" in dates[0]: #It starts with Monday
            if totalTime == 85.0 or ("split" in periods[index]): #Add to Wednesday
                schedule[2].append(periods[index])
            else:
                leftOverPeriods.append(periods[index])
        else:
            if totalTime == 85.0 or ("split" in periods[index]): #Add to Thursday
                schedule[0].append(periods[index])
            else:
                schedule[1].append(periods[index])
    if len(leftOverPeriods) > 0:
        if len(leftOverPeriods) == 7:
            for x in range(len(leftOverPeriods)):
                schedule[1].append(leftOverPeriods[x])
        else:
            for x in range(len(leftOverPeriods)):
                if x % 2 == 0:
                    schedule[0].append(leftOverPeriods[x])
                else:
                    schedule[1].append(leftOverPeriods[x])
    return schedule

CompileSchedule()
