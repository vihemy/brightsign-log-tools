import os, glob
import pandas as pd

from utils import directory_functions
from utils import date_time

def main(log_destination_root_folder):
    #sets var to this file's current directory
    player_name = "Ekspertskaerm 2"
    log_directory = log_destination_root_folder + "/" + player_name
    export_directory = log_destination_root_folder + "/exports/" + player_name # for csv-file export

    #Searchwords
    sw1="LE=touch"
    sw2="LS=Ventilationsanlaeg" #sic + undgår æøå
    sw3="LS=Vandbehandling" #undgår æøå

    #The dict that holds filename and data
    dict= {
        'Log Name': [],
        'Date': [],
        'Touch actions': [],
        'Ventilationsanlaeg': [],
        'Vandbehandling':[],
    }
    df=pd.DataFrame(dict)

    #update df with filename and counts of the three searchwords. Also shorten filename to filenameShort
    i=0
    for filename in glob.glob(os.path.join(log_directory, '*.log')):
        with open(filename, 'r') as f:
            filenameShort = directory_functions.shorten_filename(filename)
            text=f.read()
            data1=text.count(sw1)
            data2=text.count(sw2)
            data3=text.count(sw3)

            #find date in each filetext. Searches for "202" (because each date in this decade starts with "202") and set index to find exdate in each file.
            sub_index=text.find("202")
            date=text[sub_index:sub_index+10]

            #inputs data to each new row of the df
            df.loc[i]=[filenameShort, date, data1, data2, data3]
            i+=1

    # Sums any double-logs of same day, and groups the df by date (Logname is not shown in dataframe)
    df=df.groupby('Date').sum()

    # drops 'Log Name' column, as it totals weird (strings are added together)
    df = df.drop(['Log Name'], axis=1)
    
    #ads 'Total'- row at end with sums of each columns.
    df.loc['Total']=df.sum()

    #Print df in terminal
    print(df)

    #Export DF as csv to export-folder
    directory_functions.create_directory(export_directory) # creates export-directory if it doesn't exist
    date=date_time.get_date()
    df.to_csv(os.path.join(export_directory, f'Data_Export_{player_name}_{date}.csv'), sep=';') # exports csv-file with playername + date in filename

    print(f"\nExport of {player_name} data complete")