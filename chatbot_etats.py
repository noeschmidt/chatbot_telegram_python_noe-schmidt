import logging, sys, telegram

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from transports import start as start_transports
from transports import recherche_texte

# Token for Telegram Bot
token = sys.argv[1]
(MUSEUM, BARS, CLUBS, RESTAURANT, CHOICE, SORTIES_CHOICE, RESTAURANT_CHOICE, END,
 RESTAU_RESULTATS, BACK_SORTIE, BACK_RESTAURANT) = range(11)
GO_BACK = -1

# Setup logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the conversation and asks the user about if they're looking for going out or a restaurant."""
    reply_keyboard = [["Sorties", "Restaurant"]]

    await update.message.reply_text(
        "Salut, je suis le bot de Noé et je suis là pour t'aider à Genève !\n\n"
        "Envoie /cancel pour arrêter de discuter.\n\n"
        "Veux-tu que je t'assiste pour des idées de sorties ou de restaurants ?",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, resize_keyboard=True
        ),
    )

    return CHOICE


async def transport(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the conversation and asks the user about if they're looking for going out or a restaurant."""
    reply_keyboard = [["Sorties", "Restaurant"]]

    await update.message.reply_text(
        "Salut, je suis le bot de Noé et je suis là pour t'aider à Genève !\n\n"
        "Envoie /cancel pour arrêter de discuter.\n\n"
        "Veux-tu que je t'assiste pour des idées de sorties ou de restaurants ?",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, resize_keyboard=True
        ),
    )

    return CHOICE


# Handle user's choice
async def handle_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_choice = update.message.text
    context.user_data['previous_state'] = CHOICE

    if user_choice == "Sorties":
        return await handle_sorties(update, context)
    elif user_choice == "Restaurant":
        return await handle_restaurant(update, context)
    else:
        await update.message.reply_text("Je n'ai pas compris, peux-tu répéter ?")
        return CHOICE


# Handle sorties choice
async def handle_sorties(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_choice = update.message.text
    reply_keyboard = [["Musées", "Bars", "Clubs", "Restaurant", "Retour"]]

    await update.message.reply_text(
        "Tu as donc choisi une sortie!\n\n"
        "Fais maintenant ton choix entre les choix suivants.\n\n"
        "Musées, bars, clubs, ou finalement restaurant ?",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, resize_keyboard=True
        ), )
    return SORTIES_CHOICE


# Fonctions pour gérer les choix Musées, Bars et Clubs
async def handle_museum(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # Logique pour Musées
    reply_keyboard = [["Retour"]]
    user_choice = update.message.text

    await update.message.reply_text(
        """Tu as donc choisi les musées, voici une séléction des plus intéressants! Musée d'Art et d'Histoire :
Le Musée d'Art et d'Histoire est l'un des plus grands musées de Genève et offre une immersion riche dans 
l'art et la culture. Avec une collection qui s'étend de l'Antiquité à l'art moderne, le musée abrite des 
œuvres d'artistes renommés tels que Konrad Witz, Rembrandt, et Cézanne. En plus de ses expositions d'art, 
le musée présente également des artefacts historiques et archéologiques, offrant un aperçu fascinant de 
l'histoire de la civilisation.\n\nMuséum d'histoire naturelle : \nCe musée est un incontournable pour les 
amoureux de la nature et de la science. Il est réputé pour être l'un des plus grands musées d'histoire 
naturelle de Suisse. Ses expositions couvrent une vaste gamme de sujets, des dinosaures et des mammifères 
préhistoriques à la faune et la flore actuelles. Le musée est particulièrement célèbre pour ses expositions 
interactives et ses dioramas réalistes, qui captivent à la fois les enfants et les adultes.\n\n 
Musée International de la Croix-Rouge et du Croissant-Rouge : \nUnique en son genre, ce musée est dédié à l'histoire 
et aux activités de la Croix-Rouge et du Croissant-Rouge. Il offre une perspective émouvante sur les efforts 
humanitaires à travers le monde. Les expositions interactives et multimédias du musée mettent en lumière des 
thèmes tels que la défense des droits de l'homme, la réduction des catastrophes naturelles, et l'assistance 
en cas de guerre. C'est une visite enrichissante qui sensibilise à l'importance de l'aide humanitaire et de 
la solidarité internationale.""",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, resize_keyboard=True
        ),
    )

    return BACK_SORTIE


