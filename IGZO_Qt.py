# -*- coding:utf-8 -*-
#author ： 徐佳能, Canon Xu, a graduate student from Dept.EE of XJTU
#Email: canonxu@yeah.net
#Finish Time：2015/4/18

import os, sys,time
from PyQt4 import QtGui, QtCore
from IGZO_QtUi import Ui_Form
from IGZO_Data import Excel_Analysis
import IGZO_Plot

class MyWin(QtGui.QWidget, Ui_Form):
    def __init__(self):
        super(MyWin, self).__init__()
        self.setupUi(self)
        self.setWindowTitle(u'IGZO TFT分析软件')
        self.setWindowIcon(QtGui.QIcon('Transfer1.png'))


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    mywin = MyWin()
    mywin.show()
    app.exec_()
