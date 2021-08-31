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
            curr.execute(sql,(email))
            output = curr.fetchone()
            if(output):
                if(password==output[0]):
                    return 1  #correct
                else: return 0   #incorrect
            return -1  #doesnotexist
    except Exception as e:
        print(e)     

def getStuId(email):
    conn=pymysql.connect(
        host=credential.host,
        port=credential.port,
        user=credential.user,
        password=credential.password,
        db=credential.databasename
    )
    try:
        with conn.cursor() as curr:
            sql = "select student_id from student where email=(%s)"
            curr.execute(sql,(email))
            output = curr.fetchone()
            return output[0]
            
    except Exception as e:
        print(e)      

def submitAss(student_id,content_id,submission_id ):
    conn=pymysql.connect(
        host=credential.host,
        port=credential.port,
        user=credential.user,
        password=credential.password,
        db=credential.databasename
    )
    try:
        with conn.cursor() as curr:
            sql = "insert into submission (student_id,content_id,submission_id) value (%s,%s,%s)"
            curr.execute(sql ,(student_id,content_id,submission_id))
            conn.commit()
            # sql = "insert into submission_storage (submission_id , submission_link) value (%s ,%s)"
            # curr.execute(sql ,(submission_id , submission_link))
            # conn.commit()
            
            # print(output)
            # if(output):
            #     return  1
            # else:
            #     return 0
            
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
        print("in here too")
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


def get_student_id(mail):
    conn=pymysql.connect(
        host=credential.host,
        port=credential.port,
        user=credential.user,
        password=credential.password,
        db=credential.databasename
    )
    try:
        with conn.cursor() as curr:
            sql = "select student_id from student where email=(%s)"
            curr.execute(sql,(mail))
            output = curr.fetchall()
            #print(output[0][0])
            return output[0][0]
    except Exception as e:
        print(e)   

def check_class_id(code):               ## check class exists or not
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


def join_class(student_id,class_id):              ## join the new class from student
    conn=pymysql.connect(
        host=credential.host,
        port=credential.port,
        user=credential.user,
        password=credential.password,
        db=credential.databasename
    )
    try:
        with conn.cursor() as curr:
            sql = "insert into stud_classroom(student_id,class_id) value(%s,%s)"
            #sql = "REPLACE INTO stud_classroom(student_id,class_id) value(%s,%s)"
            curr.execute(sql,(student_id,class_id))
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


def joined_classes_info(class_id):   ## Retrieve join class info i.e. class name,class link,teacher name
    conn=pymysql.connect(
        host=credential.host,
        port=credential.port,
        user=credential.user,
        password=credential.password,
        db=credential.databasename
    )
    try:
        with conn.cursor() as curr:
            sql = "select C.class_name,C.class_link,C.class_id,T.name from class_table C join teacher T on (C.teacher_id = T.teacher_id and C.class_id =(%s)) order by C.creation_date "
            curr.execute(sql,(class_id))
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


def already_joined_class(student_id,class_id):      ## check if class is already joined
    conn=pymysql.connect(
        host=credential.host,
        port=credential.port,
        user=credential.user,
        password=credential.password,
        db=credential.databasename
    )
    try:
        with conn.cursor() as curr:
            #sql = "REPLACE INTO stud_classroom(student_id,class_id) value(%s,%s)"
            sql = "SELECT * from stud_classroom where student_id=(%s) and class_id=(%s)"
            curr.execute(sql,(student_id,class_id))
            output = curr.fetchall()
            #print(output)
            if len(output)==0:
                return False
            return True
    except Exception as e:
        print(e)


def get_joined_classes(student_id):
    conn=pymysql.connect(
        host=credential.host,
        port=credential.port,
        user=credential.user,
        password=credential.password,
        db=credential.databasename
    )
    try:
        with conn.cursor() as curr:
            sql = "select class_id from stud_classroom where student_id=(%s)"
            curr.execute(sql,(student_id))
            output = curr.fetchall()
            return output
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
            sql = "select content_heading,content_id,descript,upload_time from class_content where class_id=(%s) order by upload_time desc"
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
            if(max_score=="default" and due_date=="default"):
                sql = "insert into class_content (class_id,content_id,content_heading,descript) value (%s,%s,%s,%s)"
                curr.execute(sql,(class_id,content_id,content_heading,descript))
            elif max_score=="default":
                sql = "insert into class_content (class_id,content_id,content_heading,descript,due_date) value (%s,%s,%s,%s,%s)"
                curr.execute(sql,(class_id,content_id,content_heading,descript,due_date))
            elif due_date=="default":
                sql = "insert into class_content (class_id,content_id,content_heading,descript,max_score) value (%s,%s,%s,%s,%s)"
                curr.execute(sql,(class_id,content_id,content_heading,descript,max_score))
            
            else:
                sql = "insert into class_content (class_id,content_id,content_heading,descript,max_score,due_date) value (%s,%s,%s,%s,%s,%s)"
                curr.execute(sql,(class_id,content_id,content_heading,descript,max_score,due_date))
            conn.commit()
    except Exception as e:
        print(e)     


def add_content_storage_link(content_id,links):  # store the content links from teacher
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

