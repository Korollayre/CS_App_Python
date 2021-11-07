"""Программа-клиент"""

import sys
import json
import socket
import time
import logging
import argparse

from common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, \
    RESPONSE, ERROR, DEFAULT_IP_ADDRESS, DEFAULT_PORT, SENDER, MESSAGE, MESSAGE_TEXT
from common.utils import get_message, send_message
from errors import ReqFieldMissingError, ServerError
from decos import Log

CLIENT_LOGGER = logging.getLogger('client')


@Log()
def message_handler(message):
    if ACTION in message and message[ACTION] == MESSAGE and SENDER in message and MESSAGE_TEXT in message:
        print(f'Получено сообщение {message[MESSAGE_TEXT]} от пользователя {message[SENDER]}')
        CLIENT_LOGGER.info(f'Получено сообщение {message[MESSAGE_TEXT]} от пользователя {message[SENDER]}')
    else:
        CLIENT_LOGGER.error(f'Получено некорректное сообщение с сервера: {message}')


@Log()
def creat_user_message(request_socket, account_name='Guest'):
    message = input("Введите сообщение. Для завершения работы введите 'q': ")
    if message == 'q':
        request_socket.close()
        CLIENT_LOGGER.info('Завершение работы по запросу пользователя.')
        sys.exit(0)
    user_message = {
        ACTION: MESSAGE,
        TIME: time.time(),
        ACCOUNT_NAME: account_name,
        MESSAGE_TEXT: message
    }
    CLIENT_LOGGER.info(f'Сформировано сообщение {user_message}.')

    return user_message


@Log()
def user_request(user_name='Guest'):
    """
    Функция генерирует запрос о присутствии клиента
    :param user_name:
    :return:
    """
    user_data = {
        ACTION: PRESENCE,
        TIME: time.time(),
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
        elif response[RESPONSE] == 400:
            raise ServerError(f'400 : {response[ERROR]}')
    raise ReqFieldMissingError(RESPONSE)


@Log()
def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('port', default=DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('addr', default=DEFAULT_IP_ADDRESS, nargs='?')
    parser.add_argument('-m', '--mode', default='listen', nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    request_address = namespace.addr
    request_port = namespace.port
    request_mode = namespace.mode

    if not 1023 < request_port < 65536:
        CLIENT_LOGGER.critical(f'Указано неверное значение порта - {request_port}. В качестве порта может быть '
                               f'указано только число в диапазоне от 1024 до 65535.')
        sys.exit(1)

    if request_mode not in ('listen', 'send'):
        CLIENT_LOGGER.critical(f'Указано неверный режим работы - {request_mode}. Допустимые режимы - listen, send.')
        sys.exit(1)

    return request_address, request_port, request_mode


def main():
    """Загружаем параметы коммандной строки"""

    request_address, request_port, request_mode = arg_parser()

    CLIENT_LOGGER.info(f'Запущен клиент со следующими параметрами: '
                       f'адрес - {request_address}, порт - {request_port}, режим работы - {request_mode}')

    # Инициализация сокета и обмен
    try:
        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.connect((request_address, request_port))
        send_message(transport, user_request())
        response = server_response(get_message(transport))
        CLIENT_LOGGER.info(f'Ответ сервера принят: {response}')
        print(response)
    except ServerError as error:
        CLIENT_LOGGER.error(f'При установке соединения сервер вернул ошибку: {error.text}')
        sys.exit(1)
    except json.JSONDecodeError:
        CLIENT_LOGGER.error('Не удалось декодировать сообщение сервера.')
        sys.exit(1)
    except ReqFieldMissingError as missing_error:
        CLIENT_LOGGER.error(f'В ответе сервера отсутствует необходимое поле '
                            f'{missing_error.missing_field}')
        sys.exit(1)
    except ConnectionRefusedError:
        CLIENT_LOGGER.critical('Отказ узла в попытке соединения')
        sys.exit(1)
    else:
        while True:
            if request_mode == 'listen':
                try:
                    message_handler(get_message(transport))
                except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                    CLIENT_LOGGER.error(f'Соединение с сервером {request_address} разорвано.')
                    sys.exit(1)
            if request_mode == 'send':
                try:
                    send_message(transport, creat_user_message(transport))
                except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                    CLIENT_LOGGER.error(f'Соединение с сервером {request_address} разорвано.')
                    sys.exit(1)


if __name__ == '__main__':
    main()
