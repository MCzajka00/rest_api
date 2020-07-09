from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    return 'it works'


books = []


@app.route('/books', methods=['GET'])
def get_books():
    return jsonify({"message": "Ok", "data": books}), 200


@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    try:
        book = [b for b in books if b['id'] == book_id][0]
        return jsonify({"message": "Ok", "data": book}), 200
    except IndexError:
        message = f'There is no such book with id: {book_id} my friend.'
        return jsonify({"message": message, "data": []}), 404


@app.route('/books', methods=['POST'])
def new_book():
    books.append(request.get_json())
    return jsonify({"message": "Created", "data": [request.get_json()]}), 201


@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    global books
    new_data = request.get_json()
    try:
        book_for_update = [b for b in books if b['id'] == book_id][0]
        new_data['id'] = book_for_update['id']
        books = [new_data if b['id'] == book_id else b for b in books]
        return jsonify({"message": "Ok", "data": new_data}), 200
    except IndexError:
        message = f"There is no book with id: {book_id}"
        return jsonify({"message": message, "data": []}), 404
    except KeyError:
        message = f"User data is incorrect: {new_data}"
        return jsonify({"message": message, "data": []}), 400


@app.route('/books/<int:book_id>', methods=['PATCH'])
def update_book_partially(book_id):
    new_data = request.get_json()
    try:
        book_for_update = [b for b in books if b['id'] == book_id][0]
        idx = book_for_update['id']
        book_for_update.update(new_data)
        book_for_update['id'] = idx
        return jsonify({"message": "ok", "data": [book_for_update]}), 200
    except IndexError:
        message = f"There is no book with id: {book_id}"
        return jsonify({"message": message, "data": []}), 404
    except KeyError:
        message = f"User data is incorrect: {new_data}"
        return jsonify({"message": message, "data": []}), 400


@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    try:
        book_for_delete = [b for b in books if b['id'] == book_id][0]
        book_idx = books.index(book_for_delete)
        deleted_book = books.pop(book_idx)
        return jsonify({"message": "ok", "data": [deleted_book]}), 200
    except IndexError:
        message = f"There is no book with id: {book_id}"
        return jsonify({"message": message, "data": []}), 404
