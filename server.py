import os
import time
import json
import socket
import struct


def traversal(path):
    traversal_result = []
    for path, directories, files in list(os.walk(path)):
        for file in files:
            file_path = os.path.join(path, file)
            time_modified = os.path.getmtime(file_path)
            local_time = time.localtime(time_modified)
            result_time = time.strftime('%d.%m.%y %H:%M:%S', local_time)
            size = str(os.path.getsize(file_path)) + ' bytes'
            file_info = {
                'Path': file_path,
                'Last modified': result_time,
                'Size': size,
                'Object type': ' File'
            }
            traversal_result.append(file_info)

        for directory in directories:
            dir_path = os.path.join(path, directory)
            time_modified = os.path.getmtime(dir_path)
            local_time = time.localtime(time_modified)
            result_time = time.strftime('%d.%m.%y %H:%M:%S', local_time)
            dir_info = {
                'Path': dir_path,
                'Last modified': result_time,
                'Object type': 'Directory'
            }
            traversal_result.append(dir_info)

    return traversal_result


def save_to_json(data, file):
    with open('traversal_result.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '127.0.0.1'
    port = 9090
    sock.bind((host, port))
    sock.listen(1)

    connection, client_address = sock.accept()
    with connection:
        data = connection.recv(2048)  # объем результата в байтах больше 1024, беру 2048
        path = data.decode()
        result = traversal(path)
        structed_result = struct.pack('{}s'.format(len(json.dumps(result).encode())), json.dumps(result).encode())
        connection.sendall(structed_result)
        # connection.sendall(json.dumps(result).encode())  # вариант без struct
        result_msg = f'\nУспешно отправлено содержание директории {path.split("/")[-1]}'
        connection.sendall(result_msg.encode())


if __name__ == '__main__':
    main()
