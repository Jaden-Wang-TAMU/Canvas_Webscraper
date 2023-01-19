from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import urllib
import time

import tkinter as tk
import tkinter.font as tkFont
import csv
from tkinter import *
from tkinter.ttk import *

from canvasapi import Canvas
import sqlite3
from sqlite3 import Error

from datetime import date, datetime, timedelta
from tkcalendar import Calendar # must install tkcalendar

from tkinter import messagebox


# Opens tkinter and asks for username and password
window = tk.Tk()
fontStyle = tkFont.Font(family="Lucida Grande", size=15)
smallerfontStyle = tkFont.Font(family="Lucida Grande", size=12)
title = tk.Label(text="Canvas Login", font=fontStyle)
title.pack()
user_input = tk.Label(text="Enter your Katy ISD ID:", font=fontStyle)
user_input.pack()
user_entry = tk.Entry()
user_entry.pack()
password = tk.Label(text="Enter your Password:", font=fontStyle)
password.pack()
password_entry = tk.Entry(window, show="*", width=15)
password_entry.pack()

# Hides password
def mark() :
    if var.get() == 1 :
        password_entry.configure(show = "")
    elif var.get() == 0 :
        password_entry.configure(show = "*")

var = IntVar()
 
            
# # # Getting current date:
now = datetime.now()
# print("now = ", now)
nowyear, nowmonth, nowday = str(now)[0:10].split("-")
Picking_Date = Label(window, text = "Select a due date from below").pack(pady=10)
Default = Label(window, text = "Default due date is tomorrow").pack()
cal = Calendar(window, selectmode = 'day',
               year = int(nowyear), month = int(nowmonth),
               day = int(nowday))

cal.pack(pady = 20)

def getCourses():
    global maxdate
    global now
    global picked_max_date
    year,month,day = 'next_date="{}"'.format(cal.selection_get())[11: 21].split("-")
    # print(year+" "+month+" "+day)
    maxdate = datetime(int(year), int(month), int(day)-1)
    now=maxdate
    picked_max_date=True
    # print(maxdate)
    date.config(text = "Your selected due date is: " + cal.get_date())

