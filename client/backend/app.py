from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from handlers.files import Files
from handlers.filepicker import get_list, change
import argparse
from handlers.server import ServerConnection

app = Flask(__name__)
cors = CORS(app)
port_tcp = 0

files = None


@app.route("/files", methods=['GET', 'POST', 'DELETE', 'OPTIONS'])
def files():
    if request.method == 'OPTIONS':
        return "", 204
    elif request.method == 'GET':
        return jsonify(files.get_files())
    elif request.method == 'POST':
        file = request.json
        return jsonify(files.share_file(file))
    elif request.method == 'DELETE':
        file = request.json['file']
        return files.remove_file(file)
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


@app.route("/check", methods=['POST'])
def check():
    return "", 204


if __name__ == "__main__":
    # Create TCP Server for Client-Client file sharing
    parser = argparse.ArgumentParser()
    parser.add_argument("-p1", "--port_web", type=int)
    parser.add_argument("-p2", "--port_tcp", type=int)
    # parser.add_argument("-a", "--address")

    args = parser.parse_args()
    # host = args.address
    port_web = args.port_web
    port_tcp = args.port_tcp
    files = Files()
    files.set_port(port_tcp)
    # server = ServerConnection(host, port)
    app.run(host="0.0.0.0", port=port_web, debug=True)
