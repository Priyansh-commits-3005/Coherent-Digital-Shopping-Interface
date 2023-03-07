#=======================================================================================================================
#===============================================FILE FOUNDATIONS=================================================
#=======================================================================================================================
import BACKBONE_DEFINATIONS as defn
import SECONDARY_DEFINATIONS as sdefn
import mysql.connector as mysql
import MAIN_MENU as menu

info_array = sdefn.user_info()
IP_project = mysql.connect(host=f'{info_array[0]}',
                               user=f'{info_array[1]}',
                               password=f"{info_array[2]}")
cursor = IP_project.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS IP_project")
cursor.execute("use ip_project")

#TITLE NAME

#=======================================================================================================================
#===============================================START UP=================================================
#=======================================================================================================================

restart_program = True
while restart_program:
    print('''*****************COHERENT DIGITAL SHOPPING INTERFACE******************
Sign-in(press 1)                            Sign-up(press 2)                 Exit(press 3)''')

    startup_input=str(input('''                                            Enter the code: '''))


    signup_required = True
    wrong_signins = 0
    while signup_required:
        if startup_input == '1': #login 
            print('------------------LOGIN-----------------')
            signin_array = defn.SignIn()
            if signin_array[0] == 'ADMIN@ADMIN.COM' and signin_array[1] == 'ADMIN123':
                defn.Admin()
                restart_program = True
                signup_required=False
                
            elif signin_array == '0':
                wrong_signins += 1
                if wrong_signins == 3:
                    signup_required = False
                    print("***PLEASE SIGN-UP IF YOU DONT HAVE AN ACCOUNT***")
                    input("PRESS ENTER TO CONTINUE")
            else:
                userid = defn.get_user_id(signin_array[0],signin_array[1])
                signup_required=False
                restart_program = False
                menu.Main_Menu(userid[0])
                
        elif startup_input == '2': #signup
            print('------------------SIGNUP------------------')

            cursor.execute("SELECT * FROM user_table ORDER BY user_id DESC")
            userid=cursor.fetchall()
            last_id = userid[0][0]
            new_id = last_id + 1
            
            defn.SignUp(new_id)
            signup_required = False
            
        elif startup_input=='3':
            signup_required=False
            restart_program = False
            exit()

