from flask_restful import Resource, Api
from flask import request, abort, jsonify
from prisma.client import Client

class UpdateUsername(Resource):
    def post(self):
        try:
            data = request.json
            newUsername = data.get('newUsername')
            username = data.get('userName')

            print(data)

            db = Client()
            db.connect()
            try:
                updated = db.profile.update(
                    where = {
                        'username': username
                    },
                    data={
                        "username": newUsername
                    }
                )
            except Exception as e:
                print(e)
                db.disconnect()
                return jsonify([])

            db.disconnect()
            return jsonify(username=updated.username)
            db.disconnect()
        except Exception as e:
            db.disconnect()
            abort(400, e)
        return