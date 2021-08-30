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
            print(email,password)
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


def get_teacher_id(mail):
    conn=pymysql.connect(
        host=credential.host,
        port=credential.port,
        user=credential.user,
        password=credential.password,
        db=credential.databasename
    )
    try:
        with conn.cursor() as curr:
            sql = "select teacher_id from teacher where email=(%s)"
            curr.execute(sql,(mail))
            output = curr.fetchall()
            return output[0][0]
    except Exception as e:
        print(e)            


def check_class_id(code):
    conn=pymysql.connect(
        host=credential.host,
        port=credential.port,
        user=credential.user,
        password=credential.password,
        db=credential.databasename
    )
    try:
        with conn.cursor() as curr:
            sql = "select class_name from class_table where class_id=(%s)"
            curr.execute(sql,(code))
            output = curr.fetchall()
            if len(output)==0:
                return False
            return True
    except Exception as e:
        print(e)            



def create_class(class_name,class_id,class_link,teacher_id):
    conn=pymysql.connect(
        host=credential.host,
        port=credential.port,
        user=credential.user,
        password=credential.password,
        db=credential.databasename
    )
    try:
        with conn.cursor() as curr:
            sql = "insert into class_table (class_name,class_id,class_link,teacher_id) value (%s,%s,%s,%s)"
            curr.execute(sql,(class_name,class_id,class_link,teacher_id))
            conn.commit()
    except Exception as e:
        print(e)     


def check_teach_mail(email):
    conn=pymysql.connect(
        host=credential.host,
        port=credential.port,
        user=credential.user,
        password=credential.password,
        db=credential.databasename
    )
    try:
        with conn.cursor() as curr:
            sql = "select name from teacher where email=(%s)"
            curr.execute(sql,(email))
            output = curr.fetchall()
            if len(output)==0:
                return False
            return True
    except Exception as e:
        print(e)            

def check_stud_mail(email):
    conn=pymysql.connect(
        host=credential.host,
        port=credential.port,
        user=credential.user,
        password=credential.password,
        db=credential.databasename
    )
    try:
        with conn.cursor() as curr:
            sql = "select name from student where email=(%s)"
            curr.execute(sql,(email))
            output = curr.fetchall()
            if len(output)==0:
                return False
            return True
    except Exception as e:
        print(e)            

def get_teach_classes(teacher_id):
    conn=pymysql.connect(
        host=credential.host,
        port=credential.port,
        user=credential.user,
        password=credential.password,
        db=credential.databasename
    )
    try:
        with conn.cursor() as curr:
            sql = "select class_name,class_id,class_link from class_table where teacher_id=(%s) order by creation_date desc"
            curr.execute(sql,(teacher_id))
            output = curr.fetchall()
            return output
    except Exception as e:
        print(e)    

def check_class_name(class_name,teacher_id):
    conn=pymysql.connect(
        host=credential.host,
        port=credential.port,
        user=credential.user,
        password=credential.password,
        db=credential.databasename
    )
    try:
        with conn.cursor() as curr:
            sql = "select class_id from class_table where class_name=(%s) and teacher_id=(%s)"
            curr.execute(sql,(class_name,teacher_id))
            output = curr.fetchall()
            if len(output)==0:
                return False
            return True
    except Exception as e:
        print(e)     


def get_class_data(class_id):
    conn=pymysql.connect(
        host=credential.host,
        port=credential.port,
        user=credential.user,
        password=credential.password,
        db=credential.databasename
    )
    try:
        with conn.cursor() as curr:
            sql = "select content_heading,upload_time from class_content where class_id=(%s)"
            curr.execute(sql,(class_id))
            output = curr.fetchall()
            return output
    except Exception as e:
        print(e)    

def get_teach_partiular_subject(class_id):
    conn=pymysql.connect(
        host=credential.host,
        port=credential.port,
        user=credential.user,
        password=credential.password,
        db=credential.databasename
    )
    try:
        with conn.cursor() as curr:
            sql = "select class_name,class_link from class_table where class_id=(%s)"
            curr.execute(sql,(class_id))
            output = curr.fetchall()
            return output
    except Exception as e:
        print(e)    


def check_content_id(content_id):
    conn=pymysql.connect(
        host=credential.host,
        port=credential.port,
        user=credential.user,
        password=credential.password,
        db=credential.databasename
    )
    try:
        with conn.cursor() as curr:
            sql = "select class_id from class_content where content_id=(%s)"
            curr.execute(sql,(content_id))
            output = curr.fetchall()
            if len(output)==0:
                return False
            return True
    except Exception as e:
        print(e)        


def add_class_content(class_id,content_id,content_heading,descript,max_score,due_date):
    conn=pymysql.connect(
        host=credential.host,
        port=credential.port,
        user=credential.user,
        password=credential.password,
        db=credential.databasename
    )
    try:
        with conn.cursor() as curr:
            sql = "insert into class_content (class_id,content_id,content_heading,descript,max_score,due_date) value (%s,%s,%s,%s,%s,%s)"
            curr.execute(sql,(class_id,content_id,content_heading,descript,max_score,due_date))
            conn.commit()
    except Exception as e:
        print(e)     


def add_content_storage_link(content_id,links):
    conn=pymysql.connect(
        host=credential.host,
        port=credential.port,
        user=credential.user,
        password=credential.password,
        db=credential.databasename
    )
    try:
        with conn.cursor() as curr:
            sql = "insert into content_storage_links (content_id,links) value (%s,%s)"
            curr.execute(sql,(content_id,links))
            conn.commit()
    except Exception as e:
        print(e)     

def add_content_storage_files(content_id,content_links):
    conn=pymysql.connect(
        host=credential.host,
        port=credential.port,
        user=credential.user,
        password=credential.password,
        db=credential.databasename
    )
    try:
        with conn.cursor() as curr:
            sql = "insert into content_storage (content_id,content_links) value (%s,%s)"
            curr.execute(sql,(content_id,content_links))
            conn.commit()
    except Exception as e:
        print(e)     
