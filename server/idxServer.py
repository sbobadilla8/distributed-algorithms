from flask import Flask, request, current_app, jsonify
from flask_cors import CORS
from handlers.file import file_search, index_file

app = Flask(__name__)
cors = CORS(app)


@app.route("/file", methods=['GET', 'POST', 'DELETE', 'OPTIONS'])
def file():
    if request.method == 'OPTIONS':
        return "", 204
    elif request.method == 'GET':
        user_input = request.args.get('input', '')
        return jsonify(file_search(user_input))
    elif request.method == 'POST':
        user_address = request.environ['REMOTE_ADDR']
        file_shared = request.json
        return jsonify(index_file(file_shared, user_address)), 204
    else:
        return "", 404


@app.route("/check", methods=['POST'])
def check():
    return "", 204


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
