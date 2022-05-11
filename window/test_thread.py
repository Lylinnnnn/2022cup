#coding=gbk
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

sec = 0

# 编写工作线程
class WorkThread(QThread):
    timer = pyqtSignal()
    end = pyqtSignal()

    # 重构内部方法run
    def run(self):
        while True:
            self.sleep(1)  # 休眠1秒
            if sec == 5:
                self.end.emit()  # 释放end信号
                break
            self.timer.emit()  # 发送timer信号


class Count(QWidget):
    def __init__(self):
        super(Count, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("使用线程类（QThread）编写计数器")
        self.resize(300, 120)

        layout = QVBoxLayout()
        # 数码管控件
        self.lcdNumber = QLCDNumber()
        layout.addWidget(self.lcdNumber)
        button = QPushButton("开始计数")
        layout.addWidget(button)
        # 创建我们自定义的工作线程
        self.workThread = WorkThread()

        # 通过点击按钮来启动工作线程
        button.clicked.connect(self.work)

        # 此处的timer和end信号都是我们在WorkThread自定义的信号
        # 注意观察它们两个的释放的逻辑
        self.workThread.timer.connect(self.countTime)
        self.workThread.end.connect(self.end)
        self.setLayout(layout)

    def countTime(self):
        global sec  # 将外部变量sec申明为全局变量
        sec += 1
        # 数码控件会显示sec存储的数字对应的数码管
        self.lcdNumber.display(sec)

    # 启动WorkThread工作线程
    def work(self):
        self.workThread.start()

    # 结束WorkThread工作线程
    def end(self):
        # 弹出一个消息对话框，参数为：self, 对话框名字， 对话框内容， 对话框按钮
        QMessageBox.information(self, "消息", "计数结束", QMessageBox.Ok)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Count()
    main.show()
    sys.exit(app.exec_())