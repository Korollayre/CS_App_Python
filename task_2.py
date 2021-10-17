"""
Каждое из слов «class», «function», «method» записать в байтовом типе без преобразования в последовательность кодов
(не используя методы encode и decode) и определить тип, содержимое и длину соответствующих переменных.
"""

words_lst = ['class', 'function', 'method']

for el in words_lst:
    el_bytes = bytes(el, encoding='utf-8')
    print(type(el_bytes), el_bytes, len(el_bytes))
