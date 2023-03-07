#++++++++++++++++++++++++++++++++++
'''
1) FILE FOUNDATION
2) ITEM UPDATE DEFINATIONS
3) SIGN-IN AND SIGN-UP
4) ADMIN
'''
#++++++++++++++++++++++++++++++++++

#=======================================================================================================================
#=================================================FILE FOUNDATIONS===================================================
#=======================================================================================================================
import mysql.connector as mysql
import SECONDARY_DEFINATIONS as sdefn
import numpy as np
import  matplotlib.pyplot as plt
from matplotlib import pyplot as plt

info_array = sdefn.user_info()
IP_project = mysql.connect(host=f'{info_array[0]}',
                               user=f'{info_array[1]}',
                               password=f"{info_array[2]}")
cursor = IP_project.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS IP_project")
cursor.execute("use ip_project")

cursor.execute("CREATE TABLE IF NOT EXISTS itemplot_table (itemid int(3), item_name varchar(20), quantity int(3))")
cursor.execute("CREATE TABLE IF NOT EXISTS user_table (user_id int NOT NULL PRIMARY KEY, name varchar(30),password varchar(30), email_id varchar(30), address VARCHAR(255))")
cursor.execute("CREATE TABLE IF NOT EXISTS item_table (itemid int(3), item_name varchar(20), price float(10,2), itemcategory varchar(30))")
IP_project.commit()

cursor.execute("TRUNCATE TABLE item_table")
cursor.execute("INSERT INTO item_table VALUES(101,'LAPTOP',100,'ELECTRONIC'),(102,'TV',300,'ELECTRONIC'),(103,'MONOPOLY',30,'TOYS'),(104,'BATTLESHIP',35,'TOYS'),(105,'T-SHIRT small',10,'CLOTHING'),(106,'PANTS medium',10,'CLOTHING'),(107,'APPLE 500g',5,'GROCERY'),(108,'6 BANANAS',8,'GROCERY')")
IP_project.commit()

cursor.execute("SELECT email_ID, password FROM user_table WHERE email_ID = 'ADMIN@ADMIN.COM' and password = 'ADMIN123'")
cursor.fetchall()

if cursor.rowcount == 0:
    cursor.execute("INSERT INTO user_table VALUES (000, 'ADMIN', 'ADMIN123', 'ADMIN@ADMIN.COM', 'REDACTED')")
    IP_project.commit()
else:
    pass







#=======================================================================================================================
#===============================================ITEM UPDATE DEFINATIONS=================================================
#=======================================================================================================================
def plot_item():
    cursor.execute('select item_name,quantity from itemplot_table')
    results=cursor.fetchall()
    itemname=[]
    quantity=[]
    for item in results:
        itemname.append(item[0])
        quantity.append(item[1])
    plt.bar(itemname,quantity)
    ylim=(0,5)
    plt.xlabel('item name')
    plt.ylabel('quantity of items bought')
    plt.title('Item Quantity Comparison')
    plt.show()


def insert_item(itemid,itemname,price,itemcategory):
    sql="insert into item_table values(%s,%s,%s,%s)"
    val=(itemid,itemname,price,itemcategory)
    cursor.execute(sql,val)
    IP_project.commit()
    print("NEW ITEM INSERTED")
    cursor.execute(f"select * from item_table order by item_id ASC")
    
    sdefn.print_table(cursor.fetchall(),['Item_ID','Item_Name','Price','Category'])

    input("PRESS ENTER TO CONTINUE")

def delete_item(itemid):
    cursor.execute(f"DELETE FROM item_table WHERE itemid={itemid}")
    IP_project.commit()
    print(f"ITEM WITH ITEM ID {itemid} HAS BEEN DELTED")
    cursor.execute("select * from item_table order by item_id ASC")
    
    sdefn.print_table(cursor.fetchall(),['Item_ID','Item_Name','Price','Category'])

    input("PRESS ENTER TO CONTINUE")

def changeprice_item(itemprice,itemid):
    cursor.execute(f"UPDATE item_table SET price={itemprice} where itemid={itemid}")
    IP_project.commit()
    print("PRICE CHANGED SUCCESFULLY")
    cursor.execute(f"select * from item_table order by item_id ASC ")

    sdefn.print_table(cursor.fetchall(),['Item_ID','Item_Name','Price','Category'])

    input("PRESS ENTER TO CONTINUE")
    
def changecategory_item(itemcategory,itemid):
    cursor.execute(f"UPDATE item_table SET itemcategory='{itemcategory}' where itemid={itemid}")
    IP_project.commit()
    print("CATEGORY CHANGED SUCCESFULLY")
    cursor.execute(f"select * from item_table order by item_id ASC")

    sdefn.print_table(cursor.fetchall(),['Item_ID','Item_Name','Price','Category'])

    input("PRESS ENTER TO CONTINUE")

