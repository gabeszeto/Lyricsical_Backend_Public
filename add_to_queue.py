import sys
import os

trackId = input("Please enter the Tracksongid: ")

from backend.prisma.client import Client
db = Client()
db.connect()

track = db.track.find_first(
    where={
        "id": trackId
    }
)
if track.active == False:
    print("Please enter an active trackId")
else:
    response = db.queue.create(
        data={
            "trackId": trackId
        }
    )
    print(response)
db.disconnect()