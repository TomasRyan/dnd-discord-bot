##-------------------------------------------------------#
#   Tomas Ryan  
#   TomasRyanMann@gmail.com
#   dndDiscordBot
#--------------------------------------------------------#
#   29/4    version 1.0
#       Initial version created, has a dice rolling 
#       function and a wildmagic table function
#
#   04/05   Version 1.1
#       Added some server information, changed from the 
#       default help text and cleaned up a lil
#
#   04/05   Version 1.1.1
#       added in printUser function
#
#   04/05   Version 1.2
#       added in per user settings, tides of chaos and 
#       controlled chaos features. added todo list
#   05/05   Version 1.3
#       added in sqlite intergration for simple database 
#       usage and history of users use of the bot
#--------------------------------------------------------#
#   TO DO:
#       Error Checking and Handling                     []
#       Saving history                                  [x]
#       database intergration                           [x]
#       Wild Table lookup                               []
#       Charecter stat macro                            []
#       Custom prefix                                   []
#       DM incorperations                               []
##-------------------------------------------------------#

import random
import datetime
import time
import logging
#
import discord
from discord.ext import commands
#
import sqlite3
#
client = discord.Client()
#
conn = sqlite3.connect('dndDiscordBotdb.db')
c = conn.cursor()

#----------------------------
#   wildmagic table
#----------------------------
#   Dictionary of each entry of the wild magic table with format 'Text:oddNumberOfEntry'"
WildMagicTable = {
    "Roll on this table at the start of each of your turns for the next minute, ignoring this result on subsequent rolls.": 1,
    "For the next minute, you can see any invisible creature if you have line of sight to it.":3,
    "A modron chosen and controlled by the DM appears in an unoccupied space within 5 feet of you, then disappears I minute later.":5,
    "You cast Fireball as a 3rd-level spell centered on yourself.":9,
    "Roll a d10. Your height changes by a number of inches equal to the roll. If the roll is odd, you shrink. If the roll is even, you grow.":11,
    "You cast Confusion centered on yourself.":13,
    "For the next minute, you regain 5 hit points at the start of each of your turns.":15,
    "You grow a long beard made of feathers that remains until you sneeze, at which point the feathers explode out from your face.":17,
    "You cast Grease centered on yourself.":19,
    "Creatures have disadvantage on saving throws against the next spell you cast in the next minute that involves a saving throw.":21,
    "Your skin turns a vibrant shade of blue. A Remove Curse spell can end this effect.":23,
    "An eye appears on your forehead for the next minute. During that time, you have advantage on Wisdom (Perception) checks that rely on sight.":25,
    "For the next minute, all your spells with a casting time of 1 action have a casting time of 1 bonus action.":27,
    "You teleport up to 60 feet to an unoccupied space of your choice that you can see.":29,
    "You are transported to the Astral Plane until the end of your next turn, after which time you return to the space you previously occupied or the nearest unoccupied space if that space is occupied.":31,
    "Maximize the damage of the next damaging spell you cast within the next minute.":33,
    "Roll a d10. Your age changes by a number of years equal to the roll. If the roll is odd, you get younger (minimum 1 year old). If the roll is even, you get older.":35,
    "1d6 flumphs controlled by the DM appear in unoccupied spaces within 60 feet of you and are frightened of you. They vanish after 1 minute.":37,
    "You regain 2d10 hit points.":39,
    "You turn into a potted plant until the start of your next turn. While a plant, you are incapacitated and have vulnerability to all damage. If you drop to 0 hit points, your pot breaks, and your form reverts.":41,
    "For the next minute, you can teleport up to 20 feet as a bonus action on each of your turns.":43,
    "You cast Levitate on yourself.":45,
    "A unicorn controlled by the DM appears in a space within 5 feet of you, then disappears 1 minute later.":47,
    "You can't speak for the next minute. Whenever you try, pink bubbles float out of your mouth.":49,
    "A spectral shield hovers near you for the next minute, granting you a +2 bonus to AC and immunity to Magic Missile.":51,
    "You are immune to being intoxicated by alcohol for the next 5d6 days.":53,
    "Your hair falls out but grows back within 24 hours.":55,
    "For the next minute, any flammable object you touch that isn't being worn or carried by another creature bursts into flame.":57,
    "You regain your lowest-level expended spell slot.":59,
    "For the next minute, you must shout when you speak.":61,
    "You cast Fog Cloud centered on yourself.":63,
    "Up to three creatures you choose within 30 feet of you take 4d10 lightning damage.":65,
    "You are frightened by the nearest creature until the end of your next turn.":67,
    "Each creature within 30 feet of you becomes invisible for the next minute. The invisibility ends on a creature when it attacks or casts a spell.":69,
    "You gain resistance to all damage for the next minute.":71,
    "A random creature within 60 feet of you becomes poisoned for 1d4 hours.":73,
    "You glow with bright light in a 30-foot radius for the next minute. Any creature that ends its turn within 5 feet of you is blinded until the end of its next turn.":75,
    "You cast Polymorph on yourself. If you fail the saving throw, you turn into a sheep for the spell's duration.":77,
    "Illusory butterflies and flower petals flutter in the air within 10 feet of you for the next minute.":79,
    "You can take one additional action immediately.":81,
    "Each creature within 30 feet of you takes 1d10 necrotic damage. You regain hit points equal to the sum of the necrotic damage dealt.":83,
    "You cast Mirror Image.":85,
    "You cast Fly on a random creature within 60 feet of you.":87,
    "You become invisible for the next minute. During that time, other creatures can't hear you. The invisibility ends if you attack or cast a spell.":89,
    "If you die within the next minute, you immediately come back to life as if by the Reincarnate spell.":91,
    "Your size increases by one size category for the next minute.":93,
    "You and all creatures within 30 feet of you gain vulnerability to piercing damage for the next minute.":95,
    "You are surrounded by faint, ethereal music for the next minute.":97,
    "You regain all expended sorcery points.":99 }
