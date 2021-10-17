"""
Каждое из слов «разработка», «сокет», «декоратор» представить в строковом формате
и проверить тип и содержание соответствующих переменных. Затем с помощью онлайн-конвертера преобразовать
строковые представление в формат Unicode и также проверить тип и содержимое переменных.
"""

str_lst = ['разработка', 'сокет', 'декоратор']

uni_lst = ['\u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0430',
           '\u0441\u043e\u043a\u0435\u0442',
           '\u0434\u0435\u043a\u043e\u0440\u0430\u0442\u043e\u0440']

print('Строковый формат:')
for el in str_lst:
    print(type(el), el)

print('\nUnicode формат:')
for el in uni_lst:
    print(type(el), el)
