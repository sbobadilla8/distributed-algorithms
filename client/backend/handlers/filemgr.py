import math
import hashlib
import os
from pathlib import Path


class FileMgr:
    # Opens a file with the given file name. If file size is given, creates a new file of given size.
    def __init__(self, file_name, file_size=None):
        self.block_size = 4 * 1024
        self.file_name = file_name

        if file_size is not None:
            with open(self.file_name, "wb+") as f:
                f.seek(file_size-1)
                f.write(b'\0')
                f.close()
            self.file_descr = open(self.file_name, "rb+")
        else:
            self.file_descr = open(self.file_name, "rb+")
            self.file_size = self.get_file_bytes_size()

    # Get block at specified index
    def get_block(self, block_index):
        start_pos = block_index * self.block_size
        self.file_descr.seek(start_pos)
        requested_block = self.file_descr.read(self.block_size)
        return requested_block

    # Get size of file bytes list
    def get_file_bytes_size(self):
        return os.stat(self.file_descr.name).st_size

    # Get size of file block list
    def get_file_block_size(self):
        return math.ceil(self.get_file_bytes_size() / self.block_size)

    # Write block in specified index of the file
    def write_block(self, block, block_index):
        start_pos = block_index * self.block_size
        self.file_descr.seek(start_pos)
        self.file_descr.write(block)
        self.file_descr.flush()

    # Generate MD5 hash of a given block.
    # If block is not provided, generates the hash value of the file.
    def get_md5_hash(self, block=None):
        if(block is not None):
            return hashlib.md5(block).hexdigest()
        self.file_descr.seek(0)
        return hashlib.md5(self.file_descr.read()).hexdigest()
    
    def close_file(self):
        print("Closing {} . . .".format(self.file_name))
        self.file_descr.close()

    def __write_file(self):
        self.file_descr.seek(0)
        self.file_descr.write(b'\0'*self.file_size)
        self.file_descr.flush()