def changename_item(item_name,itemid):
    cursor.execute(f"UPDATE item_table SET item_name='{item_name}' where itemid={itemid}")
    IP_project.commit()
    print("ITEM NAME CHANGED SUCCESFULLY")
    cursor.execute(f"select * from item_table order by item_id ASC ")

    sdefn.print_table(cursor.fetchall(),['Item_ID','Item_Name','Price','Category'])

    input("PRESS ENTER TO CONTINUE")








    
#=======================================================================================================================
#===============================================SIGNIN AND SIGNUP=================================================
#=======================================================================================================================
def SignIn(): 
    signin = False
    while not signin:
        signin_email = str(input("----Email: ".upper()))
        signin_password = str(input("----Password: ".upper()))
        cursor.execute("SELECT user_id,email_id,password,name FROM user_table WHERE email_id = %s and password=%s",(signin_email,signin_password))
        results = cursor.fetchall()
        row_count = cursor.rowcount
        if row_count==0:
            print("***unrecognized email or password***".upper())
            return '0'
        else:
            signin=True
            print(f'Welcome {results[0][3].capitalize()} to COHERENT DIGITAL SHOPPING INTERFACE'.upper())
            return [signin_email,signin_password]
                                                 
def SignUp(userid):
    signup_name = str(input("----Set Name: ".upper()))#main name

    correct_signup=False
    while not correct_signup:
        #----------------to check email is valid or not
        email_unique = False
        while not email_unique:
            signup_user_email = str(input("----Set Email ID: ".upper()))#main email
            find_com=signup_user_email.find(".com") 
            find_A=signup_user_email.find('@')

            if find_com==-1 or find_A==-1:
                print("***Invalid Email ID, Please Make Sure Your Email Has '@' and '.com'***".upper())
            elif (signup_user_email=="ADMIN@ADMIN.COM" or signup_user_email=="admin@admin.com") :
                print("***Invalid Email ID, This Email Cannot Be Used ***".upper())
                
            else:
                correct_signup=True

                
            #----------------checks whether email is unique or not
                cursor.execute(f"SELECT email_id FROM user_table WHERE email_id= '{signup_user_email}'")
                results = cursor.fetchall()
                row_count = cursor.rowcount

                if row_count==0: #means the email is unique
                    
                    email_unique = True
                    #-------------checks if passwd and confirm passwd are equal
                    p1_equal_p2= False
                    while not p1_equal_p2:
                        Invalidpass=True
                        while Invalidpass:
                            passwd1 = str(input("----Set Password: ".upper()))
                            if len(passwd1)>30:
                                print("***Invalid Password, Password Length Should Be Less Than 30 Characters***".upper())
                            else:
                                Invalidpass=False
                        passwd2 = str(input("----Confirm Password: ".upper()))
                        if passwd1 == passwd2:
                            signup_passwd = passwd1#main passwd
                            signup_user_address = str(input("----Set Address: ".upper()))#main address
                            break
                        else:
                            print('***Passwords DO NOT Match***'.upper())
                            p1_equal_p2 = False
                            
                    #--------------inserts the signup values into mysql
                    sql = f"INSERT INTO user_table (user_id,name,password,email_id,address) VALUES (%s,%s,%s,%s,%s)"
                    val =(userid, signup_name,signup_passwd,signup_user_email,signup_user_address)
                    cursor.execute(sql, val)
                    IP_project.commit()
                    print('****=Your Account Has Been Created Successfully=****'.upper())
                    input("PRESS ENTER TO CONTINUE")
                    
                else: #means email is not unique
                    print("***This Email ID Already Exists, Please Try Again***".upper())
                    print("***PLEASE SIGN-IN OR USE ANOTHER EMAIL***")
                    input("PRESS ENTER TO CONTINUE")
                    email_unique = True

def get_user_id(email,password):
    cursor.execute("SELECT user_id FROM user_table WHERE email_id = %s and password=%s",(email,password))
    userid = cursor.fetchone()
    return userid







                    
#=======================================================================================================================
#=================================================ADMIN================================================================
#=======================================================================================================================

