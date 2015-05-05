# -*- coding: utf:8 -*-
#author ： 徐佳能, Canon Xu, a graduate student from Dept.EE of SJTU
#Email: canonxu@yeah.net
#Finish Time：2015/4/21


from IGZO_Plot import IGZO_Array_Plot
import matplotlib.pyplot as plt
import math
import numpy as np
from scipy import linalg

gas_name1 = ''
N2_plot =  IGZO_Array_Plot(gas_name1+'MidN2_initial.xls',gas_name1+'15min.xls',gas_name1+'30min.xls',\
                            gas_name1+'45min.xls' ,gas_name1+'60min.xls',gas_name1+'75min.xls',\
                            gas_name1+'90min.xls',gas_name1+'105min.xls',gas_name1+'120min.xls',\
                            gas_name1+'135min.xls',gas_name1+'150min.xls')

y = [N2_plot.Para_List()[0][0]-x for x in N2_plot.Para_List()[0]][1:]  #求得delth（Vth）,作为纵坐标
x = range(15, 165, 15)   #求得时间，作为横坐标
# print len(x), len(y)
plt.semilogy(x, y, 's', lw = 3)

#开始拟合，取log后最小二乘法线性拟合
lny = map(math.log, y)
a = np.mat([x,[1]*len(x)]).T
b = np.mat(lny).T
(t,res,rank,s) = linalg.lstsq(a,b)
r = t[0][0]
c = t[1][0]
y_ = map(lambda x_: math.exp(r*x_+c), x)
plt.semilogy(x, y_, 'r-', lw = 3)
plt.show()