import openpyxl
import pandas as pd
import mysql.connector

from numpy.random import randn

db = mysql.connector.connect(
    host='localhost',
    user='aline',
    password='Aline2022!',
    database='alinedb'
)

cursor = db.cursor()

producers = ['user', 'applicant', 'bank', 'branch', 'transaction']

for sheet in range(0, len(producers)):
    records = pd.read_excel('dummy_data.xlsx', sheet_name=sheet)
    print(producers[sheet])
    print(records.columns)
    for row in range(0, len(records)):
        columnsStr = ''
        valuesStr = ''
        for column in range(0, len(records.columns)):
            columnsStr = columnsStr + str(records.columns[column])

            if str(records.columns[column]) == 'enabled' or str(records.columns[column]) == 'member_id':
                valuesStr = valuesStr + '' + str(records.iloc[row][column]) + ''
            else:
                valuesStr = valuesStr + '\'' + str(records.iloc[row][column]) + '\''

            if column + 1 < len(records.columns):
                # print(',')
                columnsStr = columnsStr + ', '
                valuesStr = valuesStr + ', '
        query = 'INSERT INTO ' + producers[sheet] + ' (' + columnsStr + ') VALUES (' + valuesStr + ')'
        print('Query #' + str(row+1) + ': ' + query)
        # cursor.execute(query)
        # db.commit()
        # print(cursor.rowcount, "record inserted.")
    print()

