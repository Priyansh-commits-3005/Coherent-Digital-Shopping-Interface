#=======================================================================================================================
#===============================================FILE FOUNDATIONS=================================================
#=======================================================================================================================

import mysql.connector as mysql
import SECONDARY_DEFINATIONS as sdefn

info_array = sdefn.user_info()
IP_project = mysql.connect(host=f'{info_array[0]}',
                               user=f'{info_array[1]}',
                               password=f"{info_array[2]}")
cursor = IP_project.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS IP_project")
cursor.execute("use ip_project")

cursor.execute("CREATE TABLE IF NOT EXISTS cart_table(itemid int(3),itemname varchar(20),price float(10,2),quantity int(3),totalprice float(100,2))")
IP_project.commit()
cursor.execute("TRUNCATE TABLE cart_table")
IP_project.commit()

#=======================================================================================================================
#===============================================CART DEFINATIONS=================================================
#=======================================================================================================================

def view_cart():
    cursor.execute("select * from cart_table")        
    sdefn.print_table(cursor.fetchall(),["Itemid","ItemName","Price","Quantity","TotalPrice"])


def delete_cartitem(itemid,itemq,orginal_quantity):
    newquantity=orginal_quantity-itemq
    cursor.execute(f"SELECT price FROM cart_table WHERE itemid={itemid}")
    price=cursor.fetchone()[0]
    totalprice=price*newquantity
    sql="update cart_table set quantity=%s,totalprice=%s where itemid=%s"
    val=(newquantity,totalprice,itemid)
    cursor.execute(sql,val)
    IP_project.commit()


def add_product_to_cart(itemid,itemquantity): #ADD IN CART IF ALREADY NOT IN CART
    cursor.execute(f"select price from item_table where itemid={itemid}")
    item_price=cursor.fetchall()[0][0]
    totalprice=item_price*itemquantity
    cursor.execute(f"select item_name from item_table where itemid={itemid}")
    item_name=cursor.fetchall()[0][0]
    sql="insert into cart_table values(%s,%s,%s,%s,%s)"
    val=(itemid,item_name,item_price,itemquantity,totalprice)
    cursor.execute(sql,val)
    IP_project.commit()
    print("***ITEM ADDED TO CART SUCCESFULLY***")


def update_product_in_cart(itemid): #UPDATE IN CART IF ALREADY IN CART
    print("***THIS ITEM ALREADY EXISTS IN YOUR CART, ENTER NEW QUANTITY***")
    cursor.execute(f"select quantity from cart_table where itemid={itemid}")
    q=cursor.fetchone()[0]
    
    qinput=int(input("ENTER NEW QUANTITY:"))
    item_quantity=qinput
    sql="update cart_table set quantity=%s where itemid=%s"
    val=(item_quantity,itemid)
    cursor.execute(sql,val)
    IP_project.commit()
    cursor.execute(f"select price from item_table where itemid={itemid}")
    price=cursor.fetchall()[0][0]
    totalprice=item_quantity*price
    sql="update cart_table set totalprice=%s where itemid=%s"
    val=(totalprice,itemid)
    cursor.execute(sql,val)
    IP_project.commit()
    print("***ITEM ADDED TO CART SUCCESFULLY***")


def put_in_cart(): #(WHICH ITEM TO SELECT) AND (CORRECT QUANTITY OR NOT)
    in_category=True
    while in_category:
            itemid=int(input("ENTER ID: "))
            
            cursor.execute(f"select * from cart_table where itemid={itemid}")
            cursor.fetchall()
            row_count = cursor.rowcount
            
            if row_count==0:
                cursor.execute(f"select * from item_table where itemid={itemid}")
                cursor.fetchall()
                row_count = cursor.rowcount
                if row_count==0:
                    print("***ITEM ID DOES NOT EXIST***")
                else:
                    in_category=False
                    
                    correct_quantity=False
                    while not correct_quantity:
                        item_quntity=int(input("ENTER QUANTITY: "))
                        if item_quntity<0:
                            print("***INVALID QUANTITY***")
                        elif item_quntity==0:
                            print("***ITEM WAS NOT ADDED TO CART***")
                        else:
                            correct_quantity=True
                            add_product_to_cart(itemid,item_quntity)
                
            else:
                in_category=False
                update_product_in_cart(itemid)

