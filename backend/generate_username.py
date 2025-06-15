from flask_restful import Resource
from flask import request, abort, jsonify
from prisma.client import Client
from random import choice, randint

adjectives = ["Brave", "Witty", "Cheerful", "Quiet", "Fuzzy", "Gentle", "Curious", "Clever", "Zany", "Bubbly", "Lucky", "Jolly", "Sleepy", "Happy", "Sneaky", "Playful", "Merry", "Grumpy", "Nimble", "Peppy", "Spunky", "Charming", "Giddy", "Perky", "Snappy", "Sassy", "Mellow", "Wacky", "Cuddly", "Spry", "Shy", "Lively", "Feisty", "Chipper", "Rusty", "Bouncy", "Zesty", "Gleeful", "Tidy", "Sunny"]
nouns = ["Fox", "Panda", "Otter", "Tiger", "Wizard", "Gnome", "Unicorn", "Penguin", "Lynx", "Dolphin", "Falcon", "Sloth", "Panther", "Dragon", "Coyote", "Goblin", "Badger", "Griffin", "Rabbit", "Hawk", "Toad", "Pixie", "Squirrel", "Wombat", "Turtle", "Eagle", "Imp", "Raccoon", "Phoenix", "Moose", "Monkey", "Fennec", "Basilisk", "Weasel", "Yak", "Bear", "Gecko", "Lemur", "Chinchilla", "Kraken"]

def generate_display_name(db):
    for _ in range(10):  # Retry up to 10 times
        name = f"{choice(adjectives)}{choice(nouns)}{randint(0, 999)}"
        existing = db.anonymoususer.find_first(where={"displayName": name})
        if not existing:
            return name
    raise Exception("Could not find unique name")

class GenerateUsername(Resource):
    def post(self):
        db = Client()
        try:
            data = request.json
            anonId = data.get('anonId')

            db.connect()

            # If the user already exists, return their existing name
            anon_user_data = db.anonymoususer.find_first(
                where={"anonId": anonId}
            )
            if anon_user_data:
                return jsonify({"displayName": anon_user_data.displayName})

            # Otherwise, generate a new one and save it
            new_name = generate_display_name(db)

            created = db.anonymoususer.create(
                data={
                    "anonId": anonId,
                    "displayName": new_name
                }
            )

            return jsonify({"displayName": created.displayName})

        except Exception as e:
            print(e)
            abort(400, str(e))
        finally:
            db.disconnect()
