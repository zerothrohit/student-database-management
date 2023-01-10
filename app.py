# from flask import Flask

# app = Flask(__name__)

# @app.route("/")
# def hello_world():
#     return "<p>Hello, World!</p>"

# if __name__ == "__main__":
#     app.run(debug=True)

# Student Database Management(DataDose)
# College: Shah and Anchor Kutchhi Engineering College
# Batch: 2020-2021 SEM 3
# Class: SE - 13
# Members: Dimple Rathod, Farhat Shaikh, Jinay Vora, Rohit Wahwal
# A Project by SIMP group

from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb

import urllib.request
import os
from werkzeug.utils import secure_filename

app = Flask(__name__, static_url_path='/static')
app.secret_key = "6534291734"

#Upload Config
UPLOAD_FOLDER = 'static/uploads/'
  

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
#Allowed Extensions

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

# MySQL Configuration
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "rohit"
app.config["MYSQL_DB"] = "simp"

db = MySQL(app)

@app.route('/', methods = ['GET', 'POST'])


# For Login/Home Page
def index():
    error = None
    if request.method == 'POST':
        select = request.form.get('dropdwn')
        if select == 'admindrp':
            if 'username' in request.form and 'password' in request.form:
                username = request.form['username']
                password = request.form['password']
                cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute("SELECT * FROM admin WHERE username=%s AND password=%s" ,(username,password))
                info  = cursor.fetchone()
                if info:
                    session['loginsuccess'] = True
                    session['id'] = info['id']
                    session['username'] = info['username']
                    return redirect(url_for('profile_admin'))
                else:
                    error = 'Invalid Credentials! Please try again.'
        elif select == 'teacherdrp':
            if 'username' in request.form and 'password' in request.form:
                username = request.form['username']
                password = request.form['password']
                cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute("SELECT * FROM teacher WHERE username=%s AND password=%s" ,(username,password))
                info  = cursor.fetchone()
                if info:
                    session['loginsuccess'] = True
                    session['reg_id'] = info['reg_id']
                    session['username'] = info['username']
                    return redirect(url_for('profile_teacher'))
                else:
                    error = 'Invalid Credentials! Please try again.'
        elif select == 'studentdrp':
            if 'username' in request.form and 'password' in request.form:
                username = request.form['username']
                password = request.form['password']
                cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute("SELECT * FROM student WHERE username=%s AND password=%s" ,(username,password))
                info  = cursor.fetchone()
                if info:
                    session['loginsuccess'] = True
                    session['reg_id'] = info['reg_id']
                    session['username'] = info['username']
                    return redirect(url_for('profile_student'))
                else:
                    error = 'Invalid Credentials! Please try again.'
        elif select == 'select':
            if 'username' in request.form and 'password' in request.form:
                error = 'Please select a user!'
    return render_template("login.html", error = error)

# For Register
@app.route('/new', methods=['GET','POST'])
def new_user():
    if request.method == "POST":
        if request.form['action'] == 'Student':
            if "reg_id" in request.form and "fullname" in request.form and "phone" in request.form and "dob" in request.form and "username" in request.form and "password" in request.form:
                reg_id = request.form['reg_id']
                fullname = request.form['fullname']
                phone = request.form['phone']
                dob = request.form['dob']
                username = request.form['username']
                password = request.form['password']
                cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
                cur.execute("INSERT INTO simp.student(reg_id, name, phone_no, username, password, dob)VALUES(%s, %s, %s, %s, %s, %s)",(reg_id, fullname, phone, username, password, dob))
                db.connection.commit()
                return redirect(url_for('index'))
        elif request.form['action'] == 'Teacher':
            if "reg_id" in request.form and "fullname" in request.form and "phone" in request.form and "dob" in request.form and "username" in request.form and "password" in request.form:
                reg_id = request.form['reg_id']
                fullname = request.form['fullname']
                phone = request.form['phone']
                dob = request.form['dob']
                username = request.form['username']
                password = request.form['password']
                cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
                cur.execute("INSERT INTO simp.teacher(reg_id, name, phone_no, username, password, dob)VALUES(%s, %s, %s, %s, %s, %s)",(reg_id, fullname, phone, username, password, dob))
                db.connection.commit()
                return redirect(url_for('index'))

    return render_template('Register.html')

