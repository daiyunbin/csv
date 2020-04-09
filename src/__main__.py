import mysql.connector
from mysql.connector import connect
import os
import csv
import settings

class Mysql:

    def __init__(self):
        host = os.environ['DB_HOST']
        password = os.environ['DB_PASS']
        user = os.environ['DB_USER']
        db = os.environ['DB_NAME']
        port = os.environ['DB_PORT']
        
        self.cnx = connect(
                            user = user, 
                            password = password,
                            host = host,
                            database = db,
                            port = port
                            )
        self.cursor = self.cnx.cursor(buffered=True)
        return 


    def showTables(self)->list:
        self.cursor.execute('show tables')
        tables = []
        for table in self.cursor:
            if type(table[0]) == str:
                tables.append(table[0])
            elif type(table[0] == bytearray):
                tables.append(table[0].decode("utf-8"))
        return tables

    def getTable(self,tableName)->list:
        self.cursor.execute('SELECT * FROM ' + tableName)
        columns = self.cursor.column_names
        rows = [ { column:value  for value,column in zip(row,columns) } for row in self.cursor]
        return [columns,rows]
    
    def close(self):
        self.cursor.close()
        self.cnx.close()
        return

class Csv:
    def __init__(self,filename):

        self.ignore = filename in settings.IGNORED_TABLE
        if self.ignore:
            return
        print(filename + ":" + str(self.ignore))

        self.ignoreColumn = settings.IGNORED_TABLE_COLUMN.get(filename)

        self.path = settings.CSV_PATH
        if self.path[-1] != "/":
            self.path += "/"

        self.file = self.path + filename + ".csv"
        with open( self.file ,mode="w"):
            pass
        return

    def createCsv(self,table:Mysql)->bool:

        if self.ignore:
            return False
        columns,rows = table
        if self.ignoreColumn is not None:
            columnsSet = set(columns) - self.ignoreColumn
            columns = list(columnsSet)

        with open(self.file, mode="a",newline="") as f:
            writer = csv.writer(f)
            writer.writerow(columns)
            for row in rows:
                writer.writerow([row[column] for column in columns])
        return True

def main():
    db =  Mysql()
    tables = db.showTables()
    for tableName in tables:
        table = db.getTable(tableName)
        csvFile = Csv(tableName)
        csvFile.createCsv(table)

    db.close()
    return

if __name__ == "__main__":
    main()
