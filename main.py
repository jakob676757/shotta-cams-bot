import discord
from discord.ext import commands
from discord import app_commands
import os
from dotenv import load_dotenv
import json
from datetime import datetime

load_dotenv()
TOKEN = os.getenv('TOKEN')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Datei für Kundendaten
CUSTOMERS_FILE = 'customers.json'

def load_customers():
    if os.path.exists(CUSTOMERS_FILE):
        with open(CUSTOMERS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_customers(data):
    with open(CUSTOMERS_FILE, 'w') as f:
        json.dump(data, f, indent=4)

@bot.event
async def on_ready():
    print(f'{bot.user} ist online!')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

# Ticket System
@bot.tree.command(name="ticket_erstellen", description="Erstelle ein neues Ticket")
async def ticket_erstellen(interaction: discord.Interaction):
    await interaction.response.send_message("🎫 Ticket wird erstellt...", ephemeral=True)
    
    category_name = "tickets"
    category = discord.utils.get(interaction.guild.categories, name=category_name)
    
    if not category:
        category = await interaction.guild.create_category(category_name)
    
    ticket_channel = await interaction.guild.create_text_channel(
        name=f"ticket-{interaction.user.name}",
        category=category
    )
    
    embed = discord.Embed(
        title="🎫 Neues Ticket",
        description=f"Hallo {interaction.user.mention}!\n\nSchreib hier deine Anfrage auf.",
        color=discord.Color.green()
    )
    
    await ticket_channel.send(embed=embed)
    await ticket_channel.send(f"{interaction.user.mention}")
    
    await interaction.followup.send(f"✅ Ticket erstellt: {ticket_channel.mention}", ephemeral=True)

# Vorlage Befehle
@bot.tree.command(name="vorlage_ticket", description="Zeigt die Ticket-Vorlage")
async def vorlage_ticket(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🔒 TICKET GESCHLOSSEN – SHOTTA CAMS",
        description="",
        color=discord.Color.red()
    )
    
    embed.add_field(name="📅 Datum:", value="[Hier eingeben]", inline=False)
    embed.add_field(name="👤 Kunde:", value="[IGN]", inline=False)
    embed.add_field(name="💵 Preis:", value="[$ eingeben]", inline=False)
    embed.add_field(name="📦 Typ:", value="☐ Kauf  ☐ Preisanfrage  ☐ Händler  ☐ Freundschaft", inline=False)
    embed.add_field(name="👤 Bearbeitet:", value="[@mention]", inline=False)
    embed.add_field(name="📷 Verkauf IC:", value="[@mention]", inline=False)
    embed.add_field(name="💰 AUSZAHLUNG", value="45% Verkauf » $\n40% DC » $\n15% Beschaffer » $", inline=False)
    embed.add_field(name="📝 Notiz:", value="[Hier eingeben]", inline=False)
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="vorlage_kundendatei", description="Zeigt die Kundendatei-Vorlage")
async def vorlage_kundendatei(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🗂️ SHOTTA CAMS – KUNDEN AKTE",
        color=discord.Color.blue()
    )
    
    embed.add_field(name="👤 IGN:", value="[Name]", inline=False)
    embed.add_field(name="🎮 Discord:", value="[Discord Tag]", inline=False)
    embed.add_field(name="📅 Kunde seit:", value="[Datum]", inline=False)
    embed.add_field(name="🕐 Letzte Bestellung:", value="[Datum]", inline=False)
    embed.add_field(name="📦 Bestellungen gesamt:", value="[Anzahl]", inline=False)
    embed.add_field(name="📷 Bodycams gekauft:", value="[Anzahl]", inline=False)
    embed.add_field(name="💰 Gesamtumsatz:", value="[$]", inline=False)
    embed.add_field(name="📈 Größtes Paket:", value="[Paketname]", inline=False)
    embed.add_field(name="⭐ Stammkunde:", value="☐ Ja   ☐ Nein", inline=False)
    embed.add_field(name="🎁 Freundschaft:", value="☐ Ja   ☐ Nein", inline=False)
    embed.add_field(name="🤝 Mitarbeiter:", value="☐ Ja   ☐ Nein", inline=False)
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="vorlage_preise", description="Zeigt die aktuelle Preisliste")
async def vorlage_preise(interaction: discord.Interaction):
    embed = discord.Embed(
        title="💰 SHOTTA CAMS – PREISLISTE",
        color=discord.Color.gold()
    )
    
    embed.add_field(name="📷 Starter", value="25x | 21.000$ | 840$/Stück", inline=False)
    embed.add_field(name="📷 Standard", value="50x | 39.500$ | 790$/Stück", inline=False)
    embed.add_field(name="📷 Business", value="100x | 74.000$ | 740$/Stück", inline=False)
    embed.add_field(name="📷 Enterprise", value="200x | 138.000$ | 690$/Stück", inline=False)
    embed.add_field(name="🎁 Freundespreise", value="Auf Anfrage verfügbar", inline=False)
    
    await interaction.response.send_message(embed=embed)

# Gewinnspiel
@bot.tree.command(name="gewinnspiel_starten", description="Startet ein Gewinnspiel")
@app_commands.describe(preis="Der Hauptpreis des Gewinnspiels")
async def gewinnspiel_starten(interaction: discord.Interaction, preis: str):
    embed = discord.Embed(
        title="🎁 SHOTTA CAMS GEWINNSPIEL",
        description=f"**Hauptpreis:** {preis}\n\nReagiere mit ✅ um teilzunehmen!",
        color=discord.Color.green()
    )
    
    message = await interaction.response.send_message(embed=embed)
    await message.add_reaction("✅")

# Bot starten
bot.run(TOKEN)
