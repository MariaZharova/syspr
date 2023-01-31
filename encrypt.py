# -- coding: utf-8 --
"""
Шифровальщик
"""

import time
import sys
import os

import PySimpleGUI as sg
#pip install pysimplegui


def xor_crypt_data(data, c=0xA8):
    """
    ASCII Win-1251 168 (Ё)
    """
    res = bytearray([byte^c for byte in bytearray(data)])
    return res


def main_window():
    title = 'Шифровальщик'

    # Формируем верстку окна программы
    layout = [
        [sg.Text(title, justification='center', font=("Helvetica", 24))],
        [sg.Text('_' * 92)],
        [sg.Text('Выберите папку для шифрования', font=("Helvetica", 14))],
        [sg.Text('Обрабатываются все вложенные папки!')],
        [sg.InputText(size=(45, 1), key='dir'), sg.FolderBrowse('Обзор')],
        [sg.Submit('Запустить'), sg.Submit('Стоп')],
        [sg.Output(size=(90, 10), key='-OUTPUT-')],
        [sg.Cancel('Выход')]
    ]

    # Запускаем окно
    main_window = sg.Window(title, layout)
    while True:
        # Считываем события окна
        event, values = main_window.read(timeout=400)

        if event in (None, 'Выход', sg.WIN_CLOSED):
            main_window.close()
            return None

        if event == 'Запустить':
            # Валидация папки
            dir_path = values.get('dir')
            if not dir_path:
                sg.popup('Выберите папку')
                continue

            # Список всех фйлов рекурсивно
            file_list = [os.path.join(dp, f) for dp, dn, filenames in os.walk(dir_path) for f in filenames if
                         '~$' not in f]
            # print(f'Всего получено {len(file_list)} файлов в папке {dir_path}')
            print("-" * 50)
            for file in file_list:
                # Считываем события кона чтобы иметь вомзожность остановить работу
                event, values = main_window.read(timeout=400)
                if event == 'Стоп':
                    break

                try:
                    # with open(file, 'rb') as f:
                    #     data = f.read()
                    # data = xor_crypt_data(data)
                    # with open(file, 'wb') as f:
                    #     f.write(data)

                    # Открываем файл,ч итаем, шифруем, пишем, закрываем
                    f = open(file, "rb+")
                    data = f.read()
                    data = xor_crypt_data(data)
                    f.seek(0)
                    f.write(data)
                    f.truncate()
                    time.sleep(3)
                    f.close()

                except Exception as e:
                    print(f"Ошибка шифрования/дешифрования файла {file}")
                    print(str(e))
                else:
                    print(f"Файл {file} зашифрован/дешифрован")
                print("-" * 50)


            msg = f"Шифрование папки {dir_path} завершено!"
            print(msg)
            sg.popup(msg)

            # print(file_list)


if __name__ == "__main__":
    main_window()
    sys.exit()