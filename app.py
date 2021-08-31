from flask import Flask, session, render_template, redirect, request
import db as api
import credential
import generator as gen
import os
from google.oauth2 import id_token
from google.auth.transport import requests

app = Flask(__name__)
app.secret_key = credential.secret_key


@app.route('/')
def home():
    try:
        if 'email' in session:
            mail = session['email']
            who = session['who']
            list_data = []
            if who == 0:
                student_id = api.get_student_id(mail)
                joined_classes = api.get_joined_classes(
                    student_id)  # get joined classes ID's
                # print(joined_classes)
                for joined_class_id in joined_classes:
                    data = api.joined_classes_info(joined_class_id)
                    #print(type(data))
                    #data.append(joined_class_id)
                    
                    list_data.append(data)

                #print(list_data)
                return render_template('student/student_main.html', data=list_data)
            else:
                teacher_id = api.get_teacher_id(mail)
                data = api.get_teach_classes(teacher_id)
                return render_template('teacher//teacher_main.html', data=data)
           
        return render_template('index.html')
    except Exception as e:
        print(e)
        return render_template('index.html')


@app.route('/index', methods=['POST', 'GET'])
def index():
    try:
        if 'email' in session:
            return redirect('/')
        if request.method == 'POST':
            form_details = request.form
            who = form_details['who']
            return render_template('/login.html', who1=who)
        return render_template('index.html')
    except Exception as e:
        print(e)
        return render_template('index.html')


@app.route('/gs_login',methods=['POST','GET'])
def gs_login():
    try:
        if 'email' in session:
            return redirect('/')
        token = request.form["idtoken"]
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), "1050801722055-btcvqar75jhdt6shnop5esohpj5avd5c.apps.googleusercontent.com")
        print("here")
        userid = idinfo['sub']
        email = idinfo['email']
        name = idinfo['name']
        api.signup_student(name,email,"","",userid)
        print("hxsbdjhb")
        session['email']=email
        session['who']=0
        return  '/'
    except ValueError as e:
        print(e)
        return render_template('index.html')  

@app.route('/gt_login',methods=['POST','GET'])
def gt_login():
    try:
        if 'email' in session:
            return redirect('/')
        token = request.form["idtoken"]
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), "1050801722055-btcvqar75jhdt6shnop5esohpj5avd5c.apps.googleusercontent.com")
        print("here")
        userid = idinfo['sub']
        email = idinfo['email']
        name = idinfo['name']
        api.signup_teacher(name,email,"","",userid)
        print("hxsbdjhb")
        session['email']=email
        session['who']=1
        return  '/'
    except ValueError as e:
        print(e)
        return render_template('index.html')   

@app.route('/signup/<who1>', methods=['POST', 'GET'])
def signup(who1):
    try:
        if 'email' in session:
            return redirect('/')

        if(request.method == 'POST'):
            form_details = request.form

            who = form_details['who']
            email = form_details['email']
            password = form_details['password']
            name = form_details['name']
            phone_no = form_details['phone_no']

            if(who == "student"):
                if api.check_stud_mail(email):
                    return redirect('/')  # existing mail
                student_id = gen.stud_key()
                while api.check_stud_key(student_id):
                    student_id = gen.stud_key()

                api.signup_student(name, email, password, phone_no, student_id)
                session['email'] = email
                session['who'] = 0
                return redirect('/')

            else:
                if api.check_teach_mail(email):
                    return redirect('/')  # existing mail
                teacher_id = gen.teach_key()
                while api.check_teach_key(teacher_id):
                    teacher_id = gen.teach_key()

                api.signup_teacher(name, email, password, phone_no, teacher_id)
                session['email'] = email
                session['who'] = 1
                return redirect('/')

        return render_template('signup.html', who1=who1)
    except Exception as e:
        print(e)
        return render_template('signup.html', who1=who1)


