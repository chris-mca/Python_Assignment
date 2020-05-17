import sqlite3 # For communicating with DB
from sys import exit # Exit For Terminating execution 
from getpass import getpass # Hiding password from console input
from datetime import date # To fetch Date


# Since user has the rights to terminate transaction so we asking for string input instead of int only input

# Getting Current Date in the format of 17-05-2020
today = date.today()
today = today.strftime("%d-%m-%Y")

#Database connection using exact path
database_path = r'D:\Python Projects\SQLiteDB\ATM_Machine.db'
dbConnect = sqlite3.connect(database=database_path)
dbCursor = dbConnect.cursor()

#Queries used in the below operations
validate_query = "SELECT * FROM CUSTOMER_INFORMATION WHERE ID = {id} AND PASSWORD = '{pw}';"
daylimit_query = "SELECT sum(transaction_amount) FROM TRANSACTIONS WHERE account_number = '{ac}' AND transaction_date = '{date}' AND transaction_type ='withdrawal';"
trans_log_query = "INSERT INTO TRANSACTIONS VALUES('{v1}','{v2}',{v3},'{v4}','{v5}');"
update_bal_query = "UPDATE CUSTOMER_INFORMATION SET ACCOUNT_BALANCE = {v1} WHERE ACCOUNT_NUMBER ='{v2}'" 

#Terminating program by using exit() method in sys
def isExit(strArgu="none"):
    if strArgu.lower() == "cancel":
        print("Your Last Transaction Canceled !!!")
        exit("Thanks for choosing us !!!")
        return False
    elif strArgu.lower() == "invalid":
        print("Too many Invalid Credentials. Please try again letter...")
        exit("Thanks for choosing us !!!")
        return False
    elif strArgu.lower() == "exit":
        exit("Thanks for choosing us !!!")
    else:
        return True



# Getting customer ID and Validating with isnumeric()
def getCustomerID():
    cust_id = input("Please Enter Your Customer ID : ")
    isExit(cust_id)  #IF entered string is cancel then Exit
    while cust_id.isnumeric() == False:
        cust_id = input("Please Enter Your Valid Customer ID : ")
        isExit(cust_id)   #IF entered string is cancel then Exit
    return cust_id

# Getting Password from the user. Since it was sencitive info we hiding it by getpass()
def getPassword():
    get_pass = getpass("Please Enter Your Password To Proceed Futher : ")
    isExit(get_pass)  #IF entered string is cancel then Exit
    return get_pass   

def authenticateUser():
    customer_id = getCustomerID()
    customer_pw = getPassword()
    dbCursor.execute(validate_query.format(id=customer_id,pw=customer_pw))
    return dbCursor
    
def getTodayLimit(customer_ac_num):
    # print(daylimit_query.format(ac=customer_ac_num,date=today))
    count= dbCursor.execute(daylimit_query.format(ac=customer_ac_num,date=today))
    today_amount = 0
    for i in count:
        today_amount = i[0]
    if today_amount is None:
        today_amount = 0
    return int(today_amount)
    


def withdrawal(customer_id,customer_ac_num,customer_ac_bal):
    today_amount = getTodayLimit(customer_ac_num)

    if today_amount >= 30000:
        print("You have Already Reached Daily Transaction Limit. Please visit Nearest Bank...!!!")
        isExit("exit")
    trans_amount = input("Please Enter the amount to Withdraw : ")
    isExit(trans_amount)  #IF entered string is cancel then Exit
    while trans_amount.isnumeric() == False:
        trans_amount = input("Please Enter the valid amount to Withdraw : ")
        isExit(trans_amount)  #IF entered string is cancel then Exit
    trans_amount = int(trans_amount)
    today_amount = int(today_amount)
    
    trans_amount = checkTodayAvailabe(trans_amount,today_amount,int(customer_ac_bal))
    return trans_amount

def outOfbalance(customer_ac_bal,trans_amount):
    if int(customer_ac_bal) < int(trans_amount):
        return True
    else:
        return False

def checkTodayAvailabe(trans_amount,today_amount,customer_ac_bal):
    while trans_amount + today_amount > 30000 :
        print("Sorry You Cannot Withdraw More than INR 30000 per DAY")
        print(f"Today you have already Withdrawn INR {today_amount}")
        trans_amount = input("Please Enter the valid amount to Withdraw : ")
        isExit(trans_amount)  #IF entered string is cancel then Exit
        while trans_amount.isnumeric() == False:
            trans_amount = input("Please Enter the valid amount to Withdraw : ")
            isExit(trans_amount)  #IF entered string is cancel then Exit
        trans_amount = int(trans_amount)
    return trans_amount

