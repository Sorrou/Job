from ldap3 import Server, Connection, ALL
import json
import requests
import time

### Подключенипе к серверу AD, ищем OU
s = Server('172.19.39.X', port=389)
c = Connection(s, 'CN=Дачевич Владислав,OU=СЛУЖБА РАЗВИТИЯ И ПОДДЕРЖКИ ИНФРАСТРУКТУРЫ,OU=ДЕПАРТАМЕНТ ПО ИНФОРМАЦИОННЫМ ТЕХНОЛОГИЯМ,OU=ДИРЕКЦИЯ ПО ИНФОРМАЦИОННЫМ ТЕХНОЛОГИЯМ,OU=Employees,DC=moskvich,DC=ru', 'Password', auto_bind=True)
c.search('OU=Employees,DC=moskvich,DC=ru', '(&(objectclass=organizationalUnit))')
response = json.loads(c.response_to_json())

OU_yandex = []
OU_4 = []
OU_5 = []
OU_6 = []
OU_7 = []
OU_8 = []
OU_9 = []
OU_10 = []


header = {'Authorization': 'OAuth AQAEA7qkIx6zAAhEIPyds_3TnURskLvwMYhEGa0'}
create_url = 'https://api360.yandex.net/directory/v1/org/6563135/departments?perPage=1000'
change_department = 'https://api360.yandex.net/directory/v1/org/6563135/departments/'

proxy = {
    "http": "http://au07459:Qwe12345@10.232.123.126:3128",
    "https": "http://au07459:Qwe12345@10.232.123.126:3128"
}
leng = []
for i, k in response.items():
    for line in k:
        for atr, dn in line.items():
            if type(dn) == str:
                if 'DIS' in dn or 'Dismissed' in dn or 'Test' in dn or '\ ' in dn:
                    continue
                elif 'yandex' not in dn:
                    leng.append(len(dn.split(',')))
                    if len(dn.split(',')) == 4:
                        OU_4.append(dn)
                    elif len(dn.split(',')) == 5:
                        OU_5.append(dn)
                    elif len(dn.split(',')) == 6:
                        OU_6.append(dn)
                    elif len(dn.split(',')) == 7:
                        OU_7.append(dn)
                    elif len(dn.split(',')) == 8:
                        OU_8.append(dn)
                    elif len(dn.split(',')) == 9:
                        OU_9.append(dn)
                    elif len(dn.split(',')) == 10:
                        OU_10.append(dn)

dict_4 = {}

get_departmens = requests.get(create_url, headers=header, proxies=proxy)
departments = eval(get_departmens.text)
departments = departments.get('departments')
for i in departments:
    if i.get('name') == 'Все сотрудники':
        pass
    else:
        OU_yandex.append(i.get('description'))

# for i in OU_4:
#     OU_name = i.split(',')[0].replace('OU=', '')
#     Parent_OU_name = i.split(',')[1].replace('OU=', '')
#     full_OU_name = i
#     OU_AD_4.append(i)

#для 4 вложений
for ou4 in OU_4:
    #если имя больше 40
    if len(ou4) > 40:
        #как называлось полностью
        dn_start = ou4.split(',')[0].replace('OU=', '')
        dn_cut = dn_start
        #дескрипшен полностью
        descript = dn_start
        #сокращаю имя пока не будет меньше 40
        while len(dn_cut) > 40:
            dn_cut = dn_cut.split(' ')[:-1]
            dn_cut = ' '.join(dn_cut)
        #новое имя
        name = dn_cut
        #что будем пулить
        data = {"description": descript, "name": name, "parentId": 1}
        # print(data)
        #пулим
        x = requests.post(url=create_url, json=data, headers=header, proxies=proxy)
        result = x.text
        #превращаем выплюнутую строку в словарь
        result = eval(result)
        #берем ID созданной OU
        my_id = result.get('id')
        #записываем в словарь OU = id в яндексе
        dict_4[ou4] = my_id
        print('---> СОЗДАЛ ', name, my_id)
    #если имя меньше 40
    else:
        # новое имя
        name = ou4.split(',')[0].replace('OU=', '')
        # что будем пулить
        data = {"description": name, "name": name, "parentId": 1}
        # print(data)
        # пулим
        x = requests.post(url=create_url, json=data, headers=header, proxies=proxy)
        result = x.text
        #превращаем выплюнутую строку в словарь
        result = eval(result)
        # берем ID созданной OU
        my_id = result.get('id')
        # записываем в словарь OU = id в яндексе
        dict_4[ou4] = my_id
        print('---> СОЗДАЛ ', name, my_id)