#   The text for the custom help text command
helpInfo = {
    "roll" : "                  Roll whatever dice you want. use input &d& where you replace & with whatever numbers you want.",
    "getWildMagicTable" : "     Roll on the Wild Magic Table.",
    "rollWildTable" : "         Roll 1d20 for the chance of rolling on the wild Magic and if a natural 1 is rolled then roll on the wild magic table automatically.",
    "tidesOfChaos" : "          use when rolling wildmagic due to tides Of Chaos, or when when gaining the advantage on a roll due to the feature.",
    "checkTidesOfChaos" : "     check the current state of Tides of chaos.",
    "checkControlledChaos":"    Check if controlled chaos is enabled.",
    "changeControlledChaos":"   Enables Controlled Chaos if disabled, or enables it if its disabled.",
    "showHistory":"             Shows history of commands used and there results where available"}
#----------------------------
#
class user:
    userName = str
    userID = int
    tidesOfChaosReady = False
    controlledChaos = False
    #   assign the name of the account and the account id to the user
    def __init__(self, ctx):
        self.userName = ctx.message.author
        self.userID = ctx.message.author.id
    #   comapares the author of ctx to the user to check if they are the same user
    def compareUserID(self, ctx):
        return self.userID == ctx.message.author.id
    #   returns tidesOfChaosReady boolean value
    def getTidesOfChaosState(self):
        return self.tidesOfChaosReady
    #   flips tidesOfChaosReady boolean value
    def changeTidesOfChaosState(self):
        if self.tidesOfChaosReady:
            self.tidesOfChaosReady = False
        else:
            self.tidesOfChaosReady = True
    #   returns controlledChaos boolean value
    def getControlledChaosState(self):
        return self.controlledChaos
    #   flips controlledChaos boolean value
    def changeControlledChaosState(self):
        if self.controlledChaos:
            self.controlledChaos = False
        else:
            self.controlledChaos = True
    #   print user data
    def printUserData(self):
        print(self.userName)
        print(self.userID)
        print("Tides of Chaos boolean value: " + str(self.tidesOfChaosReady))
        print("Controlled Chaos boolean value: " + str(self.controlledChaos))

# Create tableto store history
c.execute('''CREATE TABLE if not exists CommandHistory
             (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT , 
                userID varchar(20) not null, 
                time datetime not null, 
                commandName varchar(20) not null, 
                commandResult varchar(1000))''')
                
#   logging
#   sets up discords logging and prints it into file dndDiscordBotLogs.log, and adds a event handler for logging
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='dndDiscordBotLogs.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)        

