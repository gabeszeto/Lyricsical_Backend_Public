from flask_restful import Resource, Api
from flask import request, abort, jsonify
from prisma.client import Client
from datetime import datetime as dt

class RetrieveGuesses(Resource):
    def post(self):
        try:
            data = request.json
            trackId = data.get('trackId')

            db = Client()
            db.connect()

            guesses_data = db.history.find_first(
                where = {
                    "trackId": trackId
                }
            )
            db.disconnect()

            guesses = {
                'correctGuesses': guesses_data.correctGuesses,
                'wrongGuesses1': guesses_data.wrongGuesses1,
                'wrongGuesses2': guesses_data.wrongGuesses2
            }

            print(guesses)

            return jsonify(guesses)
        except Exception as e:
            db.disconnect()
            abort(400, e)
        return