from flask_restful import Resource, Api
from flask import request, abort, jsonify
from prisma.client import Client
from datetime import datetime as dt

def get_useful_data(song):
    return {
        'pressTime': song.pressTime,
        'score': song.score
    }

class GetBarChart(Resource):
    def post(self):
        try:
            start = dt.now()
            data = request.json
            profileId = data.get('user_id')

            db = Client()
            db.connect()

            response = db.dailydata.find_many(
                where = {
                    "profileId": profileId,
                }
            )

            profile = db.profile.find_first(
                where = {
                    "id": profileId
                }
            )
            db.disconnect()

            playerData = {
                'streak': profile.streak,
                'maxStreak': profile.maxStreak,
                'totalPlays': profile.totalPlays
            }

            # Handle the case where no data was found
            if not response: 
                return jsonify({}) 
            

            scores = [song.score for song in response]


            scoreCounts = {
                "<0.5": 0,
                "0.5-1": 0,
                "1-2": 0,
                "2-5": 0,
                "5-10": 0,
                "10+": 0,
            }

            for time in scores:
                if time < 0.5:
                    scoreCounts["<0.5"] += 1
                elif time <= 1:
                    scoreCounts["0.5-1"] += 1
                elif time <= 2:
                    scoreCounts["1-2"] += 1
                elif time <= 5:
                    scoreCounts["2-5"] += 1
                elif time <= 10:
                    scoreCounts["5-10"] += 1
                else:
                    scoreCounts["10+"] += 1
                    
            combinedData = {
                'streaksData': playerData,
                'scoreCounts': scoreCounts
            }

            return jsonify(combinedData)
        except Exception as e:
            db.disconnect()
            abort(400, e)
        return
    