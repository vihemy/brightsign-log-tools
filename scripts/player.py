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
    """

    def __init__(self, name: str, ip: str, serial: str, collect_logs: bool):
        self.name = name
        self.ip = ip
        self.serial = serial
        self.collect_logs = collect_logs