# Admin Profile - Edit teacher
@app.route('/profile/admin', methods=['GET','POST'])
def profile_admin():
    if session['loginsuccess'] == True:
        curs = db.connection.cursor()
        curs.execute("SELECT * from teacher")
        data = curs.fetchall()
        curs.close()

        return render_template('admin_teacher.html', teacher = data)


# Admin Profile - Edit student
@app.route('/profile/s_admin', methods=['GET','POST'])
def profile_admin_student():
    if session['loginsuccess'] == True:
        cur = db.connection.cursor()
        cur.execute("SELECT * from student")
        data = cur.fetchall()
        cur.close()

    return render_template('admin_student.html', student = data)

#edit for teacher
@app.route('/updateteacher/<string:id>', methods=['GET','POST'])
def update_teacher(id):
    if session['loginsuccess'] == True:
        cur = db.connection.cursor()
        if request.method=='POST':
            reg_id = request.form['reg_id']
            fullname = request.form['fullname']
            phone = request.form['phone']
            dob = request.form['dob']
            username = request.form['username']
            password = request.form['password']
            sql = "UPDATE teacher SET reg_id = %s, name = %s, phone_no = %s, username = %s, password = %s, dob = %s WHERE reg_id = %s"
            cur.execute(sql,[reg_id, fullname, phone, username, password, dob, id])
            db.connection.commit()
            cur.close()
            return redirect(url_for('profile_admin'))
            cur = db.connection.cursor()
            
        sql = "SELECT * FROM teacher WHERE reg_id = %s"
        cur.execute(sql, [id])
        res = cur.fetchone()
        return render_template("update_user.html", data = res)

#edit for student
@app.route('/updatestudent/<string:id>', methods=['GET','POST'])
def update_student(id):
    if session['loginsuccess'] == True:
        cur = db.connection.cursor()
        if request.method=='POST':
            reg_id = request.form['reg_id']
            fullname = request.form['fullname']
            phone = request.form['phone']
            dob = request.form['dob']
            username = request.form['username']
            password = request.form['password']
            sql = "UPDATE student SET reg_id = %s, name = %s, phone_no = %s, username = %s, password = %s, dob = %s WHERE reg_id = %s"
            cur.execute(sql,[reg_id, fullname, phone, username, password, dob, id])
            db.connection.commit()
            cur.close()
            return redirect(url_for('profile_admin_student'))
            cur = db.connection.cursor()
            
        sql = "SELECT * FROM student WHERE reg_id = %s"
        cur.execute(sql, [id])
        res = cur.fetchone()
        return render_template("update_user.html", data = res)

#delete for teacher
@app.route('/delete/teacher/<string:id_data>', methods=['POST','GET'])
def delete_teacher(id_data):
    cur = db.connection.cursor()
    cur.execute("DELETE FROM teacher WHERE reg_id = %s", (id_data,))
    db.connection.commit()
    return redirect(url_for('profile_admin'))

#delete for student
@app.route('/delete/student/<string:id_data>', methods=['POST','GET'])
def delete_student(id_data):
    cur = db.connection.cursor()
    cur.execute("DELETE FROM student WHERE reg_id = %s", (id_data,))
    db.connection.commit()
    cur.execute("DELETE FROM studentdetails WHERE reg_id = %s", (id_data,))
    db.connection.commit()
    cur.execute("DELETE FROM result WHERE reg_id = %s", (id_data,))
    db.connection.commit()
    return redirect(url_for('profile_admin_student'))

# Teacher Profile
@app.route('/profile/teacher')
def profile_teacher():
    if session['loginsuccess'] == True:
        curs = db.connection.cursor()
        curs.execute("SELECT * from studentdetails")
        data = curs.fetchall()
        curs.close()
        return render_template('sd_teacher.html', details = data, username=session['username'])

@app.route('/delete/sd/<string:id_data>', methods=['POST','GET'])
def delete_sd(id_data):
    cur = db.connection.cursor()
    cur.execute("DELETE FROM studentdetails WHERE reg_id = %s", (id_data,))
    db.connection.commit()
    return redirect(url_for('profile_teacher'))

#Display Aadhar
@app.route('/aadhar_card/<string:id>', methods=['GET','POST'])
def aadhar_view(id):
    if session['loginsuccess'] == True:
        cur = db.connection.cursor()

        sql = "SELECT aadhar_card from studentdetails WHERE reg_id = %s"
        cur.execute(sql,[id])

        res = cur.fetchone()
        print(res)                  
        return render_template("display.html", data = res)