def put_in_itemplot():
    cursor.execute("SELECT itemid FROM itemplot_table")
    item_plot_results = cursor.fetchall()
    cursor.execute("SELECT itemid FROM cart_table")
    item_cart_results = cursor.fetchall()
    for itemid in item_cart_results:
        if itemid not in item_plot_results:
            cursor.execute(f"SELECT itemname, quantity FROM cart_table WHERE itemid = {itemid[0]}")
            item_tuple = cursor.fetchall()
            for item_array in item_tuple:
                itemname= item_array[0]
                itemquantity= item_array[1]
                cursor.execute(f"INSERT INTO itemplot_table VALUES({itemid[0]}, '{itemname}' ,{itemquantity})")
                IP_project.commit()
                
        else:
            cursor.execute(f"SELECT quantity FROM cart_table WHERE itemid = {itemid[0]}")
            item_quantity1 = cursor.fetchone()
            cursor.execute(f"SELECT quantity FROM itemplot_table WHERE itemid = {itemid[0]}")
            item_quantity2 = cursor.fetchone()
            item_quantity_main = item_quantity1[0] + item_quantity2[0]
            cursor.execute(f"UPDATE itemplot_table SET quantity = {item_quantity_main} WHERE itemid={itemid[0]}")
            IP_project.commit()






#=======================================================================================================================
#==================================================MAIN-MENU=======================================================
#=======================================================================================================================


def Main_Menu(userid_fromtable):
    return_to_mainmenu=True
    while return_to_mainmenu:
        print("""********************************************MAIN-MENU********************************************
    1)SHOP
    2)VIEW CART
    3)CHECKOUT
    """)
        user_input_main=int(input("----ENTER OPTION: "))

#----------------------------
#=======================================SHOP===========================================
#----------------------------
        
        if user_input_main==1:
            user_wants_to_shop=True
            while user_wants_to_shop:
                print("""********************************SHOPPING**************************
SELECT CATEGORY
1) ELECTRONIC
2) GROCERY
3) TOYS
4) CLOTHING

5)ALL ITEMS

6) EXIT SHOPPING
""")
                user_cart_input=int(input("----CHOOSE CATEGORY: "))

                table_headings = ['Item_ID','Item_Name','Price','Category']

                #---------ELECTRONICS---------
                if user_cart_input==1:
                    cursor.execute("select * from item_table where itemcategory='electronic'")
                    fetched_rows = cursor.fetchall()
                    sdefn.print_table(fetched_rows,table_headings)
                    print('''
PRESS 1- ADD AN ITEM TO CART
PRESS 2- RETURN''')
                    inp = str(input(':'))
                    if inp == '1':
                        if cursor.rowcount == 0:
                            print('***THIS CATEGORY DOES NOT CONTAIN ANY ITEM, ASK ADMIN TO ENTER ITEMS***')
                            input('PRESS ENTER TO CONTINUE')
                        else:
                            put_in_cart()
                            input('PRESS ENTER TO CONTINUE')
                    else:
                        pass

                #---------GROCERY---------
                elif user_cart_input==2:
                    cursor.execute(f"select * from item_table where itemcategory='grocery'")
                    fetched_rows = cursor.fetchall()
                    sdefn.print_table(fetched_rows ,table_headings)
                    print('''
PRESS 1- ADD AN ITEM TO CART
PRESS 2- RETURN''')
                    inp = str(input(':'))
                    if inp == '1':
                        if cursor.rowcount == 0:
                            print('***THIS CATEGORY DOES NOT CONTAIN ANY ITEM, ASK ADMIN TO ENTER ITEMS***')
                            input('PRESS ENTER TO CONTINUE')
                        else:
                            put_in_cart()
                            input('PRESS ENTER TO CONTINUE')
                    else:
                        pass

                #---------TOYS---------
                elif user_cart_input==3:
                    cursor.execute(f"select * from item_table where itemcategory='toys'")
                    fetched_rows = cursor.fetchall()
                    sdefn.print_table(fetched_rows,table_headings)
                    print('''
PRESS 1- ADD AN ITEM TO CART
PRESS 2- RETURN''')
                    inp = str(input(':'))
                    if inp == '1':
                        if cursor.rowcount == 0:
                            print('***THIS CATEGORY DOES NOT CONTAIN ANY ITEM, ASK ADMIN TO ENTER ITEMS***')
                            input('PRESS ENTER TO CONTINUE')
                        else:
                            put_in_cart()
                            input('PRESS ENTER TO CONTINUE')
                    else:
                        pass

                #---------CLOTHING---------
                elif user_cart_input==4:
                    cursor.execute(f"select * from item_table where itemcategory='clothing'")
                    fetched_rows = cursor.fetchall()
                    sdefn.print_table(fetched_rows,table_headings)
                    print('''
PRESS 1- ADD AN ITEM TO CART
PRESS 2- RETURN''')
                    inp = str(input(':'))
                    if inp == '1':
                        if cursor.rowcount == 0:
                            print('***THIS CATEGORY DOES NOT CONTAIN ANY ITEM, ASK ADMIN TO ENTER ITEMS***')
                            input('PRESS ENTER TO CONTINUE')
                        else:
                            put_in_cart()
                            input('PRESS ENTER TO CONTINUE')
                    else:
                        pass
                        
                #---------ALL ITEMS---------
                elif user_cart_input==5:
                    cursor.execute(f"select * from item_table")
                    fetched_rows = cursor.fetchall()
                    sdefn.print_table(fetched_rows,table_headings)
                    print('''
PRESS 1- ADD AN ITEM TO CART
PRESS 2- RETURN''')
                    inp = str(input(':'))
                    if inp == '1':
                        if cursor.rowcount == 0:
                            print('***NO ITEMS EXIST, ASK ADMIN TO ENTER ITEMS***')
                            input('PRESS ENTER TO CONTINUE')
                        else:
                            put_in_cart()
                            input('PRESS ENTER TO CONTINUE')
                    else:
                        pass

                #---------EXIT---------
                elif user_cart_input==6:
                    user_wants_to_shop=False

                #---------INVALID CATEGORY---------
                elif user_cart_input>6 or user_cart_input<=0:
                    print('***INVALID CATEGORY***')
                    input('PLEASE ENTER THE CORRECT NUMBER CODE GIVEN TO EACH HEADINGS(PRESS ENTER)')

                else:
                    print('***INVALID ENTRY***')
                    input('PLEASE ENTER THE CORRECT NUMBER CODE GIVEN TO EACH HEADINGS(PRESS ENTER)')











