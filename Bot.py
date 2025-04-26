import discord
from discord.ext import commands
import aiohttp
from aiohttp import ClientError
from bs4 import BeautifulSoup
import asyncio
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.command()
@commands.cooldown(rate=1, per=30, type=commands.BucketType.user)
async def good(ctx):
    def check_author(m):
        return m.author == ctx.author and m.channel == ctx.channel

    await ctx.send("🔗 Envoie-moi le lien à vérifier (format complet avec http/https) :")

    try:
        link_msg = await bot.wait_for('message', timeout=30.0, check=check_author)
        url = link_msg.content.strip()

        if not url.startswith("http"):
            await ctx.send("❌ Lien invalide. Annulation.")
            return

        await ctx.send("📝 Maintenant, envoie-moi le texte que je dois chercher sur la page :")

        text_msg = await bot.wait_for('message', timeout=60.0, check=check_author)
        search_text = text_msg.content.strip()

        if not search_text:
            await ctx.send("❌ Aucun texte reçu. Annulation.")
            return

        await ctx.send("🔎 Recherche en cours, patiente...")

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
                        await ctx.send(f"❌ Erreur d'accès à la page (Status {response.status})")
            except ClientError as e:
                await ctx.send(f"❌ Erreur réseau : {str(e)}")
            except Exception as e:
                await ctx.send(f"❌ Erreur inconnue : {str(e)}")

    except asyncio.TimeoutError:
        await ctx.send("⌛ Temps écoulé, tu n'as pas répondu assez vite. Annulation.")

@good.error
async def good_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"⏳ Patiente encore {error.retry_after:.1f} secondes avant de réutiliser cette commande.")

# Lancer le bot
TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    raise ValueError("Le token du bot Discord n'a pas été trouvé dans les variables d'environnement.")
bot.run(TOKEN)
