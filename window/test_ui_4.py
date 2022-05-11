#coding=gbk
import sys
import os
# 获取当前代码文件绝对路径
current_dir = os.path.dirname(os.path.abspath(__file__))
# 将需要导入模块代码文件相对于当前文件目录的绝对路径加入到sys.path中
sys.path.append(os.path.join(current_dir, ".."))
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtCore import QThread,pyqtSignal
import sys
import cv2
import numpy as np
from PIL import Image
from Camera import realsense
import socket
from modelNet.classifier.classification import Classification as  CLASSIFIER
from modelNet.yolox.yolo import YOLO as STATICYOLO
from modelNet.yolox.predict import static_detect,move_detect
from output import output_message
import time

def deal_ans_lst(ans_lst,cishu):
    max_dic = {}
    sum_dic = {}
    for ans in ans_lst:
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
    print(mean_dic)
    for name,num in mean_dic.items():
        if num==0 and sum_dic[name]/cishu>0.3:
            print(name)
            mean_dic[name] = 1
    temp_dic = mean_dic.copy()
    for name, num in temp_dic.items():
        if num == 0:
            del mean_dic[name]
    print(max_dic)
    print(sum_dic)
    print(mean_dic)
    return mean_dic

def merge_dic(res1,res2,res3):
    ans = {}
    for name,num in res1.items():
        if ans. __contains__(name):
            ans[name]+=num
        else:
            ans[name]=num
    for name,num in res2.items():
        if ans. __contains__(name):
            ans[name]+=num
        else:
            ans[name]=num
    for name,num in res3.items():
        if ans. __contains__(name):
            ans[name]+=num
        else:
            ans[name]=num
    return ans

result = ""

class WorkThread_move(QThread):
    end = pyqtSignal()
    middle = pyqtSignal()
    middle_end = pyqtSignal()
    def __init__(self,static_yolo,classifier,pipeline,label_show_camera,edit):
        super(WorkThread_move, self).__init__()
        self._static_yolo = static_yolo
        self._classifier = classifier
        self._pipeline  = pipeline
        self.label_show_camera = label_show_camera
        self.pixmap = QPixmap('F:\Final/show.jpg')
        self.id = bytes("YSZY001", 'UTF-8').hex()
        target_ip = '192.168.31.87'
        target_port = 6666
        my_ip = '192.168.31.87'
        my_port = 1240
        server_ip = target_ip
        servr_port = target_port

        self.tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_client.bind((my_ip, my_port))
        self.tcp_client.connect((server_ip, servr_port))

    # 重构内部方法run
    def run(self):
        global result
        self.tcp_client.send(bytes.fromhex("00000000" + "00000007" + self.id))
        img = realsense.get_data(pipeline=self._pipeline)
        res1,_ = static_detect(self._static_yolo,self._classifier,img)
        self.middle.emit()
        self.label_show_camera.setPixmap(self.pixmap)
        time.sleep(5)
        self.label_show_camera.clear()
        self.middle_end.emit()

        img = realsense.get_data(pipeline=self._pipeline)
        res2,_ = static_detect(self._static_yolo,self._classifier,img)
        self.middle.emit()
        self.label_show_camera.setPixmap(self.pixmap)
        time.sleep(5)
        self.label_show_camera.clear()
        self.middle_end.emit()


        i=0
        start_time = time.time()
        end_time = time.time()
        img = realsense.get_data(pipeline=self._pipeline)
        ans_lst = []
        while end_time-start_time<5:
            img = realsense.get_data(pipeline=self._pipeline)
            res,result_str = move_detect(yolo=self._static_yolo,img=img)
            ans_lst.append(res)
            end_time = time.time()
            i+=1
        res3 = deal_ans_lst(ans_lst,i)
        print(res1)
        print(res2)
        print(res3)
        ans = merge_dic(res1,res2,res3)
        print(ans)
        result, ans_len, hexstring = output_message.dict2str(ans)
        self.tcp_client.send(bytes.fromhex("00000001" + ans_len + hexstring))

        self.tcp_client.close()
        self.end.emit()  # 释放end信号

