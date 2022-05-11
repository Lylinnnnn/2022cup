#coding=gbk
import sys
import os
# ��ȡ��ǰ�����ļ�����·��
current_dir = os.path.dirname(os.path.abspath(__file__))
# ����Ҫ����ģ������ļ�����ڵ�ǰ�ļ�Ŀ¼�ľ���·�����뵽sys.path��
sys.path.append(os.path.join(current_dir, ".."))
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtCore import QThread,pyqtSignal
import sys
import cv2
import numpy as np
from PIL import Image
from Camera import realsense

from modelNet.yolox.yolo import YOLO as STATICYOLO
from modelNet.yolox.predict import move_detect
from output import output_message
import time
import socket

result = ""


def returnSum(myDict):
    sum = 0
    for i in myDict:
        sum = sum + myDict[i]

    return sum
def deal_ans_lst(ans_lst,cishu):
    max_dic = {}
    sum_dic = {}
    max_num = {}
    sum_label = 0
    for ans in ans_lst:
        temp_sum = returnSum(ans)
        if sum_label<temp_sum:
            max_num = ans
            sum_label = temp_sum
        for name,num in ans.items():
            if sum_dic. __contains__(name):
                sum_dic[name]+=num
            else:
                sum_dic[name]=num
            if max_dic. __contains__(name):
                if max_dic[name]<num:
                    max_dic[name]=num
            else:
                max_dic[name]=num
    mean_dic = sum_dic.copy()
    for name,num in sum_dic.items():
        mean_dic[name] = int(sum_dic[name]/cishu+0.5)
    print('mean_before',mean_dic)
    for name,num in mean_dic.items():
        if num==0 and sum_dic[name]/cishu>0.3:
            print(name)
            mean_dic[name] = 1
    temp_dic = mean_dic.copy()
    for name, num in temp_dic.items():
        if num == 0:
            del mean_dic[name]
    print('max',max_dic)
    print('sum',sum_dic)
    print('mean_after',mean_dic)
    print('max_num',max_num)

    return mean_dic#max_num


class WorkThread_move(QThread):
    end = pyqtSignal()
    def __init__(self,static_yolo,pipeline):
        super(WorkThread_move, self).__init__()
        self._static_yolo = static_yolo
        self._pipeline  = pipeline
        self.id = bytes("YSZY001", 'UTF-8').hex()
        target_ip = '192.168.31.87'
        target_port = 6666
        my_ip = '192.168.31.87'
        my_port = 1352
        server_ip = target_ip
        servr_port = target_port

        self.tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_client.bind((my_ip, my_port))
        self.tcp_client.connect((server_ip, servr_port))

    # �ع��ڲ�����run
    def run(self):
        global result
        #####
        # д��ʱ����
        self.tcp_client.send(bytes.fromhex("00000000" + "00000007" + self.id))
        i=0
        start_time = time.time()
        end_time = time.time()
        img = realsense.get_data(pipeline=self._pipeline)
        img.save(r'F:\Final\1.png')
        ans_lst = []
        while end_time-start_time<20:
            img = realsense.get_data(pipeline=self._pipeline)
            res,result_str = move_detect(yolo=self._static_yolo,img=img)
            ans_lst.append(res)
            end_time = time.time()
            i+=1
        print(i)
        result,ans_len , hexstring = output_message.dict2str(deal_ans_lst(ans_lst,i))
        self.tcp_client.send(bytes.fromhex("00000001" + ans_len + hexstring))
        self.tcp_client.close()
        self.end.emit()  # �ͷ�end�ź�

