import os
import shutil
import xlsxwriter
import cv2

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


class VideoDecode:

    def __init__(self, vid_path, filename, ext_path, file_ext):
        self.vid_path = vid_path
        self.ext_path = ext_path  # extracted
        self.filename = filename
        self.file_ext = file_ext

    def ensure_dir(self):
        directory = os.path.dirname(self.ext_path)
        if not os.path.exists(directory):
            os.makedirs(directory)

    def get(self):
        video = cv2.VideoCapture(self.vid_path + self.filename)
        num = 0
        ret = True
        while ret:
            ret, frame = video.read()
            cv2.imwrite(self.vid_path + self.ext_path + '/%010d' % num + self.file_ext, frame)
            print('Recording frame No ', num)
            num += 1


class File:

    def __init__(self, path, file_ext, step, dest_path):
        self.path = path
        self.file_ext = file_ext  # ext- расширение
        self.step = step
        self.dest_path = dest_path
        self.data_path = dest_path + 'data/'
        self.files = sorted(os.listdir(self.path))
        self.fps = cv2.CAP_PROP_FPS

    def ensure_dir(self):
        dir_data = os.path.dirname(self.data_path)
        dir_dest = os.path.dirname(self.dest_path)
        if not os.path.exists(dir_data):
            os.makedirs(dir_data)
        if not os.path.exists(dir_dest):
            os.makedirs(dir_dest)

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


Vid = VideoDecode('./', 'big_buck_bunny_720p_5mb.mp4', './edited/', '.jpg')
Vid.ensure_dir()
Vid.get()
im = File(Vid.ext_path, Vid.file_ext, 60, './edited_numbered/')
im.ensure_dir()
im.CopyEveryNthFile()
im.WriteData()
