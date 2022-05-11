import sys
import os
# 获取当前代码文件绝对路径
current_dir = os.path.dirname(os.path.abspath(__file__))
# 将需要导入模块代码文件相对于当前文件目录的绝对路径加入到sys.path中
sys.path.append(os.path.join(current_dir, ".."))
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtCore import QThread,pyqtSignal
import sys
import cv2

from Camera import realsense

class Ui_MainWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)  # 父类的构造函数

        self.depth_color_flag = True
        self.need_color_depth_img = True
        self.pipeline = realsense.turnon_camera()
        self.timer_camera = QtCore.QTimer()  # 定义定时器，用于控制显示视频的帧率

        self.set_ui()  # 初始化程序界面
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
        self.label_show_round.setText("第三轮")
        self.label_show_round.setFrameShape(QtWidgets.QFrame.Box)
        self.label_show_round.setFrameShadow(QtWidgets.QFrame.Raised)
        self.label_show_round.setFont(label_font)
        self.label_show_round.setAlignment(QtCore.Qt.AlignCenter)
        self.label_show_round.setMaximumHeight(50)
        '''信息显示'''
        self.label_show_camera = QtWidgets.QLabel()  # 定义显示视频的Label
        self.label_show_camera.setFixedSize(641, 481)  # 给显示视频的Label设置大小为641x481
        '''输出显示'''
        self.show_message_textedit = QTextEdit()
        self.show_message_textedit.setFont(edit_font)
        self.show_message_textedit.setMaximumWidth(320)
        self.show_message_textedit.setMaximumHeight(480)
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

    def button_change_camera_clicked(self):
        if self.depth_color_flag:
            self.depth_color_flag = False
        else:
            self.depth_color_flag = True
    def button_open_camera_clicked(self):
        print("kaishi")
        self.show_state_textedit.setText("识别中")
        self.show_state_textedit.setAlignment(QtCore.Qt.AlignCenter)
    def end(self):
        self.show_state_textedit.setText("结束")
        self.show_state_textedit.setAlignment(QtCore.Qt.AlignCenter)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)  # 固定的，表示程序应用
    ui = Ui_MainWindow()  # 实例化Ui_MainWindow
    ui.show()  # 调用ui的show()以显示。同样show()是源于父类QtWidgets.QWidget的
    sys.exit(app.exec_())  # 不加这句，程序界面会一闪而过
    realsense.turnoff_camera(ui.pipeline)
    
