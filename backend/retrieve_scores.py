from flask_restful import Resource, Api
from flask import request, abort, jsonify
from prisma.client import Client
from datetime import datetime as dt

def daily_data_to_dict(daily_data):
    return {
        "id": daily_data.id,
        "profileId": daily_data.profileId,
        "trackId": daily_data.trackId,
        "pressTime": daily_data.pressTime,
        "score": daily_data.score,
    }

class RetrieveScores(Resource):
    def post(self):
        try:
            data = request.json
            profileId = data.get('profileId')
            trackId = data.get('trackId')

            db = Client()
            db.connect()
            response = db.dailydata.find_many(
                where = {
                    "profileId": profileId,
                    "trackId": trackId
                }
            )

            # Handle the case where no data was found
            if not response: 
                return jsonify([])  # Return an empty JSON array or another appropriate response

            response_data = [daily_data_to_dict(item) for item in response]
            return jsonify(response_data)
        except Exception as e:
            db.disconnect()
            abort(400, e)
        return
    