from ldap3 import Server, Connection, ALL
import json

s = Server('172.19.39.X', port=389)
c = Connection(s, 'CN=Vladislav Dachevich,OU=ITBO,OU=IT,OU=DIS,OU=Employees,DC=moskvich,DC=ru', 'Password', auto_bind=True)
# print(c)
# c.search('DC=moskvich,DC=ru','(&(objectclass=user)(sAMAccountName=au07459))')
# response = json.loads(c.response_to_json())
# print(response)


ou_path = 'OU=TEST5,OU=TEST4,OU=TEST3,OU=TEST2,OU=TEST1,DC=moskvich,DC=ru'
ou_path_start = "DC=moskvich,DC=ru"
object_class = 'organizationalUnit'

lala = list(ou_path.split(','))
start_count=len(lala)-1
#print(str(lala[1])+str(','+lala[2])+str(','+lala[3]))


c.add(ou_path, object_class)
{'result': 0, 'description': 'success', 'dn': '', 'message': '', 'referrals': None, 'type': 'addResponse'}
if c.result['result'] == 0:
    print('OU Object Created Successfully')
else:
    # c.add(str(lala[1])+str(','+lala[2])+str(','+lala[3]), object_class)
    # c.add(ou_path, object_class)
    while start_count != 1:
        c.add(ou_path.split(',')[start_count-2] + ',' + ou_path_start, object_class)
        # print(ou_path.split(',')[start_count-2]+','+ou_path_start)
        ou_path_start = ou_path.split(',')[start_count-2]+','+ou_path_start
        start_count -= 1
        # print(start_count)
    # if c.result['result'] == 0:
    #     print('OU Object Created Successfully')

