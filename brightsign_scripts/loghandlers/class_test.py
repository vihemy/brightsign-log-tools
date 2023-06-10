import os, glob
import pandas as pd
import re

# from utils import directory_functions
# from utils import date_time

class Player:
  def __init__(self, player_name, log_destination_root_folder, searchwords):
    self.name = player_name
    self.root_folder = log_destination_root_folder
    self.searchwords = searchwords

  def __str__(self):
    return f"{self.name}"    

  def set_directories(self):
      #sets var to this file's current directory
      log_directory = self.root_folder + "/" + self.name
      export_directory = self.root_folder + "/exports/" + self.name # for csv-file export
      print(log_directory, export_directory)

Ekspertskaerm1 = Player("Ekspertskaerm 1", "C:/Users/Emil/Desktop/Python/brightsign_logs&scripts/brightsign_logs", "LE=touch")

  # def set_searchwords(self):
  #     #Searchwords
  #     sw1="LS=Lyttestation_20.05_DA.wav	LE=mediaEnd"
  #     sw2="LS=Lyttestation_20.05_EN.wav	LE=mediaEnd"
  #     sw3="LS=Lyttestation_20.05_TY.wav	LE=mediaEnd"
  #     sw4="LE=mediaEnd"

  # def create_dataframe(self):
  #     #The dict that holds filename and data
  #     dict= {
  #         'Log Name': [],
  #         'Date': [],
  #         'DA': [],
  #         'EN': [],
  #         'TY':[],
  #         'All':[],
  #     }
  #     df=pd.DataFrame(dict)

  # def search_logs_for_searchwords(self):
  #     #update df with filename and counts of the three searchwords. Also shorten filename to filenameShort
  #     i=0
  #     for filename in glob.glob(os.path.join(log_directory, '*.log')):
  #         with open(filename, 'r') as f:
  #             filenameShort = directory_functions.shorten_filename(filename)
  #             text=f.read()
  #             data1=text.count(sw1)
  #             data2=text.count(sw2)
  #             data3=text.count(sw3)
  #             data4=text.count(sw4)

  #             #find date in each filetext. Searches for "202" (because each date in this decade starts with "202") and set index to find date in each file.
  #             sub_index=text.find("202")
  #             date=text[sub_index:sub_index+10]

  #             #inputs data to each new row of the df
  #             df.loc[i]=[filenameShort, date, data1, data2, data3, data4]
  #             i+=1
  # def group_dataframe(self):
  #     # Sums any double-logs of same day, and groups the df by date (Logname is not shown in dataframe)
  #     df=df.groupby('Date').sum()

  #     # drops 'Log Name' column, as it totals weird (strings are added together)
  #     df = df.drop(['Log Name'], axis=1)

  #     #ads 'Total'- row at end with sums of each columns.
  #     df.loc['Total']=df.sum()
  # def print_dataframe(self):
  #     #Print df in terminal
  #     print(df)
  # def export_dataframe_as_csv(self):
  #     #Export DF as csv to export-folder
  #     directory_functions.create_directory(export_directory) # creates export-directory if it doesn't exist
  #     date=date_time.get_date()
  #     df.to_csv(os.path.join(export_directory, f'Data_Export_{player_name}_{date}.csv'), sep=';') # exports csv-file with playername + date in filename

  # def print_export_complete(self):
  #     print(f"\nExport of {player_name} data complete")