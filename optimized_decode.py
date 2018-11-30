import os
import xlsxwriter
import cv2


class VideoDecode:

    def __init__(self, vid_path, filename, ext_path, file_ext, every_nth):
        self.vid_path = vid_path
        self.ext_path = self.vid_path + ext_path  # extracted
        self.data_path = self.ext_path + 'data/'
        self.filename = filename
        self.file_ext = file_ext
        self.every_nth = every_nth
        self.fps = 0

    def ensure_dir(self):
        dir_data = os.path.dirname(self.ext_path)
        dir_dest = os.path.dirname(self.data_path)
        if not os.path.exists(dir_data):
            os.makedirs(dir_data)
        if not os.path.exists(dir_dest):
            os.makedirs(dir_dest)

    def get_write(self):
        video = cv2.VideoCapture(self.vid_path + self.filename)
        num = 0
        ret = True
        self.fps = video.get(cv2.CAP_PROP_FPS)
        workbook = xlsxwriter.Workbook(self.data_path + 'data.xlsx')
        file_list = workbook.add_worksheet()
        file_list.write('A1', 'Image_Name', workbook.add_format({'bold': True}))
        file_list.write('B1', 'Frame_№', workbook.add_format({'bold': True}))
        file_list.write('C1', 'Time, ms', workbook.add_format({'bold': True}))
        row = 1
        col = 0
        while ret:
            ret, frame = video.read()
            if not num % self.every_nth:
                cv2.imwrite(self.ext_path + '/%010d' % num + self.file_ext, frame)
                file_list.write(row, col, '%010d' % num + self.file_ext)
                file_list.write(row, col + 1, float('%010d' % num))
                file_list.write(row, col + 2, 1000 / self.fps * float('%010d' % num))
                row += 1
            # print('Recording frame No ', num)
            num += 1
        workbook.close()


Vid = VideoDecode('F:/DIC/DimSap/DIC_metal/', '00201.mp4', 'edited201/', '.jpg', 20)
Vid.ensure_dir()
Vid.get_write()
