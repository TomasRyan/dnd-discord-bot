#--------------------------------------------------------#
#   Tomas Ryan  
#   TomasRyanMann@gmail.com
#   dndDiscordBot
#--------------------------------------------------------#
#   29/4    version 1.0
#       Initial version created, has a dice rolling 
#       function and a wildmagic table function
#--------------------------------------------------------#


import random
import datetime
import time
#
import discord
from discord.ext import commands
#
client = discord.Client()
#----------------------------
#wildmagic table
#----------------------------
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
    
#----------------------------
#   sets the prefix for commands to ++
client = commands.Bot(command_prefix='++', description='This is a bot beep boop')
#----------------------------
#   rolls a 1d20 and if its rolls a natual 1 then excecute rollTable(), returning the result of either
def WildMagic(ctx):
    rollResult = roller(20)
    print(rollResult)
    if rollResult == 1 :
        return rollTable(ctx)
    else:
        messageString = str(rollResult) + "\nYour power remains in check"
        return messageString

#   rolls a d100, an then finds the result from the dictionary WildMagicTable, returing the string
def rollTable(ctx):
    rollResult = roller(100)
    tableNum = rollResult
    print(rollResult)
    if tableNum%2 == 0 :
        tableNum = tableNum - 1
    print(tableNum)
    for result, x in WildMagicTable.items():
       if x == tableNum:
           print(result)
           return result
           
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
#   input: nu,ber of the cap of the highest possible roll 
#   returns a number of the result of the roll
def roller(diceSize):
    time.sleep(0.01)
    rollResult = random.randrange(1, diceSize+1)
    print(rollResult)
    return(rollResult)
#----------------------------
@client.event
async def on_ready():
    print('------')
    print("I am here")
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await ctx.send("I have Joined and ready to do things")

#   roll the wild table, and return the results of said roll and message the server the results
@client.command()
async def rollWildTable(ctx):
    await ctx.send(WildMagic(ctx))

#   takes a roll qurey and prints the results
@client.command()
async def roll(ctx, arg):
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
    await ctx.send(resultString)
#-----------------------------

client.run("")