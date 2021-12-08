import openpyxl
import pandas as pd

from numpy.random import randn

producers = ['user', 'applicant', 'bank', 'branch', 'transaction']

for sheet in range(0, len(producers)):
    records = pd.read_excel('dummy_data.xlsx', sheet_name=sheet)
    print(producers[sheet])
    print(records.columns)
    for row in range(0, len(records)):
        for column in range(0, len(records.columns)):
            print(str(records.columns[column]) + ' = \'' + str(records.iloc[row][column]) + '\'', end='')
            if column + 1 < len(records.columns):
                print(',')
        print()

    print()

records = pd.read_excel('dummy_data.xlsx', sheet_name=0)
print(records.iloc[0][1])
