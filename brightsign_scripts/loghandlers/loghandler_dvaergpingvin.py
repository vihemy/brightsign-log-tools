import os, glob
import pandas as pd
import re

from utils import directory_functions
from utils import date_time


def main(log_destination_root_folder):
    #sets var to this file's current directory
    player_name = "Dvaergpingvin"
    log_directory = log_destination_root_folder + "/" + player_name
    export_directory = log_destination_root_folder + "/exports/" + player_name # for csv-file export

    #Searchwords (searches with re(see line 35-50) to get around use of 'ÆØÅ')
    sw1='LS=EIEM_Dv.+rgpingvin_18.05_DA_P'
    sw2='LS=EIEM_Dv.+rgpingvin_18.05_DA_S1'
    sw3='LS=EIEM_Dv.+rgpingvin_18.05_DA_S2'
    sw4='LS=EIEM_Dv.+rgpingvin_18.05_DA_S3'
    sw5='LS=EIEM_Dv.+rgpingvin_18.05_DA_S4'
    sw6='LS=EIEM_Dv.+rgpingvin_18.05_DA_S5'

    #The dict that holds filename and data
    dict= {
        'Log Name': [],
        'Date': [],
        'P': [],
        'S1': [],
        'S2':[],
        'S3':[],
        'S4':[],
        'S5':[],
    }
    df=pd.DataFrame(dict)

    #update df with filename and counts of each searchwords. Also shorten filename to filenameShort.
    #uses re.findall with wildcards (see line 10-15) to get around use of ÆØÅ
    i=0
    for filename in glob.glob(os.path.join(log_directory, '*.log')):
        with open(filename, 'r') as f:
            filenameShort = directory_functions.shorten_filename(filename)
            text=f.read()
            data1=len(re.findall(sw1, text))
            data2=len(re.findall(sw2, text))
            data3=len(re.findall(sw3, text))
            data4=len(re.findall(sw4, text))
            data5=len(re.findall(sw5, text))
            data6=len(re.findall(sw6, text))

            #find date in each filetext. Searches for "202" (because each date in this decade starts with "202") and 
            sub_index=text.find("202")
            date=text[sub_index:sub_index+10] # set index to find date in each file.

            #inputs data to each new row of the df
            df.loc[i]=[filenameShort, date, data1, data2, data3, data4, data5, data6]
            i+=1


    # Sums any double-logs of same day, and groups the df by date (Logname is not shown in dataframe)
    df=df.groupby('Date').sum()

    # drops 'Log Name' column, as it totals weird (strings are added together)
    df = df.drop(['Log Name'], axis=1)

    #ads 'Total'- row at end with sums of each columns.
    df.loc['Total'] = df.sum(numeric_only=True) # uses numeric_only=True to avoid summing the 'Log Name' column

    #Print df in terminal
    print(df)

    #Export DF as csv to export-folder
    directory_functions.create_directory(export_directory) # creates export-directory if it doesn't exist
    date=date_time.get_date()
    df.to_csv(os.path.join(export_directory, f'Data_Export_{player_name}_{date}.csv'), sep=';') # exports csv-file with playername + date in filename

    print(f"\nExport of {player_name} data complete")