def credit_to_DB(customer_ac_num,credit_amount,customer_ac_bal):
    
    v1=int(customer_ac_bal)+int(credit_amount)
    dbCursor.execute(update_bal_query.format(v1=v1,v2=customer_ac_num))
    dbConnect.commit()
    return v1

def debit_from_DB(customer_ac_num,current_trans_amount,customer_ac_bal):
    v1=int(customer_ac_bal)-int(current_trans_amount)
    dbCursor.execute(update_bal_query.format(v1=v1,v2=customer_ac_num))
    dbConnect.commit()
    return v1

def logToTransactionDB(customer_ac_num,trans_type,current_trans_amount,pan_number,today):

    dbCursor.execute(trans_log_query.format(v1=customer_ac_num,
                                            v2=trans_type,
                                            v3=current_trans_amount,
                                            v4=pan_number,
                                            v5=today))
    dbConnect.commit()
    return True

#################################

### EXECUTION OF THE PROGRAM ####

#################################


print("#################################")
print("")
print(f"Date : {today}")
print("")
print("#################################")

print("We happy to Serve You!!!")
print("At any point if you want to close the transacion just enter 'cancel'")

cursor = authenticateUser()
result = cursor.fetchall()

customer_id = 0
customer_name = customer_pass = customer_ac_num = customer_ac_bal =""
i = 0
while i <= 2:  
    for customer_details in result:
        customer_id = customer_details[0]
        customer_name = customer_details[1]
        customer_pass = customer_details[2]
        customer_ac_num = customer_details[5]
        customer_ac_bal = customer_details[6]
    if customer_id != 0:
        break        
    else:
        print("Customer ID or Password is incorrect, Please try again")
        authenticatedUser = authenticateUser()
        result = authenticatedUser.fetchall()
        i += 1
if customer_id == 0: # IF user entering wrong password more than 2 times Terminates the transaction
    isExit("Invalid")  

print("#################################")
print("")
print("*****Greetings*****")
print("")
print("#################################")
print("")

print("We happy to welcome you ",customer_name)
print("Your Current Balance is : INR ",customer_ac_bal)

print("Please Enter Your Transaction Type : ")
print("     You can Enter 1 or 'Credit' to Credit amount to your Account")
print("     You can Enter 2 or 'Withdrawal' to Withdraw amount from your Account")

trans_type = input("Please Enter : ")
isExit(trans_type)  #IF entered string is cancel then Exit

pan_number=""
if(trans_type=="1" or trans_type.lower()=="credit"):
    trans_type="credit"
    credit_amount = input("Please Enter Amount To Creadit : ")
    isExit(credit_amount)  #IF entered string is cancel then Exit
    while credit_amount.isnumeric() == False:
        credit_amount = input("Please Enter the valid amount to Credit : ")
        isExit(credit_amount)  #IF entered string is cancel then Exit
    v1 = credit_to_DB(customer_ac_num,credit_amount,customer_ac_bal)
    print("CASH credited to your account.....!!!")
    print(f"Current Balance in your Account is INR {v1}")
    logToTransactionDB(customer_ac_num,trans_type,credit_amount,pan_number,today)
elif (trans_type=="2" or trans_type.lower()=="withdrawal"):
    trans_type="withdrawal"
    current_trans_amount = withdrawal(customer_id,customer_ac_num,customer_ac_bal)
    if(current_trans_amount >= 20000):
        pan_number = input("Please Enter PAN number to complete the transaction : ")
        isExit(pan_number)  #IF entered string is cancel then Exit
        while pan_number is None:
            pan_number = input("Please Enter PAN number to complete the transaction : ")
            isExit(pan_number)  #IF entered string is cancel then Exit
    if outOfbalance(customer_ac_bal,current_trans_amount) == True:
        Print("Insufficient Balance In Your Account")
    else:
        v1 = debit_from_DB(customer_ac_num,current_trans_amount,customer_ac_bal)

        print("Please Collect your CASH.....!!!")
        print(f"Remaining Balance in your Account is INR {v1}")
        logToTransactionDB(customer_ac_num,trans_type,current_trans_amount,pan_number,today)

