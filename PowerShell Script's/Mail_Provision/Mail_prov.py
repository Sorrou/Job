from ldap3 import Server, Connection, ALL
import re
import os

server = Server('Myserver.local.my.ru', get_info=ALL)
conn = Connection(server, user='local.my.ru\\USER', password='Pa$$word', authentication='NTLM',
                  auto_bind=True)

conn.search('OU=USERS, OU=COMPANY, DC=local, DC=my, DC=ru', '(objectclass=user)',
                  attributes=['SamAccountName'])

user_list_AD = []
for user in conn.entries:
    user_list_AD.append(re.findall('sAMAccountName: (\S+)', str(user))[0])

#Не помню зачем это нужно было ( replace('п»ї', '') ), какой то из юзеров все портил.
exch_user_list = []
exch_user = open('E:\\Provision\\Current_Mailbox.txt')
for user in exch_user:
    exch_user_list.append(user.replace('\n', '').replace('п»ї', ''))

result = (set(user_list_AD) - set(exch_user_list))

new_mailbox = open('E:\\Provision\\New_Mailbox.txt', mode='w')
for user in result:
    new_mailbox.write(user + '\n')
