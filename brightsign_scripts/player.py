class Player:
    def __init__(self, name, ip, serial, searchwords):
        self.name = name
        self.ip = ip
        self.serial = serial
        self.searchwords = searchwords

    def player_name(self):
        return self.name

    def player_ip(self):
        return self.ip

    def player_serial(self):
        return self.serial

    def player_searchwords(self):
        return self.searchwords
