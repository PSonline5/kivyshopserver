from flask_restful import Resource


from models import Product, serialize_multi


class Book(Resource):

    def get(self):
        try:
            product = Product.query.all()
            return serialize_multi(product), 200
        except AttributeError:
            return "Not found", 404


class BookById(Resource):

    def get(self, id_):
        try:
            product = Product.query.filter_by(id=id_).all()
            product = product[0].price
            return serialize_multi(product), 200
        except AttributeError:
            return "Not found", 404


class BookByGenre(Resource):

    def get(self, id_: int):
        try:
            product = Product.query.filter_by(category_id=id_).all()
            return serialize_multi(product), 200
        except AttributeError:
            return "Not found", 404


class BookByAuthor(Resource):

    def get(self, author):
        try:
            product = Product.query.filter_by(author_name=author)
            return serialize_multi(product), 200
        except AttributeError:
            return "Not found", 404