def Admin():
    quit_admin=False
    while not quit_admin:
        print("""
**********************************************ADMIN OPTIONS***********************************
    1)ENTER NEW ITEM
    2)DELETE OLD ITEM
    3)CHANGE PRICE
    4)CHANGE CATEGORY
    5)CHANGE NAME
    6)GRAPH
    
    7)EXIT
    """)

    ##OPTION INPUT************************************************************
        admin_choice=int(input("----ENTER OPTION: "))
            
    ## INSERT ITEM*************************************************************
        if admin_choice==1:
            cursor.execute(f"select * from item_table order by item_id ASC ")
            sdefn.print_table(cursor.fetchall(),['Item_ID','Item_Name','Price','Category'])
            insert_item_exists=False
            while not insert_item_exists:
                itemid=int(input("ENTER ID: "))
                cursor.execute(f"select * from item_table where itemid={itemid}")
                results = cursor.fetchall()
                row_count = cursor.rowcount
                if row_count==0:
                    itemname=input("ENTER NAME: ")
                    invalidprice=True
                    while invalidprice:
                        price=float(input("ENTER PRICE: "))
                        if price<0:
                            print("***Invalid Price***")
                        else:
                            invalidprice=False
                    invalidcat=True
                    while invalidcat:
                        cat=['ELECTRONIC',"TOYS","CLOTHING","GROCERY"]
                        itemcategory=input('''
Categories Available: Electronic, Toys, Clothing, Grocery
ENTER CATEGORY: '''.upper())
                        if itemcategory.upper() not in cat:
                            print("***INVALID CATEGORY......Categories Available: Electronic, Toys, Clothing, Grocery***".upper())
                        else:
                            invalidcat=False
                        
                    insert_item(itemid,itemname,price,itemcategory)
                    insert_item_exists=True
                else:
                    print("***ITEM ID ALREADY EXSISTS***")

    ##DELETE ITEM***************************************************************
        elif admin_choice==2:
            cursor.execute("select * from item_table order by item_id ASC")
            results = cursor.fetchall()
            if cursor.rowcount == 0:
                print("***THERE ARE NO ITEMS***")
            else:
                sdefn.print_table(results,['Item_ID','Item_Name','Price','Category'])
                delete_item_exists=True
                while delete_item_exists:
                    itemid=int(input("ENTER ITEM ID: "))
                    cursor.execute(f"select * from item_table where itemid={itemid}")
                    cursor.fetchall()
                    row_count = cursor.rowcount
                    if row_count==0:
                        print("***ITEM ID DOES NOT EXIST***")
                    else:
                        delete_item(itemid)
                        delete_item_exists=False


    ## CHANGE PRICE OF ITEM***************************************************
        elif admin_choice==3:
            cursor.execute("select * from item_table order by item_id ASC")
            results = cursor.fetchall()
            if cursor.rowcount == 0:
                print("***THERE ARE NO ITEMS***")
            else:
                sdefn.print_table(results,['Item_ID','Item_Name','Price','Category'])
                price_change_item_exists=True
                while price_change_item_exists:
                    itemid=int(input("ENTER ITEM ID: "))
                    cursor.execute(f"select * from item_table where itemid={itemid}")
                    cursor.fetchall()
                    row_count = cursor.rowcount
                    if row_count==0:
                        print("***ITEM ID DOES NOT EXIST***")
                    else:
                        itemprice=float(input("ENTER NEW PRICE: "))
                        changeprice_item(itemprice,itemid)
                        price_change_item_exists = False
    ##CHANGE CATEGORY*********************************************************
        elif admin_choice==4:
            cursor.execute("select * from item_table order by item_id ASC")
            results = cursor.fetchall()
            if cursor.rowcount == 0:
                print("***THERE ARE NO ITEMS***")
            else:
                sdefn.print_table(results,['Item_ID','Item_Name','Price','Category'])
                change_cat_item_exists=True
                while change_cat_item_exists:
                    itemid=int(input("ENTER ITEM ID: "))
                    cursor.execute(f"select * from item_table where itemid={itemid}")
                    cursor.fetchall()
                    row_count = cursor.rowcount
                    if row_count==0:
                        print("***ITEM ID DOES NOT EXIST***")
                    else:
                        invalidcat=True
                        while invalidcat:
                            cat=['ELECTRONIC',"TOYS","CLOTHING","GROCERY"]
                            itemcategory=input('''
Categories Available: Electronic, Toys, Clothing, Grocery
ENTER CATEGORY: '''.upper())
                            if itemcategory.upper() not in cat:
                                print("***INVALID CATEGORY......Categories Available: Electronic, Toys, Clothing, Grocery***".upper())
                            else:
                                invalidcat=False
                        changecategory_item(itemcategory,itemid)
                        change_cat_item_exists=False

    ##CHANGE NAME*****************************************************************
        elif admin_choice==5:
            cursor.execute("select * from item_table order by item_id ASC")
            results = cursor.fetchall()
            if cursor.rowcount == 0:
                print("***THERE ARE NO ITEMS***")
            else:
                sdefn.print_table(results,['Item_ID','Item_Name','Price','Category'])
                change_name_item_exists=True
                while change_name_item_exists:
                    itemid=int(input("ENTER ITEM ID: "))
                    cursor.execute(f"select * from item_table where itemid={itemid}")
                    cursor.fetchall()
                    row_count = cursor.rowcount
                    if row_count==0:
                        print("***ITEM ID DOES NOT EXIST***")
                    else:
                        item_name=input("ENTER NEW NAME: ")
                        changename_item(item_name,itemid)
                        change_name_item_exists=False
    ##GRAPH*********************************************************************************
        elif admin_choice==6:
            plot_item()

    ## EXIT***********************************************************************************
        elif admin_choice==7:
            print("***************************THANK YOU*************************************")
            quit_admin = True
                    
    ## INVALID OPTION***********************************************************************
        elif admin_choice>7 or admin_choice<=0:
            print("***INVALID OPTION***")        
