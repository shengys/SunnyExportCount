import discord
import json
from discord.ext import tasks

# Gestion des intents
intents = discord.Intents.all()

# Créer un client Discord
client = discord.Client(intents=intents)


### Fonctions ###

## Ajoute une run au compteur ##
async def addRun(message):
  # Récupération du nom du runner
  firstCut = str.split(message.content, "] ")
  secondCut = str.split(firstCut[1], " a terminé un run")
  name = secondCut[0]

  # Ouverture du fichier Json en lecture
  with open("data.json", "r") as f:
    data = json.load(f)

  global alreadyExist
  alreadyExist = False

  # Accès aux données json
  members = data["members"]

  # Si l'employé est déjà dans le fichier, on ajoute 1 à son nombre de run
  for member in members:
    if member['name'] == name:
      member['count'] += 1
      alreadyExist = True
      break

  # Si il n'est pas dans le fichier, on le créer et on initialise son compteur à 1
  if not alreadyExist:
    new_member = {"name": name, "count": 1}
    members.append(new_member)

  # Mise à jour du fichier
  with open('data.json', 'w') as f:
    json.dump(data, f)


## Fonction pour editer le message de classement, elle se lance toutes les 1 minutes ##
@tasks.loop(minutes=1)
async def editFinal():

  # Récupération du channel "classement-runners"
  channel = client.get_channel(1080926837724684340)

  # Ouverture du Json en lecture
  with open("data.json", "r") as fop:
    data = json.load(fop)

  # Création du message final en insérant les données du Json
  gMessage = ">>> "
  members = data["members"]
  for member in members:
    gMessage += "**" + member["name"] + "** a effectué **" + str(
      member["count"]) + "** runs.\n"

  # Récupération du message de classement
  message = await channel.fetch_message(1081109092799631440)

  # Edit du message
  await message.edit(content=gMessage)


### Événements ###
@client.event
# Le bot est prêt
async def on_ready():
  print('Bot connecté en tant que {0.user}'.format(client))


# Événement pour écouter les messages
@client.event
async def on_message(message):

  # Si le message est une commande
  if message.content[0] == '!':

    # Création du message pour afficher le classement des runners
    if message.content == "!init":
      channel = client.get_channel(1080926837724684340)
      await channel.send(">>> ** **")

    # Commencer à récupérer les runs
    if message.content == "!start":
      editFinal.start()

  # Si nouveau message dans le channel suivi-run, on exécute la fonction d'ajout de run
  if message.channel.id == 1061651553531986010:
    await addRun(message)


# Lancement du bot
client.run(
  'MTA4MDU2MTk4NDMyMTM2ODE3NQ.G_l37S.8XeTScaIlyYr2zfd45Uq5V88TMsMAM7ciOHdog')
