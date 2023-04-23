import math
import hashlib

class FileMgr:
    # Opens a file with the given file name. If file size is given, creates a new file of given size.
    def __init__(self, file_name, file_size=None):
        self.block_size = 2048
        self.file_name = file_name
        
        if(file_size != None):
            self.file_descr = open(self.file_name, "w+b")
            self.file_size = file_size
            self.bytes_list = self.__create_empty_bytes_list()
            self.block_list = self.__get_block_list_from_byte_list()
            self.__write_file()
        else:
            self.file_descr = open(self.file_name, "r+b")
            self.bytes_list = list(self.file_descr.read())
            self.file_size = self.get_file_bytes_size()
            self.block_list = self.__get_block_list_from_byte_list()

    # Get block at specified index
    def get_block(self, block_index):
        start_pos = block_index * self.block_size
        end_pos = start_pos + self.block_size
        requested_block = self.bytes_list[start_pos:end_pos]
        return requested_block

    # Get file bytes list
    def get_bytes_list(self):
        return self.bytes_list

    # Get file block list
    def get_block_list(self):
        return self.block_list

    # Get size of file bytes list
    def get_file_bytes_size(self):
        return len(self.bytes_list)

    # Get size of file block list
    def get_file_block_size(self):
        return len(self.block_list)

    # Write block in specified index of the file
    def write_block(self, block, block_index):
        start_pos = block_index * self.block_size
        end_pos = start_pos + self.block_size
        self.bytes_list[start_pos: end_pos] = block
        self.file_descr.seek(start_pos)
        self.file_descr.write(bytes(block))

    # Generate MD5 hash of the file
    def get_md5_hash(self):
        return hashlib.md5(bytes(self.get_bytes_list())).hexdigest()

    def __get_block_list_from_byte_list(self):
        self.block_list = []
        blocks = math.ceil(self.get_file_bytes_size() / self.block_size)
        for block_index in range(0, blocks):
            block = self.get_block(block_index)
            self.block_list.append(block)
        return self.block_list

    def __create_empty_bytes_list(self):
        return [0]*self.file_size

    def __write_file(self):
        file_content = bytes(self.bytes_list)
        self.file_descr.seek(0)
        self.file_descr.write(file_content)
    
    def __del__(self):
        print("Closing {} . . .".format(self.file_name))
        self.file_descr.close()
    
### Working Example ###
# from random import shuffle

# # Open file to copy
# fileToCopy = FileMgr("Image.png")

# # Create new file of same length
# fileToWrite = FileMgr("Image2.png", file_size=fileToCopy.get_file_bytes_size())
# # Create a shuffled list of block indices (How a P2P algorithm will work)
# new_block_indices = list( range(0, fileToWrite.get_file_block_size()))
# shuffle(new_block_indices)

# # Write the random blocks to the new file
# for block_index in new_block_indices:
#     block = fileToCopy.get_block(block_index)
#     fileToWrite.write_block(block, block_index)

# # Check if both hash values match, if so the copying is done
# print(fileToCopy.get_md5_hash(), fileToWrite.get_md5_hash())