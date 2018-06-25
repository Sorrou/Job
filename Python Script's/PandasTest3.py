from sklearn.linear_model import LinearRegression
import pyodbc
import datetime
import numpy as np
import pandas as pd


def myPredict(cat, startDate, lastDate):
    server = 'IP.SERVER'
    database = 'DATABASE'
    username = 'LOGIN'
    password = 'PASSWORD'

    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    cnxn2 = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)

    cursor1 = cnxn.cursor()
    cursor2 = cnxn2.cursor()

    sql = """
    SELECT 
          c.[week_number] as 'Неделя'
        , cs.store_id
        , sf.ID_Fact_Category
        , sum(cs.price) as sum
      FROM [gort_OTB].[dbo].[calc] as c
      join [OTB].[dbo].[calc_vm__stat] as cs on c.date = cs.date
      join [dbo].[Suplie_Value_Fact] as sf on cs.incomes_attributes_id = sf.[incomes_attributes_id]
      where cs.date between '{startDate}' and '{lastDate}'
      and cs.store_id = 1
      and sf.ID_Fact_Category IN({cat})
      group by [week_number]
        , cs.store_id
        , sf.ID_Fact_Category
    """.format(cat=str(cat).replace('(', '').replace(')', ''), startDate=str(startDate), lastDate=str(lastDate))

    time = datetime.datetime.now()
    modele = 'LinearRegression'
    model = LinearRegression()
    df = pd.read_sql_query(sql, cnxn)
    df.columns = ['w', 's', 'c', 'p']
    print(df)
    for g in range(1, 5):
        week = [[max(df.w)+g]]
        for i in range(len(week)):
            for j in (set(df.c)):
                df2 = [[j]]
                df1 = df[np.in1d(df.c, df2)]
                trainW = np.asarray(df1.w).reshape(-1, 1)
                trainP = np.asarray(df1.p).reshape(-1, 1)
                model.fit(trainW, trainP)
                W_predict = ([week[i]])
                P_predict = model.predict(W_predict)
                print(str(df2[0][0]), week[0][0], int(P_predict))
                #sql2 = 'INSERT INTO Test_02([Analyze Date], method, Category, Week, How)VALUES(?, ?, ?, ?, ?)'
                #cursor2.execute(sql2, time, modele, str(df2[0][0]), str(week[0][0]), int(P_predict))
                #cursor2.commit()


myPredict((21), 20180101, 20180701)
