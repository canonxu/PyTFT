# -*- coding: utf-8 -*-
#author ： 徐佳能, Canon Xu, a graduate student from Dept.EE of SJTU
#Email: canonxu@yeah.net
#Finish Time：2015/4/18

import matplotlib.pyplot as plt
from  IGZO_Data import Data_Analysis
import numpy as np
from scipy import linalg
import  math


class Vth_Fit(object):
    def __init__(self,fname):
        self.fname = fname

    #做出转移特性曲线，其中曲线默认参数为坐标轴界点：left= -25, right = 45, low = 1E-12, high = 1E-4
    def Trans_Plot_Withfit(self,left= -25, right = 45, low = 1E-12, high = 1E-4):
        #实例化，获取fname的数据
        Data = Data_Analysis(self.fname)
        plt.figure()
        #做出拟合前的Trans图
        x = Data.TransferExcel()[0]
        y = Data.TransferExcel()[1]
        plt.semilogy(x, y, 's-', label = (self.fname.split('.')[0]), lw = 3)

        #做拟合曲线图，使用Scipy中的linalg类进行拟合并作图
        try:

            fit_start = Data.Get_Closest_Num(1E-10, y)
            fit_end = Data.Get_Closest_Num(1E-8, y)+1
            # print fit_start, fit_end
            y_ = Data.TransferExcel()[1][fit_start:fit_end]
            x_ = Data.TransferExcel()[0][fit_start:fit_end]
            lny_ = map(math.log , y_)  #将y轴取log，否则y值太小，拟合结果非常不准确！
            a = np.mat([x_,[1]*len(x_)]).T
            b = np.mat(lny_).T
            (t,res,rank,s) = linalg.lstsq(a,b)  #用scipy中的lstsq（least squres）函数进行线性拟合
            # print t  #获得拟合系数，为一个二维矩阵
            r = t[0][0]
            c = t[1][0]
            # print fit.TransferExcel()[0][45],  fit.TransferExcel()[0][52]+0.1
            x__ = np.arange(Data.TransferExcel()[0][fit_start],\
                            Data.TransferExcel()[0][fit_end]+0.1, 0.1)
            y__= map(lambda x_: math.exp(r*x_+c), x__)

            plt.semilogy(x__, y__, 'rs-', lw = 3)
            plt.legend(loc = 'lower right')
            plt.axis([left, right, low, high])
            plt.xlabel('VG',fontsize=20 )
            plt.ylabel('ID', fontsize=20)
            plt.title('Transfer Curve With Fit', fontsize=30)
            Fit_Vth = x__[Data.Get_Closest_Num(1E-9, y__)]
            para = Data.Extraction()
            plt.text(25, 1E-11,'Ex_Vth: '+str(para[0])+'\n'+'Fit_Vth: '+str(Fit_Vth), fontsize=18)
        #
        except:
            print 'fit_start=',fit_start, 'fit_end=',fit_end
            print 'original length:',len(x_), len(y_),'fit length:', len(x__), len(y__)
            return Fit_Vth

        finally:
            pass

#测试拟合结果，显示在figure中
if __name__ == '__main__':
     fit = Vth_Fit('N2_10min.xls')
     fit.Trans_Plot_Withfit()
     plt.show()



