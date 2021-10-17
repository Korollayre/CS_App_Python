"""
Создать текстовый файл test_file.txt, заполнить его тремя строками: «сетевое программирование», «сокет», «декоратор».
Проверить кодировку файла по умолчанию. Принудительно открыть файл в формате Unicode и вывести его содержимое.
"""

import locale
default_encoding = locale.getpreferredencoding()
# Кодировка по умолчанию - cp1251

lines = ['сетевое программирование\n', 'сокет\n', 'декоратор']

file_w = open('test_file.txt', 'w', encoding=default_encoding)
file_w.writelines([el.encode('utf-8').decode('cp1251') for el in lines])
file_w.close()

file_r = open('test_file.txt', 'r', encoding='utf-8')
print(file_r.read())
file_r.close()
