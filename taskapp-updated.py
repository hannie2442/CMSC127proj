###########################################################
# CMSC 127 S-4L FINAL PROJECT FOR S.Y '21-'22
# A simple task listing app using python and mysql(mariadb)
# Authors:
#    ඞbadines, Jhiedy Wynn
#    Cagara, Johann
#    Tuazon, Andre
###########################################################
#imports
from cgi import print_environ_usage
from venv import create
import mysql.connector as mariadb
from random import randint

'''
on mariadb root
create user 'test' w/ password 'password'
grant all priviliges on database 'taskapp'
'''
#Create mysql connection and define cursor
mariadb_connection = mariadb.connect(user='test', password='password', host = 'localhost', database = 'taskapp')
create_cursor = mariadb_connection.cursor()

#vvv for testing vvv
#Create Category Table
create_cursor.execute("CREATE TABLE category ("
                    + "Category_id INT(3) NOT NULL, "
                    + "Name VARCHAR(20) NOT NULL, "
                    + "Status VARCHAR(20) NOT NULL, "
                    + "CONSTRAINT category_Category_id_pk PRIMARY KEY(Category_id) "
                    + ");")
#Create Task Table
create_cursor.execute("CREATE TABLE task ("
                    + "Task_id INT(2) NOT NULL, "
                    + "Name VARCHAR(20) NOT NULL, "
                    + "Description VARCHAR(100), "
                    + "Date_posted DATE NOT NULL, "
                    + "Deadline DATE NOT NULL, "
                    + "Status VARCHAR(20) NOT NULL, "
                    + "Category_id INT(3) NOT NULL, "
                    + "CONSTRAINT task_Task_id_pk PRIMARY KEY(Task_id), "
                    + "CONSTRAINT task_Category_id_fk FOREIGN KEY(Category_id) REFERENCES "
                    + "category(Category_id)"
                    + ");")
#^^^ for testing ^^^

#Function declarations
def markTaskAsDone(id):
    late = "Accomplished Late"
    acc = "Accmoplished"
    sql_statement = 'UPDATE task SET Status = CASE WHEN DATEDIFF(CURDATE(), Deadline)<0 THEN %s ELSE %s END WHERE Task_id=%s;'
    to_update = (late, acc, id)
    create_cursor.execute(sql_statement, to_update)
    mariadb_connection.commit()
    print("Task %s is Marked as DONE." % id)

def addCategory(id, name):
    defaultStatus = "Not Yet Done"
    sql_statement = 'INSERT INTO category VALUES (%s, %s, %s);'
    to_insert = (id, name, defaultStatus)
    create_cursor.execute(sql_statement, to_insert)
    mariadb_connection.commit()
    print("Category %s Added!\n" % name)

def editCategory(id,name):
    sql_statement = 'UPDATE category SET Name=%s WHERE Category_id=%s;'
    to_update = (newCategName, id)
    create_cursor.execute(sql_statement, to_update)
    mariadb_connection.commit()
    print("Category %s Edited!\n" % name)

def deleteCategory(id):
    sql_statement = 'DELETE FROM category WHERE Category_id=%s;'
    to_delete = (id)
    create_cursor.execute(sql_statement, (to_delete,))
    mariadb_connection.commit()
    sql_statement = 'UPDATE task SET Category_id="None" WHERE Category_id=%s;'
    to_update = (id)
    create_cursor.execute(sql_statement, (to_update,))
    mariadb_connection.commit()
    print("Goodbye Category %s.\n" % id)

def viewCategory():
    sql_statement = 'SELECT * FROM category;'
    create_cursor.execute(sql_statement)
    category = create_cursor.fetchall()
    print("=======C A T E G O R Y=======\n")
    for x in category:
        print("● ", x)

def viewCategoryTasks(id):
    sql_statement = 'SELECT * FROM task WHERE Category_id=%s;'
    to_view = (id)
    create_cursor.execute(sql_statement, (to_view))
    task_rows = create_cursor.fetchall()
    print("=======T A S K S=======\n")
    for x in task_rows:
        print("■ ", x)

def addTaskCategory(id1, id2):
    sql_statement = 'UPDATE task SET Category_id=%s WHERE Task_id=%s;'
    to_add = (id1, id2)
    create_cursor.execute(sql_statement, (to_add))
    mariadb_connection.commit()
    print("Task successfully added to Category %s !" % id1)

def viewTaskSpecificDate(month, day):
    sql_statement = 'SELECT * FROM task WHERE MONTH(Deadline)=%s AND DAY(Deadline)=%s;'
    month_date = (month, day)
    create_cursor.execute(sql_statement, (month_date))
    specified_rows = create_cursor.fetchall()
    print("TASKS DUE ON %s / %s:\n" % month, day)
    counter = 1
    for x in specified_rows:
        print(counter, "-", x)
        counter = counter + 1

print("")

while True:
    menu = """============ M E N U ============
 [0] Add Task \n [1] Edit Task \n [2] Delete Task \n [3] View Task \n [4] Mark Task as Done \n [5] Add Category \n [6] Edit Category \n [7] Delete Category \n [8] View Category \n [9] View Tasks Under Category \n [10] Insert Task to Category \n [11] View Task per day, month \n [12] Exit
================================="""
    print(menu)
    userInput = int(input("Choice: "))

    if(userInput == 0):
        print("ඞ")
    elif(userInput == 4):
        idInput = input("Enter ID of task to mark as done: ")
        markTaskAsDone(idInput)
    elif(userInput == 5):
        genCategoryId = randint(100,999)
        categoryName = input("Enter name of new Category: ")
        addCategory(genCategoryId, categoryName)
    elif(userInput == 6):
        categoryChoice = input("Enter ID of category to be edited: ")
        newCategName = input("Enter New Name for Category %d: " % categoryChoice)  
        editCategory(categoryChoice, newCategName)
    elif(userInput == 7):
        categoryChoice = input("Enter ID of category to be deleted: ")
        deleteCategory(categoryChoice)
    elif(userInput == 8):
        viewCategory()
    elif(userInput == 9):
        categoryChoice = input("Enter ID of the category to view: ")
        viewCategoryTasks(categoryChoice)
    elif(userInput == 10):
        categoryChoice = input("Enter ID of category to be edited: ")
        taskChoice = input("Enter ID of task to be put in the category: ")
        addTaskCategory(categoryChoice, taskChoice)
    elif(userInput == 11):
        monthChoice = input("Enter the month you want to check: ")
        dayChoice = input("Enter the day you want to check: ")
        viewTaskSpecificDate(monthChoice, dayChoice)
    elif(userInput == 12):
        #exit program
        print("Goodbye")
        break
    else:
        print("Invalid Choice. Enter Again.")

#vvv for testing vvv
sql_statement = 'DROP TABLE task'
create_cursor.execute(sql_statement)
mariadb_connection.commit()
sql_statement = 'DROP TABLE category'
create_cursor.execute(sql_statement)
mariadb_connection.commit()
#^^^ for testing ^^^

mariadb_connection.close()
