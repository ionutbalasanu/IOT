import struct
import os
import random


class Users:
    users_table = {
        'Geo': {
            'password': 'abc',
            'role': 'admin'
        },
        'Hot': {
            'password': 'bca',
            'role': 'user'
        }
    }

    @staticmethod
    def get_users():
        return Users.users_table


class Util:
    @staticmethod
    def decode_value_len(size: bytes) -> int:
        return struct.unpack('<I', size)[0]

    @staticmethod
    def decode_value(value: bytes) -> float:
        return struct.unpack('f', value)[0]

    @staticmethod
    def process_bytes(reader: int) -> bytes:
        size_bytes = os.read(reader, 4)
        value_bytes = os.read(reader, Util.decode_value_len(size_bytes))
        return value_bytes

    @staticmethod
    def read_temp(file_name) -> float:
        ret_val = None
        mode = 'celsius'
        temp_value = (random.random() * 100 + 20) % 40
        if os.path.exists(file_name):
            file = open(file_name, 'r')
            mode = file.readline()

        if mode == 'celsius':
            ret_val = temp_value
        elif mode == 'kelvin':
            ret_val = temp_value - 273.15

        return ret_val

    @staticmethod
    def encode_msg_size(size: int) -> bytes:
        return struct.pack('<I', size)

    @staticmethod
    def create_msg(content: bytes) -> bytes:
        dim = len(content)
        return Util.encode_msg_size(dim) + content

    @staticmethod
    def create_get_msg(content) -> bytes:
        return Util.create_msg(content)

    @staticmethod
    def create_response_msg(content):
        return Util.create_msg(bytearray(struct.pack('f', content)))
