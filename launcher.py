import subprocess

PROCESS = []

while True:

    ACTION = input("Для запуска сервера и клиентов введите 's', для выхода - 'q', для закрытия всех окон 'x': ")

    if ACTION == 'q':
        break
    elif ACTION == 's':
        PROCESS.append(subprocess.Popen('python server.py', creationflags=subprocess.CREATE_NEW_CONSOLE))

        for i in range(2):
            PROCESS.append(subprocess.Popen('python client.py -m send', creationflags=subprocess.CREATE_NEW_CONSOLE))

        for i in range(4):
            PROCESS.append(subprocess.Popen('python client.py -m listen', creationflags=subprocess.CREATE_NEW_CONSOLE))
    elif ACTION == 'x':
        while PROCESS:
            PROCESS.pop().kill()
