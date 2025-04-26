import discord
from discord.ext import commands
import aiohttp
from bs4 import BeautifulSoup
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Déclencheurs pour arrêter l'analyse
IGNORED_STARTS = ("1.", "2.", "3.", "4.", "@everyone")

@bot.command()
async def good(ctx):
    target_user_id = 1365648480571232328

    async for message in ctx.channel.history(limit=100):
        if message.author.id == target_user_id:
            content = message.content.strip()
            lines = content.splitlines()

            cleaned_lines = []
            for line in lines:
                stripped_line = line.strip()
                if not stripped_line:
                    # Si ligne vide -> on arrête
                    break
                if any(stripped_line.startswith(start) for start in IGNORED_STARTS):
                    # Si ligne commence par 1., 2., etc. -> on arrête
                    break
                cleaned_lines.append(stripped_line)

            if len(cleaned_lines) < 2:
                await ctx.send("❌ Format invalide : lien + texte attendu avant instructions/sauts de ligne.")
                return

            url = cleaned_lines[0]
            search_text = ' '.join(cleaned_lines[1:])

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
