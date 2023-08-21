class Player:
    """
    A class to represent a BrightSign player

    Attributes
    ----------
    name : str
        the name of the player
    ip : str
        the ip address of the player
    serial : str
        the serial number of the player
    searchwords : str
        the searchwords, used in analyzing the players logs
    headers : str
        the headers, used in analyzing the players logs
    """

    def __init__(self, name: str, ip: str, serial: str, searchwords: str, headers: str):
        self.name = name
        self.ip = ip
        self.serial = serial
        self.searchwords = searchwords
        self.headers = headers
