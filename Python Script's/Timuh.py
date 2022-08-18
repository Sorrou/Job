import ldap3
from ldap3 import Server, Connection, ALL
import json
import argparse


#ЗАГРУЖАЕМ АРГУМЕНТЫ ИЗ КОНСОЛИ
parser = argparse.ArgumentParser()
#СОЗДАЕМ АРГУМЕНТЫ КОТОРЫЕ БУДЕМ ЖДАТ
parser.add_argument('-user', help='user', type=str)
parser.add_argument('-password', help='password', type=str)

argument = parser.parse_args()

s = Server('172.19.39.X',use_ssl=True, port=636)
c = Connection(s, 'CN=Дачевич Владислав,OU=СЛУЖБА РАЗВИТИЯ И ПОДДЕРЖКИ ИНФРАСТРУКТУРЫ,OU=ДЕПАРТАМЕНТ ПО ИНФОРМАЦИОННЫМ ТЕХНОЛОГИЯМ,OU=ДИРЕКЦИЯ ПО ИНФОРМАЦИОННЫМ ТЕХНОЛОГИЯМ,OU=Employees,DC=moskvich,DC=ru', 'Password', auto_bind=True)
# print(c)
c.search('DC=moskvich,DC=ru','(&(objectclass=user)(sAMAccountName='+argument.user+'))')
response = json.loads(c.response_to_json())

madn = ''
mastring = response['entries']
for i in mastring:
    madn = i['dn']

user_dn = madn
new_pass = argument.password

r = c.extend.microsoft.modify_password(user_dn, new_pass)

password_expire = {"pwdLastSet": (ldap3.MODIFY_REPLACE, [0])}
c.modify(dn=user_dn, changes=password_expire)

# print(c.result)
