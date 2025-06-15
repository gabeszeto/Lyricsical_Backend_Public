import requests
from prisma.client import Client
import random
import json
import pandas as pd
from decimal import Decimal
from datetime import datetime as dt, timedelta

DEFAULT_TRACK_ID = '26501700' # Toxic by Britney
PLAYLIST_ID = '1764032334' # Gabe's playlist of songs



class Daily:
    def __init__(self):
        # self.API_KEY = API_KEY
        self.DAY_SONG = self.update_index()

    def reset_actives(self):
        print("Resetting Actives")
        db = Client()
        db.connect() 
        db.track.update_many(
            where={
                'active': False
            },
            data={
                'active': True
            }
        )
        db.disconnect()
        return
    

    def update_index(self):
        # self.update_streaks()
        db = Client()
        db.connect()

        print('index_updated')

        queue_song = db.queue.find_first()

        print(queue_song)

        if queue_song:
            response = db.track.find_many(
                where={
                    'id': queue_song.trackId
                },
                include = {
                    'start': True
                }
            )

            delete_queue = db.queue.delete(
                where={
                    "id": queue_song.id
                }
            )
        
        else: 
            response = db.track.find_many(
                where={
                    'active': True
                },
                include = {
                    'start': True
                }
            )

        if not response:
            self.reset_actives()
            response = db.track.find_many(
                where={
                    'active': True
                },
                include = {
                    'start': True
                }
            )

        index = random.randint(0, len(response) - 1)
        db.track.update(
            where={
                'id': response[index].id
            },
            data={
                'active': False
            }
        )

        current_song = db.history.find_first(
            order={
                "counter": "desc"  # order by descending
            }
        )

        if current_song:
            print('song_exists')
            self.update_streaks(current_song)
            counter = current_song.counter
        else:
            counter = 0
            print('no songs yet')
        # add current song intop the history database
        add_history = db.history.create(
            data={
                # 'trackId': response[index].id,
                'realName': response[index].name,
                'counter': counter + 1,
                "track": {
                    "connect": {
                        "id": response[index].id
                    }
                }
            },
            
        )

        db.disconnect()
        # self.DAY_SONG = response[index]
        self.DAY_SONG = {
            "track": response[index],
            "counter": counter + 1
        }
        return self.DAY_SONG
    
    def update_streaks(self, current_song):
        print(current_song.trackId)

        try:
            db = Client()
            db.connect()

            # find users who have a streak and save as 'users'
            users = db.profile.find_many(
                where={
                    "streak" : {
                        "gt": 0,
                    }
                }
            )
            # stop function if all users have no streak
            if not users:
                print('no users')
                return
            
            print("******")
            print(users)
            print("******")
            # check daily data and save 'active' as users who have played today's song and have an active streak
            try:
                active = db.dailydata.find_many(
                    where={
                        "profileId": {
                            "in": [profile.id for profile in users]
                        },
                        "trackId": current_song.trackId
                    }
                )
            except Exception as e:
                # print(Daily.)
                print("streak daily updater: ", e)
                return
            print(active)
            # Update the streaks table for every profileId in inactive
            res = db.profile.update_many(
                where={
                    "id": {
                        "notIn": [user.profileId for user in active]
                    }
                },
                data={
                    "streak": 0
                }
            )
            print("*******")
            print(res)

            db.disconnect()
        except Exception as e:
            print("Streaks", e)

        return 
DAILY_CLASS = Daily()
