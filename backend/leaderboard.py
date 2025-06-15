from flask_restful import Resource, Api
from flask import request, abort, jsonify
from prisma.client import Client
import pandas as pd

def serialize_player_profile(user_profile, user_score):
    return {
        "id": str(user_profile.id),
        "username": user_profile.username,
        "displayname": user_profile.displayname,
        "email": user_profile.email,
        "picture": user_profile.picture,
        "score": user_score
    }

def serialize_anon_score(anon_profile, user_score):
    return {
        "id": anon_profile.anonId,
        "username": None,
        "displayname": anon_profile.displayName,
        "email": None,
        "picture": None,
        "score": user_score
    }


class RetrieveLeaderboard(Resource):
    def post(self):
        try:
            data = request.json

            user_id = data.get('user_id')
            lookback = data.get('lookback')
            day_counter = data.get('day_counter')

            db = Client()
            db.connect()

            # Find trackId for the current song
            trackId = db.history.find_first(
                skip=lookback,
                order={
                    'counter': 'desc'
                }
            ).trackId

            # Find the artist and song names of trackId
            names = db.timing.find_first(
                where = {
                    'trackId': trackId
                }
            )

            realName = names.realName
            realArtist = names.realArtist

            # Find all instances of scores
            response = db.dailydata.find_many(
                where={
                    "trackId": trackId,
                    "day_counter": day_counter
                },
                include={
                    "profile": True,
                    "anonymousUser": True
                }
            )

            all_users = []
            current_user = None

            for entry in response:
                is_current_user = (
                    (not entry.anon and entry.profileId == user_id) or
                    (entry.anon and entry.anonId == user_id)
                )

                if entry.anon:
                    user_data = serialize_anon_score(entry.anonymousUser, entry.score)
                else:
                    user_data = serialize_player_profile(entry.profile, entry.score)

                if is_current_user:
                    current_user = user_data

                all_users.append(user_data)

            if current_user is None:
                if user_id.startswith("anon_"):
                    anonUser = db.anonymoususer.find_first(
                        where = {
                            'anonId': user_id
                        }
                    )
                    current_user = {
                        "id": user_id,
                        "username": None,
                        "displayname": anonUser.displayName,
                        "email": None,
                        "picture": None,
                        "score": None
                    }
                else:
                    profile = db.profile.find_first(where={"id": user_id})

                    if profile:
                        current_user = serialize_player_profile(profile, None)
            
            db.disconnect()
                
            final_result = {
                "user_profile": current_user,
                "all_users": all_users,
                "realName": realName,
                "realArtist": realArtist
            }
            return jsonify(final_result)
        except Exception as e:
            print(e)
