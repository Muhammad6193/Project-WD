import discord
from discord.ext import commands
import undetected_chromedriver.v2 as uc
import asyncio

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.command()
async def avis(ctx, *, entreprise):
    await ctx.send("🕵️‍♂️ Recherche de l'avis en cours, patiente...")

    try:
        print("[INFO] Début de la recherche...")

        # Lancer le navigateur en headless
        options = uc.ChromeOptions()
        options.headless = True
        driver = uc.Chrome(options=options)

        print("[INFO] Navigateur lancé.")

        # Exemple d'ouverture de page
        search_url = f"https://www.google.com/search?q={entreprise}+avis"
        driver.get(search_url)

        print(f"[INFO] Page chargée : {search_url}")

        # Attendre que la page charge
        await asyncio.sleep(3)

        # Ici tu fais ton scraping par exemple :
        avis_text = "⭐ Exemple d'avis trouvé ⭐"  # (à remplacer avec ton vrai scraping)

        # Envoyer le résultat
        await ctx.send(f"✅ Avis trouvé pour **{entreprise}** : {avis_text}")

        # Fermer le navigateur
        driver.quit()

    except Exception as e:
        print(f"[ERROR] Une erreur est survenue : {e}")
        await ctx.send(f"❌ Erreur pendant la recherche : {e}")

