import pandas as pd

def get_dict_from_player_index(index_path):
    df = pd.read_excel(str(index_path), usecols=['Navn', 'IP-adresse', 'Serienummer']) # get relavant columns from excel file (IP is used for download, serial for distribution)
    df['IP_serial'] = list(zip(df['IP-adresse'], df['Serienummer']))  #create new tuple-column from columns ip-adresse and serienummer
    players = df.set_index('Navn')['IP_serial'].to_dict() # creates dict with new tuple as value
    return players