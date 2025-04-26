import discord
from discord.ext import commands
import undetected_chromedriver as uc
import asyncio

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Connecté en tant que {bot.user}")

@bot.command()
async def check(ctx):
    await ctx.send("📎 Merci d'envoyer le lien de la page Google Maps.")

    def check_msg(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        msg_link = await bot.wait_for('message', timeout=60.0, check=check_msg)
        lien = msg_link.content.strip()

        await ctx.send("📝 Merci maintenant d'envoyer le texte de l'avis.")

        msg_avis = await bot.wait_for('message', timeout=120.0, check=check_msg)
        texte_recherche = msg_avis.content.strip()

        await ctx.send("🔎 Recherche de l'avis... Patientez...")

        options = uc.ChromeOptions()
        options.binary_location = "/usr/bin/chromium"
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        driver = uc.Chrome(options=options)

        try:
            driver.get(lien)
            await asyncio.sleep(5)

            avis_elements = driver.find_elements("css selector", "div[jscontroller='e6Mltc']")

            trouve = False
            for avis in avis_elements:
                try:
                    contenu = avis.text
                    if texte_recherche.lower() in contenu.lower():
                        trouve = True
                        break
                except Exception:
                    continue

            if trouve:
                await ctx.send("✅ Avis trouvé !")
            else:
                await ctx.send("❌ Aucun avis correspondant trouvé.")

        except Exception as e:
            await ctx.send(f"⚠️ Erreur pendant la recherche : {e}")
        finally:
            driver.quit()

    except asyncio.TimeoutError:
        await ctx.send("⏰ Temps écoulé sans réponse. Merci de recommencer.")

bot.run("TON_TOKEN_DISCORD_ICI")
