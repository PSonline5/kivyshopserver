from settings import app, api
from views.products import Book, BookById, BookByGenre, BookByAuthor
from views.categories import Genre




api.add_resource(Book, '/books')
api.add_resource(Genre, '/genres')

api.add_resource(BookByGenre, '/genres/books/<int:id_>')
api.add_resource(BookById, '/books/<int:id_>')
api.add_resource(BookByAuthor, '/books/<author>')




if __name__ == '__main__':
    app.run(debug=True)