@app.route('/login', methods=['POST', 'GET'])
def login():
    try:
        if 'email' in session:
            mail = session['email']
            who = session['who']
            return redirect('/')

        if request.method == 'POST':
            form_details = request.form

            who = form_details['who']
            email = form_details['email']
            password = form_details['password']
            if(who == 'student'):
                
                flag = api.login_student(email, password)

                if(flag == 1):
                    session['email'] = email
                    session['who'] = 0
                    return redirect('/')
                elif(flag == 0):
                    # remove print statements and add reply him with proper reply
                    print("wrong password")
                    return render_template('login.html')
                else:
                    print("user not exist")
                    return render_template('login.html')

            else:
                flag = api.login_teacher(email, password)
                if(flag == 1):
                    session['email'] = email
                    session['who'] = 1
                    return redirect('/')
                elif(flag == 0):
                    print("wrong password")
                    return render_template('login.html')
                else:
                    print("user not exist")
                    return render_template('login.html')
        return render_template('login.html')
    except Exception as e:
        print(e)
        return render_template('login.html')


@app.route('/create_class')
def create_class():
    return render_template('teacher/create_class.html')


@app.route('/add_class')
def add_class():
    return render_template('student/add_class.html')


@app.route('/create_class_data', methods=['POST', 'GET'])
def create_class_data():
    try:
        if request.method == 'POST':
            form_details = request.form
            class_name = form_details['class_name']
            class_link = form_details['class_link']
            if 'email' not in session:
                return redirect('/')
            mail = session['email']
            teacher_id = api.get_teacher_id(mail)
            if api.check_class_name(class_name, teacher_id):
                return redirect('/')  # after this return alert
            class_id = gen.class_id()
            while api.check_class_id(class_id):
                class_id = gen.class_id()
            api.create_class(class_name, class_id, class_link, teacher_id)
            return redirect('/')
        return render_template("teacher/create_class.html")

    except Exception as e:
        print(e)
        return render_template("teacher/create_class.html")


# for student joinining class
@app.route('/add_class_data', methods=['POST', 'GET'])
def join_class_data():
    try:
        if request.method == 'POST':
            # print('HEllo')
            form_details = request.form
            class_code = form_details['class_code']
           # print(class_code)
            if 'email' not in session:
                return redirect('/')
            # print("fuck")
            if api.check_class_id(class_code) == False:
                return redirect('/')  # WRONG class code alert
            # print('suck')
            mail = session['email']
            student_id = api.get_student_id(mail)
            # print('Hello')
            if api.already_joined_class(student_id, class_code):
                # after this alert that class is already joined
                return redirect('/')
            # print('BYE')
            api.join_class(student_id, class_code)
            return redirect('/')
        return render_template("student/add_class.html")
    except Exception as e:
        print(e)
        return render_template("student/add_class.html")


@app.route('/class/<code>')
def class_info(code):
    try:
        if 'email' not in session:
            return redirect('/')
        data = api.get_class_data(code)
        details = api.get_teach_partiular_subject(code)
        return render_template('teacher/class_content.html', data=data, details=details, code=code)
    except Exception as e:
        print(e)
        return redirect('/')

@app.route('/stuAss/<assId>' , methods=['GET', 'POST'])
def stuAss(assId):
    try:
        if 'email' not in session:
            return redirect('/')
        print("mofosssssssss")
        return render_template('student/stuAss.html' , assId=assId)
    except Exception as e:
        print(e)
        return redirect('/')

@app.route('/stuAssSubmit/<assId>', methods=['GET', 'POST'])
def stuAssSubmit(assId):
    try:
        print("hereeeeeeee")
        if 'email' not in session:
            return redirect('/')
        print("here")
        if request.method == 'POST':
            form_details = request.form
            content_id = form_details['assId']
            mail = session['email']
            print(content_id)
            print(mail)
            StuId=api.getStuId(mail)
            print(StuId)
            api.submitAss(StuId, content_id,"StuId+content_id")
        return render_template('student/stuAss.html' , assId=assId)
    except Exception as e:
        print(e)
        return redirect('/')


