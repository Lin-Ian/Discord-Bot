"""
Name:       main.py
Purpose:    main file for MCU Quote Bot

Authors:    Lin.I

Created:    05/13/2021
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
        activity=discord.Game('Endgame | $help')
    )


# reacting to messages
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content.lower()

    if msg.startswith("$help"):
        # add the supported commands to the help menu
        embedVar = discord.Embed(
            title="Command Help",
            description="Here's what MCU Quotes can do",
            color=0xcc0000
        )
        embedVar.add_field(
            name="$character_name (ex. $stark)",
            value="get a random quote from a character",
            inline=False
        )
        embedVar.add_field(
            name="$quote",
            value="get a random quote from a random character",
            inline=False
        )
        embedVar.add_field(
            name="character_name (ex. steve)",
            value="get a random quote from characters mentioned in messages",
            inline=False
        )
        embedVar.add_field(
            name="$responding on",
            value="turn on character auto detection",
            inline=False
        )
        embedVar.add_field(
            name="$responding off",
            value="turn off character auto detection",
            inline=False
        )
        embedVar.add_field(
            name="$supported",
            value="get a list of supported characters",
            inline=False
        )
        embedVar.add_field(
            name="$github",
            value="get the GitHub repository link",
            inline=False
        )

        # send help menu
        await message.channel.send(embed=embedVar)

    # $quote, print a random quote from a random character
    elif msg.startswith("$quote"):

        # generate a random index to get a random character
        random_index = random.randint(0, len(character_list)-1)

        # get a random character
        character = character_list[random_index][0]

        # get character alias
        character_alias = character_list[random_index][1]

        # get a random quote from the character
        quote = random.choice(quote_list[random_index])

        # get a random image of the character
        image = random.choice(image_list[random_index])

        # set message parameters
        embedVar = discord.Embed(
            title="Here's a random quote from:\n" +
                  character + " (" + character_alias + ")",
            description=quote,
            color=0xcc0000
        )
        embedVar.set_thumbnail(
            url=image
        )

        # send character quote
        await message.channel.send(embed=embedVar)

    # 9responding, turn on and off character auto detection
    elif msg.startswith("$responding "):

        # remove the command prefix
        msg = msg.split("$responding ", 1)[1]

        # turn on responding if msg is on
        if msg == "on":
            db["responding"] = True
            embedVar = discord.Embed(
                title="Responding",
                description="ON",
                color=0xcc0000
            )
            # send status of responding
            await message.channel.send(embed=embedVar)

        # turn off responding if msg is off
        elif msg == "off":
            db["responding"] = False
            embedVar = discord.Embed(
                title="Responding",
                description="OFF",
                color=0xcc0000
            )
            # send status of responding
            await message.channel.send(embed=embedVar)

    # $supported, print a list of characters supported by the bot
    elif msg.startswith("$supported"):

        # create list of supported characters
        supported_characters = ""
        for character in range(len(character_list)):
            supported_characters += (" - "+character_list[character][0]+"\n")

        # set message parameters
        embedVar = discord.Embed(
            title="Supported Characters",
            description=supported_characters,
            color=0xcc0000
        )

        # send list of supported characters
        await message.channel.send(embed=embedVar)

    # 9github, get the GitHub Repository Link
    elif msg.startswith("$github"):

        # set message parameters
        embedVar = discord.Embed(
            title="GitHub",
            description="Check out the code for MCU Quotes here:\n"
                        "[GitHub Link]"
                        "(https://github.com/Lin-Ian/Discord-Bot)",
            color=0xcc0000
        )

        # send the GitHub repository link
        await message.channel.send(embed=embedVar)

    # 9character_name, get a random quote from a character
    elif msg.startswith("$"):

        # remove the command prefix from the message
        msg = msg.split("$", 1)[1]

        # check for if command is valid
        name_exists = False

        # check if the character name is in the pre-existing names
        for character in range(len(character_list)):
            for name in range(len(character_list[character])):
                if msg == character_list[character][name].lower():

                    # command is valid
                    name_exists = True

                    # get the character name
                    character_name = character_list[character][0]

                    # get the character alias
                    character_alias = character_list[character][1]

                    # get a random quote from the character
                    quote = random.choice(quote_list[character])

                    # get a random image of the character
                    image = random.choice(image_list[character])

                    # set message parameters
                    embedVar = discord.Embed(
                        title=character_name + " (" + character_alias + ")",
                        description=quote,
                        color=0xcc0000
                    )
                    embedVar.set_thumbnail(
                        url=image
                    )

                    # send character quote
                    await message.channel.send(embed=embedVar)
                    break

        # command does not exist, send error message
        if name_exists is False:
            # create error message if character name is not recognized
            embedVar = discord.Embed(
                title="Invalid Command",
                description="$help for supported commands",
                color=0xcc0000
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

                    # get the character alias
                    character_alias = character_list[character][1]

                    # get a random quote from the character
                    quote = random.choice(quote_list[character])

                    # get a random image of the character
                    image = random.choice(image_list[character])

                    # set message parameters
                    embedVar = discord.Embed(
                        title=character_name + " (" + character_alias + ")",
                        description=quote,
                        color=0xcc0000
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
