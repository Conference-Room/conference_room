from flask import Flask,session,render_template,redirect,request
import db as api
import credential
import generator as gen

app = Flask(__name__)
app.secret_key = credential.secret_key



@app.route('/')
def home():
    if 'email' in session:
        mail = session['email']
        who = session['who']
        if who==0:
            return render_template('student/student_main.html')
        else:
            return render_template('//teacher//teacher_main.html')    
        # return render_template('class.html')
    return redirect('/login')


@app.route('/signup',methods=['POST','GET'])
def signup():
    if 'email' in session:
        return redirect('/')
    
    if(request.method=='POST'):
        form_details=request.form
        
        who = form_details['who']
        email = form_details['email']
        password = form_details['password'] 
        name = form_details['name']
        phone_no = form_details['phone_no']
        
        if(who=='student'):
            print("Im in student")
            print(form_details)
            student_id = gen.stud_key()
            while api.check_stud_key(student_id):
                student_id=gen.stud_key()

            api.signup_student(name,email,password,phone_no,student_id)  
            session['email']=email
            session['who']=0
            return redirect('/')  

        else:
            teacher_id = gen.teach_key()
            while api.check_teach_key(teacher_id):
                teacher_id=gen.teach_key()

            api.signup_teacher(name,email,password,phone_no,teacher_id)  
            session['email']=email
            session['who']=1
            return redirect('/')    
    return render_template('signup.html')        
            

@app.route('/login',methods=['POST','GET'])
def login():
    if 'email' in session:
        mail = session['email']
        who = session['who']
        if who==0:
            return render_template('student\student_main.html')
        else:
            return render_template('\\teacher\\teacher_main.html')  

    if request.method=='POST':
        form_details=request.form
        
        who = form_details['who']
        email = form_details['email']
        password = form_details['password']
        
        if(who=='student'):
            flag = api.login_student(email,password)
            if(flag==1):
                session['email']=email
                session['who']=0
                return redirect('/')
            elif(flag==0):
                print("wrong password") #remove print statements and add reply him with proper reply
                return render_template('login.html')
            else:
                print("user not exist")
                return render_template('login.html')        
        
        else:
            flag = api.login_teacher(email,password)
            if(flag==1):
                session['email']=email
                session['who']=1
                return redirect('/')
            elif(flag==0):
                print("wrong password")
                return render_template('login.html')
            else:
                print("user not exist")
                return render_template('login.html')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('email')
    session.pop('who')
    print("logout done")
    return redirect('/')


if __name__ =='__main__':
    app.run(debug=True)