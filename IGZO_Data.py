# -*- coding:utf-8 -*-
#author ： 徐佳能, Canon Xu, a graduate student from Dept.EE of XJTU
#Email: canonxu@yeah.net
#Finish Time：2015/4/18

import xlrd, xlwt
import math

#IGZO工艺参数
IGZO_W = 1000*1E-4
IGZO_L = 0.025    #上海交通大学电子工程系董承远老师组所用掩模板，6行8列，第一列尺寸0.0275cm，每列递减0.0025cm
IGZO_GiThick = 3E-5
IGZO_GiDieleCons = 3.5
IGZO_GiCap = 8.85*1E-14*IGZO_GiDieleCons/IGZO_GiThick


class Excel_Analysis(object):
    def __init__(self,fname):
        self.fname = fname

    #读取采集到数据中的ID和VG值，并将VG取绝对值
    def TransferExcel(self):
        Data = xlrd.open_workbook(self.fname)
    #   Transfer_table = Data.sheet_by_name(u"表单01")
    #   Transfer_table = Data.sheets()[0]
        Transfer_table = Data.sheet_by_index(1) #三种获取表单的方法。对EXCEL文件中的第二张表进行处理
    #   print Transfer_table.nrows, Transfer_table.ncols
        Id_TestValue = Transfer_table.col_values(2)  #表中第三列为Id值
        Vg_Value = Transfer_table.col_values(1)   #表中第二列为Vg值
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


    #提取参数：Vth、亚阈值摆幅SS、开关电流比Ion/Ioff和迁移率
    def Extraction(self):
        Id_AbsValue = self.TransferExcel()[1]
        Vg = self.TransferExcel()[0]

        #提取Vth参数，采用1E-9进行提取
        target = 1E-9*(IGZO_W/IGZO_L)
        i = self.Get_Closest_Num(target,Id_AbsValue )
        if Vg[i] > 0:
            Vth = math.floor(2*Vg[i])/2
        else:
            Vth =  math.ceil(2*Vg[i])/2
        # print 'The value of Vth:', Vth

        #提取亚阈值摆幅SS，采用1E-8和1E-10进行提取
        target1 = 1E-8
        i = self.Get_Closest_Num(target1,Id_AbsValue)
        if Vg[i] > 0:
            s1 = math.floor(2*Vg[i])/2
        else:
            s1 =  math.ceil(2*Vg[i])/2
        target2 = 1E-10
        i = self.Get_Closest_Num(target2,Id_AbsValue )
        if Vg[i] > 0:
            s2 = math.floor(2*Vg[i])/2
        else:
            s2 =  math.ceil(2*Vg[i])/2
        SS = abs(s1-s2)/2
        # print 'The value of SS:', SS

        #提取开关电流比Ion/Ioff参数:
        Ioff = sum((Id_AbsValue[4] ,Id_AbsValue[5], Id_AbsValue[6], Id_AbsValue[7], Id_AbsValue[8]))/5
        Ion = sum((Id_AbsValue[115], Id_AbsValue[116], Id_AbsValue[117], Id_AbsValue[118], Id_AbsValue[119]))/5
        Ion_off = int(Ion/Ioff)
        Ion_off = '%E' %(Ion_off)
        Rate_OnOff = Ion_off
        # print 'The rate of On/Off: %e' %Rate_OnOff


        #提取迁移率Mobility参数
        Id_SqrtValue = map(math.sqrt, Id_AbsValue)
        Differential = [0]
        for i in range(1, 120):
            Differential.append((Id_SqrtValue[i]-Id_SqrtValue[i-1])/(Vg[i]-Vg[i-1]))
        Mobility = (max(Differential[20:100])**2)*2*IGZO_L/(IGZO_W*IGZO_GiCap)
        Mobility = '%.2f' %Mobility# print 'The mobility is :', Mobility

        para = [Vth, SS, Mobility, Rate_OnOff]  #经过类型转换的Rate_OnOff和Moblility为srt类型，其余为float型
        return para

    #获取一个数组中，最接近target数值的数，
    #输入target为目标数值，array为数组，start为从数组中的第start个值开始（默认为10），返回array数组中最接近该数值的位置i
    def Get_Closest_Num(self, target, array, start=10):
        for i in range(start, len(array)-1):
            if (target - array[i])*(target - array[i+1]) <= 0:
                return i



if __name__ == '__main__':
    #参数提取测试
    Trans11 = Excel_Analysis('Ar_30min.xls')
    print Trans11.Extraction()



#将处理后的ID和VG值写入新的Excel表中
#Newfile = xlwt.Workbook()
#NewTable = Newfile.add_sheet("Transfer")
#for i in range(121):
#    NewTable.write(i, 1, Id_AbsValue[i])
#    NewTable.write(i, 0, Vg[i])







