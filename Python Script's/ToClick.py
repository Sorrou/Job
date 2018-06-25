import sqlite3
import datetime
import os
import time
import schedule
import subprocess

from winreg import *

#База, откуда будем дёргать логи
confBase = open('D:\\1CtoClickHouse\\Config.ini', mode='r').readlines()[22].strip()

#Config
confLog = open('D:\\1CtoClickHouse\\Config.ini', mode='r').readlines()[1].strip()
confLfr = open((open('D:\\1CtoClickHouse\\Config.ini', mode='r').readlines()[13].strip()), mode='r')
confLfr = int(confLfr.read())
confLfw = open('D:\\1CtoClickHouse\\Config.ini', mode='r').readlines()[13].strip()
confClick = open('D:\\1CtoClickHouse\\Config.ini', mode='r').readlines()[4].strip()
confDb = open('D:\\1CtoClickHouse\\Config.ini', mode='r').readlines()[7].strip()
confCSV = open('D:\\1CtoClickHouse\\Config.ini', mode='r').readlines()[10].strip()
howRow = open('D:\\1CtoClickHouse\\Config.ini', mode='r').readlines()[16].strip()
howRow = int(howRow)
schedTime = open('D:\\1CtoClickHouse\\Config.ini', mode='r').readlines()[19].strip()
schedTime = int(schedTime)

