#coding=gbk
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

sec = 0

# ��д�����߳�
class WorkThread(QThread):
    timer = pyqtSignal()
    end = pyqtSignal()

    # �ع��ڲ�����run
    def run(self):
        while True:
            self.sleep(1)  # ����1��
            if sec == 5:
                self.end.emit()  # �ͷ�end�ź�
                break
            self.timer.emit()  # ����timer�ź�


class Count(QWidget):
    def __init__(self):
        super(Count, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("ʹ���߳��ࣨQThread����д������")
        self.resize(300, 120)

        layout = QVBoxLayout()
        # ����ܿؼ�
        self.lcdNumber = QLCDNumber()
        layout.addWidget(self.lcdNumber)
        button = QPushButton("��ʼ����")
        layout.addWidget(button)
        # ���������Զ���Ĺ����߳�
        self.workThread = WorkThread()

        # ͨ�������ť�����������߳�
        button.clicked.connect(self.work)

        # �˴���timer��end�źŶ���������WorkThread�Զ�����ź�
        # ע��۲������������ͷŵ��߼�
        self.workThread.timer.connect(self.countTime)
        self.workThread.end.connect(self.end)
        self.setLayout(layout)

    def countTime(self):
        global sec  # ���ⲿ����sec����Ϊȫ�ֱ���
        sec += 1
        # ����ؼ�����ʾsec�洢�����ֶ�Ӧ�������
        self.lcdNumber.display(sec)

    # ����WorkThread�����߳�
    def work(self):
        self.workThread.start()

    # ����WorkThread�����߳�
    def end(self):
        # ����һ����Ϣ�Ի��򣬲���Ϊ��self, �Ի������֣� �Ի������ݣ� �Ի���ť
        QMessageBox.information(self, "��Ϣ", "��������", QMessageBox.Ok)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Count()
    main.show()
    sys.exit(app.exec_())