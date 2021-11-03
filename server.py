"""Программа-сервер"""

import socket
import sys
import json
import logging
import logs.server_log_config

from common.variables import ACTION, ACCOUNT_NAME, RESPONSE, MAX_CONNECTIONS, \
    PRESENCE, TIME, USER, ERROR, DEFAULT_PORT, RESPONDEFAULT_IP_ADDRESSSE, PORT
from common.utils import get_message, send_message
from errors import IncorrectDataRecivedError
from decos import Log

SERVER_LOGGER = logging.getLogger('server')


@Log()
def process_user_message(message):
    """
    Обработчик сообщений от клиентов, принимает словарь -
    сообщение от клинта, проверяет корректность,
    возвращает словарь-ответ для клиента

    :param message:
    :return:
    """
    SERVER_LOGGER.info(f'Разбор сообщения {message}.')
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
            and USER in message and PORT in message and message[USER][ACCOUNT_NAME] == 'Guest':
        return {RESPONSE: 200}
    return {
        RESPONDEFAULT_IP_ADDRESSSE: 400,
        ERROR: 'Bad Request'
    }


def main():
    """
    Загрузка параметров командной строки, если нет параметров, то задаём значения по умоланию.
    Сначала обрабатываем порт:
    server.py -p 8888 -a 127.0.0.1
    :return:
    """

    try:
        if '-p' in sys.argv:
            listen_port = int(sys.argv[sys.argv.index('-p') + 1])
        else:
            listen_port = DEFAULT_PORT
        if listen_port < 1024 or listen_port > 65535:
            raise ValueError
    except IndexError:
        SERVER_LOGGER.critical(f'После параметра -\'p\' отсутствует номер порта.')
        sys.exit(1)
    except ValueError:
        SERVER_LOGGER.critical(f'Указано неверное значение порта - {listen_port}. В качестве порта может быть '
                               f'указано только число в диапазоне от 1024 до 65535.')
        sys.exit(1)

    # Затем загружаем какой адрес слушать

    try:
        if '-a' in sys.argv:
            listen_address = sys.argv[sys.argv.index('-a') + 1]
        else:
            listen_address = ''

    except IndexError:
        SERVER_LOGGER.critical(f'После параметра -\'a\' отсутствует адрес.')
        sys.exit(1)

    SERVER_LOGGER.info(f'Сервер запущен. Порт для подключения: {listen_port}, адрес: {listen_address}. '
                       f'При отсутствии адреса сервер принимает соединения со любых адресов')
    # Готовим сокет
    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.bind((listen_address, listen_port))

    SERVER_LOGGER.info(f'Настройка сокета завершена.')

    # Слушаем порт
    transport.listen(MAX_CONNECTIONS)

    while True:
        user, user_address = transport.accept()
        SERVER_LOGGER.info(f'Соединение с  {user_address} установлено')
        try:
            message_from_user = get_message(user)
            SERVER_LOGGER.info(f'Получено сообщение клиента {user_address} - {message_from_user}')
            response = process_user_message(message_from_user)
            SERVER_LOGGER.info(f'Сформирован ответ клиенту {user_address}')
            send_message(user, response)
            SERVER_LOGGER.info(f'Ответ {response} клиенту {user_address} отправлен. Закрытие соединения.')
            user.close()
        except json.JSONDecodeError:
            SERVER_LOGGER.error(f'Не удалось декодировать сообщение клиента {user_address}. Закрытие соединения.')
            user.close()
        except IncorrectDataRecivedError:
            SERVER_LOGGER.error(f'Клиент {user_address} отправил некорректные данные. Закрытие соединения.')
            user.close()


if __name__ == '__main__':
    main()
