"""Программа-клиент"""

import sys
import json
import socket
import time
from common.variables import ACTION, PRESENCE, PORT, TIME, USER, ACCOUNT_NAME, \
    RESPONSE, ERROR, DEFAULT_IP_ADDRESS, DEFAULT_PORT
from common.utils import get_message, send_message


def user_request(port, user_name='Guest'):
    """
    Функция генерирует запрос о присутствии клиента
    :param port:
    :param user_name:
    :return:
    """
    user_data = {
        ACTION: PRESENCE,
        TIME: time.time(),
        PORT: port,
        USER: {
            ACCOUNT_NAME: user_name
        }
    }
    return user_data


def server_response(response):
    """
    Функция разбирает ответ сервера
    :param response:

    :return:
    """
    if RESPONSE in response:
        if response[RESPONSE] == 200:
            return '200 : OK'
        return f'400 : {response[ERROR]}'
    raise ValueError


def main():
    """Загружаем параметы коммандной строки"""
    try:
        request_port = int(sys.argv[1])
        request_address = sys.argv[2]
        if request_port < 1024 or request_port > 65535:
            raise ValueError
    except IndexError:
        request_address = DEFAULT_IP_ADDRESS
        request_port = DEFAULT_PORT
    except ValueError:
        print('В качестве порта может быть указано только число в диапазоне от 1024 до 65535.')
        sys.exit(1)

    # Инициализация сокета и обмен

    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.connect((request_address, request_port))
    user_message = user_request(request_port)
    send_message(transport, user_message)
    try:
        response = server_response(get_message(transport))
        print(response)
    except (ValueError, json.JSONDecodeError):
        print('Не удалось декодировать сообщение сервера.')


if __name__ == '__main__':
    main()
