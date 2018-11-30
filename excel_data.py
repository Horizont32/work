import xlsxwriter
import os


def WriteTimetable(path, step, file_type, path_to_excel_file):
    files = os.listdir(path)
    workbook = xlsxwriter.Workbook(path_to_excel_file)
    file_list = workbook.add_worksheet()
    # Start from the first cell. Rows and columns are zero indexed.
    row = 0
    col = 0
    for i in range(1, len(files), step):
        if files[i].endswith(file_type):
            file_list.write(row, col, files[i][4:-len(file_type)])
            file_list.write(row, col+1, 0.016 * float(files[i][4:-len(file_type)]))
            row = row + 1
            print(path + files[i][4:-len(file_type)])
            print((files[i][4:-len(file_type)]))
            print((files[i][4:-len(file_type)]))

WriteTimetable('d:/YandexDisk/Фотки/', 20, '.JPG', 'd:\Expenses01.xlsx')
"""
# Create a workbook and add a worksheet.
workbook = xlsxwriter.Workbook('d:\Expenses01.xlsx')
worksheet = workbook.add_worksheet()

# Some data we want to write to the worksheet.
expenses = (
    ['Rent', 1000],
    ['Gas',   100],
    ['Food',  300],
    ['Gym',    50],
)

# Start from the first cell. Rows and columns are zero indexed.
row = 0
col = 0

# Iterate over the data and write it out row by row.
for item, cost in (expenses):
    worksheet.write(row, col,     item)
    worksheet.write(row, col + 1, cost)
    row += 1

    'd:\YandexDisk\Фотки\' 

"""