#для 5 вхождений
for ou5 in OU_5:
    #если имя больше 40
    if len(ou5.split(',')[0].replace('OU=', '')) > 40:
        # как называлось полностью
        dn_start = ou5.split(',')[0].replace('OU=', '')
        dn_cut = dn_start
        # дескрипшен полностью
        descript = dn_start
        # сокращаю имя пока не будет меньше 40
        while len(dn_cut) > 40:
            dn_cut = dn_cut.split(' ')[:-1]
            dn_cut = ' '.join(dn_cut)
        # новое имя
        name = dn_cut
        parrent_id = dict_4.get(ou5.split(",", 1)[1])
        # что будем пулить
        data = {"description": descript, "name": name, "parentId": parrent_id}
        # пулим
        x = requests.post(url=create_url, json=data, headers=header, proxies=proxy)
        result = x.text
        # превращаем выплюнутую строку в словарь
        result = eval(result)
        # берем ID созданной OU
        my_id = result.get('id')
        # записываем в словарь OU = id в яндексе
        dict_4[ou5] = my_id
        print('---> СОЗДАЛ ', name, my_id)
    # если имя меньше 40
    else:
        # новое имя
        name = ou5.split(',')[0].replace('OU=', '')
        # что будем пулить
        parrent_id = dict_4.get(ou5.split(",", 1)[1])
        descript = ou5.split(',')[0].replace('OU=', '')
        data = {"description": descript, "name": name, "parentId": parrent_id}
        # пулим
        x = requests.post(url=create_url, json=data, headers=header, proxies=proxy)
        result = x.text
        # превращаем выплюнутую строку в словарь
        result = eval(result)
        # берем ID созданной OU
        my_id = result.get('id')
        # записываем в словарь OU = id в яндексе
        dict_4[ou5] = my_id
        print('---> СОЗДАЛ ', name, my_id)

#для 6 вхождений
for ou6 in OU_6:
    #если имя больше 40
    if len(ou6.split(',')[0].replace('OU=', '')) > 40:
        # как называлось полностью
        dn_start = ou6.split(',')[0].replace('OU=', '')
        dn_cut = dn_start
        # дескрипшен полностью
        descript = dn_start
        # сокращаю имя пока не будет меньше 40
        while len(dn_cut) > 40:
            dn_cut = dn_cut.split(' ')[:-1]
            dn_cut = ' '.join(dn_cut)
        # новое имя
        name = dn_cut
        parrent_id = dict_4.get(ou6.split(",", 1)[1])
        # что будем пулить
        data = {"description": descript, "name": name, "parentId": parrent_id}
        # пулим
        x = requests.post(url=create_url, json=data, headers=header, proxies=proxy)
        result = x.text
        # превращаем выплюнутую строку в словарь
        result = eval(result)
        # берем ID созданной OU
        my_id = result.get('id')
        # записываем в словарь OU = id в яндексе
        dict_4[ou6] = my_id
        print('---> СОЗДАЛ ', name, my_id)
    # если имя меньше 40
    else:
        # новое имя
        name = ou6.split(',')[0].replace('OU=', '')
        # что будем пулить
        parrent_id = dict_4.get(ou6.split(",", 1)[1])
        descript = ou6.split(',')[0].replace('OU=', '')
        data = {"description": descript, "name": name, "parentId": parrent_id}
        # пулим
        x = requests.post(url=create_url, json=data, headers=header, proxies=proxy)
        result = x.text
        # превращаем выплюнутую строку в словарь
        result = eval(result)
        # берем ID созданной OU
        my_id = result.get('id')
        # записываем в словарь OU = id в яндексе
        dict_4[ou6] = my_id
        print('---> СОЗДАЛ ', name, my_id)

