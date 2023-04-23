from flask import Flask, request
from flask_cors import CORS
from handlers.file import file_search

app = Flask(__name__)
cors = CORS(app)


@app.route("/file", methods=['GET', 'POST', 'DELETE'])
def file():
    if request.method == 'GET':
        user_input = request.args.get('input', '')
        return file_search(user_input)
    elif request.method == 'POST':
        return {
            "hello": "world"
        }
    else:
        return "", 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
