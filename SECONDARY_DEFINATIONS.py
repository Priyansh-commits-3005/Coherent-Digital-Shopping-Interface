#+++++++++++++++PLEASE ENTER THE MYSQL DETAILS+++++++++++++++++
host='localhost'
user='root'
password='mysql'
#try to input these
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
from prettytable import PrettyTable as PT

def user_info():
    return [host,user,password]

def print_table(tuple_array, fieldname_array):
    table = PT()
    table.field_names = fieldname_array
    for items in tuple_array:
        table.add_row(items)
    print(table)

