from os import system
from discord import Status

# On call of the /users command, this will print
# out a nicely sorted, colored list of all users
# connected to the clients current server and pipe
# it to the system pager, (in this case `less`)

class UserList:

    def __init__(self, colors):
        self.colors = colors
        # place to store the names, separted in categories
        self.online = []
        self.offline = []
        self.idle = []
        self.dnd = []

    def add(self, member, tag):
        listing = member.name + tag + " \n"
        if member.status is Status.online:
            self.online.append(listing)
        elif member.status is Status.offline:
            self.offline.append(listing)
        elif member.status is Status.idle:
            self.idle.append(listing)
        elif member.status is Status.dnd:
            self.dnd.append(listing)

    def sort(self):
        self.online = sorted(self.online, key=str.lower)
        self.offline = sorted(self.offline, key=str.lower)
        self.idle = sorted(self.idle, key=str.lower)
        self.dnd = sorted(self.dnd, key=str.lower)

        tmp = []
        for name in self.online:
            tmp.append((name, self.colors["green"]))
        self.online = list(tmp)
        del tmp[:]

        for name in self.idle:
            tmp.append((name, self.colors["yellow"]))
        self.idle = list(tmp)
        del tmp[:]

        for name in self.dnd:
            tmp.append((name, self.colors["red"]))
        self.dnd = list(tmp)
        del tmp[:]

        for name in self.offline:
            tmp.append((name, self.colors["magenta"]))
        self.offline = list(tmp)
        del tmp[:]

        return (*self.online, *self.idle, *self.dnd, *self.offline)