#MegaFunction
def job():
    #Лезем в реестр, смотрим где лежат логи нашей базы
    aReg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
    aKey = OpenKey(aReg, 'SYSTEM\\CurrentControlSet\\Services\\1C:Enterprise 8 Server Agent #4')
    #Расшифровываем значение ключа
    imagePath = QueryValueEx(aKey, 'ImagePath')
    tup = imagePath[0].split()
    #Получаем полный путь к lst, записываем в файлик#
    path = (tup[12].replace('"', ''), tup[13].replace('"', '') + '\\reg_' + tup[6] + '\\1CV8Clst.lst')
    with open('D:\\1CtoClickHouse\\Config2.ini', mode='w', encoding='utf-8') as whlog:
        print(*path, file=whlog)
    with open('D:\\1CtoClickHouse\\Config2.ini', mode='r', encoding='utf-8') as whlog2:
        path2 = whlog2.read().strip()
    fkn = open(path2, mode='r', encoding='utf-8')
    #Ищем где лежит наша база(лог) (которая указанна в переменной confBase)
    #записываем ID кластера, порт, имя сервера, id базы
    for line in fkn:
        for word in line.replace('"', '').split('\n'):
            if len(word) > 4:
                myWord = word.replace('{', '').replace('}', '').split(',')[1].split()
                for lines in myWord:
                    with open('D:\\1CtoClickHouse\\Config2.ini', mode='a', encoding='utf-8') as whlog:
                        if lines == confBase:
                            print(*word.replace('{', '').replace('}', '').split(',')[0].split(), file=whlog)
                        if lines == 'Локальный':
                            print(*word.replace('{', '').replace('}', '').split(',')[0].split(), file=whlog)
                            print(*word.replace('{', '').replace('}', '').split(',')[2].split(), file=whlog)
                            print(*word.replace('{', '').replace('}', '').split(',')[3].split(), file=whlog)

    #Записываем полный путь к лог-файлу в файлик
    with open('D:\\1CtoClickHouse\\Config2.ini', mode='r', encoding='utf-8') as whlog2:
        myPath = (tup[12].replace('"', ''), tup[13].replace('"', '') + '\\reg_' + tup[6] + '\\' + whlog2.readlines()[
            4].strip() + '\\1Cv8Log\\1Cv8.lgd')
    with open('D:\\1CtoClickHouse\\Config2.ini', mode='a', encoding='utf-8') as whlog2:
        print(*myPath, file=whlog2)
    myBase = open('D:\\1CtoClickHouse\\Config2.ini', mode='r', encoding='utf-8').readlines()[5].strip()
    #Копируем лог файл в D:\1CtoClickHouse для дальнейшей обработки, во избежания блокировки базы, и глюков со стороны
    #1С
    proc = subprocess.Popen(['powershell', 'Copy-Item "' + myBase + '" -Destination "D:\\1CtoClickHouse\\1Cv8.lgd"'])
    proc.wait()

    IDBase = open('D:\\1CtoClickHouse\\Config2.ini', mode='r').readlines()[4].strip()
    IDCluster = open('D:\\1CtoClickHouse\\Config2.ini', mode='r').readlines()[1].strip()

    #Подлючаемся к скопированной копии лога
    conn = sqlite3.connect('D:\\1CtoClickHouse\\1Cv8.lgd')
    cursor = conn.cursor()

    #Обьединяем таблицы
    sql = "SELECT date, *, UserCodes.name, ComputerCodes.name, AppCodes.code, EventCodes.code, MetadataCodes.code," \
          " WorkServerCodes.code, PrimaryPortCodes.code" \
          " FROM EventLog" \
          " LEFT JOIN UserCodes ON EventLog.UserCode = UserCodes.code" \
          " LEFT JOIN ComputerCodes ON EventLog.computerCode = ComputerCodes.code" \
          " LEFT JOIN AppCodes ON EventLog.appCode = AppCodes.code" \
          " LEFT JOIN EventCodes ON EventLog.eventCode = EventCodes.code" \
          " LEFT JOIN MetadataCodes ON EventLog.metadataCodes = MetadataCodes.code" \
          " LEFT JOIN WorkServerCodes ON EventLog.workServerCode = WorkServerCodes.code" \
          " LEFT JOIN PrimaryPortCodes ON EventLog.primaryPortCode = PrimaryPortCodes.code" \
          " LEFT JOIN SecondaryPortCodes ON EventLog.secondaryPortCode = SecondaryPortCodes.code" \
          " WHERE date > ?"

    #Обрабатываем Данные, записываем в файл, если они ещё не выгружались
    check = 0
    for row in cursor.execute(sql, [confLfr]):
        a = (datetime.datetime.fromtimestamp(int(row[0] / 10000 - 62135578800)).strftime('%Y-%m-%d'))
        t = (datetime.datetime.fromtimestamp(int(row[0] / 10000 - 62135578800))).strftime('%H:%M:%S')
        tt = (datetime.datetime.fromtimestamp(int(row[0] / 10000 - 62135578800))).strftime('%Y-%m-%d %H:%M:%S')
        b = row
        if b[3] > confLfr:
            with open(confCSV, mode='a', encoding='utf-8') as f:
                c = b[18].replace("'", '"')
                if c[:1] == '"':
                    c = '\\' + c
                d = (b[13].replace('\r\n', '').replace('\n', '')).replace(',', '+')
                e = (b[17].replace('\r\n', '').replace(',', '+')).replace('"', '\\')
                c = c.replace(',', '+')
                o = b[26].replace('"', '')
                g = b[28].replace('"', '')
                h = b[30].replace('"', '')
                if b[19] == 0:
                    i = b[35]
                else:
                    i = b[35].replace('"', '')
                b = b[1], b[2], b[3], b[4], b[5], b[6], b[7], b[8], b[9], b[23], b[24], b[10], o, b[11], g, b[12], h, d, \
                    b[14],b[32], b[15], b[16], e, c, b[19], i, b[20], b[37], b[21], b[39]
                print(a, confBase, IDBase, IDCluster, t, tt, *b, sep=',', file=f)
                check += 1
                if check == howRow:
                    f.close()
                # Пишем последний date
                    with open(confLfw, mode='w') as Last:
                        print(b[2], file=Last)
                    proc = subprocess.Popen(['powershell', 'Copy-Item "D:\\1CtoClickHouse\\Retail.csv" -Destination "D:\\1CtoClickHouse\\ClickCSV\\Retail.csv"'])
                    proc.wait()
                # Удаляем CSV'шник
                    os.remove(confCSV)
                    check = 0
        # Пишем последний date файла, что бы в следующий раз начать с него
        with open(confLfw, mode='w', encoding='utf-8') as LFW:
            print(b[2], file=LFW)
    try:
        file = open('D:\\1CtoClickHouse\\Retail.csv')
    except IOError as e:
        print('Netu')
    else:
        file.close()
        proc = subprocess.Popen(['powershell',
                             'Copy-Item "D:\\1CtoClickHouse\\Retail.csv" -Destination "D:\\1CtoClickHouse\\ClickCSV\\Retail.csv"'])
        proc.wait()
        os.remove(confCSV)
    conn.close()
    os.remove('D:\\1CtoClickHouse\\1Cv8.lgd')


def VACUUM():
    conn = sqlite3.connect(myBase)
    cursor = conn.cursor()

    #Смотрим дату, отнимаем месяц
    nowTime = datetime.datetime.now()
    oldTime = datetime.timedelta(days=30, hours=0, minutes=0)
    oldTime = str(nowTime - oldTime)[0:10]
    oldTimeInSql = time.mktime(datetime.datetime.strptime(oldTime, '%Y-%m-%d').timetuple())
    oldTimeInSql = str((oldTimeInSql + 62135578800) * 10000)[0:15]

    #Удаляем записи старше месяца
    sql2 = "DELETE FROM EventLog WHERE date < ?;"
    cursor.execute(sql2, [oldTimeInSql])
    conn.commit()
    cursor.execute("VACUUM;")
    conn.commit()
    conn.close()


schedule.every(schedTime).minutes.do(job)
schedule.every().day.at('00:00').do(VACUUM)

while True:
    schedule.run_pending()
    time.sleep(30)
