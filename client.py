import socket

def main():
    client_socket = socket.socket()
    client_socket.connect(('localhost', 9090))

    path = r'C:\Users\danya\Downloads\Folder'  # созданная мной папка, дубликат в директории с проектом
    # path = input('Enter path: ')  # если клиенту требуется ввести самостоятельно
    client_socket.sendall(path.encode())

    result_data = client_socket.recv(2048).decode()  # объем результата в байтах больше 1024, беру 2048
    output = client_socket.recv(1024).decode()
    client_socket.close()

    print(result_data)  # содержание директории в формате json объекта (str, но это json)
    # Вывод: [{"Path": "C:\\Users\\danya\\Downloads\\Folder\\book.txt", "Last modified": "29.02.24 19:21:13",
    # "Size": "11424 bytes", "Object type": " File"}, {"Path": "C:\\ .......}]
    print(output)  # результат обработки запроса клиента сервером


if __name__ == '__main__':
    main()
