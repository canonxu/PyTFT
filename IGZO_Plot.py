# -*- coding:utf-8 -*-
#author ： 徐佳能, Canon Xu, a graduate student from Dept.EE of XJTU
#Email: canonxu@yeah.net
#Finish Time：2015/4/18

import os, time
import threading
from multiprocessing import Process
from IGZO_Data import Excel_Analysis
import numpy as np
import matplotlib.pyplot as plt


class IGZO_Array_Plot(object):
    #使用该类进行实例化的时候，传入可变参数*Fname，为两个及以上的文件名
    def __init__(self, *Fname):
        self.Fname=Fname


        #尝试用两个线程解决plt.show()不能同时显示两幅图的问题。失败。

        # t1 = threading.Thread(target = self.Trans_ArrayPlot(),name = 'Trans')
        # t1.start()
        # t1.join()
        # t2 = threading.Thread(target = self.VSM_ArrayPlot(),name = 'VSM')
        # t2.start()
        # t2.join()

        #尝试用两个进程解决plt.show()不能同时显示两幅图的问题。失败。
        # p1 = Process(target = self.Trans_ArrayPlot(),args=())
        # p1.start()
        # p1.join()
        # p2 = Process(target = self.VSM_ArrayPlot(),args=())
        # p2.start()
        # p2.join()

        #尝试用PIL中的image.show()函数同时显示两幅图。失败。
        # import Image
        # image1 = Image.open(fname0.split('_')[0]+'_Trans'+'.png')
        # image1.show()
        # image2 = Image.open(fname0.split('_')[0]+'_Para'+'.png')
        # image2.show()

        #plt.show()是一个烦人的函数。程序执行到此，显示一个图然后就暂停，手动关闭此图后，程序继续进行。
        #所以，一般最后一步才进行plt.show操作。

        #plt.show()的最终解决方案为：每个需要单独画出的图前，添加plt.figure，程序最后，一起进行ply.show()



    #做出转移特性曲线系列图，并存入指定文件夹中
    def Trans_ArrayPlot(self):
        root_dir = os.path.abspath('.')
        dir_name = self.Fname[0].split('_')[0]
        if not os.path.exists(dir_name):
            os.path.join(root_dir, dir_name )
            os.mkdir(dir_name)
        else:
             pass
        os.chdir(root_dir)
        plt.figure()

        #作图

        for i in np.arange(0,len(self.Fname)):
            self.Trans_Plot(self.Fname[i])

        os.chdir(dir_name)
        plt.savefig(self.Fname[0].split('_')[0]+'_Trans')
        os.chdir(root_dir)


    #做出参数提取系列图，并存入指定文件夹中
    def VSM_ArrayPlot(self):
        root_dir = os.path.abspath('.')
        dir_name = self.Fname[0].split('_')[0]
        if not os.path.exists(dir_name):
            os.path.join(root_dir, dir_name )
            os.mkdir(dir_name)
            print dir_name
        else:
             pass
        os.chdir(root_dir)
        plt.figure()

        #作图
        self.VSM_Plot()

        os.chdir(dir_name)
        plt.savefig(self.Fname[0].split('_')[0]+'_Para')
        os.chdir(root_dir)


    #做出转移特性曲线的单个图
    def Trans_Plot(self,fname):
        x = Excel_Analysis(fname).TransferExcel()[0]
        y = Excel_Analysis(fname).TransferExcel()[1]
        plt.semilogy(x, y, 's-', label = (fname.split('.')[0]), lw = 3)
        plt.legend(loc = 'lower right')
        plt.axis([-25, 45, 1E-12, 1E-4])
        plt.xlabel('VG',fontsize=20 )
        plt.ylabel('ID', fontsize=20)
        plt.title('Transfer Curve', fontsize=30)


    #做出参数曲线的单个图
    def VSM_Plot(self):
        x = np.arange(0, len(self.Fname))
        y = []
        for i in np.arange(0, 3):
            y.append([])
            for j in np.arange(0, len(self.Fname)):
                ins = Excel_Analysis(self.Fname[j])
                y[i].append(ins.Extraction()[i])

        #Vth变化图
        plt.subplot(3,1,1,label ='V' )
        plt.plot(x, y[0], 'bs-')
        plt.ylabel(u'Vth')
        # plt.legend( u'Vth', loc = 'upper left', handlelength=2)
        plt.xticks(x, ([]),)
        plt.title('Parameter Extraction Curve', fontsize=30)

        #SS变化图
        plt.subplot(3,1,2,label ='V' )
        plt.plot(x, y[1], 'ks-')
        plt.ylabel(u'SS')
        # plt.legend(labels = 'S', loc = 'upper left', handlelength=2)
        plt.xticks(x, ([]),)

        #Mobility变化图
        plt.subplot(3,1,3,label ='V' )
        plt.plot(x, y[2], 'rs-')
        # plt.legend(labels = 'M', loc = 'upper left', handlelength=2)
        xtick_list = []
        for i in range(0, len(self.Fname)):
            xtick_list.append(self.Fname[i].split('.')[0])
        plt.xticks(x, xtick_list, rotation = 15,)
        plt.ylabel(u'Mobility')

class IGZO_SingleTrans_Plot(object):
    def __init__(self, fname):
        self.fname = fname

    #做出转移特性曲线，其中曲线默认参数为坐标轴界点：left= -25, right = 45, low = 1E-12, high = 1E-4
    def Trans_Plot(self, left= -25, right = 45, low = 1E-12, high = 1E-4):
        x = Excel_Analysis(self.fname).TransferExcel()[0]
        y = Excel_Analysis(self.fname).TransferExcel()[1]
        para = Excel_Analysis(self.fname).Extraction()
        plt.figure()
        plt.semilogy(x, y, 's-', label = (self.fname.split('.')[0]), lw = 3)
        plt.legend(loc = 'lower right',handlelength=4)
        plt.axis([left, right, low, high]) # ([-25, 45, 1E-14, 1E-4])
        plt.xlabel('VG',fontsize=20 )
        plt.ylabel('ID', fontsize=20)
        plt.text(20, 1E-11,'Vth: '+str(para[0])+'   '+'SS: '+str(para[1])+'\n'+'Mobility: '+str(para[2])\
            +'\n'+'On/Off: '+str(para[3]), fontsize=14)
        plt.grid(True)
        plt.title('Transfer Curve', fontsize=30)



if __name__ == '__main__':

    #一族曲线测试
     Ar_plot =  IGZO_Array_Plot('Ar_initial.xls','Ar_15min.xls','Ar_30min.xls','Ar_45min.xls')
     Ar_plot.Trans_ArrayPlot()
     Ar_plot.VSM_ArrayPlot()

     #单个曲线测试
     N2_plot = IGZO_SingleTrans_Plot('N2_10min.xls')
     N2_plot.Trans_Plot()

     plt.show()





