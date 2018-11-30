import os
import shutil
import xlsxwriter
"""
# Create a workbook and add a worksheet.
workbook = xlsxwriter.Workbook('Expenses01.xlsx')
worksheet = workbook.add_worksheet()

-----------------------------
My 1st way to import
# Open a file

path = "d:/YandexDisk/Фотки/"
destination = "d:/testcopy1/"
file_list = open("d:/testcopy1/list.xls", 'tw')
file_type = ".JPG"
files = os.listdir(path)
print(files)
print(len(files))

    for i in range(1, len(files), step):
        if files[i].endswith(file_type):
            source = path+files[i]
            shutil.copy(source, dest)
            file_list.write(files[i][:-len(file_type)] + '\t' + str(0.016*float(files[i][:-len(file_type)])) + '\n')
            print(path+files[i][:-len(file_type)])
            print((files[i][:-len(file_type)]))
            print((files[i][:-len(file_type)]))
            
-----------------------------------
FullFunc

def ImportNthFile(path, dest, file_type, path_to_excel_file, step):
    files = os.listdir(path)
    print(files)
    print(len(files))
    file_list = open(path_to_excel_file, 'tw')
    for i in range(1, len(files), step):
        if files[i].endswith(file_type):
            source = path+files[i]
            shutil.copy(source, dest)
            file_list.write(files[i][:-len(file_type)] + '\t' + str(0.016*float(files[i][:-len(file_type)])) + '\n')
            print(path+files[i][:-len(file_type)])
            print((files[i][:-len(file_type)]))
            print((files[i][:-len(file_type)]))

ImportNthFile('f:/vid/', 'f:/vid_test/', '.jpg', 'f:/vid_test/data/list.xls')
"""

"""
----------------------------------------------------
Last modification of programm, but it is not optimized


def CopyEveryNthFile(path, dest, file_type, step):
    files = os.listdir(path)
    print(files)
    print(len(files))
    #file_list = open(path_to_excel_file, 'tw')
    #workbook = xlsxwriter.Workbook(path_to_excel_file)
    #file_list = workbook.add_worksheet()
    for i in range(1, len(files), step):
        if files[i].endswith(file_type):
            source = path+files[i]
            shutil.copy(source, dest)
    return path, file_type, step


def WriteTimetable(path, step, file_type, path_to_excel_file):
    files = os.listdir(path)
    workbook = xlsxwriter.Workbook(path_to_excel_file)
    file_list = workbook.add_worksheet()
    for i in range(1, len(files), step):
        if files[i].endswith(file_type):
            file_list.write(files[i][:-len(file_type)] + '\t' + str(0.016 * float(files[i][:-len(file_type)])) + '\n')
            print(path + files[i][:-len(file_type)])
            print((files[i][:-len(file_type)]))
            print((files[i][:-len(file_type)]))

#'f:/vid_test/data/list.xls'

CopyEveryNthFile('f:/vid/', 'f:/vid_test/', '.jpg', 60)
print(CopyEveryNthFile())

"""


'''
        self.path = 'f:/vid/'
        self.file_ext = '.jpg' #ext- расширение
        self.step = 60
        self.dest_path = 'f:/vid_test/'
        self.data_path = 'f:/vid_test/data/'
    '''

class File:

    def __init__(self, path, file_ext, step, dest_path, data_path, fps):
        self.path = path
        self.file_ext = file_ext #ext- расширение
        self.step = step
        self.dest_path = dest_path
        self.data_path = data_path
        self.files = os.listdir(self.path)
        self.fps = fps

    def CopyEveryNthFile(self):

        for i in range(0, len(self.files), self.step):
            if self.files[i].endswith(self.file_ext) or self.files[i].endswith(self.file_ext.upper()):
                source = self.path+self.files[i]
                shutil.copy(source, self.dest_path)

    def WriteData(self):

        workbook = xlsxwriter.Workbook(self.data_path + 'data.xlsx')
        file_list = workbook.add_worksheet()
        file_list.write('A1', 'Image_Name', workbook.add_format({'bold': True}))
        file_list.write('B1', 'Frame_№', workbook.add_format({'bold': True}))
        file_list.write('C1', 'Time, ms', workbook.add_format({'bold': True}))
        row = 1
        col = 0
        for i in range(0, len(self.files), self.step):
            if self.files[i].endswith(self.file_ext) or self.files[i].endswith(self.file_ext.upper()):
                file_list.write(row, col, self.files[i])
                file_list.write(row, col + 1, float(self.files[i][:-len(self.file_ext)]))
                file_list.write(row, col + 2, 1000/self.fps*float(self.files[i][:-len(self.file_ext)]))
                row += 1
        workbook.close()

im = File('f:/NikNik/20july/MOV_0850img/', '.jpg', 60, 'f:/NikNik/20july/MOV_0850imgedit/', 'f:/NikNik/20july/MOV_0850imgedit/', 60)
im.CopyEveryNthFile()
im.WriteData()
