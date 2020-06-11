#!/anaconda3/bin/python
#!/usr/bin/python
import os
import pandas as pd

def ReadHeaderLog(FILE="header.log"):
    if os.path.exists(FILE):
        return pd.read_csv(FILE,sep="\t",index_col=0)
    else:
        print("No Header File : %s"%FILE)
        return

def MakeList(pd_table):
    list_band = ['u','Rc','Ic']
    pd_table = pd_table.loc[pd_table["MODE"] != 'DARK']
    dict_exp = {}
    for band in list_band:
        pd_band  = pd_table.loc[pd_table['FILTER'] == band]
        np_exp   = pd_band['EXPTIME'].unique()
        if len(np_exp) > 0:
            dict_exp[band] = np_exp
    return dict_exp

def Exposure(dict_exp):
    dict_exposure = {}
    for band in dict_exp.keys():
        dict_exposure['u']  = "0"
        dict_exposure['Rc'] = "0"
        dict_exposure['Ic'] = "0"
        for exp in dict_exp[band]:
            dict_exposure[band] = exp
            cmd = 'python CameraClient.py -d -t %s,%s,%s '%(dict_exposure["u"],dict_exposure["Rc"],dict_exposure["Ic"])
            print(cmd)
            os.system(cmd)
    return

def main():
    pd_table = ReadHeaderLog()
    dict_exp = MakeList(pd_table)
    Exposure(dict_exp)
    print("\nEnd Taking Dark Frames.\n")
    return

if __name__ == '__main__':
    main()