#----------------------------
#=======================================VIEW-CART===========================================
#----------------------------

        elif user_input_main==2:
            print("""********************************************CART********************************************""")
            
            return_to_menu=False
            while not return_to_menu:
                view_cart()            
                cursor.execute("select sum(totalprice) from cart_table")
                totalcost=cursor.fetchall()[0][0]
                print("GRAND TOTAL: ",totalcost)
                
                print("""
    1)DELETE ITEM
    2)RETURN
        """)
                viewcart_user_choice=int(input("----ENTER OPTION: "))

                #---------DELETE-ITEM-------
                if viewcart_user_choice==1:
                    cursor.execute('select * from cart_table')
                    cursor.fetchall()

                    if cursor.rowcount == 0:
                        print("***THERE ARE NO ITEMS IN YOUR CART***")
                        A= input('PRESS ENTER TO CONTINUE')
                    else: #ITEMS ARE IN CART
                        itemid_correct=True
                        while itemid_correct:
                            itemid=int(input("ENTER ID: "))
                            cursor.execute(f"select * from cart_table where itemid={itemid}")
                            results = cursor.fetchall()
                            row_count = cursor.rowcount
                            
                            if row_count==0: 
                                print("***ITEM ID DOES NOT EXIST***")
                            else: #ITEM ID EXISTS IN CART
                                itemquantitycorrect=True
                                while itemquantitycorrect:#CORRECT QUANTITY OR NOT
                                    
                                    itemquantity=int(input("ENTER QUANTITY: "))
                                    cursor.execute(f"SELECT quantity FROM cart_table WHERE itemid={itemid}")
                                    item_quantity_of_table=cursor.fetchone()[0]
                                    if itemquantity<0 or itemquantity>item_quantity_of_table:
                                        print("***INVALID QUANTITY***")
                                        print('-----------------------------------------------------------------------------------')
                                    elif itemquantity == 0:
                                        print("***NO ITEMS WERE REMOVED FROM YOUR CART***")
                                        itemquantitycorrect=False
                                        print('-----------------------------------------------------------------------------------')
                                    elif itemquantity==item_quantity_of_table:
                                        cursor.execute(f"delete from cart_table where itemid={itemid}")
                                        IP_project.commit()
                                        print("***ITEM DELETED SUCCESFULLY***")
                                        input('PRESS ENTER TO CONTINUE')
                                        itemid_correct = False
                                        itemquantitycorrect=False
                                        return_to_menu = False
                                        print('-----------------------------------------------------------------------------------')
    
                                    else:
                                        itemquantitycorrect=False
                                        delete_cartitem(itemid,int(itemquantity),int(item_quantity_of_table))
                                        itemid_correct = False
                                        print('-----------------------------------------------------------------------------------')
                                    
                #---------RETURN------------
                elif viewcart_user_choice==2:
                    return_to_menu=True
                else:
                    pass









