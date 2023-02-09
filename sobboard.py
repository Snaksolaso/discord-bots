import nextcord
from nextcord.ext import commands
from sobboardtoken import TOKEN
SOB_THRESHOLD = 3
intents = nextcord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.members = True

client = commands.Bot(command_prefix='.', intents=intents)
soblist = {}


@client.event
async def on_ready():
    print("ready.")

@client.event
async def on_reaction_add(reaction, user):
    sobchannel = client.get_channel(1070499079982960670)
    message = reaction.message
    print("reaction added")
    if reaction.message.channel.id == sobchannel.id:
        return
    if reaction.emoji == "😭" and reaction.count >= SOB_THRESHOLD:
        await update_soblist(reaction, message, sobchannel)

@client.event
async def on_reaction_remove(reaction, user):
    sobchannel = client.get_channel(1070499079982960670)
    print("reaction removed")
    if reaction.message.channel.id == sobchannel.id:
        return
    if reaction.emoji == "😭":
        await update_soblist(reaction, reaction.message, sobchannel)

@client.event
async def on_reaction_clear(message):
    sobchannel = client.get_channel(1070499079982960670)
    print("reaction cleared")
    if message.channel.id == sobchannel.id:
        return
    if soblist.get(message.id) != None:
        await soblist[message.id].delete()
        soblist[message.id] = None

async def update_soblist(reaction, message, sobchannel):
    if soblist.get(message.id) == None:
        embed = nextcord.Embed(description=message.content)
        embed.add_field(name="Source",value="[jump]("+message.jump_url+")")
        if len(message.attachments) > 0:
            embed.set_image(url=message.attachments[0].url)
        messageauthor = reaction.message.author
        print(messageauthor)
        embed.set_author(name=messageauthor.nick, icon_url=messageauthor.display_avatar.url)
        soblist[message.id] = await sobchannel.send(embed=embed, content="😭 **"+str(reaction.count)+"** #" + reaction.message.channel.name)
        return
    else:
        if reaction.count == 0:
            await soblist[message.id].delete()
            soblist[message.id] = None
        else:
            await soblist[message.id].edit(content="😭 **"+str(reaction.count)+"** #" + reaction.message.channel.name)


client.run(TOKEN)