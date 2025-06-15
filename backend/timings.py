from flask_restful import Resource, Api
from flask import request, jsonify, abort
from prisma.client import Client
import json
from daily import DAILY_CLASS
import pandas as pd

timing_path = "backend\timings.csv"
class Timings(Resource):
    def get(self):
        return
    
    def post(self):
        timings = json.loads(pd.read_csv(r"backend\timings.csv", header=0).to_json(orient="records"))

        db = Client()
        db.connect()
        for entry in timings:
            track_id = entry["trackId"]
            start_time = entry.get("startTime", None)
            fade_time = entry.get("fadeTime", None)
            realName = entry.get("song_name", None)
            artistName = entry.get("artist_name", None)
            track = db.track.find_unique(
                where={"trackId": track_id},
            )

            response = db.timing.create(
                data = {
                    "startTime": start_time,
                    "fadeTime": fade_time,
                    "realName": realName,
                    "realArtist": artistName,
                    "track": {
                        "connect": {
                            "id": track.id
                        }
                    }
                }
            )

        db.disconnect()
        return 