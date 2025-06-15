from flask_restful import Resource, Api
from flask import request, abort
from prisma.client import Client
from datetime import datetime as dt

class AddScores(Resource):
    def post(self):
        try:
            data = request.json
            profileId = data.get('profileId')
            trackId = data.get('trackId')
            score = data.get('score')
            press_time = data.get('pressTime')
            day_counter = data.get('dayCounter')

            is_anon = profileId is not None and 'anon' in profileId

            db = Client()
            db.connect()

            daily_data_payload = {
                "trackId": trackId,
                "day_counter": day_counter,
                "score": float(score),
                "pressTime": float(press_time),
                "anon": is_anon
            }

            if is_anon:
                daily_data_payload["anonId"] = profileId
            else:
                daily_data_payload["profileId"] = profileId

            try:
                added = db.dailydata.create(data=daily_data_payload)
            except Exception as e:
                print("Error creating DailyData:", e)
                db.disconnect()
                return

            
            # Profile-related logic only for non-anon users
            if not is_anon and profileId:
                profile = db.profile.find_first(
                    where={"id": profileId}
                )

                if profile:
                    db.profile.update(
                        where={"id": profileId},
                        data={
                            "streak": profile.streak + 1,
                            "maxStreak": max(profile.streak + 1, profile.maxStreak),
                            "totalPlays": profile.totalPlays + 1
                        }
                    )

            db.disconnect()
        except Exception as e:
            db.disconnect()
            print(e)
            abort(400, e)
        return
