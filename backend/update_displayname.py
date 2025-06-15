from flask_restful import Resource, Api
from flask import request, abort, jsonify
from prisma.client import Client

class UpdateDisplayName(Resource):
    def post(self):
        try:
            data = request.json
            oldDisplayName = data.get('oldDisplayName')
            newDisplayName = data.get('newDisplayName')
            username = data.get('userName')

            # print(data)

            db = Client()
            db.connect()
            try:
                updated = db.profile.update(
                    where = {
                        'username': username
                    },
                    data={
                        "displayname": newDisplayName
                    }
                )
            except Exception as e:
                print(e)
                db.disconnect()
                return
            # print(updated)
            db.disconnect()
            return jsonify(displayName=updated.displayname)
            db.disconnect()
        except Exception as e:
            db.disconnect()
            abort(400, e)
        return