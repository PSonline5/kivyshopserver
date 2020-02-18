from flask_restful import Resource

from models import Category, serialize_multi


class Genre(Resource):

    def get(self):
        try:
            category = Category.query.all()
            return serialize_multi(category), 200
        except AttributeError:
            return "Not found", 404