def search():
    global picked_max_date
    global now
    user = user_entry.get()
    password=password_entry.get()
    if(user!="" and password!=""):
        global driver
        # Opens Canvas and inputs username and password
        driver = webdriver.Chrome(ChromeDriverManager().install())
        url = 'https://katyisd.instructure.com/login/ldap'
        driver.get(url)
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)

        time.sleep(1)
        user = driver.find_element_by_xpath("//input[@class='ic-Input text']").send_keys(user)
        password = driver.find_element_by_xpath("//input[@type='password']").send_keys(password)
        driver.find_element_by_xpath("//button[@type='submit']").click()
        time.sleep(1)

        # # Gets Access Key
        url = 'https://katyisd.instructure.com/profile/settings'
        driver.get(url)
        driver.find_element_by_xpath("//a[@class='btn btn-primary add_access_token_link']").click()
        time.sleep(1)
        driver.find_element_by_xpath("//input[@name='access_token[purpose]']").send_keys("Indepedent Study Hackathon #1")
        time.sleep(1)
        driver.find_element_by_xpath("//button[@class='btn btn-primary submit_button button_type_submit ui-button ui-widget ui-state-default ui-corner-all ui-button-text-only']").click()
        time.sleep(1)
        API_URL = "https://katyisd.instructure.com"
        API_KEY=driver.find_element_by_xpath("//div[@class='visible_token']").text

        canvas = Canvas(API_URL, API_KEY)
        
        courses = canvas.get_courses()
        courses_list=[]
        all_assignments=[]
        all_dates=[]
        for course in courses:
            if(hasattr(course,'course_code')):
                # print(course)
                temp_assignments=[]
                temp_dates=[]
                assignments = course.get_assignments(bucket='future')
                for assignment in assignments:
                    # print(assignment.__dict__)
                    name = assignment.name
                    dueDate = assignment.due_at
                    # description = assignment.description
                    # sprint(description)
                    # allowedAttempts = str(assignment.allowed_attempts)
                    if(dueDate!=None):
                        # print(name + "\nDue Date: " + dueDate)
                            # print(name + "\nDue Date: " + dueDate)
                            tempyear, tempmonth, tempday = str(dueDate)[0:10].split("-")
                            try:
                                tempdate = datetime(int(tempyear),int(tempmonth),int(tempday))
                                if(tempdate>maxdate):
                                    name = assignment.name
                                    temp_dates.append(dueDate)
                                    temp_assignments.append(name)
                                    print(name+ " Due Date:" +tempyear +" "+ tempmonth +" "+tempday)
                            except:
                                name = assignment.name
                                print(name+" Due Date: Unknown")
                                temp_dates.append(dueDate)
                                temp_assignments.append(name)
                            
                        
                if (len(temp_assignments)!=0):
                    all_assignments.append(temp_assignments)
                    all_dates.append(temp_dates)
                    courses_list.append(course.name)
        print("Done getting courses, assignments, and due dates")
        
        # print("Courses:")
        # for course in courses_list:
        #     print(course)

        # print("Assignments:")
        # for assign in all_assignments:
        #     print(assign)

        # print("Due Dates:")
        # for date in all_dates:
        #     print(date)

        rows=[]
        for x in range(len(all_assignments)):
            assignment_list=all_assignments[x]
            due_date_list=all_dates[x]
            for y in range(len(assignment_list)):
                field=[]
                field.append(str(courses_list[x]))
                field.append(str(assignment_list[y]))
                field.append(str(due_date_list[y]))
                rows.append(field)
        for row in rows:
            print(row)

        with open('assignments.csv', 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            fields=["Course", "Title", "Due_Date"]
            csvwriter.writerow(fields)
            csvwriter.writerows(rows)

        if picked_max_date!=True:
            now = datetime.now()
        nowyear, nowmonth, nowday = str(now)[0:10].split("-")

        # # # Creating Table and Database
        con = sqlite3.connect("data.sqlite")
        cur = con.cursor()
        full_command='''CREATE TABLE IF NOT EXISTS assignments(Course TEXT NOT NULL, Title TEXT NOT NULL, Due_Date TEXT NOT NULL);'''
        cur.execute(full_command)
        insert_records="INSERT INTO assignments VALUES(?, ?, ?)"
        a_file = open('assignments.csv')
        rows = csv.reader(a_file)
        cur.executemany(insert_records, rows)
        cur.execute("SELECT * FROM assignments")
        cur.fetchall()

        con.commit()

        messages=""
        result=con.execute("SELECT Course, Title, Due_Date FROM assignments")
        final_rows=result.fetchall()
        for each in final_rows:
            assign_date=each[2]
            if assign_date != "Date" and assign_date != "Due_Date":
                tempyear, tempmonth, tempday = str(assign_date)[0:10].split("-")
                if(tempyear==nowyear and tempmonth==nowmonth and int(tempday)==int(nowday)+1):
                    messages=messages+str(each[1])+"\n"
                    print(each[1], tempyear, tempmonth, tempday)
        if messages=="":
            messages="None"
        print('Done with tomorrow assignments')
            

        con.close()
        if picked_max_date!=True:
            messagebox.showinfo("Assignments due tomorrow:", messages)
        else:
            messagebox.showinfo("Assignments due on this day:", messages)


#Creates Login Button
B = tk.Button(window, text ="Search", command = search, bg='green')
B.pack()

#Creates Reveal Password Button
bt = Checkbutton(window, command = mark, offvalue = 0, onvalue = 1, variable = var)
bt.place(x = 185, y = 107)

Button(window, text = "Select Due Date",
       command = getCourses).pack(pady = 20)
date = Label(window, text = "")
date.pack(pady = 20)

window.mainloop()