#для 7 вхождений
for ou7 in OU_7:
    #если имя больше 40
    if len(ou7.split(',')[0].replace('OU=', '')) > 40:
        # как называлось полностью
        dn_start = ou7.split(',')[0].replace('OU=', '')
        dn_cut = dn_start
        # дескрипшен полностью
        descript = dn_start
        # сокращаю имя пока не будет меньше 40
        while len(dn_cut) > 40:
            dn_cut = dn_cut.split(' ')[:-1]
            dn_cut = ' '.join(dn_cut)
        # новое имя
        name = dn_cut
        parrent_id = dict_4.get(ou7.split(",", 1)[1])
        # что будем пулить
        data = {"description": descript, "name": name, "parentId": parrent_id}
        # пулим
        x = requests.post(url=create_url, json=data, headers=header, proxies=proxy)
        result = x.text
        # превращаем выплюнутую строку в словарь
        result = eval(result)
        # берем ID созданной OU
        my_id = result.get('id')
        # записываем в словарь OU = id в яндексе
        dict_4[ou7] = my_id
        print('---> СОЗДАЛ ', name, my_id)
    # если имя меньше 40
    else:
        # новое имя
        name = ou7.split(',')[0].replace('OU=', '')
        # что будем пулить
        parrent_id = dict_4.get(ou7.split(",", 1)[1])
        descript = ou7.split(',')[0].replace('OU=', '')
        data = {"description": descript, "name": name, "parentId": parrent_id}
        # пулим
        x = requests.post(url=create_url, json=data, headers=header, proxies=proxy)
        result = x.text
        # превращаем выплюнутую строку в словарь
        result = eval(result)
        # берем ID созданной OU
        my_id = result.get('id')
        # записываем в словарь OU = id в яндексе
        dict_4[ou7] = my_id
        print('---> СОЗДАЛ ', name, my_id)

#для 8 вхождений
for ou8 in OU_8:
    #если имя больше 40
    if len(ou8.split(',')[0].replace('OU=', '')) > 40:
        # как называлось полностью
        dn_start = ou8.split(',')[0].replace('OU=', '')
        dn_cut = dn_start
        # дескрипшен полностью
        descript = dn_start
        # сокращаю имя пока не будет меньше 40
        while len(dn_cut) > 40:
            dn_cut = dn_cut.split(' ')[:-1]
            dn_cut = ' '.join(dn_cut)
        # новое имя
        name = dn_cut
        parrent_id = dict_4.get(ou8.split(",", 1)[1])
        # что будем пулить
        data = {"description": descript, "name": name, "parentId": parrent_id}
        # пулим
        x = requests.post(url=create_url, json=data, headers=header, proxies=proxy)
        result = x.text
        print(result)
        # превращаем выплюнутую строку в словарь
        result = eval(result)
        print(result)
        # берем ID созданной OU
        my_id = result.get('id')
        # записываем в словарь OU = id в яндексе
        dict_4[ou8] = my_id
        print('---> СОЗДАЛ ', name, my_id)
    # если имя меньше 40
    else:
        # новое имя
        name = ou8.split(',')[0].replace('OU=', '')
        # что будем пулить
        parrent_id = dict_4.get(ou8.split(",", 1)[1])
        descript = ou8.split(',')[0].replace('OU=', '')
        data = {"description": descript, "name": name, "parentId": parrent_id}
        # пулим
        x = requests.post(url=create_url, json=data, headers=header, proxies=proxy)
        result = x.text
        print(result)
        # превращаем выплюнутую строку в словарь
        result = eval(result)
        print(result)
        # берем ID созданной OU
        my_id = result.get('id')
        # записываем в словарь OU = id в яндексе
        dict_4[ou8] = my_id
        print('---> СОЗДАЛ ', name, my_id)

