import keyring as k
import hashlib
import string, random

class main():
    def __init__(self):
        self.Menu = '''1 - set new password\n2 - delete password\n3 - get all passwords\n4 - get passwords by service\n5 - get passwords by email\n6 - get passwords by login'''
        self.alphabet = string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation
        
        with open('salt.txt', 'r', encoding='utf-8') as f:
            self.salt = eval(f.readline())
            self.secretKey = eval(f.readline())
            
        while True:
            password = input('Enter main password: ')
            if (hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), self.salt, 1000000) == self.secretKey):
                print("You're in!")
                break
            else:
                print("The password isn't correct")
            
        self.pwnMng()
                
                
    def pwnMng(self):
        while True:
            print('-'*30)
            print(self.Menu)
            print('-'*30)
            
            choice = input('-> ')
            print('-'*30)
            if (choice == '1'): # Set new acc -> password
                print('write ur email | service | login | password')
                try:
                    email, service, login, password = input().split(' | ')
                    k.set_password(f'{email} | {service} | {login}', 'Oleg', self.encrypt(password))
                    self.writeInFile(f'{email} | {service} | {login}')
                except ValueError:
                    print('Ошибка: Введите ровно 4 значения')
                        
            elif (choice == '2'): # Del acc
                try:
                    service, logOrEmail = input('write service + email or service + login -> ').split(' | ')
                    
                    acc = self.findInFile('del', f'{service} | {logOrEmail}')[0]
                    self.deleteLine(acc)
                    k.delete_password(acc,'Oleg')
                except ValueError:
                    print('Ошибка: Введите ровно 2 значения')
                except IndexError:
                    print('Такого аккаунта - нет')
                except Exception as exp:
                    print(exp)
                
            elif (choice == '3'): # get all passwords
                with open('Service.txt', 'r', encoding='utf-8') as f:
                    if (len(f.read()) > 0):
                        print('email | service | login | password')
                        f.seek(0)    
                    
                        for line in f:
                            print(line.strip('\n') + ' | ' + self.decrypt(k.get_password(line.strip('\n'), 'Oleg')))
                    else:    
                        print('Ни одного аккаунта не создано')
                        
            elif (choice == '4'): # get all passwords on service
                service = input('write service name -> ')
                accs = self.findInFile('service', service)

                print('email | service | login | password')
                if len(accs) > 0:
                    for acc in accs:
                        print(f"{acc} | {self.decrypt(k.get_password(acc, 'Oleg'))}")
                else:
                    print('Ни одного аккаунта не найдено')
                
            elif (choice == '5'): # get all passwords by email
                email = input('write ur email -> ')
                accs = self.findInFile('email', email)

                print('email | service | login | password')
                if len(accs) > 0:
                    for acc in accs:
                        print(f"{acc} | {self.decrypt(k.get_password(acc, 'Oleg'))}")
                else:
                    print('Ни одного аккаунта не найдено')

            elif (choice == '6'): # get all passwords by login
                login = input('write ur login -> ')
                accs = self.findInFile('login', login)

                print('email | service | login | password')
                if len(accs) > 0:
                    for acc in accs:
                        print(f"{acc} | {self.decrypt(k.get_password(acc, 'Oleg'))}")
                else:
                    print('Ни одного аккаунта не найдено')
                    
            else:
                print('Такого варианта нет')
       
                
    def encrypt(self, password):
        x = 2
        while x <= len(password)+1:
            if (x % 2 == 0):
                password = password[:x-1] + random.choice(self.alphabet) + password[x-1:]
            x += 1
        return password
    
    def decrypt(self, password):
        return password[::2]
    
    # File management
    def writeInFile(self, text):
        with open('Service.txt', 'a', encoding='utf-8') as f:
            f.write(f'{text}\n')
            
    def findInFile(self, whatNeedToFind, name):
        arrToReturn = []
        with open('Service.txt', 'r', encoding='utf-8') as f:
            for line in f:
                email, service, login = line.split(' | ')
                if (whatNeedToFind == 'service' and name in service):
                    arrToReturn.append(line.rstrip('\n'))
                elif(whatNeedToFind == 'email' and name in email):
                    arrToReturn.append(line.rstrip('\n'))
                elif(whatNeedToFind == 'login' and name in login):
                    arrToReturn.append(line.rstrip('\n'))
                elif (whatNeedToFind == 'del'):
                    args = name.split(' | ')
                    # service + email or email + service | service + login or login + service
                    if(args[0] in service and (args[1] in email or args[1] in login) or args[1] in service and (args[0] in email or args[0] in login)):
                        arrToReturn.append(line.rstrip('\n'))
        
        return arrToReturn
                 
    def deleteLine(self, lineToDel):
        with open('Service.txt', 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        with open('Service.txt', 'w', encoding='utf-8') as f:
            for line in lines:
                if line.strip("\n") != lineToDel:
                    f.write(line)
        
        
Main = main()