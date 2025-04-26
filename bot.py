import discord
from discord.ext import commands
import asyncio
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.command()
@commands.cooldown(1, 30, commands.BucketType.user)
async def check(ctx):
    def check_msg(m):
        return m.author == ctx.author and m.channel == ctx.channel

    await ctx.send("🔗 Envoie-moi le lien Google Maps de l'entreprise :")

    try:
        msg_link = await bot.wait_for('message', timeout=30.0, check=check_msg)
        link = msg_link.content.strip()

        await ctx.send("📝 Maintenant, envoie-moi le texte exact de l'avis à vérifier :")

        msg_text = await bot.wait_for('message', timeout=60.0, check=check_msg)
        target_text = msg_text.content.strip().lower()

        await ctx.send("🕵️‍♂️ Recherche de l'avis en cours, patiente...")

        # Setup Chrome headless
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')

        driver = webdriver.Chrome(options=chrome_options)

        try:
            driver.get(link)
            time.sleep(5)  # attendre que la page charge

            body = driver.find_element(By.TAG_NAME, "body")
            for _ in range(10):
                body.send_keys(Keys.PAGE_DOWN)
                time.sleep(0.5)

            reviews = driver.find_elements(By.CLASS_NAME, "wiI7pd")
            found = False
            for review in reviews:
                if target_text in review.text.lower():
                    found = True
                    break

            if found:
                await ctx.send("✅ Avis trouvé sur la page !")
            else:
                await ctx.send("❌ Avis non trouvé.")
        except Exception as e:
            await ctx.send(f"❌ Erreur pendant la recherche : {str(e)}")
        finally:
            driver.quit()

    except asyncio.TimeoutError:
        await ctx.send("⌛ Temps écoulé, commande annulée.")

@check.error
async def check_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"⏱️ Patiente {error.retry_after:.1f} secondes avant de refaire la commande !")

# Lancer le bot
TOKEN = os.getenv("DISCORD_TOKEN")
bot.run(TOKEN)