def add_content_storage_files(content_id,content_links):  #store the teacher uploaded files assignment
    conn=pymysql.connect(
        host=credential.host,
        port=credential.port,
        user=credential.user,
        password=credential.password,
        db=credential.databasename
    )
    try:
        with conn.cursor() as curr:
            print(content_id,content_links)
            sql = "insert into content_storage (content_id,content_links) value (%s,%s)"
            curr.execute(sql,(content_id,content_links))
            conn.commit()
    except Exception as e:
        print(e) 
        
def add_student_storage_files(submission_id,submission_link):  #Student
    conn=pymysql.connect(
        host=credential.host,
        port=credential.port,
        user=credential.user,
        password=credential.password,
        db=credential.databasename
    )
    try:
        with conn.cursor() as curr:
            sql = "insert into submission_storage (submission_id,submission_link) value (%s,%s)"
            curr.execute(sql,(submission_id,submission_link))
            conn.commit()
    except Exception as e:
        print(e)   

def is_assignment_submitted(submission_id):  #Student
    conn=pymysql.connect(
        host=credential.host,
        port=credential.port,
        user=credential.user,
        password=credential.password,
        db=credential.databasename
    )
    try:
        with conn.cursor() as curr:
            sql = "select submit_time from submission where submission_id=(%s)"
            curr.execute(sql,(submission_id))
            output = curr.fetchall()
            if len(output)==0:
                return False
            return True
    except Exception as e:
        print(e)

print(is_assignment_submitted("Hdo0g0wrgp4vxnvUBG3331PjDmY3N9"))     


def get_content_specific_data(content_id):  ## get the content specific data for teacher
    conn=pymysql.connect(
        host=credential.host,
        port=credential.port,
        user=credential.user,
        password=credential.password,
        db=credential.databasename
    )
    try:
        with conn.cursor() as curr:
            sql = "select class_id,content_heading,descript,due_date from class_content where content_id=(%s)"
            curr.execute(sql,(content_id))
            output = curr.fetchall()
            return output[0]
    except Exception as e:
        print(e)




def get_total_students(class_id):   ## get count of  total students for particular class
    conn=pymysql.connect(
        host=credential.host,
        port=credential.port,
        user=credential.user,
        password=credential.password,
        db=credential.databasename
    )
    try:
        with conn.cursor() as curr:
            sql = "select count(*) from stud_classroom where class_id =(%s)"
            curr.execute(sql,(class_id))
            output = curr.fetchall()
            return output[0][0]
    except Exception as e:
        print(e)



def get_smart_students(content_id):  ## get the count of students that completed assignment
    conn=pymysql.connect(
        host=credential.host,
        port=credential.port,
        user=credential.user,
        password=credential.password,
        db=credential.databasename
    )
    try:
        with conn.cursor() as curr:
            sql = "select count(*) from submission where content_id =(%s) "
            curr.execute(sql,(content_id))
            output = curr.fetchall()
            return output[0][0]
    except Exception as e:
        print(e) 


def  get_data_smart_students(content_id):   ## get the student name and it's pending score with content_id
    conn=pymysql.connect(
        host=credential.host,
        port=credential.port,
        user=credential.user,
        password=credential.password,
        db=credential.databasename
    )
    try:
        with conn.cursor() as curr:
            sql = "select S.name,C.score from student S join submission C on(S.student_id = C.student_id and content_id =(%s)) "
            curr.execute(sql,(content_id))
            output = curr.fetchall()
            return output
    except Exception as e:
        print(e) 


def get_Max_marks(content_id):
    conn=pymysql.connect(
        host=credential.host,
        port=credential.port,
        user=credential.user,
        password=credential.password,
        db=credential.databasename
    )
    try:
        with conn.cursor() as curr:
            sql = "select max_score from class_content where content_id=(%s)"
            curr.execute(sql,(content_id))
            output = curr.fetchall()
            return output[0][0]
    except Exception as e:
        print(e)  

print(get_Max_marks('7sZoeoQ7GBtc3rl'))

def get_teacher_id_class_id(class_id):
    conn=pymysql.connect(
        host=credential.host,
        port=credential.port,
        user=credential.user,
        password=credential.password,
        db=credential.databasename
    )
    try:
        with conn.cursor() as curr:
            sql = "select teacher_id from class_table where class_id=(%s)"
            curr.execute(sql,(class_id))
            output = curr.fetchall()
            return output[0][0]
    except Exception as e:
        print(e)     

def get_teacher_name(teacher_id):
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
            curr.execute(sql,(teacher_id))
            output = curr.fetchall()
            return output[0][0]
    except Exception as e:
        print(e)     


def get_students_id(class_id):
    conn=pymysql.connect(
        host=credential.host,
        port=credential.port,
        user=credential.user,
        password=credential.password,
        db=credential.databasename
    )
    try:
        with conn.cursor() as curr:
            sql = "select student_id from stud_classroom where class_id=(%s)"
            curr.execute(sql,(class_id))
            output = curr.fetchall()
            return output
    except Exception as e:
        print(e)     

def get_student_name(student_id):
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
            curr.execute(sql,(student_id))
            output = curr.fetchall()
            return output[0][0]
    except Exception as e:
        print(e)     
