import discord
from TOKEN import TOKEN

client = discord.Client()

waitingList = []
prefferences = {}

def intersect(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3

@client.event
async def on_ready():
    print(f"\033[31mLogged in as {client.user}\033[39m")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if "Direct Message with " in str(message.channel):
        content = message.content.lower()
        if content == "start" or content == "help":
            await message.channel.send(
                "To start using randgle please set your tags by sending:\n"
                "-> am add/remove <tags> (to add/remove tags which describe you)\n"
                "-> looking add/remove <tags> (to add/remove tags which you are intrested in)\n"
                "-> block add/remove <tags> (to add/remove tags you are not intrested in)\n"
                "(a server reboot may reset all prefferences)"
                "After that send:\n"
                "-> wait (if you prefer to wait for someone to add you)\n"
                "-> stop (to delete yourself from the waiting list)"
                "-> search (if you prefer to add someone)"
                "Other commands:\n"
                "-> pref (to get your prefferences)\n"
                "-> reset\n"
                "To report misbehavior please message the developer"
            )
            try: prefferences[message.author]
            except: prefferences[message.author] = {"am": set(), "looking": set(), "block": set()}

        elif message.content.lower().startswith("am add"):
            try:
                prefferences[message.author]["am"].update(content.split(" ")[2:])
            except KeyError: await message.channel.send('Error: type "start" to initialize')
        elif message.content.lower().startswith("am remove"):
            try:
                for prefference in content.split(" ")[2:]:
                    prefferences[message.author]["am"].remove(prefference)
            except KeyError: await message.channel.send('Error: type "start" to initialize')

        elif message.content.lower().startswith("looking add"):
            try:
                prefferences[message.author]["looking"].update(content.split(" ")[2:])
            except KeyError: await message.channel.send('Error: type "start" to initialize')
        elif message.content.lower().startswith("looking remove"):
            try:
                for prefference in content.split(" ")[2:]:
                    prefferences[message.author]["looking"].remove(prefference)
            except KeyError: await message.channel.send('Error: type "start" to initialize')

        elif message.content.lower().startswith("block add"):
            try:
                prefferences[message.author]["block"].update(content.split(" ")[2:])
            except KeyError: await message.channel.send('Error: type "start" to initialize')
        elif message.content.lower().startswith("block remove"):
            try:
                for prefference in content.split(" ")[2:]:
                    prefferences[message.author]["block"].remove(prefference)
            except KeyError: await message.channel.send('Error: type "start" to initialize')

        elif message.content.lower().startswith("pref"):
            await message.channel.send(prefferences[message.author])
        elif message.content.lower().startswith("reset"):
            prefferences[message.author] = {"am": set(), "looking": set(), "block": set()}

        elif message.content.startswith("wait"):
            waitingList.append(message.author)
        elif message.content.startswith("stop"):
            waitingList.remove(message.author)
        elif message.content.startswith("search"):
            for stranger in waitingList:
                if str(stranger) == str(message.author):
                    continue
                if len(prefferences[message.author]["am"].intersection(prefferences[stranger]["block"])) >= 1:
                    continue
                if len(prefferences[message.author]["block"].intersection(prefferences[stranger]["am"])) >= 1:
                    continue
                if not len(prefferences[message.author]["am"].intersection(prefferences[stranger]["looking"])) >= 1:
                    continue
                if not len(prefferences[message.author]["looking"].intersection(prefferences[stranger]["am"])) >= 1:
                    continue
                if not prefferences[message.author]["looking"].issubset(prefferences[stranger]["am"]):
                    continue
                if not prefferences[stranger]["looking"].issubset(prefferences[message.author]["am"]):
                    continue
                if prefferences[message.author]["block"] & prefferences[stranger]["am"]:
                    continue
                if not prefferences[stranger]["block"] & prefferences[message.author]["am"]:
                    continue
                await message.channel.send(stranger)
                await message.channel.send(prefferences[stranger])
                await message.channel.send("(sorry for the lazy formatting)")
                #TODO: figre out what to do here
            await message.channel.send('Not found, pleasee delete tags from "looking"')
        else:
            await message.channel.send('Type "start" to begin')

    else:
        pass

if __name__ == "__main__":
    client.run(TOKEN)