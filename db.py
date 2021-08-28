import pymysql
import credential

def login_teacher(email,password):
    conn=pymysql.connect(
        host=credential.host,
        port=credential.port,
        user=credential.user,
        password=credential.password,
        db=credential.databasename
    )
    try:
        with conn.cursor() as curr:
            sql = "select password from teacher where email=(%s)"
            curr.execute(sql,email)
            output = curr.fetchone()
            if(output):
                if(password==output[0]):
                    return 1  #correct
                else: return 0   #incorrect
            return -1  #doesnotexist
    except Exception as e:
        print(e)        

def login_student(email,password):
    conn=pymysql.connect(
        host=credential.host,
        port=credential.port,
        user=credential.user,
        password=credential.password,
        db=credential.databasename
    )
    try:
        with conn.cursor() as curr:
            sql = "select password from student where email=(%s)"
            curr.execute(sql,email)
            output = curr.fetchone()
            if(output):
                if(password==output[0]):
                    return 1  #correct
                else: return 0   #incorrect
            return -1  #doesnotexist
    except Exception as e:
        print(e)            

def signup_teacher(name,email,password,phone_no,teacher_id):
    conn=pymysql.connect(
        host=credential.host,
        port=credential.port,
        user=credential.user,
        password=credential.password,
        db=credential.databasename
    )
    try:
        with conn.cursor() as curr:
            sql = "insert into teacher (name,email,password,phone_no,teacher_id) value (%s,%s,%s,%s,%s)"
            # phone_no = int(phone_no)
            curr.execute(sql,(name,email,password,phone_no,teacher_id))
            conn.commit()
    except Exception as e:
        print(e)            

def signup_student(name,email,password,phone_no,student_id):
    conn=pymysql.connect(
        host=credential.host,
        port=credential.port,
        user=credential.user,
        password=credential.password,
        db=credential.databasename
    )
    try:
        with conn.cursor() as curr:
            sql = "insert into student (name,email,password,phone_no,student_id) value (%s,%s,%s,%s,%s)"
            # phone_no = int(phone_no)
            curr.execute(sql,(name,email,password,phone_no,student_id))
            conn.commit()
    except Exception as e:
        print(e)            

def check_teach_key(key):
    conn=pymysql.connect(
        host=credential.host,
        port=credential.port,
        user=credential.user,
        password=credential.password,
        db=credential.databasename
    )
    try:
        with conn.cursor() as curr:
            sql = "select name from teacher where teacher_id=(%s)"
            curr.execute(sql,key)
            output = curr.fetchall()
            if len(output)==0:
                return False
            else:
                return True   
    except Exception as e:
        print(e)


def check_stud_key(key):
    conn=pymysql.connect(
        host=credential.host,
        port=credential.port,
        user=credential.user,
        password=credential.password,
        db=credential.databasename
    )
    try:
        with conn.cursor() as curr:
            sql = "select name from student where student_id=(%s)"
            curr.execute(sql,key)
            output = curr.fetchall()
            if len(output)==0:
                return False
            else:
                return True 
    except Exception as e:
        print(e)            