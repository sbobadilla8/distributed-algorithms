import socket
import pickle as rick
import random
from collections import deque
from .filemgr import FileMgr
from .mutex.hemlock import HemlockThread, Lock


def send_message(connection, data):
    connection.send(rick.dumps(data))


def read_message(connection):
    # self.peerConnectionMutex.acquire()
    data = connection.recv(32 * 1024)
    message = rick.loads(data)
    # self.peerConnectionMutex.release()
    return message


class FileDownloadManagerAlt:
    def __init__(self, file_name, file_size, peers):
        self.connected_peers = []
        self.file_name = file_name
        self.file_size = file_size
        self.peers = peers
        self.block_indices = None
        self.file_to_download = None
        self.peerConnectionMutex = Lock()
        self.fileWriteMutex = Lock()
        self.blockIndexMutex = Lock()

    def initiate_download(self):
        # Create FileMgr object with given size
        file_thread = HemlockThread(target=self.create_download_file, args=())
        file_thread.start()

        # Request Connection to all available peers which respond all get stored in connected_peers
        print("DownloadManager::initiate_download::Connecting to peers ...")
        max_threads = 12
        connection_threads = []
        for threadIndex in range(0, max_threads):
            thread = HemlockThread(target=self.request_peer_connection,
                                   args=[self.peers[threadIndex % len(self.peers)]])
            thread.start()
            connection_threads.append(thread)

        for thread in connection_threads:
            thread.join()

        file_thread.join()

        # Get indices of blocks to download
        self.block_indices = deque(list(range(0, self.file_to_download.get_file_block_size())))
        random.shuffle(self.block_indices)

        # Request blocks from connected peers
        print("DownloadManager::initiate_download::Downloading file blocks ...")
        block_threads = []
        for threadIndex in range(0, max_threads):
            thread = HemlockThread(target=self.request_blocks_from_peer,
                                   args=[self.connected_peers[threadIndex]])
            thread.start()
            block_threads.append(thread)

        for thread in block_threads:
            thread.join()

        # TODO: Verify file integrity

        # Close all connected peers
        print("DownloadManager::initiate_download::Closing all peers ...")
        for connectedPeer in self.connected_peers:
            thread = HemlockThread(target=self.close_peer_connection, args=[connectedPeer])
            thread.start()
            thread.join()

    def create_download_file(self):
        self.file_to_download = FileMgr("downloads/" + self.file_name, self.file_size)

    def request_peer_connection(self, peer):
        address = peer.split(':')
        connected_peer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connected_peer.settimeout(2 * 60)
        connected_peer.connect((address[0], int(address[1])))
        send_message(connected_peer, {'action': 'Request_Download',
                                      'payload': {'file_name': self.file_name}})
        message = read_message(connected_peer)
        if message['result'] == 'ACK':
            self.peerConnectionMutex.lock()
            try:
                self.connected_peers.append(connected_peer)
            finally:
                self.peerConnectionMutex.unlock()

    def request_blocks_from_peer(self, connected_peer):
        while True:
            # Get block_index from the queue in a thread safe manner
            self.blockIndexMutex.lock()
            if len(self.block_indices) == 0:
                self.blockIndexMutex.unlock()
                break
            block_index = self.block_indices.popleft()
            self.blockIndexMutex.unlock()
            # Request block from the connectedPeer
            # print("DownloadManager::request_blocks_from_peer::Requesting block
            # {} from {}".format(block_index, connectedPeer.getpeername()))
            send_message(connected_peer, {'action': 'Request_Block',
                                          'payload': {'block_index': block_index,
                                                      'file_name': self.file_name}})
            message = read_message(connected_peer)
            if message['result']:
                # print("DownloadManager::request_blocks_from_peer::Received block {} from {}".format(block_index,
                # connectedPeer.getpeername()))
                block = message['result']['block']
                self.fileWriteMutex.lock()
                self.file_to_download.write_block(block, block_index)
                self.fileWriteMutex.unlock()
                # print("DownloadManager::request_blocks_from_peer::Finished writing block {} to file".format(
                # block_index))

    def close_peer_connection(self, connected_peer):
        send_message(connected_peer, {'action': 'Close_Connection',
                                      'payload': {'file_name': self.file_name}})
        connected_peer.close()

    def get_download_progress(self):
        if self.block_indices is None:
            return 0.0
        self.blockIndexMutex.lock()
        remaining_blocks = len(self.block_indices)
        print(f"Remaining blocks: {remaining_blocks}")
        self.blockIndexMutex.unlock()
        total_blocks = self.file_to_download.get_file_block_size()
        progress = (total_blocks - remaining_blocks) / total_blocks
        return progress