#для 9 вхождений
for ou9 in OU_9:
    #если имя больше 40
    if len(ou9.split(',')[0].replace('OU=', '')) > 40:
        # как называлось полностью
        dn_start = ou9.split(',')[0].replace('OU=', '')
        dn_cut = dn_start
        # дескрипшен полностью
        descript = dn_start
        # сокращаю имя пока не будет меньше 40
        while len(dn_cut) > 40:
            dn_cut = dn_cut.split(' ')[:-1]
            dn_cut = ' '.join(dn_cut)
        # новое имя
        name = dn_cut
        parrent_id = dict_4.get(ou9.split(",", 1)[1])
        # что будем пулить
        data = {"description": descript, "name": name, "parentId": parrent_id}
        # пулим
        x = requests.post(url=create_url, json=data, headers=header, proxies=proxy)
        result = x.text
        print(result)
        # превращаем выплюнутую строку в словарь
        result = eval(result)
        print(result)
        # берем ID созданной OU
        my_id = result.get('id')
        # записываем в словарь OU = id в яндексе
        dict_4[ou9] = my_id
        print('---> СОЗДАЛ ', name, my_id)
    # если имя меньше 40
    else:
        # новое имя
        name = ou9.split(',')[0].replace('OU=', '')
        # что будем пулить
        parrent_id = dict_4.get(ou9.split(",", 1)[1])
        descript = ou9.split(',')[0].replace('OU=', '')
        data = {"description": descript, "name": name, "parentId": parrent_id}
        # пулим
        x = requests.post(url=create_url, json=data, headers=header, proxies=proxy)
        result = x.text
        print(result)
        # превращаем выплюнутую строку в словарь
        result = eval(result)
        print(result)
        # берем ID созданной OU
        my_id = result.get('id')
        # записываем в словарь OU = id в яндексе
        dict_4[ou9] = my_id
        print('---> СОЗДАЛ ', name, my_id)

#для 10 вхождений
for ou10 in OU_10:
    #если имя больше 40
    if len(ou10.split(',')[0].replace('OU=', '')) > 40:
        # как называлось полностью
        dn_start = ou10.split(',')[0].replace('OU=', '')
        dn_cut = dn_start
        # дескрипшен полностью
        descript = dn_start
        # сокращаю имя пока не будет меньше 40
        while len(dn_cut) > 40:
            dn_cut = dn_cut.split(' ')[:-1]
            dn_cut = ' '.join(dn_cut)
        # новое имя
        name = dn_cut
        parrent_id = dict_4.get(ou10.split(",", 1)[1])
        # что будем пулить
        data = {"description": descript, "name": name, "parentId": parrent_id}
        # пулим
        x = requests.post(url=create_url, json=data, headers=header, proxies=proxy)
        result = x.text
        print(result)
        # превращаем выплюнутую строку в словарь
        result = eval(result)
        # берем ID созданной OU
        my_id = result.get('id')
        # записываем в словарь OU = id в яндексе
        dict_4[ou10] = my_id
        print('---> СОЗДАЛ ', name, my_id)
    # если имя меньше 40
    else:
        # новое имя
        name = ou10.split(',')[0].replace('OU=', '')
        # что будем пулить
        parrent_id = dict_4.get(ou10.split(",", 1)[1])
        descript = ou10.split(',')[0].replace('OU=', '')
        data = {"description": descript, "name": name, "parentId": parrent_id}
        # пулим
        x = requests.post(url=create_url, json=data, headers=header, proxies=proxy)
        result = x.text
        print(result)
        # превращаем выплюнутую строку в словарь
        result = eval(result)
        # берем ID созданной OU
        my_id = result.get('id')
        # записываем в словарь OU = id в яндексе
        dict_4[ou10] = my_id
        print('---> СОЗДАЛ ', name, my_id)

print(dict_4)