from flask_restful import Resource, reqparse
from db.base import Session
from db.schema import Courier as Courier_db


class Courier(Resource):
    def get(self, courier_id):

        # db.query(Courier_db).get(courier_id)

        return
