import discord
import pytesseract
from PIL import Image
import io
import os

# Récupération du token via variables d'environnement
TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
bot = discord.Client(intents=intents)

@bot.event
async def on_ready():
    print(f'Bot connecté en tant que {bot.user}')

@bot.event
async def on_message(message):
    # Ignorer les messages du bot
    if message.author == bot.user:
        return

    if message.content == '!done':
        await message.channel.send("🔍 Analyse des 3 derniers messages...")

        messages = await message.channel.history(limit=1).flatten()

        embed = discord.Embed(
            title="Résultat de l'analyse",
            description="Voici l'état du dernier avis envoyé 📝",
            color=discord.Color.blue()
        )

        images_trouvees = False

        msg = messages[0]
        for attachment in msg.attachments:
                if attachment.filename.endswith(('.png', '.jpg', '.jpeg')):
                    images_trouvees = True
                    img_bytes = await attachment.read()
                    image = Image.open(io.BytesIO(img_bytes))
                    text = pytesseract.image_to_string(image, lang='fra')

                    if "En attente" in text:
                        resultat = "⏳ Ton avis est en attente, patiente pour voir s'il est publié."
                    elif "Non publié" in text:
                        resultat = "🚫 Ton avis n'est pas publié. Réessaie avec un autre compte Google, un VPN ou un autre appareil (ou les deux)."
                    elif "NOUVEAU" in text:
                        resultat = "✅ Ton avis est publié, c'est validé !"
                    else:
                        resultat = "❓ Impossible de déterminer l'état de cet avis."

                    embed.add_field(
                        name=f"Avis de {msg.author.mention}",
                        value=resultat,
                        inline=False
                    )

        if images_trouvees:
            await message.channel.send(embed=embed)
        else:
            await message.channel.send("❌ Aucune image détectée dans les 3 derniers messages.")

bot.run(TOKEN)