@app.route('/add_class_content/<code>', methods=['POST', 'GET'])
def add_class_content(code):
    try:
        return render_template('teacher/add_class_content.html', code=code)
    except Exception as e:
        print(e)


@app.route('/student_class/<code>')    ## for student class info 
def stud_class_info(code):
    try:
        if 'email' not in session:
            return redirect('/')
        data = api.get_class_data(code)  ## get the content heading,content_id, descript and uploadtime
        details = api.get_teach_partiular_subject(code)  ## same as teacher for class link and name
        return render_template('student/student_class_content.html',data=data,details=details,code=code)
    except Exception as e:
        print(e)
        return redirect('/')



@app.route('/add_content', methods=['POST', 'GET'])
def add_content():
    try:
        if request.method == 'POST':
            form_details = request.form
            content_heading = form_details['content_heading']
            
            
            descript = form_details['description']
            reference_link = form_details['reference_link']
            max_score = form_details['max_score']
            due_date = form_details['due_date']
            files = request.files.getlist("files")
            # print(type(files))
            # print(files.list().empty())
            class_id = form_details['class_id']
            flag = True
            if(max_score == ""):
                max_score = "default"
            if(due_date == ""):
                due_date = "default"
            if(reference_link == ""):
                reference_link = "None"

            if(len(files) == 1):
                for f in files:
                    if f.filename=="":
                        flag = False

            content_id = gen.content_id()
            while api.check_content_id(content_id):
                content_id = gen.content_id()

            api.add_class_content(class_id, content_id, content_heading, descript, max_score, due_date)
            if reference_link != "None":
                api.add_content_storage_link(content_id, reference_link)

            if flag == True:
                app.config['UPLOAD_FOLDER'] = credential.file_path
                parent = credential.file_path
                directory = content_id
                path = os.path.join(parent, directory)
                os.mkdir(path)
                for f in files:
                    f.save(os.path.join(path, f.filename))
                    api.add_content_storage_files(content_id, os.path.join(path, f.filename))
            
            link = '/class/'+str(class_id)
            return redirect(link)
        return render_template('teacher/teacher_main.html')
    except Exception as e:
        print(e)
        return redirect('/')



@app.route('/show_all_students/<code>',methods=['POST','GET'])
def show_all_joinned_students(code):            ### show the joined teachers and students with class id
    try:
        if 'email' not in session:
            return redirect('/')
        teach_id = api.get_teacher_id_class_id(code)
        teach_name = api.get_teacher_name(teach_id)
        stud_all_id = api.get_students_id(code)
        stud_name=[]
        for stud_id in stud_all_id:
            stud_name.append(api.get_student_name(stud_id[0]))
        return render_template("student/joinned_people.html",teach_name=teach_name,stud_name=stud_name)  
    except Exception as e:
        print(e)
        link='/class/'+str(code)
        return redirect(link) 




@app.route('/show_students/<code>',methods=['POST','GET'])
def show_joinned_students(code):            ### show the joined teachers and students with class id
    try:
        if 'email' not in session:
            return redirect('/')
        teach_id = api.get_teacher_id_class_id(code)
        teach_name = api.get_teacher_name(teach_id)
        stud_all_id = api.get_students_id(code)
        stud_name=[]
        for stud_id in stud_all_id:
            stud_name.append(api.get_student_name(stud_id[0]))
        return render_template("teacher/joinned_people.html",teach_name=teach_name,stud_name=stud_name)  
    except Exception as e:
        print(e)
        link='/class/'+str(code)
        return redirect(link) 



@app.route('/logout')
def logout():
    try:
        session.pop('email')
        session.pop('who')
        print("logout done")
        return redirect('/')
    except Exception as e:
        print(e)
        return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
