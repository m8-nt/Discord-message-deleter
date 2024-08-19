import discord, json, time
from discord.ext import commands
from colorama import Fore

with open("./data/config.json", "r") as f:
    config = json.load(f)

bot = commands.Bot(command_prefix=config["prefix"], help_command=None, self_bot=True)

@bot.event
async def on_ready():
    print(f"[Logged in as {bot.user}]\nLatency: {bot.latency*1000}ms")

@bot.command()
async def purge(ctx, amount: int=None, limit=None):
    if amount is None and limit is None:
        await ctx.reply("message purge command.\nusage: -purge [amount] [float(time)]")
    count = 0
    messages = [message async for message in ctx.channel.history(limit=amount + 1)]
    for msg in messages:
        if msg.author == bot.user:
            try:
                await msg.delete()
                count += 1
                print(Fore.RED+"[DELETED]"+Fore.RESET+f" {msg.author} | {msg.content}")
                time.sleep(float(limit))
            except discord.errors.Forbidden as e:
                if e.code == 50021: 
                    pass
    await ctx.send(f"`deleted`", delete_after=5)
    print(Fore.GREEN+"[FINISHED]"+Fore.RESET+f" Count: {count}")

bot.run(config["token"])
