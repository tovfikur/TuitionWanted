import sqlite3

con = sqlite3.connect('db.sqlite3')
cur = con.cursor()

for row in cur.execute('SELECT * FROM Teacher_teacher'):
    print(row)

with open('Cleaned-1.csv', 'r') as lines:
    for line in lines:
        # print(line.split(','))
        sql_query = """INSERT INTO "main"."Teacher_teacher"
    
    ("id","Name","Email","Phone",
    "Facebook_Link","Expertise","Gender","Type",
    "Running_Tuition","Location2","Location3","Location4",
    "Note","Important_Note","Rating","BAN",
    "Avatar","Certificate","NID","Reminder",
    "Graduation_Institute_id","Graduation_Subject_id","RatedPerson",
    "Graduation_GPA","HSC_GOLDEN","HSC_GPA","HSC_Institute",
    "HSC_Subject_id","SSC_GOLDEN","SSC_GPA","SSC_Institute",
    "SSC_Subject_id","PermanentLocation","PresentLocation","HSC_Year",
    "SSC_Year","HSC_MEDIUM","Post_Graduation_GPA","Post_Graduation_Institute_id",
    "Post_Graduation_Subject_id","ExpectedSalary","TuitionStyle","BloodGroup",
    "Guardian_phone","Graduation_Year","Post_Graduation_Year","Refer_phone",
    "Refer_Name","SSC_MEDIUM") 
    VALUES (NULL,'"""+line.split(',')[0]+"""',NULL,"""+line.split(',')[1]+""",
    NULL,NULL,NULL,0,
    0,NULL,NULL,NULL,
    '"""+line.split(',')[31]+line.split(',')[32]+line.split(',')[33]+line.split(',')[34]+line.split(',')[35]+line.split(',')[36]+"""'"""+""",NULL,NULL,'',
    NULL,NULL,NULL,NULL,
    NULL,NULL,NULL,
    NULL,NULL,NULL,NULL,
    NULL,NULL,NULL,NULL,
    NULL,NULL,NULL,NULL,
    NULL,NULL,NULL,NULL,
    NULL,NULL,NULL,NULL,
    NULL,NULL,NULL,NULL,
    NULL,NULL);"""
        print(sql_query)
        count = cur.execute(sql_query)
        con.commit()
