from datetime import datetime
class ATM:        
    def Dis(self,users):
        
        name = input("Enter your name: ")
        password = input("Enter your password: ")
                
        if name not in users and password not in users[name]:
            print("User Does't exists!")
        else:
            print(f"Hi, {name} Your Balance Is: {users[name]['balance']}")    
        
    def wid(self,users):
        name = input("Enter your name: ")
        password = input("Enter your password: ")
        account_type = str(input("Enter your Account Type: "))
                
        if name not in users and password not in users[name]:
            print("User Does't exists!")
        else:
            if account_type != users[name]['account_type']:
                print(f"{name} Your Account Type {account_type} Not Valid")
            else:
                amount = int(input("Enter Widrawal AMount = "))
                if amount > users[name]['balance']:
                    print(f"You Have Not Supisuint Balance. Your Balance Is {users[name]['balance']}")
                else:
                    users[name]["history"].append({
                        "type": "Debit",
                        "amount": amount,
                        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
                    users[name]['balance'] -= amount
                    print(f"Hi, {name} Your Balance Is: {users[name]['balance']}")   
    
    def dep(self,users):
        name = input("Enter your name: ")
        password = input("Enter your password: ")
        account_type = str(input("Enter your Account Type: "))
                
        if name not in users and password not in users[name]:
            print("User Does't exists!")
        else:
            if account_type != users[name]['account_type']:
                print(f"{name} Your Account Type {account_type} Not Valid")
            else:
                amount = int(input("Enter Deposite AMount = "))
                users[name]["history"].append({
                    "type": "Credit",
                    "amount": amount,
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
                users[name]['balance'] += amount
                print(f"Hi, {name} Your Balance Is: {users[name]['balance']}")    
            
    def userList(self,users):
        if  users:
            print(users)
        else:
            print("No Users Found...")      
    
    def history(self,users):
        name = input("Enter your name: ")
        password = input("Enter your password: ")
        account_type = str(input("Enter your Account Type: "))
                
        if name not in users and password not in users[name]:
            print("User Does't exists!")
        else:
            if account_type != users[name]['account_type']:
                print(f"{name} Your Account Type {account_type} Not Valid")
            else:
                for i in users[name]['history']:
                    print(f"\n {i['type']}: {i['amount']}: {i['date']},")  
                    
    def fundt(self,users):
        name = input("Enter your name: ")
        password = input("Enter your password: ")
        account_type = str(input("Enter your Account Type: "))
                
        if name not in users and password not in users[name]:
            print("User Does't exists!")
        else:
            if account_type != users[name]['account_type']:
                print(f"{name} Your Account Type {account_type} Not Valid")
            else:
                rname = input("Enter Receiver name: ")
                if rname not in users:
                    print("User Does't exists!")
                else:
                    amount = int(input("Enter AMount To Transfer = "))
                    if amount> users[rname]['balance']:
                        users[rname]["history"].append({
                            "type": "Credit",
                            "amount": amount,
                            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        })
                        users[name]["history"].append({
                            "type": "Debit",
                            "amount": amount,
                            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        })
                        users[rname]['balance'] += amount
                        users[name]['balance'] -= amount
                        print("Funds Transfer SuccessFully!")                
                    else:
                        print(f"You Have Not Supisuint Balance. Your Balance Is {users[rname]['balance']}")
    def changePass(self,users):
            name = input("Enter your name: ")
            account_type = str(input("Enter your Account Type: "))
                    
            if name not in users:
                print("User Does't exists!")
            else:
                if account_type != users[name]['account_type']:
                    print(f"{name} Your Account Type {account_type} Not Valid")
                else:
                    password = input("Enter your Current password: ")
                    if password not in users[name]['password']:
                        print("Wrong Password")
                    else:
                        newpassword = input("Enter your new password: ")
                        users[name]['password']=newpassword
                        print("Password CHnage SuccessFully")
                    
                    
        
    def exit(self):
        exit()        
        
        
def atm_menu():
    atm = ATM()
    users = {}
    
    while(True):
        print("1. Resgister User")
        print("2. Check User List")
        print("3. Check Balance")
        print("4. Widthraw Amount")
        print("5. Deposite Am0utn")
        print("6. Check Statement")
        print("7. Funds Transfer")
        print("8. Change Password")
        print("0. Exit")
        
        try:
            c = int(input("Enter Your Choice := "))
            if c==1:
                
                name = input("Enter your name: ")
                password = input("Enter your password: ")
                account_type = input("Enter account type (Savings/Current): ")
                
                if name in users:
                    print("User already exists!")
                else:
                    users[name] = {
                        "password": password,
                        "account_type": account_type,
                        "balance": 0,
                        "history":[]
                    }
                    print(f"User {name} added successfully!")
                    
            elif c==2:
                atm.userList(users)
                
            elif c==3:
                atm.Dis(users)
                
            elif c==4:
                atm.wid(users)   
                     
            elif c==5:
                atm.dep(users)
            elif c==6:
                atm.history(users)
            elif c==7:
                atm.fundt(users)
                
            elif c==8:
                atm.changePass(users)

            elif c==0:
                atm.exit()
                
        except ValueError:
            print("Enter Valid Digit No of CHoice")
            
if __name__ == "__main__":
    atm_menu()        