import discord
import os
from discord.ext import commands
import urllib.request as urllib2

token = # your token
bot = commands.Bot(command_prefix="!")
bot.remove_command('help')


# Will print bot is online when the bot is online
@bot.event
async def on_ready():
    print("Bot is online!")


# Help command
@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Commands:", color=0x8b1818)
    embed.add_field(name="```!runfile```", value="Runs a file and gives the output.", inline=False)
    embed.add_field(name="```!filecontent```", value="Gives the content of the file given.", inline=False)
    embed.add_field(name="```!listfiles```", value="Lists all the current files.", inline=False)
    embed.add_field(name="```!writefile```", value="Writes to a file.", inline=False)
    embed.add_field(name="```!createfile```", value="Creates a file.", inline=False)
    embed.add_field(name="```!deletefile```", value="Deletes a file.", inline=False)
    embed.add_field(name="```!clearfile```", value="Clears a files code.", inline=False)
    embed.add_field(name="```!renamefile```", value="Renames a file.", inline=False)
    embed.add_field(name="```!commandsyntax```", value="Shows the syntax for all of the commands.", inline=False)
    embed.add_field(name="```!help```", value="This command ;)", inline=False)
    await ctx.send(embed=embed)

# Lists files
@bot.command()
async def listfiles(ctx):
    embed = discord.Embed(title="Files:", color=0x8b1818)
    files = []
    for filename in os.listdir(os.getcwd()):
        if filename.endswith(".py") and filename != "Discord Bot.py":
            files.append(filename)
    for file in files:
        embed.add_field(name=f"```{file}```", value=f"Use command: !filecontent {file} : to view the files contents.", inline=False)
    await ctx.send(embed=embed)

# Rewrites a files contents
@bot.command()
async def writefile(ctx, *, file_and_code):
    files = []
    things = file_and_code.split("/|/\n")
    file = things[0]
    code = things[1]
    code = "".join([x for x in code if x != "`"])
    for filename in os.listdir(os.getcwd()):
        if filename.endswith(".py") and filename != "Discord Bot.py":
            files.append(filename)
    if ".py" not in file:
        file += ".py"
    if "https://pastebin.com/raw/" in code and file in files:
        req = urllib2.urlopen(code, timeout=7)
        text = req.read().decode("utf-8")
        pastebin = True
    elif "https://" in code and "raw" not in code and file in files:
        code = code.split("/")
        code.insert(-1, "raw")
        code = "/".join(code)
        req = urllib2.urlopen(code, timeout=7)
        text = req.read().decode("utf-8")
        pastebin = True
    elif file in files:
        pastebin = False
    if pastebin and file in files:
        cool_text = "\n" + text
        text = cool_text + "\n"
        lines_in_code = text.split("\n")
        lines_in_code = [f"\t{x}" for x in lines_in_code]
        code = "".join(lines_in_code)
        with open(file, "w") as current_file:
            current_file.write(f'import sys\nimport traceback\nsys.stdout = open("code.txt", "w")\ntry:\n{code}\nexcept Exception as exception:\n\tthing = traceback.format_exc()\n\tprint(thing)\nsys.stdout.close()')
        embed = discord.Embed(title=f"Successfully wrote to file: {file}", color=0x8b1818)
        await ctx.send(embed=embed)
    elif not pastebin and file in files:
        lines_in_code = code.split("\n")
        lines_in_code = [f"\t{x}" for x in lines_in_code]
        code = "\n".join(lines_in_code)
        with open(file, "w") as current_file:
            current_file.write(
                f'import sys\nimport traceback\nsys.stdout = open("code.txt", "w")\ntry:\n{code}\nexcept Exception as exception:\n\tthing = traceback.format_exc()\n\tprint(thing)\nsys.stdout.close()')
        embed = discord.Embed(title=f"Successfully wrote to file: {file}", color=0x8b1818)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="File does not exist!", color=0x8b1818)
        await ctx.send(embed=embed)

# Runs an existing file
@bot.command()
async def runfile(ctx, *, file):
    files = []
    for filename in os.listdir(os.getcwd()):
        if filename.endswith(".py") and filename != "Discord Bot.py":
            files.append(filename)
    if ".py" not in file:
        file += ".py"
    if file in files:
        os.popen(file).read()
        with open("code.txt", "r") as current_file:
            lines = current_file.readlines()
        with open("code.txt", "w") as current_file:
            current_file.write("")
        output = "\n".join([x for x in lines if x != "`"])
        embed = discord.Embed(title=f"Output:", description=f"```{output}```", color=0x8b1818)
        await ctx.send("**Output...**⚙", embed=embed)
    else:
        embed = discord.Embed(title="File does not exist!", color=0x8b1818)
        await ctx.send(embed=embed)

