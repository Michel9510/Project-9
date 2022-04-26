from flask import Flask, jsonify, request
from peewee import *
from playhouse.shortcuts import model_to_dict, dict_to_model

db = PostgresqlDatabase('michel', user='michel',
                        password='12345', host='localhost', port=5432)


class BaseModel(Model):
    class Meta:
        database = db


class GamesList(BaseModel):
    title = CharField()
    genre = CharField()
    year = IntegerField()
    description = CharField()


db.connect()
db.drop_tables([GamesList])
db.create_tables([GamesList])

Pokemon_Legend = GamesList(title='Pokemon Legend: Arceus', genre='Action role-playing', year='2022',
                       description='Pokémon Legends: Arceus is an action role-playing game that preserves the core gameplay of past entries in the main line series. The player is able to roam freely across the game map, divided into five large areas of individual biomes.')
Pokemon_Unite = GamesList(title='Pokemon Unite', genre='Multiplayer online battle arena, real-time strategy', year='2021',
                      description='Pokémon Unite is a multiplayer online battle arena game, with standard matches consisting of two teams of five players. Each match is time-limited, and the team with the highest total score by the end of each match wins. There is also quick battles, which has 4 people per team, and is 5 minutes long.')
Call_of_Duty_MW2 = GamesList(title='Call of Duty: Modern Warfare 2', genre='RPG, Multiplayer, Action', year='2009',
                         description='Call of Duty: Modern Warfare 2 is a 2009 first-person shooter game developed by Infinity Ward and published by Activision. It is the sixth installment in the Call of Duty series and the direct sequel to Call of Duty 4: Modern Warfare.')
Call_of_Duty_BO = GamesList(title='Call of Duty: Black Ops', genre='RPG, Multiplayer, Action', year='2010',
                        description='Call of Duty: Black Ops is a 2010 first-person shooter game developed by Treyarch and published by Activision. It was released worldwide in November 2010 for Microsoft Windows, the PlayStation 3, Wii, and Xbox 360, with a separate version for Nintendo DS developed by n-Space.')
Battlefield_BC2 = GamesList(title='Battlefield: Bad Company 2', genre='RPG, Multiplayer, Action', year='2010',
                        description='Battlefield: Bad Company 2 is a first-person shooter video game developed by the Swedish firm DICE and published by Electronic Arts for Microsoft Windows, PlayStation 3, Xbox 360, iOS and Kindle Fire systems. It is a direct sequel to Battlefield: Bad Company and is part of the Battlefield game series.')
Battlefield4 = GamesList(title='Battlefield 4', genre='RPG, Multiplayer, Action', year='2013',
                     description='Battlefield 4™ features an intense and character-driven single player campaign, fused with the strongest elements of multiplayer. Pilot vehicles, take advantage of the dynamic destructible environments.')

Pokemon_Legend.save()
Pokemon_Unite.save()
Call_of_Duty_MW2.save()
Call_of_Duty_BO.save()
Battlefield_BC2.save()
Battlefield4.save()

app = Flask(__name__)


@app.route('/gameslists',  methods=['GET', 'POST', 'PUT', 'DELETE'])
@app.route('/gameslists/<id>',  methods=['GET', 'POST', 'PUT', 'DELETE'])
# def games(id=None):
   if request.method == 'GET':
        if id:
            game = GamesList.get(GamesList.id == id)
            game = model_to_dict(game)
            return jsonify(game)
        else:
            games = []
            for game in GamesList.select():
                games.append(model_to_dict(game))
            return jsonify(games)

    if request.method == 'POST':
        gameslist = request.get_json()
        gameslist = dict_to_model(GamesList, gameslist)
        gameslist.save()
        gameslist = model_to_dict(gameslist)
        gameslist = jsonify(gameslist)
        return gameslist

    if request.method == 'DELETE':
        gameslist = GamesList.get(GamesList.id == id)
        gameslist.delete_instance()
        return jsonify({"deleted": True})

    if request.method == 'PUT':
        update_game = request.get_json()
        gameslist = GamesList.get(GamesList.id == id)
        gameslist.title = update_game['title']
        gameslist.genre = update_game['genre']
        gameslist.year = update_game['year']
        gameslist.description = update_game['description']
        gameslist.save()
        gameslist = model_to_dict(gameslist)
        gameslist = jsonify(gameslist)
        return gameslist

app.run(port=3000, debug=True)
