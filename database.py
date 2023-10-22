from pymongo.mongo_client import MongoClient
import pprint
import os

uri = os.environ.get('uri')
client = MongoClient(uri)

def display(posts):
    for post in posts.find():
        pprint.pprint(post)

def add_player(player_name, player_score):
    if player_name is None or len(player_name) == 0:
        return

    post = {
        "name":player_name,
        "score":int(player_score)
    }

    # if player already exists update score if greater than the previous one.
    search_player = highscores.find_one({"name": post['name']})
    if (search_player):
        print(f"Name [{player_name}] already exists")
        if (post['score'] > int(search_player['score'])):
            print(f"Updating player's [{player_name}] score")
            highscores.update_one({'name': post['name']}, {'$set': {'score': player_score}})
    else:
        print(f"Adding new player -> Name: {player_name} | Score: {player_score}")
        highscores.insert_one(post).inserted_id

def get_leaderboard(posts, top):
    data = list(posts.find())
    sorted_data = sorted(data, key=lambda x: x['score'], reverse=True)
    result_string = '-----------------------------\n     LEADERBOARD\n-----------------------------\n'

    for i, d in enumerate(sorted_data[:top]):
        #print(f"Name: {d['name']:<10} | Score: {d['score']}")
        result_string += f"{i+1}. {d['name']:<10} - {d['score']}\n"
    return result_string

def show_leaderboard(posts, top):
    data = list(posts.find())
    sorted_data = sorted(data, key=lambda x: x['score'], reverse=True)

    for d in sorted_data[:top]:
        print(f"Name: {d['name']:<10} | Score: {d['score']}")

def get_highscores():
    return highscores

try:
    client.admin.command('ping')
    db = client.database_main
    highscores = db.highscores
    #show_leaderboard(highscores, 5)
    #get_leaderboard(highscores,5)

except Exception as e:
    print(e)