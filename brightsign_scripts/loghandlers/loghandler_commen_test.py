def test():
    print("hello world")


# import os, glob
# import pathlib
# from posixpath import sep
# import pandas as pd
# import matplotlib.pyplot as plt
# import re

# players = {
#     "dvaergpingvin": ("10.0.1.105", "46D98V000729"),
#     "kongepingvin" : ("10.0.1.106", "46D98C000712"),
#     "lyttestation1": ("10.0.1.107", "TKD1C8001289"),
#     "lyttestation2": ("10.0.1.108", "46D98X000709"),
#     "lyttestation3": ("10.0.1.109", "46D9C8000602"),
#     "ekspertskaerm1": ("10.0.1.115", "TKD1CN002225"),
#     "ekspertskaerm2": ("10.0.1.116", "TKD1C1001220"),
# }

# searchWords = {
#     "dvaergpingvin": ('LS=EIEM_Dv.+rgpingvin_18.05_DA_P', 'LS=EIEM_Dv.+rgpingvin_18.05_DA_S1', 'LS=EIEM_Dv.+rgpingvin_18.05_DA_S2', 'LS=EIEM_Dv.+rgpingvin_18.05_DA_S3', 'LS=EIEM_Dv.+rgpingvin_18.05_DA_S4', 'LS=EIEM_Dv.+rgpingvin_18.05_DA_S5')
# }

# folder_path_base="C:\VHM_local\Kodning\\brightsign_logs\\"

# def set_path():
#     player_name = "dvaergpingvin"
#     folder_path = folder_path_base + player_name
#     return folder_path

# def set_searchwords(player_name):
#     sw1 = searchWords[player_name][0]
#     sw2 = searchWords[player_name][1]

# #sets var to this files current directory
# folder_path="C:\VHM_local\Kodning\\brightsign_logs"

# #Searchwords (searches with re(see line 35-50) to get around use of 'ÆØÅ')
# sw1='LS=EIEM_Dv.+rgpingvin_18.05_DA_P'
# sw2='LS=EIEM_Dv.+rgpingvin_18.05_DA_S1'
# sw3='LS=EIEM_Dv.+rgpingvin_18.05_DA_S2'
# sw4='LS=EIEM_Dv.+rgpingvin_18.05_DA_S3'
# sw5='LS=EIEM_Dv.+rgpingvin_18.05_DA_S4'
# sw6='LS=EIEM_Dv.+rgpingvin_18.05_DA_S5'

# #The dict that holds filename and data
# dict= {
#     'Log Name': [],
#     'Date': [],
#     'P': [],
#     'S1': [],
#     'S2':[],
#     'S3':[],
#     'S4':[],
#     'S5':[],
# }
# df=pd.DataFrame(dict)

# #update df with filename and counts of each searchwords. Also shorten filename to filenameShort.
# #uses re.findall with wildcards (see line 10-15) to get around use of ÆØÅ
# i=0
# for filename in glob.glob(os.path.join(folder_path, '*.log')):
#     with open(filename, 'r') as f:
#         text=f.read()
#         data1=len(re.findall(sw1, text))
#         data2=len(re.findall(sw2, text))
#         data3=len(re.findall(sw3, text))
#         data4=len(re.findall(sw4, text))
#         data5=len(re.findall(sw5, text))
#         data6=len(re.findall(sw6, text))


#         #find date in each filetext. Searches for "202" (because each date in this decade starts with "202") and set index to find date in each file.
#         sub_index=text.find("202")
#         date=text[sub_index:sub_index+10]

#         #inputs data to each new row of the df
#         df.loc[i]=[filename, date, data1, data2, data3, data4, data5, data6]
#         i+=1


# # Sums any double-logs of same day, and groups the df by date (Logname is not shown in dataframe)
# df=df.groupby('Date').sum()

# #ads 'Total'- row at end with sums of each columns.
# df.loc['Total']=df.sum()

# #Print df in terminal
# print(df)

# #Export df to  in same folder, it opened the logs.
# df.to_csv(os.path.join(folder_path, 'Data_Export.csv'), sep=';')


# '''
# #Exporting visualisation of language-data using matplotlib. First by dropping the total-row, because it schewes the visualisation
# df=df.drop('Total')
# df_DA=df.groupby('Date')[['P', 'S1', 'S2', 'S3', 'S4', 'S5']].sum()
# df_DA.plot(kind="bar")
# plt.title("Dvaergpingvin - DA")
# #plt.xticks(rotation=45, ha='right')
# plt.savefig(os.path.join(folder_path, 'Data_Export_Chart_DA.png'))

# print("\nExport Complete")
# '''