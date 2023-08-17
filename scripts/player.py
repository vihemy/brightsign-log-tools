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
        the searchwords, used in anlysing the player's logs
    """

    def __init__(self, name: str, ip: str, serial: str):
        self.name = name
        self.ip = ip
        self.serial = serial
