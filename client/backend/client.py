import sys
import argparse
import os
import threading
from flask import Flask, request, jsonify, send_from_directory, render_template
from flask_cors import CORS, cross_origin
from handlers.files import Files
from handlers.filepicker import get_list, change
from handlers.uploadmanager import FileUploadManager
import mimetypes

app = Flask(__name__, template_folder='dist', static_folder='dist', static_url_path='/')
# cors = CORS(app, origins=['http://localhost'])
port_tcp = 0

files = None
serverAddress = ""
backendAddress = ""


@app.route('/', defaults={'path': ''})
def catch_all(path):
    return render_template('index.html', serverAddress=serverAddress, backendAddress=backendAddress)


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
        filename = request.args.get("filename", "")
        server = request.args.get("server", "")
        file = {"filename": filename, "serverAddress": server}
        return jsonify(files.remove_file(file))
    else:
        return "", 404


@app.route("/picker", methods=['POST'])
def picker():
    cmd_input = request.json
    if cmd_input['cmd'] == "ls":
        return jsonify(get_list())
    elif cmd_input['cmd'] == "cd":
        return change(cmd_input['dir'])


@app.route("/download", methods=['POST', 'GET'])
def download():
    if request.method == 'POST':
        file = request.json
        return files.download_file(file), 200
    elif request.method == 'GET':
        file = request.args.get('filename', '')
        return jsonify(files.get_update(file))


@app.route("/check", methods=['POST'])
def check():
    return "", 204


def create_listener(port):
    FileUploadManager("", port)


if __name__ == "__main__":
    mimetypes.add_type('application/javascript', '.js')
    mimetypes.add_type('text/css', '.css')
    # Create TCP Server for Client-Client file sharing
    # parser = argparse.ArgumentParser()
    # parser.add_argument("-p1", "--port_web", type=int)
    # parser.add_argument("-p2", "--port_tcp", type=int)
    # parser.add_argument("-sa", "--server", type=string)
    # parser.add_argument("-ba", "--backend", type=string)
    # parser.add_argument("-a", "--address")

    # args = parser.parse_args()
    # host = args.address
    port_web = int(sys.argv[1])
    port_tcp = int(sys.argv[2])
    serverAddress = sys.argv[3]
    backendAddress = sys.argv[4]
    files = Files()
    files.set_port(port_tcp)

    try:
        os.makedirs("downloads")
    except OSError:
        print("Directory for downloads already exists")

    thread = threading.Thread(target=create_listener, args=[port_tcp])
    thread.daemon = True
    thread.start()
    cors = CORS(app, origins=['http://localhost:'+str(port_web)])
    app.run(host="0.0.0.0", port=port_web, debug=True)
