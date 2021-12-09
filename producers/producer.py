import pandas as pd
import mysql.connector

# Connect to MySQL DB
db = mysql.connector.connect(
    host='localhost',
    user='aline',
    password='Aline2022!',
    database='alinedb'
)

# Define cursor variable to execute queries
cursor = db.cursor()

# Provide a list of tables/sheets for the script to cycle through
producers = ['user', 'applicant', 'bank', 'branch', 'transaction']

# Iterate over the list of tables/sheets
for sheet in range(0, len(producers)):
    # Pull the data from the dummy data Excel sheet into a dataset
    records = pd.read_excel('dummy_data.xlsx', sheet_name=sheet)
    values = []

    # Iterate over each row of the Pandas Dataset
    for row in range(0, len(records)):
        valuesStr = ''

        # Iterate over each column to create the query string
        for column in range(0, len(records.columns)):
            # Check if the value in the spreadsheet is blank
            if str(records.iloc[row][column]) == 'nan':
                valuesStr = valuesStr + 'NULL'
            else:
                # Provide column names for non-string columns
                nonString = ['enabled', 'member_id', 'income', 'bank_id']

                # Check if the column exists in the provided list or if the column is for passwords
                if str(records.columns[column]) in nonString:
                    valuesStr = valuesStr + str(records.iloc[row][column])
                elif str(records.columns[column]) == 'password':
                    valuesStr = valuesStr + 'MD5(\'' + str(records.iloc[row][column]) + '\')'
                else:
                    valuesStr = valuesStr + '\'' + str(records.iloc[row][column]) + '\''

                # Check if the column is the last in the dataset
                if column + 1 < len(records.columns):
                    valuesStr = valuesStr + ', '

        # Append query string into list
        values.append('(' + valuesStr + ')')
    # Check if values exist within list
    if len(values) > 0:
        query = 'INSERT INTO ' + producers[sheet] + ' (' + ', '.join(records.columns) + ') VALUES ' + ', '.join(values)
        cursor.execute(query)
        db.commit()
        print(cursor.rowcount, 'record(s) inserted into ' + producers[sheet] + ' table.')
    print()

