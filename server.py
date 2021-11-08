"""Программа-сервер"""
import select
import socket
import sys
import logging
import argparse
import time

import logs.server_log_config

from common.variables import ACTION, ACCOUNT_NAME, RESPONSE, MAX_CONNECTIONS, \
    PRESENCE, TIME, USER, ERROR, DEFAULT_PORT, RESPONDEFAULT_IP_ADDRESSSE, PORT, MESSAGE, MESSAGE_TEXT, SENDER
from common.utils import get_message, send_message
from decos import Log

SERVER_LOGGER = logging.getLogger('server')


@Log()
def process_user_message(message, messages, user):
    """
    Обработчик сообщений от клиентов, принимает словарь -
    сообщение от клинта, проверяет корректность,
    возвращает словарь-ответ для клиента

    :param message:
    :param messages:
    :param user:
    :return:
    """
    SERVER_LOGGER.info(f'Разбор сообщения {message}.')
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
            and USER in message and message[USER][ACCOUNT_NAME] == 'Guest':
        send_message(user, {RESPONSE: 200})
        return
    elif ACTION in message and message[ACTION] == MESSAGE and \
            TIME in message and MESSAGE_TEXT in message:
        messages.append((message[ACCOUNT_NAME], message[MESSAGE_TEXT]))
        return
    else:
        send_message(user, {
            RESPONSE: 400,
            ERROR: 'Bad Request'})
        return


@Log()
def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', default=DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-a', default='', nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    listen_address = namespace.a
    listen_port = namespace.p

    if not 1023 < listen_port < 65536:
        SERVER_LOGGER.critical(f'Попытка запуска сервера с указанием неподходящего порта {listen_port}')
        sys.exit(1)

    return listen_address, listen_port


def main():
    """
    Загрузка параметров командной строки, если нет параметров, то задаём значения по умоланию.
    Сначала обрабатываем порт:
    server.py -p 8888 -a 127.0.0.1
    :return:
    """

    listen_address, listen_port = arg_parser()

    SERVER_LOGGER.info(f'Сервер запущен. Порт для подключения: {listen_port}, адрес: {listen_address}. '
                       f'При отсутствии адреса сервер принимает соединения со любых адресов')
    # Готовим сокет
    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.bind((listen_address, listen_port))
    transport.settimeout(1)

    SERVER_LOGGER.info(f'Настройка сокета завершена.')

    clients_list, messages_list = [], []

    # Слушаем порт
    transport.listen(MAX_CONNECTIONS)

    while True:
        try:
            user, user_address = transport.accept()
        except OSError:
            pass
        else:
            SERVER_LOGGER.info(f'Соединение с {user_address} установлено')
            clients_list.append(user)

        recv_sockets_list, send_sockets_list, errors_sockets_list = [], [], []

        try:
            if clients_list:
                recv_sockets_list, send_sockets_list, errors_sockets_list = select.select(clients_list, clients_list,
                                                                                          [], 0)
        except OSError:
            pass

        if recv_sockets_list:
            for sender in recv_sockets_list:
                try:
                    process_user_message(get_message(sender), messages_list, sender)
                except Exception:
                    SERVER_LOGGER.info(f'Соединение с {sender.getpeername()} разорвано.')
                    sender.close()
                    clients_list.remove(sender)

        if messages_list and send_sockets_list:
            message_data = messages_list.pop(0)
            message = {
                ACTION: MESSAGE,
                TIME: time.time(),
                SENDER: message_data[0],
                MESSAGE_TEXT: message_data[1]
            }
            for receiver in send_sockets_list:
                try:
                    send_message(receiver, message)
                    SERVER_LOGGER.info(f'Ответ {message} клиенту {receiver} отправлен.')
                except Exception:
                    SERVER_LOGGER.info(f'Соединение с {receiver.getpeername()} разорвано.')
                    receiver.close()
                    clients_list.remove(receiver)


if __name__ == '__main__':
    main()
