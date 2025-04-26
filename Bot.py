import discord
from discord.ext import commands
import aiohttp
from bs4 import BeautifulSoup
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.command()
async def good(ctx):
    target_user_id = 1364607789296521336

    # Chercher dans les 100 derniers messages du salon
    async for message in ctx.channel.history(limit=100):
        if message.author.id == target_user_id:
            content = message.content.strip()

            # On va supposer que le message est sous la forme : "lien texte"
            parts = content.split(maxsplit=1)

            if len(parts) != 2:
                await ctx.send("❌ Le dernier message de l'utilisateur n'a pas le bon format (lien + texte).")
                return

            url, search_text = parts

            # Vérifier que l'url commence par http
            if not url.startswith("http"):
                await ctx.send("❌ L'URL trouvée n'est pas valide.")
                return

            # Aller chercher la page web
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        html = await response.text()
                        soup = BeautifulSoup(html, 'html.parser')
                        page_text = soup.get_text(separator=' ').lower()

                        if search_text.lower() in page_text:
                            await ctx.send("✅ Avis valide tu en veux encore !avis !")
                        else:
                            await ctx.send("❌ Avis non posté.")
                    else:
                        await ctx.send(f"Erreur en accédant à la page (Status {response.status})")
            return

    # Si aucun message trouvé
    await ctx.send("❌ Aucun Avis en cours dans ce salon.")

# Lancer le bot
TOKEN = os.getenv("DISCORD_TOKEN")
bot.run(TOKEN)
