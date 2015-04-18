# -*- coding:utf-8 -*-
import xlrd,xlwt
import os
import math
import matplotlib.pyplot as plt
import sys,time
from PyQt4 import QtGui, QtCore

#IGZO工艺参数
IGZO_W = 1000*1E-4
IGZO_L = 0.0275
IGZO_GiThick = 3E-5
IGZO_GiDieleCons = 3.5
IGZO_GiCap = 8.85*1E-14*IGZO_GiDieleCons/IGZO_GiThick


class MyWin(QtGui.QWidget):
    def __init__(self):
        super(MyWin, self).__init__()
        self.setWindowTitle(u'IGZO TFT分析软件')
        self.setWindowIcon(QtGui.QIcon('Transfer1.png'))
        self.resize(1000, 600)

        gridLayout = QtGui.QGridLayout()

        button_file = QtGui.QPushButton( u'浏览' )
        button_file.setFont(QtGui.QFont("Times",12))
        button_file.setFixedSize(100,30)
        gridLayout.addWidget( button_file, 0, 0 )
        self.connect( button_file, QtCore.SIGNAL( 'clicked()' ), self.Onbutton)

        dir = " E:\ "
        textfile_Dir = QtGui.QLineEdit(dir)
        textfile_Dir.setFixedSize(150,30)
        gridLayout.addWidget(textfile_Dir, 0,1)
        self.connect( textfile_Dir, QtCore.SIGNAL( 'clicked()' ), self.Onbutton)



        button_ok = QtGui.QPushButton( u'确认' )
        button_ok.setFont(QtGui.QFont("Times",12))
        button_ok.setFixedSize(100,30)
        gridLayout.addWidget( button_ok, 0, 2)
        self.connect( textfile_Dir, QtCore.SIGNAL( 'clicked()' ), self.Ok)



        label_argv1 = QtGui.QLabel(u'阈值电压Vth')
        label_argv2 = QtGui.QLabel(u'亚阈值摆幅SS')
        label_argv3 = QtGui.QLabel(u'开关态电流比Ion/Ioff')
        label_argv4 = QtGui.QLabel(u'迁移率Mobility')

        Out_Vth = 'Threshod Voltage'
        Out_SS = 'Subthread Swing'
        Out_Rate = 'Rate of On/Off Current'
        Out_Mobility = 'Mobility'
        textfile_Vth = QtGui.QLineEdit(Out_Vth)#str(self.Extraction()[0]))
        textfile_SS = QtGui.QLineEdit(Out_SS)#str(self.Extraction()[1]))
        textfile_Rate = QtGui.QLineEdit(Out_Rate)#str(self.Extraction()[2]))
        textfile_Mobility = QtGui.QLineEdit(Out_Mobility)#str(self.Extraction()[3]))

        gridLayout.addWidget(label_argv1,1,1)
        gridLayout.addWidget(label_argv2,2,1)
        gridLayout.addWidget(label_argv3,3,1)
        gridLayout.addWidget(label_argv4,4,1)

        gridLayout.addWidget(textfile_Vth,1,2)
        gridLayout.addWidget(textfile_SS,2,2)
        gridLayout.addWidget(textfile_Rate,3,2)
        gridLayout.addWidget(textfile_Mobility,4,2)

        self.setLayout(gridLayout)


    def Onbutton( self ):
        self.fname = QtGui.QFileDialog.getOpenFileName( self, self.tr('Open Excel File'))
        from os.path import isfile
        if isfile(self.fname):
            dir_text = str(self.fname)
            print dir_text


    def Ok(self):
            Out_Vth = str(self.Extraction()[0])
            Out_SS = str(self.Extraction()[1])
            Out_Rate = str(self.Extraction()[2])
            Out_Mobility = str(self.Extraction()[3])



    def TransferExcel(self):
        fname = self.Onbutton.fname
        Data = xlrd.open_workbook(fname)
    #   Transfer_table = Data.sheet_by_name(u"表单01")
    #   Transfer_table = Data.sheets()[0]
        Transfer_table = Data.sheet_by_index(1) #三种获取表单的方法
    #   print Transfer_table.nrows, Transfer_table.ncols
        Id_TestValue = Transfer_table.col_values(2)
        Vg_Value = Transfer_table.col_values(1)
        Vg = []
        for ele in Vg_Value:
            if isinstance(ele, float):
                Vg.append(ele)
        Id_AbsValue = []
        for ele in Id_TestValue:
            if isinstance(ele, float):
                Id_AbsValue.append(abs(ele))
        TransferExcel = [Vg, Id_AbsValue]
        return TransferExcel

    def TransferPlot(self):
        fname = self.Onbutton.fname
        x = self.TransferExcel()[0]
        y = self.TransferExcel()[1]
        plt.semilogy(x, y, 's-', label = (fname.split('.')[0]), lw = 3)
        plt.legend(loc = 'lower right')
        plt.axis([-25, 45, 1E-12, 1E-4])
        plt.xlabel('VG',fontsize=20 )
        plt.ylabel('ID', fontsize=20)
        plt.title('Transfer Curve', fontsize=30)
        plt.savefig("Tc.png", dpi = 75)
        plt.show()

    def Extraction(self):
        fname = self.Onbutton.fname
        Id_AbsValue = self.TransferExcel()[1]
        Vg = self.TransferExcel()[0]

        #提取Vth参数
        Vth = 0
        for i in range(1, 120):
            target = 1E-9*(IGZO_W/IGZO_L)
            if (target-Id_AbsValue[i])*(target-Id_AbsValue[i+1]) <= 0:
                if Vg[i] > 0:
                    Vth = math.floor(2*Vg[i])/2
                else:
                    Vth =  math.ceil(2*Vg[i])/2
        # print 'The value of Vth:', Vth

        #提取亚阈值摆幅SS
        for i in range(1, 120):
            target = 1E-10
            if (target-Id_AbsValue[i])*(target-Id_AbsValue[i+1]) <= 0:
                if Vg[i] > 0:
                    s1 = math.floor(2*Vg[i])/2
                else:
                    s1 = math.ceil(2*Vg[i])/2
        for i in range(1, 120):
            target = 1E-8
            if (target-Id_AbsValue[i])*(target-Id_AbsValue[i+1]) <= 0:
                if Vg[i] < 0:
                    s2 = math.ceil(2*Vg[i])/2
                else:
                    s2 = math.floor(2*Vg[i])/2
        SS = abs(s1-s2)/2
        # print 'The value of SS:', SS

        #提取开关电流比Ion/Ioff参数:
        Ioff = sum((Id_AbsValue[4] ,Id_AbsValue[5], Id_AbsValue[6], Id_AbsValue[7], Id_AbsValue[8]))/5
        Ion = sum((Id_AbsValue[115], Id_AbsValue[116], Id_AbsValue[117], Id_AbsValue[118], Id_AbsValue[119]))/5
        Rate_OnOff = Ion/Ioff
        # print 'The rate of On/Off: %e' %Rate_OnOff

        #提取迁移率Mobility参数
        Id_SqrtValue = map(math.sqrt, Id_AbsValue)
        Differential = [0]
        for i in range(1, 120):
            Differential.append((Id_SqrtValue[i]-Id_SqrtValue[i-1])/(Vg[i]-Vg[i-1]))
        Mobility = (max(Differential[20:100])**2)*2*IGZO_L/(IGZO_W*IGZO_GiCap)
        # print 'The mobility is :', Mobility

        parameter = [Vth, SS, Rate_OnOff, Mobility]
        return parameter

app = QtGui.QApplication(sys.argv)
mywin = MyWin()
mywin.show()
app.exec_()