from flask_restful import Resource, Api
from flask import request, abort, jsonify
from prisma.client import Client
import pandas as pd

def serialized_data(response):
    return {
        "id": response.id,
        "email": response.email,
        "displayname": response.displayname,
        "username": response.username,
        "picture": response.picture
    }

class RetrieveProfile(Resource):
    def post(self):
        try:
            data = request.json
            profileId = data.get('user_id')

            if not profileId:
                abort(400, description="user_id is missing from request")

            db = Client()
            db.connect()
            response = db.profile.find_first(
                where={
                    "id": profileId,
                }
            )

            db.disconnect()

            if not response:
                abort(404, description="Profile not found")

            return jsonify(serialized_data(response))

        except Exception as e:
            print("Error:", e)
            abort(400, description=str(e))

    