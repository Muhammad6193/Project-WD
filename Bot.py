import discord
from discord.ext import commands
import aiohttp
from bs4 import BeautifulSoup
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Partie à ignorer
PARTIE_A_IGNORER = """1.✂️ Copie colle le texte écrit mais si il n'y a pas de texte écris un texte en rapport avec l'entreprise ! 
2.⭐ Mets 5 étoiles 
3.✅ Tape !done et ajoute une capture d'écran de ton avis publié en pièce jointe 
4.⏰ Tu as 10 minutes maximum pour réaliser l'avis ! 

@everyone"""

@bot.command()
async def good(ctx):
    target_user_id = 1365648480571232328

    async for message in ctx.channel.history(limit=100):
        if message.author.id == target_user_id:
            content = message.content.strip()

            # Supprimer la partie à ignorer
            cleaned_content = content.replace(PARTIE_A_IGNORER, "").strip()

            # Séparer par lignes
            lines = cleaned_content.splitlines()
            lines = [line.strip() for line in lines if line.strip()]

            if len(lines) < 2:
                await ctx.send("❌ Le dernier message de l'utilisateur n'a pas le bon format (lien + texte sur 2 lignes).")
                return

            url = lines[0]
            search_text = lines[1]

            if not url.startswith("http"):
                await ctx.send("❌ L'URL trouvée n'est pas valide.")
                return

            async with aiohttp.ClientSession() as session:
                try:
                    async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                        if response.status == 200:
                            html = await response.text()
                            soup = BeautifulSoup(html, 'html.parser')
                            page_text = ' '.join(soup.get_text(separator=' ').split()).lower()

                            if search_text.lower() in page_text:
                                await ctx.send("✅ Le texte a été trouvé sur la page !")
                            else:
                                await ctx.send("❌ Texte introuvable sur la page.")
                        else:
                            await ctx.send(f"❌ Erreur en accédant à la page (Status {response.status})")
                except Exception as e:
                    await ctx.send(f"❌ Erreur lors de la connexion au site : {str(e)}")
            return

    await ctx.send("❌ Aucun message récent de cet utilisateur trouvé.")

# Lancer le bot
TOKEN = os.getenv("DISCORD_TOKEN")
bot.run(TOKEN)
