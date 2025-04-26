import discord
from discord.ext import commands
from PIL import Image
import imagehash
import aiohttp
import io
import os

# Important : définir les intents
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

image_to_message = {}
last_image_hash_by_user = {}

@bot.event
async def on_ready():
    print(f'Connecté en tant que {bot.user}!')

@bot.event
async def on_message(message):
    if message.attachments:
        for attachment in message.attachments:
            if any(attachment.filename.lower().endswith(ext) for ext in ["png", "jpg", "jpeg"]):
                async with aiohttp.ClientSession() as session:
                    async with session.get(attachment.url) as resp:
                        img_bytes = await resp.read()
                        img = Image.open(io.BytesIO(img_bytes))
                        img_hash = str(imagehash.average_hash(img))
                        last_image_hash_by_user[message.author.id] = img_hash

    await bot.process_commands(message)

@bot.command()
async def good(ctx):
    user_id = ctx.author.id
    img_hash = last_image_hash_by_user.get(user_id)

    if img_hash and img_hash in image_to_message:
        await ctx.send(image_to_message[img_hash])
    else:
        await ctx.send("Ce n'est pas un avis google valide 😕")

@bot.command()
async def teach(ctx, *, msg):
    user_id = ctx.author.id
    img_hash = last_image_hash_by_user.get(user_id)

    if img_hash:
        image_to_message[img_hash] = msg
        await ctx.send("Message associé à l'image !")
    else:
        await ctx.send("Pas d'image récente trouvée.")

# Le token depuis Railway
TOKEN = os.getenv("DISCORD_TOKEN")
bot.run(TOKEN)
