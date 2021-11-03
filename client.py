"""Программа-клиент"""

import sys
import json
import socket
import time
import logging

from common.variables import ACTION, PRESENCE, PORT, TIME, USER, ACCOUNT_NAME, \
    RESPONSE, ERROR, DEFAULT_IP_ADDRESS, DEFAULT_PORT
from common.utils import get_message, send_message
from errors import ReqFieldMissingError
from decos import Log

CLIENT_LOGGER = logging.getLogger('client')


@Log()
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
    CLIENT_LOGGER.info(f'Генерация запроса {PRESENCE} пользователя {user_name}')
    return user_data


@Log()
def server_response(response):
    """
    Функция разбирает ответ сервера
    :param response:

    :return:
    """
    CLIENT_LOGGER.info(f'Принят ответ сервера')
    if RESPONSE in response:
        if response[RESPONSE] == 200:
            return '200 : OK'
        return f'400 : {response[ERROR]}'
    raise ReqFieldMissingError(RESPONSE)


def main():
    """Загружаем параметы коммандной строки"""
    try:
        request_port = int(sys.argv[1])
        request_address = sys.argv[2]
        if request_port < 1024 or request_port > 65535:
            raise ValueError
    except IndexError:
        CLIENT_LOGGER.error(f'Адрес и(или) порт не переданы, значения установлены по умолчанию')
        request_address = DEFAULT_IP_ADDRESS
        request_port = DEFAULT_PORT
    except ValueError:
        CLIENT_LOGGER.critical(f'Указано неверное значение порта - {request_port}. В качестве порта может быть '
                               f'указано только число в диапазоне от 1024 до 65535.')
        sys.exit(1)

    CLIENT_LOGGER.info(f'Запущен клиент со следующими параметрами: адрес - {request_address}, адрес - {request_port}')

    # Инициализация сокета и обмен

    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.connect((request_address, request_port))
    user_message = user_request(request_port)
    send_message(transport, user_message)
    try:
        response = server_response(get_message(transport))
        CLIENT_LOGGER.info(f'Ответ сервера принят: {response}')
        print(response)
    except json.JSONDecodeError:
        CLIENT_LOGGER.error('Не удалось декодировать сообщение сервера.')
    except ReqFieldMissingError as missing_error:
        CLIENT_LOGGER.error(f'В ответе сервера отсутствует необходимое поле '
                            f'{missing_error.missing_field}')
    except ConnectionRefusedError:
        CLIENT_LOGGER.critical('Отказ узла в попытке соединения')


if __name__ == '__main__':
    main()
