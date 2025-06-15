from flask_restful import Resource, Api
from flask import request, abort
from prisma.client import Client
from datetime import datetime as dt

class UpdateGuesses(Resource):
    def post(self):
        try:
            data = request.json
            guess = data.get('guessData')
            trackId = data.get('trackId')
            counter = data.get('day_counter')
            db = Client()
            db.connect()
            try: 
                db.history.update_many(
                    where={
                        "trackId": trackId,
                        "counter": counter,
                    },
                    data={
                        guess: {
                            'increment': 1
                        }
                    }
                )
            except Exception as e:
                print(e)
                db.disconnect()
                return

            db.disconnect()
        except Exception as e:
            db.disconnect()
            print(e)
            abort(400, e)
        return