async def handle_bars(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # Logique pour bars
    reply_keyboard = [["Retour"]]
    user_choice = update.message.text
    context.user_data['previous_state'] = CHOICE  # Stocke l'état actuel

    await update.message.reply_text(
        """L'Atelier Cocktail Club : \n
Situé au cœur de Genève, L'Atelier Cocktail Club est réputé pour son ambiance 
sophistiquée et sa vaste sélection de cocktails créatifs. Ce bar est l'endroit idéal pour les amateurs de 
cocktails qui cherchent à explorer des saveurs uniques. L'intérieur élégant et l'éclairage tamisé créent une 
atmosphère parfaite pour une soirée détendue. Leur équipe de barmans expérimentés est toujours prête à 
recommander ou à créer un cocktail sur mesure selon tes goûts.\n\n 
Le Verre à Monique : \n
Ce bar à cocktails intime et quelque peu caché offre une expérience unique avec une touche vintage. Le Verre à Monique 
est connu pour son ambiance rétro-chic et sa carte de cocktails innovants. C'est l'endroit parfait pour ceux qui 
cherchent à s'évader dans un monde de saveurs exquises et de mélanges audacieux. Le décor, inspiré des années 1920, 
associé à une musique d'ambiance, fait de ce bar un joyau pour une soirée mémorable.\n\n 
La Clémence : \n
Situé dans le charmant quartier de la Vieille-Ville, La Clémence est célèbre pour son cadre historique et sa terrasse 
animée. C'est un lieu de rencontre populaire tant pour les locaux que pour les touristes. Idéal pour profiter 
d'un verre en plein air, ce bar offre une vue pittoresque sur les rues pavées et les bâtiments anciens de 
Genève. Avec une bonne sélection de bières et de vins, c'est l'endroit parfait pour se détendre après une 
journée de travail ou pour se retrouver entre amis.""",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, resize_keyboard=True
        ),
    )
    return BACK_SORTIE


async def handle_clubs(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # Logique pour clubs
    reply_keyboard = [["Retour"]]
    user_choice = update.message.text
    context.user_data['previous_state'] = CHOICE  # Stocke l'état actuel

    await update.message.reply_text(
        """Le Java Club : \n
Situé sous l'hôtel N'vY, le Java Club est l'un des clubs les plus branchés de Genève. Avec 
son design moderne et son système de son de pointe, ce club attire une foule chic et tendance. Les DJ 
internationaux et locaux qui s'y produisent assurent une ambiance électrisante, jouant une variété de genres 
musicaux allant de la house à la musique électronique. C'est l'endroit idéal pour ceux qui cherchent à danser 
toute la nuit dans un cadre élégant et contemporain. \n\n
L'Usine : \n
L'Usine, un centre culturel alternatif situé dans une ancienne usine, est le cœur de la scène underground de Genève. 
Ce club est connu pour sa  programmation éclectique, incluant des concerts de rock, de l'électro, du hip-hop, 
et bien plus. Avec  plusieurs espaces, dont une salle de concert et un cinéma, L'Usine offre une expérience plus brute 
et authentique, parfaite pour ceux qui cherchent à découvrir la scène alternative de Genève.\n\n 
Le Mambo Club : \n
Le Mambo Club offre une ambiance plus intime et conviviale, idéale pour ceux qui aiment la salsa, le reggaeton, 
et les rythmes latins. Avec des cours de danse en début de soirée suivis de soirées dansantes, c'est un lieu 
parfait pour les débutants comme pour les danseurs expérimentés. Le club attire une foule diversifiée et 
énergique, et c'est un excellent choix pour une soirée amusante et décontractée.""",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, resize_keyboard=True
        ),
    )
    return BACK_SORTIE