class Ui_MainWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)  # 父类的构造函数
        self.set_ui()  # 初始化程序界面
        self._static_yolo = STATICYOLO()
        self._classifier = CLASSIFIER()
        static_detect(self._static_yolo,self._classifier,Image.fromarray(np.zeros((640,480))))

        self.depth_color_flag = True
        self.need_color_depth_img = True
        self.pipeline = realsense.turnon_camera()
        self.workThread_move = WorkThread_move(self._static_yolo,self._classifier,self.pipeline,self.label_show_state_png,self.show_state_textedit)
        self.timer_camera = QtCore.QTimer()  # 定义定时器，用于控制显示视频的帧率
        # self.pixmap = QPixmap('F:\Final\show.jpg')

        self.slot_init()  # 初始化槽函数
        self.init_camera()

    '''程序界面布局'''
    def set_ui(self):
        self.__layout_main = QtWidgets.QHBoxLayout()  # 总布局
        self.__layout_fun_button = QtWidgets.QVBoxLayout()  # 按键布局
        self.__layout_message_show = QtWidgets.QVBoxLayout()  # 输出信息显示布局
        self.button_open_camera = QtWidgets.QPushButton()
        self.button_change_camera = QtWidgets.QPushButton()
        self.label_show_message = QtWidgets.QLabel()
        self.label_show_state = QtWidgets.QLabel()
        self.label_show_round = QtWidgets.QLabel()
        '''设置字体'''
        label_font = QtGui.QFont()
        # 字体
        label_font.setFamily('微软雅黑')
        # 加粗
        label_font.setBold(False)
        # 大小
        label_font.setPointSize(13)

        edit_font = QtGui.QFont()
        # 字体
        edit_font.setFamily('宋体')
        # 加粗
        edit_font.setBold(False)
        # 大小
        edit_font.setPointSize(13)

        btn_font = QtGui.QFont()
        # 字体
        btn_font.setFamily('黑体')
        # 加粗
        btn_font.setBold(True)
        # 大小
        btn_font.setPointSize(13)
        '''设置按钮值'''
        self.button_open_camera.setText("开始")
        self.button_open_camera.setMinimumHeight(50)  # 设置按键大小
        self.button_open_camera.setFont(btn_font)

        self.button_change_camera.setText("改变视图")
        self.button_change_camera.setMinimumHeight(50)  # 设置按键大小
        self.button_change_camera.setFont(btn_font)
        '''设置标签值'''
        self.label_show_message.setText("识别结果输出区")
        self.label_show_message.setFrameShape(QtWidgets.QFrame.Box)
        self.label_show_message.setFrameShadow(QtWidgets.QFrame.Raised)
        self.label_show_message.setFont(label_font)
        self.label_show_message.setAlignment(QtCore.Qt.AlignCenter)
        self.label_show_state.setText("识别状态输出区")
        self.label_show_state.setFrameShape(QtWidgets.QFrame.Box)
        self.label_show_state.setFrameShadow(QtWidgets.QFrame.Raised)
        self.label_show_state.setFont(label_font)
        self.label_show_state.setAlignment(QtCore.Qt.AlignCenter)
        self.label_show_round.setText("第四轮")
        self.label_show_round.setFrameShape(QtWidgets.QFrame.Box)
        self.label_show_round.setFrameShadow(QtWidgets.QFrame.Raised)
        self.label_show_round.setFont(label_font)
        self.label_show_round.setAlignment(QtCore.Qt.AlignCenter)
        self.label_show_round.setMaximumHeight(50)
        '''信息显示'''
        self.label_show_camera = QtWidgets.QLabel()  # 定义显示视频的Label
        self.label_show_state_png = QtWidgets.QLabel()
        self.label_show_camera.setFixedSize(641, 481)  # 给显示视频的Label设置大小为641x481
        self.label_show_state_png.setFixedSize(151,151)
        '''输出显示'''
        self.show_message_textedit = QTextEdit()
        self.show_message_textedit.setFont(edit_font)
        self.show_message_textedit.setMaximumWidth(320)
        self.show_message_textedit.setMaximumHeight(480)
        # self.show_state_textedit = QTextEdit()
        # self.show_state_textedit.setFont(edit_font)
        # self.show_state_textedit.setMaximumWidth(320)
        # self.show_state_textedit.setMaximumHeight(40)
        # self.show_state_textedit.setText("空闲")
        # self.show_state_textedit.setAlignment(QtCore.Qt.AlignCenter)
        self.show_state_textedit = QTextEdit()
        self.show_state_textedit.setFont(edit_font)
        self.show_state_textedit.setMaximumWidth(320)
        self.show_state_textedit.setMaximumHeight(40)
        self.show_state_textedit.setText("空闲")
        self.show_state_textedit.setAlignment(QtCore.Qt.AlignCenter)

        '''把按键加入到按键布局中'''
        self.__layout_fun_button.addWidget(self.label_show_round)
        self.__layout_fun_button.addWidget(self.button_open_camera)
        self.__layout_fun_button.addWidget(self.button_change_camera)
        self.__layout_fun_button.addWidget(self.label_show_state_png)

        '''把输出信息加入到布局中'''
        self.__layout_message_show.addWidget(self.label_show_message)
        # self.__layout_message_show.addStretch(1)
        self.__layout_message_show.addWidget(self.show_message_textedit)
        # self.__layout_message_show.addStretch(2)
        self.__layout_message_show.addWidget(self.label_show_state)
        self.__layout_message_show.addWidget(self.show_state_textedit)
        # self.__layout_message_show.addStretch(1)
        '''把某些控件加入到总布局中'''
        self.__layout_main.addWidget(self.label_show_camera)  # 把用于显示视频的Label加入到总布局中
        self.__layout_main.addLayout(self.__layout_message_show)  # 把用于显示视频的Label加入到总布局中
        self.__layout_main.addLayout(self.__layout_fun_button)  # 把按键布局加入到总布局中

        '''总布局布置好后就可以把总布局作为参数传入下面函数'''
        self.setLayout(self.__layout_main)  # 到这步才会显示所有控件

    '''初始化所有槽函数'''
    def slot_init(self):
        self.workThread_move.end.connect(self.end)
        self.workThread_move.middle.connect(self.middle)
        self.workThread_move.middle_end.connect(self.middle_end)

        self.button_open_camera.clicked.connect(
            self.button_open_camera_clicked)  # 若该按键被点击，则调用button_open_camera_clicked()
        self.button_change_camera.clicked.connect(
            self.button_change_camera_clicked)
        self.timer_camera.timeout.connect(self.show_camera)  # 若定时器结束，则调用show_camera()

    '''槽函数之一'''
    def init_camera(self):
        if self.timer_camera.isActive() == False:  # 若定时器未启动
            flag = True
            if flag != False:  # flag表示open()成不成功
                self.timer_camera.start(10)  # 定时器开始计时30ms，结果是每过30ms从摄像头中取一帧显示
        else:
            self.timer_camera.stop()  # 关闭定时器
            self.label_show_camera.clear()  # 清空视频显示区域
    def show_camera(self):
        if self.depth_color_flag:
            self.image = realsense.get_camera_image(self.pipeline,self.depth_color_flag)
            show = cv2.resize(self.image, (640, 480))  # 把读到的帧的大小重新设置为 640x480
            show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)  # 视频色彩转换回RGB，这样才是现实的颜色
            showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0],
                                     QtGui.QImage.Format_RGB888)  # 把读取到的视频数据变成QImage形式
            self.label_show_camera.setPixmap(QtGui.QPixmap.fromImage(showImage))  # 往显示视频的Label里 显示QImage
        else:
            self.image = realsense.get_camera_image(self.pipeline,self.depth_color_flag)
            show = cv2.resize(self.image, (640, 480))  # 把读到的帧的大小重新设置为 640x480
            showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0],
                                     QtGui.QImage.Format_RGB888)  # 把读取到的视频数据变成QImage形式
            self.label_show_camera.setPixmap(QtGui.QPixmap.fromImage(showImage))  # 往显示视频的Label里 显示QImage

    '''启动WorkThread工作线程'''
    def work_move(self):
        self.workThread_move.start()
    def button_change_camera_clicked(self):
        if self.depth_color_flag:
            self.depth_color_flag = False
        else:
            self.depth_color_flag = True
    def button_open_camera_clicked(self):
        self.work_move()
        print("kaishi")
        self.show_state_textedit.setText("识别中")
        self.show_state_textedit.setAlignment(QtCore.Qt.AlignCenter)

    def end(self):
        self.show_state_textedit.setText("结束")
        self.show_state_textedit.setAlignment(QtCore.Qt.AlignCenter)
        self.show_message_textedit.setText(result)
        file = open(r'F:\Final\result.txt', 'w')
        file.write(result)
        file.close()
    def middle(self):
        self.show_state_textedit.setText("待转动")
        self.show_state_textedit.setAlignment(QtCore.Qt.AlignCenter)

    def middle_end(self):
        self.show_state_textedit.setText("识别中")
        self.show_state_textedit.setAlignment(QtCore.Qt.AlignCenter)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)  # 固定的，表示程序应用
    ui = Ui_MainWindow()  # 实例化Ui_MainWindow
    ui.show()  # 调用ui的show()以显示。同样show()是源于父类QtWidgets.QWidget的
    sys.exit(app.exec_())  # 不加这句，程序界面会一闪而过
