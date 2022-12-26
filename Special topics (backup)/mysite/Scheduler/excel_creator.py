import datetime

import sys
# This is to got one directory back, so that we can access Specialtopic.admin files.
sys.path.append('../')

# Importing models and admin class for querying and extracting data from database.
from Specialtopic.models import System_database
from Specialtopic.admin import System_databaseResource

# Library to create excel sheet.
import xlsxwriter


def excel_creation():

    today = datetime.date.today()

    # Creating a query to get data for current date.
    query = System_database.objects.filter(Date__year = datetime.datetime.now().year, Date__month = datetime.datetime.now().month, Date__day = datetime.datetime.now().day)


    # Extracting data from import_export from the admin.py file.
    dataset = System_databaseResource().export(query)
    dataset = str(dataset.csv).split('\r\n')
    del dataset[-1]
    # print(dataset)


    # Creating new excel sheet for everyday.
    book = xlsxwriter.Workbook("Excel_files\\" + today.strftime("%d.%m.%Y") + ".xlsx")
    sheet = book.add_worksheet()
    row = 0

    
    # Inserting the values in the excel sheet.
    for value in dataset:
        id, date, student_name, branch, usn, system_no, time_in, time_out  = value.split(",")
        sheet.write(row, 0, id)
        sheet.write(row, 1, date)
        sheet.write(row, 2, student_name)
        sheet.write(row, 3, branch)
        sheet.write(row, 4, usn)
        sheet.write(row, 5, system_no)
        sheet.write(row, 6, time_in)
        sheet.write(row, 7, time_out)
        row += 1
    book.close()
    
