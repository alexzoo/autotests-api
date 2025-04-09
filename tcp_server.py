import socket  # Импортируем модуль socket для работы с сетевыми соединениями


def server():
    # Создаем TCP-сокет
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Привязываем его к адресу и порту
    server_address = ('localhost', 12345)
    server_socket.bind(server_address)

    # Начинаем слушать входящие подключения (максимум 5 в очереди)
    server_socket.listen(5)
    print("Сервер запущен и ждет подключений...")

    while True:
        # Принимаем соединение от клиента
        client_socket, client_address = server_socket.accept()
        print(f"Подключение от {client_address}")

        # Получаем данные от клиента
        data = client_socket.recv(1024).decode()
        print(f"Получено сообщение: {data}")

        # Отправляем ответ клиенту
        response = f"Сервер получил: {data}"
        client_socket.send(response.encode())

        # Закрываем соединение с клиентом
        client_socket.close()


if __name__ == '__main__':
    server()
