# Hack-A-Thon Plan

Are you sick of missing assignments because of your horrible memory?

We are going to be creating a program that will warn you in one day's advance of a upcoming school assignment's due date for any class you have in Canvas.

## Steps

Our program will ask for the user's email address, name, and Canvas login information at the very start of the program's usage.

While it is running, our program will send an email as a reminder to a provided email address at 2:35 pm the day before the assignment is due.

The program will be able to tell what day it is and at what time.

## Process

After the user's data is inputted, the program will login to Canvas and search through each course subject using Canvas' 


 storing the data of all assignments except for those whose due date is past.

While running, the program will check each canvas course once an hour to see if new assignments have been created, and if so, it will store the assignment's name, subject, and due date until the email is sent.

The assignment's data will be deleted after the email is sent to save space and also because we will not be sending the same email twice.