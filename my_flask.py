# File to deploy project on pythonanywhere.com
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
api = Api(app)




class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(100), unique=True, nullable=False)

    products = db.relationship('Product', backref='category')

    def __repr__(self):
        return '<Category %r>' % self.category_name

    def serialize(self) -> dict:
        return {
            "id": self.id,
            "category_name": self.category_name,
        }


class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100), nullable=False)
    author_name = db.Column(db.String(100), nullable=False)
    product_description = db.Column(db.Text(500), nullable=False)
    price = db.Column(db.Float, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"),
                            nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    status = db.Column(db.String(50), default="IN STOCK")
    #image = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<Product %r>' % self.product_name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.product_name,
            "author_name": self.author_name,
            "product_description": self.product_description,
            "price": self.price,
            "category": self.category.category_name,
            "created at": str(self.created_at),
            "status": self.status,
            #"image": self.image
        }


def serialize_multi(objects: list) -> list:
    return [obj.serialize() for obj in objects]

# p1 = Product(product_name="1984", author_name="George Orwell",
#              product_description="Among the seminal texts of the 20th century, Nineteen Eighty-Four is a rare work that grows more haunting as its futuristic purgatory becomes more real. Published in 1949, the book offers political satirist George Orwell's nightmarish vision of a totalitarian, bureaucratic world and one poor stiff's attempt to find individuality. The brilliance of the novel is Orwell's prescience of modern life—the ubiquity of television, the distortion of the language—and his ability to construct such a thorough version of hell. Required reading for students since it was published, it ranks among the most terrifying novels ever written.",
#              price=7.89, category_id=1)
# p2 = Product(product_name="Python Crash Course", author_name="Eric Matthes",
#              product_description="Readers will learn how to create a simple video game, use data visualization techniques to make graphs and charts, and build and deploy an interactive web application. Python Crash Course, teaches beginners the essentials of Python quickly so that they can build practical programs and develop powerful programming techniques.",
#              price=31.95, category_id=2)
# p3 = Product(product_name="The Lord of the Rings", author_name="J.R.R. Tolkien",
#              product_description="One Ring to rule them all, One Ring to find them, One Ring to bring them all and in the darkness bind them. In ancient times the Rings of Power were crafted by the Elven-smiths, and Sauron, the Dark Lord, forged the One Ring, filling it with his own power so that he could rule all others. But the One Ring was taken from him, and though he sought it throughout Middle-earth, it remained lost to him. After many ages it fell by chance into the hands of the hobbit Bilbo Baggins.",
#              price=15.99, category_id=1)
# p4 = Product(product_name="Learn Python the Hard Way", author_name="Zed Shaw",
#              product_description="In Learn Python the Hard Way, you'll learn Python by working through 52 brilliantly crafted exercises. Read them. Type their code precisely. (No copying and pasting!) Fix your mistakes. Watch the programs run. As you do, you'll learn how software works; what good programs look like; how to read, write, and think about code; and how to find and fix your mistakes using tricks professional programmers use.",
#              price=19.28, category_id=2)
# p5 = Product(product_name="ee", author_name="test",
#              product_description="In Learn Python the Hard Way, you'll learn Python by working through 52 brilliantly crafted exercises. Read them. Type their code precisely. (No copying and pasting!) Fix your mistakes. Watch the programs run. As you do, you'll learn how software works; what good programs look like; how to read, write, and think about code; and how to find and fix your mistakes using tricks professional programmers use.",
#              price=29.28, category_id=2)
#https://www.google.com/imgres?imgurl=https%3A%2F%2Fimages-na.ssl-images-amazon.com%2Fimages%2FI%2F51EstVXM1UL._SX331_BO1%2C204%2C203%2C200_.jpg&imgrefurl=https%3A%2F%2Fwww.amazon.com%2FLord-Rings-J-R-R-Tolkien%2Fdp%2F0544003411&tbnid=qZtycADfEdnL7M&vet=12ahUKEwiw7vrli8LnAhUcf5oKHXbHALAQMygCegUIARDWAQ..i&docid=Or3N5bOak0HWgM&w=333&h=499&q=lord%20of%20the%20rings%20book&ved=2ahUKEwiw7vrli8LnAhUcf5oKHXbHALAQMygCegUIARDWAQ
#data:image/jpeg;base64,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
# c1 = Category(category_name="Fiction")
# c2 = Category(category_name="Programming")
# db.session.add(p1)
# db.session.add(p2)
# db.session.add(p3)
# db.session.add(p4)
# db.session.add(p5)
# db.session.add(c2)
# db.session.commit()


if __name__ == '__main__':
    db.create_all()



class Genre(Resource):

    def get(self):
        try:
            category = Category.query.all()
            return serialize_multi(category), 200
        except AttributeError:
            return "Not found", 404



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



















api.add_resource(Book, '/books')
api.add_resource(Genre, '/genres')

api.add_resource(BookByGenre, '/genres/books/<int:id_>')
api.add_resource(BookById, '/books/<int:id_>')
api.add_resource(BookByAuthor, '/books/<author>')




if __name__ == '__main__':
    app.run(debug=True)