#Display SSC Marksheet
@app.route('/ssc_marksheet/<string:id>', methods=['GET','POST'])
def ssc_view(id):
    if session['loginsuccess'] == True:
        cur = db.connection.cursor()

        sql = "SELECT ssc_marksheet from studentdetails WHERE reg_id = %s"
        cur.execute(sql,[id])

        res = cur.fetchone()
        print(res)                  
        return render_template("display.html", data = res)
    
#Display HSC Marksheet
@app.route('/hsc_marksheet/<string:id>', methods=['GET','POST'])
def hsc_view(id):
    if session['loginsuccess'] == True:
        cur = db.connection.cursor()

        sql = "SELECT hsc_marksheet from studentdetails WHERE reg_id = %s"
        cur.execute(sql,[id])

        res = cur.fetchone()
        print(res)                  
        return render_template("display.html", data = res)

#Display Leaving Certificate
@app.route('/leaving_certificate/<string:id>', methods=['GET','POST'])
def lc_view(id):
    if session['loginsuccess'] == True:
        cur = db.connection.cursor()

        sql = "SELECT leaving_certificate from studentdetails WHERE reg_id = %s"
        cur.execute(sql,[id])

        res = cur.fetchone()
        print(res)                  
        return render_template("display.html", data = res)

#Display Photosign
@app.route('/photosign/<string:id>', methods=['GET','POST'])
def photosign_view(id):
    if session['loginsuccess'] == True:
        cur = db.connection.cursor()

        sql = "SELECT photosign from studentdetails WHERE reg_id = %s"
        cur.execute(sql,[id])

        res = cur.fetchone()
        print(res)                  
        return render_template("display.html", data = res)

# Student Profile/Details
@app.route('/profile/student', methods=['GET','POST'])
def profile_student():
    if session['loginsuccess'] == True:
        curs = db.connection.cursor()
        id = session['reg_id']
        print(id)
        sql = "SELECT * FROM studentdetails WHERE reg_id= %s"
        curs.execute(sql, [id])
        res = curs.fetchone()
        db.connection.commit()
        print(res)
        if res == None:
            if request.method == 'POST':
                
                # if session[id] == res:
                if "fname" in request.form and "lname" in request.form and "reg_id" in request.form and "gen" in request.form:
                    fname = request.form['fname']
                    lname = request.form['lname']
                    f_name = request.form['f_name']
                    m_name = request.form['m_name']
                    date_of_birth = request.form['date_of_birth']
                    gender = request.form['gen']
                    address = request.form['address']
                    phone_number = request.form['phone_number']
                    reg_id = request.form['reg_id']
                    
                    roll_number = request.form['roll_number']
                    #upload aadhar
                    aadhar_card = request.files['aadhar_card']

                    if aadhar_card and allowed_file(aadhar_card.filename):
                        reg_id = request.form['reg_id']
                        filename_a = secure_filename(aadhar_card.filename)
                        basedir = os.path.abspath(os.path.dirname(__file__))
                        aadhar_card.save(os.path.join(basedir, app.config['UPLOAD_FOLDER'], filename_a))
                    
                    #upload SSC Marksheet
                    ssc_marksheet = request.files['ssc_marksheet']

                    if ssc_marksheet and allowed_file(ssc_marksheet.filename):
                        reg_id = request.form['reg_id']
                        filename_s = secure_filename(ssc_marksheet.filename)
                        basedir = os.path.abspath(os.path.dirname(__file__))
                        ssc_marksheet.save(os.path.join(basedir, app.config['UPLOAD_FOLDER'], filename_s))
                    #upload HSC Marksheet
                    hsc_marksheet = request.files['hsc_marksheet']

                    if hsc_marksheet and allowed_file(hsc_marksheet.filename):
                        reg_id = request.form['reg_id']
                        filename_h = secure_filename(hsc_marksheet.filename)
                        basedir = os.path.abspath(os.path.dirname(__file__))
                        hsc_marksheet.save(os.path.join(basedir, app.config['UPLOAD_FOLDER'], filename_h))
                    #upload Leaving Certificate
                    leaving_certificate = request.files['leaving_certificate']

                    if leaving_certificate and allowed_file(leaving_certificate.filename):
                        reg_id = request.form['reg_id']
                        filename_lc = secure_filename(leaving_certificate.filename)
                        basedir = os.path.abspath(os.path.dirname(__file__))
                        leaving_certificate.save(os.path.join(basedir, app.config['UPLOAD_FOLDER'], filename_lc))
                    #upload Photosign
                    photosign = request.files['photosign']

                    if photosign and allowed_file(photosign.filename):
                        reg_id = request.form['reg_id']
                        filename_p = secure_filename(photosign.filename)
                        basedir = os.path.abspath(os.path.dirname(__file__))
                        photosign.save(os.path.join(basedir, app.config['UPLOAD_FOLDER'], filename_p))
                        
                    submitcur = db.connection.cursor(MySQLdb.cursors.DictCursor)
                    submitcur.execute("INSERT INTO simp.studentdetails(reg_id, f_name, l_name, father_name, mother_name, dob, gender, address, phone_no, roll_no, aadhar_card, ssc_marksheet, hsc_marksheet, leaving_certificate, photosign)VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",(reg_id, fname, lname, f_name, m_name, date_of_birth, gender, address, phone_number, roll_number, filename_a, filename_s, filename_h, filename_lc, filename_p))
                    db.connection.commit()
                    #file upload        
                    return render_template('sd_hidden.html')
                    

            return render_template('sd_student.html', username=session['username'])
        else:
            return render_template('sd_hidden.html', username=session['username'])


