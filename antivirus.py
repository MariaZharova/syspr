# -- coding: utf-8 --
"""
Антивирус
"""

import time
import sys
import os
import psutil
from pprint import pprint as pp

import PySimpleGUI as sg
#pip install pysimplegui


def main_window():
    title = 'Антивирус'
    layout = [
        [sg.Text(title, justification='center', font=("Helvetica", 24))],
        [sg.Text('_' * 92)],
        [sg.Text('Выберите папку для слежения', font=("Helvetica", 14))],
        [sg.Text('Обрабатываются все вложенные папки!')],
        [sg.InputText(size=(45, 1), key='dir'), sg.FolderBrowse('Обзор')],
        # [sg.Text('Скольк подряд измененных файлов считать подозрительной активностью'), sg.Input(5, size=(5, 1), key='num')],
        [sg.Submit('Запустить'), sg.Submit('Стоп')],
        [sg.Output(size=(90, 10), key='-OUTPUT-')],
        [sg.Cancel('Выход')]
    ]

    main_window = sg.Window(title, layout)
    while True:
        event, values = main_window.read(timeout=400)

        if event in (None, 'Выход', sg.WIN_CLOSED):
            main_window.close()
            return None

        if event == 'Запустить':
            dir_path = values.get('dir')
            if not dir_path:
                sg.popup('Выберите папку')
                continue
            dir_path = dir_path.replace('/', '\\')

            # try:
            #     num = int(values['num'])
            # except:
            #     sg.popup('Введите число')
            #     continue
            num = 1

            print(f"Запущено слежение за файлами папки {dir_path}")
            print("*" * 50)

            stop_flag = False
            i = 0
            while True:
                if stop_flag:
                    break

                # print(pp([(p.pid, p.info['name'], sum(p.info['cpu_times'])) for p in sorted(psutil.process_iter(['name', 'cpu_times']), key = lambda p: sum(p.info['cpu_times'][:2]))][-3:]))

                # Получаем все процессы системы
                for process in psutil.process_iter():

                    # Так же читаем события кона чтобы остановить
                    event, values = main_window.read(timeout=1)
                    if event == 'Стоп':
                        stop_flag = True
                        break

                    # Читаем файлы с которыми работает каждый процесс
                    flist = None
                    try:
                        flist = process.open_files()
                    except:
                        pass
                    if flist:
                        for nt in flist:
                            # Проверяем не входит ли наш путь в путь к файлу используемому процессом
                            if dir_path in nt.path:
                                print(f"Процесс {process.pid} меняет файлы в отcлеживаемой папке")
                                i += 1
                            if i >= num:
                                # Спрашиваем пользователя
                                ask = sg.popup_yes_no(f'Процесс {process .pid} превысил порог подозрительности. Удалить процесс?')
                                if ask == 'Yes':
                                    # Останаливаем подозрительный процесс
                                    process.terminate()
                                    msg = f"Процесс {process .pid} остановлен"
                                    print(msg)
                                    print("*" * 50)
                                    sg.popup(msg)
                                    stop_flag = True
                                    break
                    if stop_flag:
                        break

                # for p in psutil.process_iter(['name', 'open_files']):
                #     if stop_flag:
                #         break
                #
                #     if 'encrypt' not in p.info['name']:
                #         continue
                #
                #     for file in p.info['open_files'] or []:
                #         if stop_flag:
                #             break
                #
                #         event, values = main_window.read()
                #         if event == 'Стоп':
                #             stop_flag = True
                #
                #         # print(os.path.dirname(file.path))
                #         # print("%-5s %-10s %s" % (p.pid, p.info['name'][:10], file.path))
                #         if dir_path in os.path.dirname(file.path):
                #             print("%-5s %-10s %s" % (p.pid, p.info['name'][:10], file.path))

            msg = f"Слежение за папкой {dir_path} завершено!"
            print(msg)
            print("*" * 50)
            sg.popup(msg)

            # print(file_list)


if __name__ == "__main__":
    main_window()
    sys.exit()