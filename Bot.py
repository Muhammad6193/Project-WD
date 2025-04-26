import discord
from discord.ext import commands
import aiohttp
from aiohttp import ClientError
from bs4 import BeautifulSoup
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Déclencheurs pour arrêter l'analyse
IGNORED_STARTS = ("1.", "2.", "3.", "4.", "@everyone")

@bot.command()
@commands.cooldown(rate=1, per=30, type=commands.BucketType.user)
async def good(ctx):
    target_user_id = 1364607789296521336

    async for message in ctx.channel.history(limit=100):
        if message.author.id == target_user_id:
            content = message.content.strip()
            lines = [line.strip() for line in content.splitlines()]

            cleaned_lines = []
            for line in lines:
                if not line:
                    break
                if any(line.startswith(start) for start in IGNORED_STARTS):
                    break
                cleaned_lines.append(line)

            if len(cleaned_lines) < 2:
                await ctx.send("❌ Format invalide : lien + texte attendu avant instructions/sauts de ligne.")
                return

            url = cleaned_lines[0]

            search_text_lines = cleaned_lines[1:]
            search_text = ' '.join(search_text_lines)

            if not url.startswith("http"):
                await ctx.send("❌ L'URL trouvée n'est pas valide.")
                return

            if not search_text:
                await ctx.send("❌ Aucun texte trouvé après l'URL.")
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
                except ClientError as e:
                    await ctx.send(f"❌ Erreur réseau : {str(e)}")
                except Exception as e:
                    await ctx.send(f"❌ Erreur inconnue : {str(e)}")
            return

    await ctx.send("❌ Aucun message récent de cet utilisateur trouvé.")

@good.error
async def good_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"⏳ Patiente encore {error.retry_after:.1f} secondes avant de réutiliser cette commande.")

# Lancer le bot
TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    raise ValueError("Le token du bot Discord n'a pas été trouvé dans les variables d'environnement.")
bot.run(TOKEN)