class Ui_MainWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)  # ����Ĺ��캯��
        self._static_yolo = STATICYOLO()
        move_detect(yolo=self._static_yolo,img=Image.fromarray(np.zeros((640,480))))

        self.depth_color_flag = True
        self.need_color_depth_img = True
        self.pipeline = realsense.turnon_camera()
        self.workThread_move = WorkThread_move(self._static_yolo,self.pipeline)
        self.timer_camera = QtCore.QTimer()  # ���嶨ʱ�������ڿ�����ʾ��Ƶ��֡��

        self.set_ui()  # ��ʼ���������
        self.slot_init()  # ��ʼ���ۺ���
        self.init_camera()

    '''������沼��'''
    def set_ui(self):
        self.__layout_main = QtWidgets.QHBoxLayout()  # �ܲ���
        self.__layout_fun_button = QtWidgets.QVBoxLayout()  # ��������
        self.__layout_message_show = QtWidgets.QVBoxLayout()  # �����Ϣ��ʾ����
        self.button_open_camera = QtWidgets.QPushButton()
        self.button_change_camera = QtWidgets.QPushButton()
        self.label_show_message = QtWidgets.QLabel()
        self.label_show_state = QtWidgets.QLabel()
        self.label_show_round = QtWidgets.QLabel()
        '''��������'''
        label_font = QtGui.QFont()
        # ����
        label_font.setFamily('΢���ź�')
        # �Ӵ�
        label_font.setBold(False)
        # ��С
        label_font.setPointSize(13)

        edit_font = QtGui.QFont()
        # ����
        edit_font.setFamily('����')
        # �Ӵ�
        edit_font.setBold(False)
        # ��С
        edit_font.setPointSize(13)

        btn_font = QtGui.QFont()
        # ����
        btn_font.setFamily('����')
        # �Ӵ�
        btn_font.setBold(True)
        # ��С
        btn_font.setPointSize(13)
        '''���ð�ťֵ'''
        self.button_open_camera.setText("��ʼ")
        self.button_open_camera.setMinimumHeight(50)  # ���ð�����С
        self.button_open_camera.setFont(btn_font)

        self.button_change_camera.setText("�ı���ͼ")
        self.button_change_camera.setMinimumHeight(50)  # ���ð�����С
        self.button_change_camera.setFont(btn_font)
        '''���ñ�ǩֵ'''
        self.label_show_message.setText("ʶ���������")
        self.label_show_message.setFrameShape(QtWidgets.QFrame.Box)
        self.label_show_message.setFrameShadow(QtWidgets.QFrame.Raised)
        self.label_show_message.setFont(label_font)
        self.label_show_message.setAlignment(QtCore.Qt.AlignCenter)
        self.label_show_state.setText("ʶ��״̬�����")
        self.label_show_state.setFrameShape(QtWidgets.QFrame.Box)
        self.label_show_state.setFrameShadow(QtWidgets.QFrame.Raised)
        self.label_show_state.setFont(label_font)
        self.label_show_state.setAlignment(QtCore.Qt.AlignCenter)
        self.label_show_round.setText("������")
        self.label_show_round.setFrameShape(QtWidgets.QFrame.Box)
        self.label_show_round.setFrameShadow(QtWidgets.QFrame.Raised)
        self.label_show_round.setFont(label_font)
        self.label_show_round.setAlignment(QtCore.Qt.AlignCenter)
        self.label_show_round.setMaximumHeight(50)
        '''��Ϣ��ʾ'''
        self.label_show_camera = QtWidgets.QLabel()  # ������ʾ��Ƶ��Label
        self.label_show_camera.setFixedSize(641, 481)  # ����ʾ��Ƶ��Label���ô�СΪ641x481
        '''�����ʾ'''
        self.show_message_textedit = QTextEdit()
        self.show_message_textedit.setFont(edit_font)
        self.show_message_textedit.setMaximumWidth(320)
        self.show_message_textedit.setMaximumHeight(480)
        self.show_state_textedit = QTextEdit()
        self.show_state_textedit.setFont(edit_font)
        self.show_state_textedit.setMaximumWidth(320)
        self.show_state_textedit.setMaximumHeight(40)
        self.show_state_textedit.setText("����")
        self.show_state_textedit.setAlignment(QtCore.Qt.AlignCenter)

        '''�Ѱ������뵽����������'''
        self.__layout_fun_button.addWidget(self.label_show_round)
        self.__layout_fun_button.addWidget(self.button_open_camera)
        self.__layout_fun_button.addWidget(self.button_change_camera)

        '''�������Ϣ���뵽������'''
        self.__layout_message_show.addWidget(self.label_show_message)
        # self.__layout_message_show.addStretch(1)
        self.__layout_message_show.addWidget(self.show_message_textedit)
        # self.__layout_message_show.addStretch(2)
        self.__layout_message_show.addWidget(self.label_show_state)
        self.__layout_message_show.addWidget(self.show_state_textedit)
        # self.__layout_message_show.addStretch(1)
        '''��ĳЩ�ؼ����뵽�ܲ�����'''
        self.__layout_main.addWidget(self.label_show_camera)  # ��������ʾ��Ƶ��Label���뵽�ܲ�����
        self.__layout_main.addLayout(self.__layout_message_show)  # ��������ʾ��Ƶ��Label���뵽�ܲ�����
        self.__layout_main.addLayout(self.__layout_fun_button)  # �Ѱ������ּ��뵽�ܲ�����

        '''�ܲ��ֲ��úú�Ϳ��԰��ܲ�����Ϊ�����������溯��'''
        self.setLayout(self.__layout_main)  # ���ⲽ�Ż���ʾ���пؼ�

    '''��ʼ�����вۺ���'''
    def slot_init(self):
        self.workThread_move.end.connect(self.end)
        self.button_open_camera.clicked.connect(
            self.button_open_camera_clicked)  # ���ð���������������button_open_camera_clicked()
        self.button_change_camera.clicked.connect(
            self.button_change_camera_clicked)
        self.timer_camera.timeout.connect(self.show_camera)  # ����ʱ�������������show_camera()

    '''�ۺ���֮һ'''
    def init_camera(self):
        if self.timer_camera.isActive() == False:  # ����ʱ��δ����
            flag = True
            if flag != False:  # flag��ʾopen()�ɲ��ɹ�
                self.timer_camera.start(10)  # ��ʱ����ʼ��ʱ30ms�������ÿ��30ms������ͷ��ȡһ֡��ʾ
        else:
            self.timer_camera.stop()  # �رն�ʱ��
            self.label_show_camera.clear()  # �����Ƶ��ʾ����
    def show_camera(self):
        if self.depth_color_flag:
            self.image = realsense.get_camera_image(self.pipeline,self.depth_color_flag)
            show = cv2.resize(self.image, (640, 480))  # �Ѷ�����֡�Ĵ�С��������Ϊ 640x480
            show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)  # ��Ƶɫ��ת����RGB������������ʵ����ɫ
            showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0],
                                     QtGui.QImage.Format_RGB888)  # �Ѷ�ȡ������Ƶ���ݱ��QImage��ʽ
            self.label_show_camera.setPixmap(QtGui.QPixmap.fromImage(showImage))  # ����ʾ��Ƶ��Label�� ��ʾQImage
        else:
            self.image = realsense.get_camera_image(self.pipeline,self.depth_color_flag)
            show = cv2.resize(self.image, (640, 480))  # �Ѷ�����֡�Ĵ�С��������Ϊ 640x480
            showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0],
                                     QtGui.QImage.Format_RGB888)  # �Ѷ�ȡ������Ƶ���ݱ��QImage��ʽ
            self.label_show_camera.setPixmap(QtGui.QPixmap.fromImage(showImage))  # ����ʾ��Ƶ��Label�� ��ʾQImage

    '''����WorkThread�����߳�'''
    def work(self):
        self.workThread_move.start()
    def button_change_camera_clicked(self):
        if self.depth_color_flag:
            self.depth_color_flag = False
        else:
            self.depth_color_flag = True
    def button_open_camera_clicked(self):
        self.work()
        print("kaishi")
        self.show_state_textedit.setText("ʶ����")
        self.show_state_textedit.setAlignment(QtCore.Qt.AlignCenter)
    def end(self):
        self.show_state_textedit.setText("����")
        self.show_state_textedit.setAlignment(QtCore.Qt.AlignCenter)
        self.show_message_textedit.setText(result)
        file = open(r'F:\Final\result.txt', 'w')
        file.write(result)
        file.close()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)  # �̶��ģ���ʾ����Ӧ��
    ui = Ui_MainWindow()  # ʵ����Ui_MainWindow
    ui.show()  # ����ui��show()����ʾ��ͬ��show()��Դ�ڸ���QtWidgets.QWidget��
    sys.exit(app.exec_())  # ������䣬��������һ������
    realsense.turnoff_camera(ui.pipeline)
    
