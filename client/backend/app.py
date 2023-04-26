from flask import Flask, request, jsonify
from flask_cors import CORS
from handlers.files import get_files, share_file, remove_file

app = Flask(__name__)
cors = CORS(app)

@app.route("/files", methods=['GET', 'POST', 'DELETE', 'OPTIONS'])
def files():
    if request.method == 'OPTIONS':
        return "", 204
    elif request.method == 'GET':
        return jsonify(get_files())
    elif request.method == 'POST':
        file = request.files['file']
        return jsonify(share_file(file))
    elif request.method == 'DELETE':
        file = request.json
        return remove_file(file)
    else:
        return "", 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
