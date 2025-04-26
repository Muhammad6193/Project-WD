import discord
from discord.ext import commands
from PIL import Image
import imagehash
import aiohttp
import io
import os  # <-- important pour récupérer le token

bot = commands.Bot(command_prefix="!")

# Base de données temporaire
image_to_message = {}

# Dernière image vue par utilisateur
last_image_hash_by_user = {}

@bot.event
async def on_ready():
    print(f'Connecté en tant que {bot.user}!')

@bot.event
async def on_message(message):
    if message.attachments:
        for attachment in message.attachments:
            if any(attachment.filename.lower().endswith(ext) for ext in ["png", "jpg", "jpeg"]):
                # Télécharger l'image
                async with aiohttp.ClientSession() as session:
                    async with session.get(attachment.url) as resp:
                        img_bytes = await resp.read()
                        img = Image.open(io.BytesIO(img_bytes))
                        img_hash = str(imagehash.average_hash(img))

                        # Enregistrer l'image vue pour l'utilisateur
                        last_image_hash_by_user[message.author.id] = img_hash

    await bot.process_commands(message)

@bot.command()
async def good(ctx):
    user_id = ctx.author.id
    img_hash = last_image_hash_by_user.get(user_id)

    if img_hash and img_hash in image_to_message:
        await ctx.send(image_to_message[img_hash])
    else:
        await ctx.send("Je ne connais pas encore cette image 😕")

@bot.command()
async def teach(ctx, *, msg):
    user_id = ctx.author.id
    img_hash = last_image_hash_by_user.get(user_id)

    if img_hash:
        image_to_message[img_hash] = msg
        await ctx.send("Message associé à l'image !")
    else:
        await ctx.send("Pas d'image récente trouvée.")

# ------------------------
# Partie du TOKEN sécurisé
# ------------------------

# Le bot récupère le token de l'environnement
TOKEN = os.getenv("DISCORD_TOKEN")

# Démarrer le bot
bot.run(TOKEN)