prefix = '++'
listOfUsers = []
#----------------------------
#   sets the prefix for commands to ++, or the variable prefix
client = commands.Bot(command_prefix=prefix, description='This is a bot beep boop')
client.remove_command('help')
#----------------------------
#   rolls a 1d20 and if its rolls a natual 1 then excecute rollTable(), returning the result of either
def WildMagic(ctx):
    rollResult = roller(20)
    print(rollResult)
    if rollResult == 1:
        return rollTable(ctx)
    else:
        messageString = str(rollResult) + "\nYour power remains in check"
        return messageString

#   rolls a d100, an then finds the result from the dictionary WildMagicTable, returning the string
def rollTable(ctx):
    # check controlled chaos and do the function twice if needed   
    rollTableCount = 1
    for users in listOfUsers:
        if users.compareUserID(ctx):
            if users.getControlledChaosState():
                rollTableCount = 2
    wildMagicText = '' 
    for _ in range(rollTableCount):
        rollResult = roller(100)
        tableNum = rollResult
        print(rollResult)
        if tableNum%2 == 0 :
            tableNum = tableNum - 1
        for result, x in WildMagicTable.items():
           if x == tableNum:
               print(result)
               wildMagicText = wildMagicText + str(result)
               wildMagicText = wildMagicText +'\n\n'
    return wildMagicText
           
#   rolls x amount of dice of size y
#   input: string of form "x"d"y" where x is the amount of dice to be rolled, y is the size of dice to be rolled 
#   returns a list of each roll   
def rollDice(request):
    lowerCaseQury = str(request).lower()
    diceParse = lowerCaseQury.split("d")
    diceCount = int(diceParse[0])
    total = []
    diceRolled = 0
    diceSize = int(diceParse[1])
    while diceRolled < diceCount :
        total.append(roller(diceSize))
        diceRolled = diceRolled + 1
    return(total)
    
#   rolls a dice by random chance up to the number passed to it (diceSize)
#   input: number of the cap of the highest possible roll 
#   returns a number of the result of the roll
def roller(diceSize):
    random.seed(datetime.datetime.now())
    time.sleep(0.01)
    rollResult = random.randrange(1, diceSize+1)
    print(rollResult)
    return(rollResult)

#   print The current Date and time for debug reasons
def printTime():
    now = datetime.datetime.now()
    print ("called on date and time : ")
    print (now.strftime("%Y-%m-%d %H:%M:%S"))
    
#   print the user object's name and id from the ctx for debug reasons
def printUser(ctx):
    print('Called by: ' + str(ctx.message.author))
    print('Caller id: ' + str(ctx.message.author.id))
    printTime()
    
#   check if user exists and makes a new one if it doesnt
def userCheck(ctx):
    isNewUser = True
    for users in listOfUsers:
        if users.compareUserID(ctx):
            isNewUser = False
    if isNewUser:
        listOfUsers.append(user(ctx))
        
#   Database
#   Insert Into database user id and the result of the input
def insertIntoCommandHistory(ctx, commandName, result):
    c.execute("INSERT INTO CommandHistory (userID, time, commandName, commandResult) VALUES (?, datetime('now'),?, ?)", (str(ctx.message.author.id), commandName, str(result)))
    conn.commit()
    
#   print out users result history
def printUsersCommandHistory(ctx):
    history = ""
    for row in c.execute('SELECT commandName, commandResult FROM CommandHistory where userID=?', (str(ctx.message.author.id),)):
        print(row) # row is a touple object of everything returned
        history = history + str(row[0]) + ": " + str(row[1]) + "\n"
    return history
#----------------------------
@client.command()
#   Help command
async def help(ctx):
    print('Help function ran')
    printUser(ctx)
    helpOutput = "```Hello! \nThis bot is here to help you with dnd stuff, currently tuned to help with Wild magic sorcerer :D \n"
    for command, helpText in helpInfo.items():
        helpOutput = helpOutput + command + ":    " + helpText + "\n"
    helpOutput = helpOutput + "```"
    print(helpOutput)
    print('------')
    insertIntoCommandHistory(ctx, "Help", "")
    await ctx.send(helpOutput)
    
