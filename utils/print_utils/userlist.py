from os import system
from discord import Status
from utils.globals import gc

# On call of the /users command, this will print
# out a nicely sorted, colored list of all users
# connected to the clients current server and pipe
# it to the system pager, (in this case `less`)

class UserList:
        
    def __init__(self):
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
        
        # now they are sorted, we can colorize them
        # we couldn't before as the escape codes mess with
        # the sorting algorithm
        tmp = []
        for name in self.online: 
            tmp.append(gc.term.green + name)
        self.online = list(tmp)
        del tmp[:]

        for name in self.idle: 
            tmp.append(gc.term.yellow + name)
        self.idle = list(tmp)
        del tmp[:]
       
        for name in self.dnd: 
            tmp.append(gc.term.black + name)
        self.dnd = list(tmp)
        del tmp[:]

        for name in self.offline: 
            tmp.append(gc.term.red + name)
        self.offline = list(tmp)
        del tmp[:]

        return "".join(self.online) + "".join(self.offline) \
                + "".join(self.idle) + "".join(self.dnd)

async def print_userlist():
    if len(gc.client.servers) == 0:
        print("Error: You are not in any servers.")
        return
    
    if len(gc.client.get_current_server().channels) == 0:
        print("Error: Does this server not have any channels?")
        return

    # lists to contain our "Member" objects
    nonroles = UserList()
    admins = UserList()
    mods = UserList() 
    bots = UserList() 
    everything_else = UserList() 

    for member in gc.client.get_current_server().members:
        if member is None: continue # happens if a member left the server
        
        if member.top_role.name == "admin" or member.top_role.name == "Admin":
            admins.add(member, " - (Admin)")
        elif member.top_role.name == "mod" or member.top_role.name == "Mod":
            mods.add(member, "- (Mod)")
        elif member.top_role.name == "bot" or member.top_role.name == "Bot":
            bots.add(member, " - (bot)")
        elif member.top_role.is_everyone: nonroles.add(member, "")
        else: everything_else.add(member, " - " + member.top_role.name)

   
    # the final buffer that we're actually going to print
    buffer = []

    if admins is not None: buffer.append(admins.sort())
    if mods is not None: buffer.append(mods.sort())

    buffer.append("\n" + gc.term.magenta + "---------------------------- \n\n")

    if bots is not None: buffer.append(bots.sort())
    if everything_else is not None: buffer.append(everything_else.sort())

    buffer.append("\n" + gc.term.magenta + "---------------------------- \n\n")

    if nonroles is not None: buffer.append(nonroles.sort())

    buffer_copy = []
    for name in buffer:
        name = name.replace("'", "")
        name = name.replace('"', "")
        name = name.replace("`", "")
        name = name.replace("$(", "")
        buffer_copy.append(name)

    system("echo '" + gc.term.yellow + "Members in " \
           + gc.client.get_current_server().name + ": \n" \
           + gc.term.magenta + "---------------------------- \n \n" \
           + "".join(buffer_copy) \
           + gc.term.green + "~ \n" \
           + gc.term.green + "~ \n" \
           + gc.term.green + "(press \'q\' to quit this dialog) \n" \
           # NOTE: the -R flag here enables color escape codes
           + "' | less -R")

# takes in a member, returns a color based on their status
def get_status_color(member):
    if member.status is Status.online:
        return gc.term.green
    if member.status is Status.idle:  # aka "away"
        return gc.term.yellow
    if member.status is Status.offline:
        return gc.term.red
    if member.status is Status.dnd: # do not disturb
        return gc.term.black

    # if we're still here, something is wrong
    return "ERROR: get_status_color() has returned 'None' for " \
            + member.name + "\n"
