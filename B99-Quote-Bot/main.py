"""
Name:       main.py
Purpose:    main file for B99 Quote Bot

Authors:    Lin.I

Created:    07/31/2021
"""

# import libraries
import os
import random
import discord
from replit import db
from dotenv import load_dotenv

# import files
from characters import *
from quotes import *
from images import *
from keep_alive import keep_alive

# get token from environment file
load_dotenv()
TOKEN = os.getenv('TOKEN')

# create instance of Client to connect to discord
client = discord.Client()

# create database key for on/off message responding
if "responding" not in db.keys():
    db["responding"] = True


# setting up bot in server
@client.event
async def on_ready():
    # connection to server(s) message
    print(f'{client.user} has connected to:')
    for guild in client.guilds:
        print(f' - {guild.name}(id: {guild.id})')

    # bot status message
    await client.change_presence(
        activity=discord.Game('Clips Rent Free | 9help')
    )


# reacting to messages
@client.event
async def on_message(message):
    # check that the message came from a user and not another bot
    if message.author == client.user:
        return

    # convert message into lowercase for easier processing
    msg = message.content.lower()

    # 9help, print help menu, the commands that the bot supports
    if msg.startswith("9help"):

        # add the supported commands to the help menu
        embedVar = discord.Embed(
            title="Command Help",
            description="Here's what B99 Quotes can do",
            color=0xFFFF00
        )
        embedVar.add_field(
            name="9character_name (ex. 9jake)",
            value="get a random quote from a character",
            inline=False
        )
        embedVar.add_field(
            name="9quote",
            value="get a random quote from a random character",
            inline=False
        )
        embedVar.add_field(
            name="character_name (ex. jake)",
            value="get a random quote from characters mentioned in messages",
            inline=False
        )
        embedVar.add_field(
            name="9responding on",
            value="turn on character auto detection",
            inline=False
        )
        embedVar.add_field(
            name="9responding off",
            value="turn off character auto detection",
            inline=False
        )
        embedVar.add_field(
            name="9supported",
            value="get a list of supported characters",
            inline=False
        )
        embedVar.add_field(
            name="9github",
            value="get the GitHub repository link",
            inline=False
        )

        # send help menu
        await message.channel.send(embed=embedVar)

    # 9quote, print a random quote from a random character
    elif msg.startswith("9quote"):

        # generate a random index to get a random character
        random_index = random.randint(0, len(character_list)-1)

        # get a random character
        character = character_list[random_index][0]

        # get a random quote from the character
        quote = random.choice(quote_list[random_index])

        # get a random image of the character
        image = random.choice(image_list[random_index])

        # set message parameters
        embedVar = discord.Embed(
            title="Here's a random quote from:\n" + character,
            description=quote,
            color=0xFFFF00
        )
        embedVar.set_thumbnail(
            url=image
        )

        # send character quote
        await message.channel.send(embed=embedVar)

    # 9responding, turn on and off character auto detection
    elif msg.startswith("9responding "):

        # remove the command prefix
        msg = msg.split("9responding ", 1)[1]

        # turn on responding if msg is on
        if msg == "on":
            db["responding"] = True
            embedVar = discord.Embed(
                title="Responding",
                description="ON",
                color=0xFFFF00
            )
            # send status of responding
            await message.channel.send(embed=embedVar)

        # turn off responding if msg is off
        elif msg == "off":
            db["responding"] = False
            embedVar = discord.Embed(
                title="Responding",
                description="OFF",
                color=0xFFFF00
            )
            # send status of responding
            await message.channel.send(embed=embedVar)

    # 9supported, print a list of characters supported by the bot
    elif msg.startswith("9supported"):

        # create list of supported characters
        supported_characters = ""
        for character in range(len(character_list)):
            supported_characters += (" - "+character_list[character][0]+"\n")

        # set message parameters
        embedVar = discord.Embed(
            title="Supported Characters",
            description=supported_characters,
            color=0xFFFF00
        )

        # send list of supported characters
        await message.channel.send(embed=embedVar)

    # 9github, get the GitHub Repository Link
    elif msg.startswith("9github"):

        # set message parameters
        embedVar = discord.Embed(
            title="GitHub",
            description="Check out the code for B99 Quotes here:\n"
                        "[GitHub Link]"
                        "(https://github.com/Lin-Ian/Discord-Bot)",
            color=0xFFFF00
        )

        # send the GitHub repository link
        await message.channel.send(embed=embedVar)

    # 9character_name, get a random quote from a character
    elif msg.startswith("9"):

        # remove the command prefix from the message
        msg = msg.split("9", 1)[1]

        # check for if command is valid
        command_exists = False

        # check if the character name is in the pre-existing names
        for character in range(len(character_list)):
            for name in range(len(character_list[character])):
                if msg == character_list[character][name].lower():

                    # command is valid
                    command_exists = True

                    # get the character name
                    character_name = character_list[character][0]

                    # get a random quote from the character
                    quote = random.choice(quote_list[character])

                    # get a random image of the character
                    image = random.choice(image_list[character])

                    # set message parameters
                    embedVar = discord.Embed(
                        title=character_name,
                        description=quote,
                        color=0xFFFF00
                    )
                    embedVar.set_thumbnail(
                        url=image
                    )

                    # send character quote
                    await message.channel.send(embed=embedVar)
                    break

        # command does not exist, send error message
        if command_exists is False:
            # create error message if character name is not recognized
            embedVar = discord.Embed(
                title="Invalid Command",
                description="9help for supported commands",
                color=0xFFFF00
            )

            # send character message
            await message.channel.send(embed=embedVar)

    # print a random quote from a character that is mentioned
    # in a message if auto detection is on
    elif db["responding"] is True:

        # check if the pre-existing names are in the message
        for character in range(len(character_list)):
            for name in range(len(character_list[character])):
                if character_list[character][name].lower() in msg:

                    # get the character name
                    character_name = character_list[character][0]

                    # get a random quote from the character
                    quote = random.choice(quote_list[character])

                    # get a random image of the character
                    image = random.choice(image_list[character])

                    # set message parameters
                    embedVar = discord.Embed(
                        title=character_name,
                        description=quote,
                        color=0xFFFF00
                    )
                    embedVar.set_thumbnail(
                        url=image
                    )

                    # send character quote
                    await message.channel.send(embed=embedVar)
                    break

# keep bot alive
keep_alive()

# run bot
client.run(TOKEN)