async def handle_restaurant(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    reply_keyboard = [["Suisse", "Italien", "Asiatique", "Française", "Lebanese", "Retour"]]
    await update.message.reply_text(
        "Choix judicieux, maintenant choisis un type de restaurant\n",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True),
    )
    return RESTAURANT_CHOICE


# Fonction pour gérer les restaurants

async def handle_restaurant_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    reply_keyboard = [["Les Curiades", "Au Furet", "Châteauvieux", "Couronne", "KFC", "Retour"]]
    await update.message.reply_text(
        "Ma foi, plusieurs restaurants te sont proposés en fonction de ta caste. \n Fais le bon choix.",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True),
    )
    return RESTAU_RESULTATS


async def restaurant_details(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_choice = update.message.text
    reply_keyboard = [["Autres restaurants"]]

    await update.message.reply_text(
        """Adresse : Avenue d'Aïre 40, 1203 Genève\n
Telephone : 022 345 39 20\n
Site web : www.aufuret.com\n
Courte description : N°1 des gambas à Gogo ! C’est en 1985 que Chantal et Michel Corajod reprennent l’établissement, 
d’abord café-restaurant P.M.U. Mais c’est 10 ans plus tard que l’aventure
des GAMBAS A GOGO démarre réellement avec sa fameuse recette à l’ail et sa formule à volonté accompagné d’une salade
et de frites fraîches.
Ce produit noble connaît vite un succès à la fois local mais aussi cosmopolite.
A ceci ajoutés une carte de brasserie variée et un plat du jour attrayant, don son fameux coquelet entier aux bolets à 15.-  
et  l’entrecôte parisienne beurre maison à 17.-
C’est toujours avec grand plaisir qu’ils vous ouvrent tout grand leurs portes et leur savoir-faire.""",
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True),
    )
    return BACK_RESTAURANT


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text(
        "Conversation annulée. À bientôt !",
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(token).build()

    # Add conversation handler with the differents states
    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("start", start),
            CommandHandler("transport", start_transports),
        ],
        states={
            CHOICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_choice)],
            SORTIES_CHOICE: [
                MessageHandler(filters.Regex('^Musées$'), handle_museum),
                MessageHandler(filters.Regex('^Bars'), handle_bars),
                MessageHandler(filters.Regex('^Clubs'), handle_clubs),
                MessageHandler(filters.Regex('^Restaurant'), handle_restaurant),
                MessageHandler(filters.Regex('^Retour$'), start),
            ],
            RESTAURANT_CHOICE: [
                MessageHandler(filters.Regex('^Suisse'), handle_restaurant_choice),
                MessageHandler(filters.Regex('^Italien'), handle_restaurant_choice),
                MessageHandler(filters.Regex('^Asiatique'), handle_restaurant_choice),
                MessageHandler(filters.Regex('^Française'), handle_restaurant_choice),
                MessageHandler(filters.Regex('^Lebanese'), handle_restaurant_choice),
                MessageHandler(filters.Regex('^Retour$'), start),
            ],
            RESTAU_RESULTATS: [
                MessageHandler(filters.Regex('^Les Curiades'), restaurant_details),
                MessageHandler(filters.Regex('^Au Furet'), restaurant_details),
                MessageHandler(filters.Regex('^Châteauvieux'), restaurant_details),
                MessageHandler(filters.Regex('^Couronne'), restaurant_details),
                MessageHandler(filters.Regex('^KFC'), restaurant_details),
                MessageHandler(filters.Regex('^Retour'), handle_restaurant)
            ],
            BACK_SORTIE: [
                MessageHandler(filters.Regex('^Retour'), handle_sorties),
            ],
            BACK_RESTAURANT: [
                MessageHandler(filters.Regex('^Retour'), handle_restaurant_choice),
                MessageHandler(filters.Regex('^Autres restaurants'), handle_restaurant_choice),
            ],
            END: [
                MessageHandler(filters.Regex('^Retour'), start),
            ],
        },
        fallbacks=[
            CommandHandler("cancel", cancel),
            CommandHandler("stop", recherche_texte)
        ],
    )

    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
