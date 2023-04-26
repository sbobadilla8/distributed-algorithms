from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from handlers.files import get_files, share_file, remove_file
from handlers.filepicker import get_list, change

app = Flask(__name__)
cors = CORS(app)


@app.route("/files", methods=['GET', 'POST', 'DELETE', 'OPTIONS'])
def files():
    if request.method == 'OPTIONS':
        return "", 204
    elif request.method == 'GET':
        return jsonify(get_files())
    elif request.method == 'POST':
        file = request.json['file']
        return jsonify(share_file(file))
    elif request.method == 'DELETE':
        file = request.json['file']
        return remove_file(file)
    else:
        return "", 404


# @cross_origin("127.0.0.1")
@app.route("/picker", methods=['POST'])
def picker():
    cmd_input = request.json
    if cmd_input['cmd'] == "ls":
        return jsonify(get_list())
    elif cmd_input['cmd'] == "cd":
        return change(cmd_input['dir'])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