#Result - Student
@app.route('/profile/studentresult', methods=['GET','POST'])
def result_student():
    if session['loginsuccess'] == True:
        curs = db.connection.cursor()
        resultid = session['reg_id']
        sql = "SELECT * FROM result WHERE reg_id= %s"
        curs.execute(sql, (resultid,))
        res = curs.fetchone()
        db.connection.commit()   
        
        return render_template('result_student.html', data = res, username=session['username'])


# Student - Course
@app.route('/profile/studentcourse', methods=['GET','POST'])
def course_student():
    if session['loginsuccess'] == True:
        curs = db.connection.cursor()
        curs.execute("SELECT * from course")
        data = curs.fetchall()
        curs.close()
    return render_template('course_student.html', course = data, username=session['username'])

# Teacher - Course
@app.route('/profile/teachercourse', methods=['GET','POST'])
def course_teacher():
    if session['loginsuccess'] == True:
        curs = db.connection.cursor()
        curs.execute("SELECT * from course")
        data = curs.fetchall()
        curs.close()
    return render_template('course_teacher.html', course = data, username=session['username'])

#Update course
@app.route('/updatecourse/<string:id>', methods=['GET','POST'])
def update_course(id):
    if session['loginsuccess'] == True:
        cur = db.connection.cursor()
        if request.method=='POST':
            subject_id = request.form['sub_id']
            subject_name = request.form['sub_name']
            teacher_name = request.form['teacher_name']
            sql = "UPDATE course SET subject_id = %s, subject = %s, teacher = %s WHERE subject_id = %s"
            cur.execute(sql,[subject_id, subject_name, teacher_name, id])
            db.connection.commit()
            cur.close()
            return redirect(url_for('course_teacher'))
            cur = db.connection.cursor()
        sql = "SELECT * FROM course WHERE subject_id = %s"
        cur.execute(sql, [id])
        res = cur.fetchone()
        print(res)
        return render_template("update_course.html", data = res)

# Student - routine
@app.route('/profile/studentroutine', methods=['GET','POST'])
def routine_student():
    if session['loginsuccess'] == True:
        curs = db.connection.cursor()
        curs.execute("SELECT * from routine")
        data = curs.fetchall()
        curs.close()
    return render_template('routine_student.html', routine = data, username=session['username'])

#Routine - Teacher
@app.route('/profile/teacherroutine', methods=['GET','POST'])
def routine_teacher():
    if session['loginsuccess'] == True:
        curs = db.connection.cursor()
        curs.execute("SELECT * from routine")
        data = curs.fetchall()
        curs.close()
    return render_template('routine_teacher.html', routine = data, username=session['username'])


