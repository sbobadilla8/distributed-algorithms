from flask import Flask, request
from handlers.files import get_files, share_file, remove_file

app = Flask(__name__)


@app.route("/files", methods=['GET', 'POST', 'DELETE'])
def files():
    if request.method == 'GET':
        return get_files()
    elif request.method == 'POST':
        file = request.json
        return share_file(file)
    elif request.method == 'DELETE':
        file = request.json
        return remove_file(file)
    else:
        return "", 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
