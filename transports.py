import logging
import math
import sys
import time

import requests

token = sys.argv[1]

from telegram import Update
from telegram.ext import ContextTypes
from datetime import datetime

TRANSPORTS = "TRANSPORTS"

# Setup logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


def appeler_opendata(path):
    url = f"http://transport.opendata.ch/v1{path}"
    reponse = requests.get(url)
    print(reponse.json()) # Debug
    return reponse.json()

def rechercher_arrets(parametres):
    data = appeler_opendata(parametres)
    arrets = data['stations']
    message_texte = "Voici les résultats:\n"

    for arret in arrets:
        if arret['id']:
            message_texte = f'{message_texte}\n /s{arret["id"]}'
            message_texte = f'{message_texte} {arret["name"]}'
            message_texte = f'{message_texte} ({arret["icon"]})'

    return message_texte

def rechercher_prochains_departs(id):

    data = appeler_opendata(f'/stationboard?id={id}')
    stationboard = data['stationboard']

    message_texte = "Voici les prochains départs:\n"
    maintenant = time.time()

    for depart in stationboard:
        message_texte += f"\n\n{depart['number']} → {depart['to']}\n"

        timestamp_depart = depart['stop']['departureTimestamp']
        diff = timestamp_depart - maintenant
        temps_en_minutes = math.floor(diff/60)

        if temps_en_minutes < 0:
            message_texte += ' Déjà parti...'
        elif temps_en_minutes < 2:
            message_texte += ' COURS!'
        else:
            message_texte += f' dans {temps_en_minutes} minutes'

    return message_texte


async def recherche_arret_commande(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Vérifiez si le nom de l'arrêt est fourni
    if context.args:
        nom_arret = ' '.join(context.args)
        arrets = rechercher_arrets(f'/locations?query={nom_arret}')
        await update.message.reply_text(arrets)
    else:
        # Si aucun nom d'arrêt n'est fourni, vous pouvez envoyer un message d'erreur ou d'instructions
        await update.message.reply_text("Veuillez fournir le nom de l'arrêt après /stop. Exemple: /stop [nom de "
                                        "l'arrêt]")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}, utilise les commandes /stop '
                                    f'ou donne directement des cordonnées et un lieu.')
    return TRANSPORTS


async def handle_transport_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Traiter le texte ou la localisation envoyée par l'utilisateur
    user_input = update.message.text  # ou update.message.location pour les coordonnées
    prochains_departs = appeler_opendata(f'/stationboard?station={user_input}')  # Appelez la fonction avec les bons paramètres
    reponse = formater_prochains_departs(prochains_departs)  # Formatez la réponse
    await update.message.reply_text(reponse)


async def handle_stop_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Assurez-vous que l'utilisateur a bien fourni le nom de l'arrêt après /stop
    if len(context.args) > 0:
        nom_arret = ' '.join(context.args)
        # Appeler la fonction de recherche d'arrêt
        prochains_departs = rechercher_arrets(f'/stationboard?station={nom_arret}')
        # Formater et envoyer la réponse
        reponse = formater_prochains_departs(prochains_departs)
        await update.message.reply_text(reponse)
    else:
        await update.message.reply_text("Veuillez fournir le nom de l'arrêt après /stop. Par exemple: /stop Gare Cornavin")


"""
    Formate les données des prochains départs en un message texte.
    :param data: Les données récupérées de l'API de transport.
    :return: Une chaîne de caractères formatée avec les informations des prochains départs.
    """
def formater_prochains_departs(data):
    if 'stationboard' not in data:
        return "Aucune information de départ trouvée pour cet arrêt."

    message = "Prochains départs:\n\n"

    for depart in data['stationboard']:
        ligne = depart['number']
        destination = depart['to']
        heure_depart = depart['stop']['departure']

        # Convertir le temps de départ en un format lisible (si nécessaire)
        heure_depart = datetime.fromisoformat(heure_depart).strftime('%H:%M')
        # ...

        message += f"Ligne {ligne} vers {destination} - Départ à {heure_depart}\n"

    return message


async def afficher_arret(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    identifiant = update.message.text[2:]
    prochains_departs = rechercher_prochains_departs(identifiant)
    await update.message.reply_text(prochains_departs)


async def recherche_texte(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    texte_a_rechercher = update.message.text
    arrets = rechercher_arrets(f'/locations?query={texte_a_rechercher}')
    await update.message.reply_text(arrets)

"""
app = ApplicationBuilder().token(token).build()

app.add_handler(CommandHandler("transport", start))
app.add_handler(CommandHandler("stop", recherche_texte))
app.add_handler(MessageHandler(filters.COMMAND, afficher_arret))
app.add_handler(MessageHandler(filters.LOCATION, recherche_gps))
app.add_handler(MessageHandler(filters.TEXT, recherche_texte))

app.run_polling()
"""