#Add course button
@app.route('/add/routine')
def add_routine():
    submitcur = db.connection.cursor(MySQLdb.cursors.DictCursor)
    empty = "0"
    submitcur.execute("INSERT INTO simp.routine(time, monday, tuesday, wednesday, thursday, friday, saturday) VALUES(%s, %s, %s, %s, %s, %s, %s)",(empty, empty, empty, empty, empty, empty, empty))
    db.connection.commit()
    return redirect(url_for('routine_teacher'))

#Update routine
@app.route('/updateroutine/<string:id>', methods=['GET','POST'])
def update_routine(id):
    if session['loginsuccess'] == True:
        cur = db.connection.cursor()
        if request.method=='POST':
            time = request.form['time']
            monday = request.form['mon']
            tuesday = request.form['tue']
            wednesday = request.form['wed']
            thursday = request.form['thurs']
            friday = request.form['fri']
            saturday = request.form['sat']
            sql = "UPDATE routine SET time = %s, monday = %s, tuesday = %s, wednesday = %s, thursday = %s, friday = %s, saturday = %s WHERE sr_no = %s"
            cur.execute(sql,[time, monday, tuesday, wednesday, thursday, friday, saturday, id])
            db.connection.commit()
            cur.close()
            return redirect(url_for('routine_teacher'))
            cur = db.connection.cursor()
        sql = "SELECT * FROM routine WHERE sr_no = %s"
        cur.execute(sql, [id])
        res = cur.fetchone()
        return render_template("update_routine.html", data = res, username=session['username'])

#Delete routine
@app.route('/delete/routine/<string:id_data>', methods=['POST','GET'])
def delete_routine(id_data):
    cur = db.connection.cursor()
    cur.execute("DELETE FROM routine WHERE sr_no = %s", (id_data,))
    db.connection.commit()
    return redirect(url_for('routine_teacher'))


#Delete course
@app.route('/delete/course/<string:id_data>', methods=['POST','GET'])
def delete_course(id_data):
    cur = db.connection.cursor()
    cur.execute("DELETE FROM course WHERE subject_id = %s", (id_data,))
    db.connection.commit()
    return redirect(url_for('course_teacher'))

#Add course button
@app.route('/add/course')
def add_course():
    submitcur = db.connection.cursor(MySQLdb.cursors.DictCursor)
    empty = "0"
    submitcur.execute("INSERT INTO simp.course(subject_id, subject, teacher) VALUES(%s, %s, %s)",(empty, empty, empty))
    db.connection.commit()
    return redirect(url_for('course_teacher'))

# Result - Teacher
@app.route('/profile/teacherresult', methods=['GET','POST'])
def result_teacher():
    if session['loginsuccess'] == True:
        curs = db.connection.cursor()
        curs.execute("SELECT * from result")
        data = curs.fetchall()
        curs.close()
        return render_template("result_teacher.html", result = data, username=session['username'])

#Delete result
@app.route('/delete/result/<string:id_data>', methods=['POST','GET'])
def delete_result(id_data):
    cur = db.connection.cursor()
    cur.execute("DELETE FROM result WHERE reg_id = %s", (id_data,))
    db.connection.commit()
    return redirect(url_for('result_teacher'))

