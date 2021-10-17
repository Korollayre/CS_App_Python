"""
Преобразовать слова «разработка», «администрирование», «protocol», «standard»
из строкового представления в байтовое и выполнить обратное преобразование (используя методы encode и decode).
"""

words_lst = ['разработка', 'администрирование', 'protocol', 'standard']
bytes_lst = []

print('Байтовый формат:')
for el in words_lst:
    el_bytes = el.encode('utf-8')
    print(type(el_bytes), el_bytes)
    bytes_lst.append(el_bytes)

print('\nСтроковый формат:')
for el in bytes_lst:
    el_bytes = el.decode('utf-8')
    print(type(el_bytes), el_bytes)
    bytes_lst.append(el_bytes)