#----------------------------
#=====================================================CHECKOUT=========================================================
#----------------------------
        elif user_input_main==3:
            #input into item_plot table for graph
            put_in_itemplot()

            #the checkout screen
            print("**********************************CHECKOUT**********************************")

            cursor.execute("select * from cart_table")
            sdefn.print_table(cursor.fetchall(),["Itemid","Itemname","Price","Quantity","Totalprice"])
            cursor.execute("select sum(totalprice) from cart_table")
            totalcost=cursor.fetchall()[0][0]
            print(f"GRAND TOTAL: {totalcost}\n")
            print('''
PRESS 1- CONTINUE
PRESS 2- RETURN''')
            continue_or_not = str(input("ENTER YOUR CHOICE: "))

            if continue_or_not == '2':
                pass
            elif continue_or_not == '':
                pass

            elif continue_or_not == '1':
                print("========================================================================")
                review_checkout=True
                while review_checkout:
                    cursor.execute(f"SELECT address FROM user_table WHERE user_id = {userid_fromtable}")
                    resultadrs=cursor.fetchone()

                    print(f'''This is the registered address:  {resultadrs[0]}

Do you want to change the delivery address
     Press 1- To change the delivery address
     Press 2- To proceed with the aforementioned delivery address\n'''.upper())
                    user_adrschnginput=int(input("Enter your choice for the substituition of the delivery address: ".upper()))
                    if user_adrschnginput==1:
                        newadrs=input("Enter The New Delivery Address: ".upper())## newadrs- new address enetered by user
                        newadrs2 = str(newadrs)
                        cursor.execute(f"UPDATE user_table SET address='{newadrs}' WHERE user_id = {userid_fromtable}")
                        print("The delivery address has been changed successfully".upper())
                    elif user_adrschnginput==2:
                        pass
                    else:
                        print("*** INVALID INPUT ***")
                        input("PRESS ENTER TO CONTINUE")
                    print("========================================================================")
                    cursor.execute(f"SELECT address FROM user_table WHERE user_id = {userid_fromtable}")
                    final_adress_main=cursor.fetchone()
                    print(f"This is the current delivery address: {final_adress_main[0]}".upper())

                    print('''
PLEASE CHOOSE A MODE OF PAYMENT:
     PRESS 1-------------- CASH ON DELIVERY
     PRESS 2-------------- DOORSTEP CREDIT/DEBIT CARD PAYMENT MODE\n''')

                    correct_payment_mode = False
                    while not correct_payment_mode:
                        mode_of_payment=int(input("Enter The Preferred Mode Of Payment: ".upper()))
                        if mode_of_payment==1:
                            payms="Cash"
                            correct_payment_mode = True
                        elif mode_of_payment==2:
                            payms="Credit/Debit Card"
                            correct_payment_mode = True
                        else:
                            print("*** INVALID INPUT ***")
                        ## payms- message to be displayed for mode of payment
                    print("========================================================================")

                    proceed_input=int(input('''
Do you want to proceed to Order Bill Payment
    Press 1- to proceed further
    Press 2- to review window again

----Enter choice: '''.upper()))## loop to review the window again as per choice of the user
                    if proceed_input==2:
                        pass
                    elif proceed_input==1:
                        review_checkout=False
                        print("========================================================================")
                    else:
                        print("*** INVALID INPUT ***")
                        input("PRESS ENTER TO CONTINUE")

                print(f'''*******************ORDER SUMMARY********************''')
                cursor.execute("select * from cart_table")
                sdefn.print_table(cursor.fetchall(),["Itemid","Itemname","Price","Quantity","Totalprice"])
                cursor.execute("select sum(totalprice) from cart_table")
                totalcost=cursor.fetchall()[0][0]
                
                print(f'''
DELIVERY ADDRESS: {final_adress_main[0]}
MODE OF PAYMENT: {payms}
ESTIMATED DATE OF DELIVERY: The order will be delivered within 3 days
== GRAND TOTAL: {totalcost}'''.upper())

                order_placed = False
                while not order_placed:
                    userorder_input=int(input('''
Press 1 - to place your order
Press 2 - to cancel your order:
ENTER OPTION: '''.upper()))
                    if userorder_input==1:
                        print("Your Order Has Been Placed Successfully".upper())
                        order_placed = True
                        return_to_mainmenu = False
                        cursor.execute("TRUNCATE TABLE cart_table")
                        IP_project.commit()
                        
                    elif userorder_input==2:
                        print("YOUR ORDER HAS BEEN CANCELLED")

                    else:
                        print("*** INVALID INPUT ***")
                        input("PRESS ENTER TO CONTINUE")