#   On login of the bot print to cmd window that we have logged in and where
@client.event
async def on_ready():
    print('------')
    print("I am here")
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    for server in client.guilds: # for each server connected to
        print("Server Name: " + str(server.name))
        print("Server ID: " + str(server.id))
    print('------')

#   roll the wild table, and return the results of said roll and message the server the results
@client.command()
async def getWildMagicTable(ctx):
    print('Wild Magic table result function ran')
    printUser(ctx)
    print('------')
    result = rollTable(ctx)
    insertIntoCommandHistory(ctx, "getWildMagicTable", result)
    await ctx.send(result)
    
#   roll the wild table, and return the results of said roll and message the server the results
@client.command()
async def rollWildTable(ctx):
    print('WildTable roll function ran')
    printUser(ctx)
    print('------')
    result = WildMagic(ctx)
    insertIntoCommandHistory(ctx, "rollWildTable", result)
    await ctx.send(result)

#   takes a roll qurey and prints the results
@client.command()
async def roll(ctx, arg):
    print('Roll Dice function ran')
    printUser(ctx)
    lowerCaseQury = str(arg).lower()
    diceParse = lowerCaseQury.split("d")
    maxRoll = int(diceParse[1])
    #
    rolls = rollDice(arg)
    #
    resultString = ""
    for i in rolls:
        if i == 1 :
            resultString = resultString + "*" + str(i) + "*" + "+"
        elif i == maxRoll:
            resultString = resultString + "**" + str(i) + "**" + "+"
        else:
            resultString = resultString + str(i) + "+"
    resultString = resultString[:-1]
    resultString = resultString + "=" + str(sum(rolls))
    print('------')
    insertIntoCommandHistory(ctx, "roll", resultString)
    await ctx.send(resultString)
    
#   using the tidesOfChaosReady bool to see if 
@client.command()
async def tidesOfChaos(ctx):
    print('tidesOfChaos function ran')
    printUser(ctx)
    userCheck(ctx)
    result = ''
    for users in listOfUsers:
        if users.compareUserID(ctx):
            if users.getTidesOfChaosState():
                result = str(rollTable(ctx))
                users.changeTidesOfChaosState()
            else:
                users.changeTidesOfChaosState()
                result = 'The magic is due to go crazy soon'
    print(result)
    print('------')
    insertIntoCommandHistory(ctx, "tidesOfChaos", result)
    await ctx.send(result)
    
#   using the tidesOfChaosReady bool and let the user know the current state of 
@client.command()
async def checkTidesOfChaos(ctx):
    print('checkTidesOfChaos function ran')
    printUser(ctx)
    userCheck(ctx)
    result = ''
    for users in listOfUsers:
        if users.compareUserID(ctx):
            if users.getTidesOfChaosState():
                result = 'Tides Of Chaos is waiting on a table roll or a long rest'
            else:
                result = 'Tides Of Chaos is available for use'
    print(result)
    print('------')
    insertIntoCommandHistory(ctx, "checkTidesOfChaos", result)
    await ctx.send(result)

#   returns if Tides of Chaos is enabled for the user
@client.command()
async def checkControlledChaos(ctx):
    print('checkControlledChaos function ran')
    printUser(ctx)
    userCheck(ctx)
    result = ''
    for users in listOfUsers:
        if users.compareUserID(ctx):
            if users.getControlledChaosState():
                result = 'Controlled Chaos is enabled'
            else:
                result = 'Controlled chaos is disabled'
    print(result)
    print('------')
    insertIntoCommandHistory(ctx, "checkControlledChaos", result)
    await ctx.send(result)
    
#   returns if Tides of Chaos is enabled for the user
@client.command()
async def changeControlledChaos(ctx):
    print('changeControlledChaos function ran')
    printUser(ctx)
    userCheck(ctx)
    result = ''
    for users in listOfUsers:
        if users.compareUserID(ctx):
            users.changeControlledChaosState()
            if users.getControlledChaosState():
                result = 'Controlled Chaos is now enabled'
            else:
                result = 'Controlled chaos is now disabled'
    print(result)
    print('------')
    insertIntoCommandHistory(ctx, "changeControlledChaos", result)
    await ctx.send(result)
    
#   prints out users command history
@client.command()
async def showHistory(ctx):
    await ctx.send(str(printUsersCommandHistory(ctx)))
#-----------------------------

client.run("")