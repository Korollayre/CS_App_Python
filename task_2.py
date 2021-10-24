"""
Задание на закрепление знаний по модулю json. Есть файл orders в формате JSON с информацией о заказах.
Написать скрипт, автоматизирующий его заполнение данными.
Для этого:

Создать функцию write_order_to_json(), в которую передается 5 параметров —
товар (item), количество (quantity), цена (price), покупатель (buyer), дата (date).
Функция должна предусматривать запись данных в виде словаря в файл orders.json.
При записи данных указать величину отступа в 4 пробельных символа;

Проверить работу программы через вызов функции write_order_to_json() с передачей в нее значений каждого параметра.
"""
import datetime
import json


def write_order_to_json(**kwargs):
    with open('orders.json', 'r', encoding='utf-8') as f_n:
        data = json.load(f_n)
        data['orders'].append(kwargs)

        with open('orders.json', 'w', encoding='utf-8') as f_n_writer:
            json.dump(data, f_n_writer, indent=4)


write_order_to_json(item='Graphic Card MSI NVIDIA GeForce RTX 3060', quantity=1, price=81740, buyer='Sad Man',
                    date=datetime.datetime.now().strftime("%d-%m-%Y %H:%M"))

write_order_to_json(item='Processor AMD Ryzen 5 3600 OEM', quantity=1, price=13999, buyer='Funny Man',
                    date=datetime.datetime.now().strftime("%d-%m-%Y %H:%M"))
