import threading
import socket
import pickle as rick
import time
import random
from multiprocessing.pool import ThreadPool
from concurrent.futures import as_completed, ThreadPoolExecutor
from collections import deque
from filemgr import FileMgr

class FileDownloadManager:
    def __init__(self, fileName, fileSize, peers):
        connectedPeers = []
        self.peerConnectionMutex = threading.Lock()
        self.fileWriteMutex = threading.Lock()
        self.blockIndexMutex = threading.Lock()
        # Request Connection to all available peers
        # Peers which respond all get stored in connectedPeers
        print("Connecting to peers ...")
        for peer in peers:
            thread = threading.Thread(target=self.request_peer_connection, args=[peer, connectedPeers, fileName])
            thread.start()
            thread.join()
        print("Number of connected peers: {}".format(len(connectedPeers)))
        time.sleep(3)

        # Create FileMgr object with given size
        self.fileToDownload = FileMgr(fileName, fileSize)

        # Get indices of blocks to download
        self.blockIndices = deque(list( range(0, self.fileToDownload.get_file_block_size())))
        random.shuffle(self.blockIndices)

        # Request blocks from connected peers
        # for connectedPeer in connectedPeers:
        #     thread = threading.Thread(target=self.request_blocks_from_peer, args=[connectedPeer])
        #     thread.start()
        #     #thread.join()

        # max_workers = 12
        # with ThreadPoolExecutor(max_workers) as executor:
        #     #future_executor = {executor.submit(self.request_blocks_from_peer, connectedPeer): connectedPeer for connectedPeer in connectedPeers}
        #     future_executor = []
        #     for peerIndex in range(0, max_workers):
        #         future_executor.append(executor.submit(self.request_blocks_from_peer, connectedPeers[peerIndex % len(connectedPeers)]))
        #     for future in as_completed(future_executor):
        #         # result = future_executor[future]
        #         print("Result: {}".format(future.result()))

        maxThreads = 2
        threads = []

        for threadIndex in range(0, maxThreads):
            thread = threading.Thread(target=self.request_blocks_from_peer, args=[connectedPeers[threadIndex % len(connectedPeers)]])
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()


        # time.sleep(3)
        # TODO: Verify file integrity

        # Close all connected peers
        print("Closing all peers ...")
        for connectedPeer in connectedPeers:
            thread = threading.Thread(target=self.close_peer_connection, args=[connectedPeer])
            thread.start()
            thread.join()
        
    def request_peer_connection(self, peer, connectedPeers, fileName):
        peerConnection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        peerConnection.settimeout(30)
        peerConnection.connect((peer['host'], peer['port']))
        self.send_message(peerConnection, { 'action': 'Request_Download', 'payload': { 'file_name': fileName}})
        message = self.read_message(peerConnection)
        if(message['result'] == 'ACK'):
            self.peerConnectionMutex.acquire()
            try:
                connectedPeers.append(peerConnection)
            finally:
                self.peerConnectionMutex.release()

    def request_blocks_from_peer(self, peerConnection):
        while(len(self.blockIndices) > 0):

            # Get blockIndex from the queue in a thread safe manner
            self.blockIndexMutex.acquire()
            blockIndex = self.blockIndices.popleft()
            self.blockIndexMutex.release()
            # Request block from the connectedPeer
            print("Requesting block {} from {}".format(blockIndex, peerConnection.getpeername()))
            self.send_message(peerConnection, {'action': 'Request_Block', 'payload': { 'block_index': blockIndex }})
            message = self.read_message(peerConnection)
            if(message['result']):
                print("Received block {} from {}".format(blockIndex, peerConnection.getpeername()))
                block = message['result']['block']
                self.fileWriteMutex.acquire()
                self.fileToDownload.write_block(block, blockIndex)
                self.fileWriteMutex.release()
                print("Finished writing block {} to file".format(blockIndex))
        return True

    def close_peer_connection(self, peerConnection):
        self.send_message(peerConnection, { 'action': 'Close_Connection' })
        peerConnection.close()

    def send_message(self, connection, data):
        msg = rick.dumps(data)
        connection.send(msg)

    def read_message(self, connection):
        data = connection.recv(64 * 1024)
        msg = rick.loads(data)
        return msg

downloadFile = FileDownloadManager("Image.png", 494787, [{'host': '127.0.0.1', 'port': 6000},{'host': '127.0.0.1', 'port': 6001}])

### Client Requests
# {
#     action: 'Request_Download' / 'Request_Block' / 'Close_Connection'
#     payload: {file_name: 'File Name'} / {block_index: 1}
# }

### Client Responses
# {
#     result: { 'ACK' / block: [1,2,3,4 . . .]}
# }