#Add result
@app.route('/add/result')
def add_result():
    submitcur = db.connection.cursor(MySQLdb.cursors.DictCursor)
    empty = "0"
    submitcur.execute("INSERT INTO simp.result(reg_id, attendance, ep1_ia1, ec1_ia1, em1_ia1, em_ia1, bee_ia1, ep1_ia2, ec1_ia2, em1_ia2, em_ia2, bee_ia2, ep1_tw, ec1_tw, em1_tw, em_tw, bee_tw, ep1_sem1, ec1_sem1, em1_sem1, em_sem1, bee_sem1, sem1_final, status) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(empty, empty,empty,empty,empty,empty,empty,empty,empty,empty,empty,empty,empty,empty,empty,empty,empty,empty,empty,empty,empty,empty,empty,empty))
    db.connection.commit()
    return redirect(url_for('result_teacher'))

#Update result
@app.route('/updateresult/<string:id>', methods=['GET','POST'])
def update_result(id):
    if session['loginsuccess'] == True:
        cur = db.connection.cursor()
        if request.method=='POST':
            reg_id = request.form['reg_id']
            attendance = request.form['attendance']
            ep1_ia1 = request.form['ep1_ia1']
            ec1_ia1 = request.form['ec1_ia1']
            em1_ia1 = request.form['em1_ia1']
            em_ia1 = request.form['em_ia1']
            bee_ia1 = request.form['bee_ia1']
            ep1_ia2 = request.form['ep1_ia2']
            ec1_ia2 = request.form['ec1_ia2']
            em1_ia2 = request.form['em1_ia2']
            em_ia2 = request.form['em_ia2']
            bee_ia2 = request.form['bee_ia2']
            ep1_tw = request.form['ep1_tw']
            ec1_tw = request.form['ec1_tw']
            em1_tw = request.form['em1_tw']
            em_tw = request.form['em_tw']
            bee_tw = request.form['bee_tw']
            ep1_sem1 = request.form['ep1_sem1']
            ec1_sem1 = request.form['ec1_sem1']
            em1_sem1 = request.form['em1_sem1']
            em_sem1 = request.form['em_sem1'] 
            bee_sem1 = request.form['bee_sem1']
            

            sql = "UPDATE result SET reg_id = %s, attendance = %s, ep1_ia1 = %s, ec1_ia1 = %s, em1_ia1 = %s, em_ia1 = %s, bee_ia1 = %s, ep1_ia2 = %s, ec1_ia2 = %s, em1_ia2 = %s, em_ia2 = %s, bee_ia2 = %s, ep1_tw = %s, ec1_tw = %s, em1_tw = %s, em_tw = %s, bee_tw = %s, ep1_sem1 = %s, ec1_sem1 = %s, em1_sem1 = %s, em_sem1 = %s, bee_sem1 = %s WHERE reg_id = %s"
            cur.execute(sql,[reg_id, attendance, ep1_ia1, ec1_ia1, em1_ia1, em_ia1, bee_ia1, ep1_ia2, ec1_ia2, em1_ia2, em_ia2, bee_ia2, ep1_tw, ec1_tw, em1_tw, em_tw, bee_tw, ep1_sem1, ec1_sem1, em1_sem1, em_sem1, bee_sem1, id])
            db.connection.commit()
            cur.close()
            return redirect(url_for('update_result', id = id))
            cur = db.connection.cursor()
        sql = "SELECT * FROM result WHERE reg_id = %s"
        cur.execute(sql, [id])
        res = cur.fetchone()
        return render_template("update_result.html", data = res, username=session['username'])

#Calculate result
@app.route('/calculateresult/<string:id_data>', methods=['GET','POST'])
def calculate_result(id_data):
    curs = db.connection.cursor()
    sql = "SELECT * FROM result WHERE reg_id= %s"
    curs.execute(sql, [id_data,])
    res = curs.fetchone()
    db.connection.commit()
    ep1_ia_avg = (res[1] + res[6])/2
    ec1_ia_avg = (res[2] + res[7])/2
    em1_ia_avg = (res[3] + res[8])/2
    em_ia_avg = (res[4] + res[9])/2
    bee_ia_avg = (res[5] + res[10])/2

    obt = ep1_ia_avg+ec1_ia_avg+em1_ia_avg+em_ia_avg+bee_ia_avg+res[11]+res[12]+res[13]+res[14]+res[15]+res[16]+res[17]+res[18]+res[19]+res[20]

    total = 625

    per = (obt/total)*100

    cgpa = (per-11)/7.1

    if cgpa>=10:
        print_cgpa = 10.0
    else:
        print_cgpa = cgpa
    print(print_cgpa)
    if print_cgpa < 4.8:
        status = 'Fail'
    else:
        status = 'Pass'
    curs.execute("UPDATE result SET sem1_final = %s, status = %s WHERE reg_id = %s", (print_cgpa,status,id_data,))
    db.connection.commit()
    return redirect(url_for('update_result', id = id_data))

        

# For Logout 
@app.route('/new/logout')
def logout():
    session.pop('loginsuccess', None)
    session.pop('id', None)
    session.pop('reg_id', None)
    session.pop('username', None)
    return redirect(url_for('index'))

# About 
@app.route('/about')
def about():
    return render_template('about.html')

# Team
@app.route('/team')
def team():
    return render_template('team.html')

# Help
@app.route('/help')
def help():
    return render_template('help.html')

@app.route("/testpage")
def success():
     return "<p>Success!</p>"

if __name__ == "__main__":
    app.run(debug=True)

        
