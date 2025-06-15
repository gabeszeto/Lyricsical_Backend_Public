from flask_restful import Resource, Api
from flask import request, abort
from prisma.client import Client
from datetime import datetime as dt

class TotalPlays(Resource):
    def post(self):
        try:
            data = request.json
            trackId = data.get('trackId')
            counter = data.get('day_counter')
            db = Client()
            db.connect()

            print(trackId)

            #  why the fuck does this not work
            try: 
                db.history.update_many(
                    where={
                        "trackId": trackId,
                        "counter": counter
                    },
                    data={
                        "totalPlays": {
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
