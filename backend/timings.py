from flask_restful import Resource, Api
from flask import request, jsonify, abort
from prisma.client import Client
import requests
import pydash
import json
from daily import DAILY_CLASS
import pandas as pd

timing_path = "backend\timings.csv"
class Timings(Resource):
    def get(self):
        return
    
    def post(self):
        timings = json.loads(pd.read_csv(r"backend\timings.csv", header=0).to_json(orient="records"))
        # print(timings)
        db = Client()
        db.connect()
        for entry in timings:
            track_id = entry["trackId"]
            start_time = entry.get("startTime", None)
            fade_time = entry.get("fadeTime", None)
            realName = entry.get("song_name", None) #this line
            artistName = entry.get("artist_name", None) #this line
            track = db.track.find_unique(
                where={"trackId": track_id},
            )

            response = db.timing.create(
                data = {
                    "startTime": start_time,
                    "fadeTime": fade_time,
                    "realName": realName, #this line
                    "realArtist": artistName, #this line
                    "track": {
                        "connect": {
                            "id": track.id
                        }
                    }
                }
            )

        db.disconnect()
        return 
    
    # def update_timings(self, entry, db):
    #     track_id = entry["trackId"]
    #     start_time = entry.get("startTime", None)
    #     fade_time = entry.get("fadeTime", None)

    #     track = db.track.find_unique(
    #         where={"trackId": track_id},
    #     )

    #     response = db.timing.create(
    #         data = {
    #             "startTime": start_time,
    #             "fadeTime": fade_time,
    #             "track": {
    #                 "connect": {
    #                     "id": track.id
    #                 }
    #             }
    #         }
    #     )
        
