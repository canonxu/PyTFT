#PyTFT#
**Here is a library of thin film transistor(TFT) data analysis.**
 --------------
##Modules
Until 2015/4/18, we have mainly designed 3 modules as follows. You can check the fold `examples` to get example curves.
 ---------------------------------------------

###Py_Data module
- Read the data from Excel.
- Calculate the parameter of TFT depending on simple forum.
<br/>Tips: parameter includes threshold voltage(Vth), subthreshold swing(SS),mobility and rate of Ion/Ioff.
<br/>For example: We extract the para of a IGZO-TFT and get the result list: [-9.5, 0.5, '9.12', '1.766731E+07'],elements are the Vth, SS, mobility and rate of Ion/Ioff respectively. 


###Py_Plot module
- Draw the signal transfer curve.
- Draw a array of transfer curve.
- Draw the comparison curve TFT parameter.

###Py_Vth_Fit module
- Calculate more accurate value of Vth with the method of least square.

###Py_FormationEnergy_Fit module
- Depending on the formula, fit the experiment data to get formation energy.

###Py_QT
- Design a QT for convenient parameter test.

 ---------------------------------------------

##License & Authors
- **MIT**
- **Canon XU(canonxu@sjtu.edu.cn),  Dept. EE of SJTU**

