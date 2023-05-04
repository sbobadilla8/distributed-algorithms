import math
import hashlib
import os
from pathlib import Path


class FileMgr:
    # Opens a file with the given file name. If file size is given, creates a new file of given size.
    def __init__(self, file_name, file_size=None):
        self.block_size = 4 * 1024
        self.file_name = file_name

        if (file_size is not None):
            Path(self.file_name).touch()
            self.file_descr = open(self.file_name, "r+b")
            self.file_size = file_size
            self.__write_file()
            self.file_descr.close()
            Path(self.file_name).touch()
            self.file_descr = open(self.file_name, "r+b")
            self.__write_file()

        else:
            self.file_descr = open(self.file_name, "r+b")
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

    # Generate MD5 hash of the file
    def get_md5_hash(self):
        self.file_descr.seek(0)
        return hashlib.md5(self.file_descr.read()).hexdigest()
    
    def close_file(self):
        print("Closing {} . . .".format(self.file_name))
        self.file_descr.close()

    def __write_file(self):
        self.file_descr.seek(0)
        self.file_descr.write(b'\0'*self.file_size)

    # def __del__(self):
    #     print("Closing {} . . .".format(self.file_name))
    #     self.file_descr.close()

# Working Example ###
# from random import shuffle

# # Open file to copy
# fileToCopy = FileMgr("hello.txt")
# fileSize = fileToCopy.get_file_bytes_size()
# print(f"fileName: {fileToCopy}, fileSize: {fileSize}")
# # Create new file of same length
# fileToWrite = FileMgr("downloads/hello.txt", fileSize)
# fileSize = fileToWrite.get_file_bytes_size()
# print(f"fileName: {fileToCopy}, fileSize: {fileSize}")
# # Create a shuffled list of block indices (How a P2P algorithm will work)
# new_block_indices = list( range(0, fileSize))
# shuffle(new_block_indices)

# # Write the random blocks to the new file
# for block_index in new_block_indices:
#     block = fileToCopy.get_block(block_index)
#     # print(block)
#     fileToWrite.write_block(block, block_index)

# # Check if both hash values match, if so the copying is done
# print(fileToCopy.get_md5_hash(), fileToWrite.get_md5_hash())
