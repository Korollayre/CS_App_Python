"""
Определить, какие из слов «attribute», «класс», «функция», «type» невозможно записать в байтовом типе.
"""

words_lst = ['attribute', 'класс', 'функция', 'type']

for el in words_lst:
    try:
        print(bytes(el, 'ascii'))
    except UnicodeEncodeError:
        print(f'"{el}" невозможно записать в байтовом типе')