# Clears messages
@bot.command()
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)

# Shows a files content
@bot.command()
async def filecontent(ctx, *, file):
    files = []
    for filename in os.listdir(os.getcwd()):
        if filename.endswith(".py") and filename != "Discord Bot.py":
            files.append(filename)
    if ".py" not in file:
        file += ".py"
    if file in files:
        with open(file, "r") as current_file:
            lines = current_file.readlines()
        try:
            del lines[0]
            del lines[0]
            del lines[0]
            del lines[0]
            del lines[-1]
            del lines[-1]
            del lines[-1]
            del lines[-1]
            del lines[-1]
        except:
            pass
        lines = "".join([x.replace("\t", "", 1) for x in lines])
        embed = discord.Embed(title="Content:", description=f"```{lines}```", color=0x8b1818)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="File does not exist!", color=0x8b1818)
        await ctx.send(embed)

# Deletes a file
@bot.command()
async def deletefile(ctx, *, file):
    files = []
    for filename in os.listdir(os.getcwd()):
        if filename.endswith(".py") and filename != "Discord Bot.py":
            files.append(filename)
    if ".py" not in file:
        file += ".py"
    if file in files:
        os.remove(file)
        embed = discord.Embed(title=f"Successfully deleted the file: {file}", color=0x8b1818)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="File does not exist!", color=0x8b1818)
        await ctx.send(embed)

# Creates a file
@bot.command()
async def createfile(ctx, *, file):
    files = []
    for filename in os.listdir(os.getcwd()):
        if filename.endswith(".py") and filename != "Discord Bot.py":
            files.append(filename)
    if ".py" not in file:
        file += ".py"
    if file not in files:
        with open(file, "w") as new_file:
            pass
        embed = discord.Embed(title=f"Successfully created the file: {file}", color=0x8b1818)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title=f"The file: {file} already exists!", color=0x8b1818)
        await ctx.send(embed=embed)

# Clears a files contents
@bot.command()
async def clearfile(ctx, *, file):
    files = []
    for filename in os.listdir(os.getcwd()):
        if filename.endswith(".py") and filename != "Discord Bot.py":
            files.append(filename)
    if ".py" not in file:
        file += ".py"
    if file in files:
        with open(file, "w") as current_file:
            current_file.write("import sys\nimport traceback\nsys.stdout = open('code.txt', 'w')\ntry:\n\tpass\nexcept Exception as exception:\n\tthing = traceback.format_exc()\n\tprint(thing)\nsys.stdout.close()")
        embed = discord.Embed(title="Successfully cleared file!", color=0x8b1818)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="File does not exist!", color=0x8b1818)
        await ctx.send(embed)

# Renames a file
@bot.command()
async def renamefile(ctx, *, file_and_new_file):
    file_things = file_and_new_file.split(":")
    files = []
    for filename in os.listdir(os.getcwd()):
        if filename.endswith(".py") and filename != "Discord Bot.py":
            files.append(filename)
    if file_things[0] in files:
        os.rename(file_things[0], file_things[1])
        embed = discord.Embed(title=f"Successfully renamed file, {file_things[0]} to {file_things[1]}!", color=0x8b1818)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="File does not exist!", color=0x8b1818)
        await ctx.send(embed)

@bot.command()
async def commandsyntax(ctx):
    embed = discord.Embed(title="The syntax for commands:", color=0x8b1818)
    embed.add_field(name="```!runfile```", value="Syntax: !runfile (file you are using)", inline=False)
    embed.add_field(name="```!writefile```", value="Syntax: !writefile (file you are using)/|/\n(code)", inline=False)
    embed.add_field(name="```!clearfile```", value="Syntax: !clearfile (file you are using)", inline=False)
    embed.add_field(name="```!filecontent```", value="Syntax: !filecontent (file you are using)", inline=False)
    embed.add_field(name="```!createfile```", value="Syntax: !createfile (name of the new file)", inline=False)
    embed.add_field(name="```!deletefile```", value="Syntax: !deletefile (name of the file)", inline=False)
    embed.add_field(name="```!renamefile```", value="Syntax: !renamefile (the old file name):(new file name)", inline=False)
    embed.add_field(name="```!help```", value="Syntax: !help", inline=False)
    embed.add_field(name="```!commandsyntax```", value="Syntax: !commandsyntax", inline=False)
    await ctx.send(embed=embed)

bot.run(token)
