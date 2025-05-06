#importing flask library 
from flask import Flask,redirect,url_for,render_template,request

#import sql python based library for connecting to database
import sqlite3

#import logging for tracking the required program status 
import logging

#creating object for application
app = Flask(__name__)

# Configure the logging level and file handler
app.logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('app.log')

# Define a custom logging format
#formatter = logging.Formatter('%(asctime)s %(message)s')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%m-%Y %H:%M:%S')

# Set the formatter for the file handler
file_handler.setFormatter(formatter)

# Add the file handler to Flask's logger
app.logger.addHandler(file_handler)

app.logger.info("Program Started...")

#function tht retrives the req info of stud roll no given in the input
def get_info(roll_number):
    app.logger.info("inside get_info")
    
    conn = sqlite3.connect('studentsdb.db')
    cusr = conn.cursor()

    cusr.execute('SELECT RollNo,StudentName,Maths,Science,Social,English FROM student_grades WHERE RollNo = ?', (roll_number,))
    res = cusr.fetchall()
    app.logger.info(res)
    return res
#defining the function which gives u the percentage ,according to tht grades are also given with this
def percentage(student):
    avg = ((student[0][2]+student[0][3]+student[0][4]+student[0][5])/400) * 100
    total = round(avg)
    if total in range(75,100):
        gra = 'A'
    elif total in range(55,75):
        gra = 'B'
    elif total in range(35,55):
        gra = 'C'
    else:
        gra = 'Fail'
    return total,gra

#home page for students to enter the roll no
@app.route('/')
def ResHome():
    app.logger.info("Inside ResHome")
    return render_template('submit.html')

#now go for submit page 
@app.route('/submit',methods = ['POST','GET'])
def submit():
    app.logger.info("Inside submit")
    if request.method == 'POST':
        roll_number = request.form['rollno']
        student_info = get_info(roll_number)
        per,gra = percentage(student_info)
        app.logger.info(student_info)
        if len(student_info) > 0:
            app.logger.info("inside student_info")
            return render_template('stddetails.html', student=student_info,Percentage = per,Grades = gra)
        else:
            return render_template('stddetails.html', error = 'Students roll not found')
        
#this is where the program gets start
if __name__=='__main__':
    app.logger.info("inside main...")
    app.run(debug = True)