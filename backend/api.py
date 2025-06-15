from flask_restful import Resource, Api
import requests, json, random, schedule, time
from datetime import datetime as dt
from flask_cors import CORS
from flask_apscheduler import APScheduler
from flask import Flask, request, jsonify, abort
import scores_endpoints, retrieve_scores, leaderboard, retrieve_profile, barchart_data, modify_pp, update_displayname, update_username, total_plays, update_guesses, retrieve_guesses, generate_username
from prisma.client import Client
from daily import DAILY_CLASS
import os

app = Flask(__name__)
api = Api(app)

CORS(app)

class SelectedSong(Resource):
    def get(self):
        song_data = DAILY_CLASS.DAY_SONG
        song_json = song_data["track"].model_dump(round_trip=True)
        song_json["counter"] = song_data["counter"]
        return jsonify(song_json)

      
sched = APScheduler()

# Endpoints
api.add_resource(SelectedSong, '/selected-song/')
api.add_resource(scores_endpoints.AddScores, '/add-scores/')
api.add_resource(retrieve_scores.RetrieveScores, '/retrieve-scores/')
api.add_resource(leaderboard.RetrieveLeaderboard, '/retrieve-leaderboard/')
api.add_resource(retrieve_profile.RetrieveProfile, '/retrieve-profile/')
api.add_resource(barchart_data.GetBarChart, '/barchart/')
api.add_resource(modify_pp.ModifyProfilePicture, '/modify-profile-picture/')
api.add_resource(update_displayname.UpdateDisplayName, '/update-displayname/')
api.add_resource(update_username.UpdateUsername, '/update-username/')
api.add_resource(total_plays.TotalPlays, '/total-plays/')
api.add_resource(update_guesses.UpdateGuesses, '/update-guesses/')
api.add_resource(retrieve_guesses.RetrieveGuesses, '/retrieve-guesses/')
api.add_resource(generate_username.GenerateUsername, '/generate_username/')

# Every day scheduler
sched.add_job(id='refreshNumber', func=DAILY_CLASS.update_index, trigger = 'cron', day_of_week = 'mon-sun', hour = 23, minute = 00)

# Every minute scheduler (while developing)
# sched.add_job(id='refreshNumber', func=DAILY_CLASS.update_index, trigger = 'interval', seconds = 60)
sched.start()

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=True, use_reloader=False)

