from flask_restful import Resource, Api
from flask import request, abort, jsonify
from prisma.client import Client

class ModifyProfilePicture(Resource):
    def post(self):
        try:
            data = request.json
            username = data.get('userName')
            pictureUrl = data.get('pictureUrl')


            db = Client()
            db.connect()
            try:
                updated = db.profile.update(
                    where = {
                        'username': username
                    },
                    data={
                        "picture": pictureUrl
                    }
                )
            except Exception as e:
                print(e)
                db.disconnect()
                return

            db.disconnect()

            return jsonify(pictureUrl=updated.picture)

        except Exception as e:
            db.disconnect()
            abort(400, e)
        return