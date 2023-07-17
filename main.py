# КЕША
import voice
import time
import subprocess
import config as config
import stt
import tts
from fuzzywuzzy import fuzz
import datetime
from num2words import num2words
import random


print(f"{config.VA_NAME} (v{config.VA_VER}) начал свою работу ...")


def va_respond(voice: str):
    print(voice)
    if voice.startswith(config.VA_ALIAS):
        # обращаются к ассистенту
        cmd = recognize_cmd(filter_cmd(voice))

        if cmd['cmd'] not in config.VA_CMD_LIST.keys():
            tts.va_speak("Что?")
        else:
            execute_cmd(cmd['cmd'])


def filter_cmd(raw_voice: str):
    cmd = raw_voice

    for x in config.VA_ALIAS:
        cmd = cmd.replace(x, "").strip()

    for x in config.VA_TBR:
        cmd = cmd.replace(x, "").strip()

    return cmd


def recognize_cmd(cmd: str):
    rc = {'cmd': '', 'percent': 0}
    for c, v in config.VA_CMD_LIST.items():

        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > rc['percent']:
                rc['cmd'] = c
                rc['percent'] = vrt

    return rc


def execute_cmd(cmd: str):
    if cmd == 'help':
        # help
        text = "Я умею: ..."
        text += "произносить время ..."
        text += "рассказывать анекдоты ..."
        text += "и открывать браузер"
        tts.va_speak(text)
        pass
    elif cmd == 'ctime':
        # current time
        now = datetime.datetime.now()
        text = "Сейч+ас " + num2words(now.hour, lang='ru') + " " + num2words(now.minute, lang='ru')
        tts.va_speak(text)

    elif cmd == 'joke':
        jokes = ['Как смеются программисты? ... ехе ехе ехе',
                'ЭсКьюЭль запрос заходит в бар, подходит к двум столам и спрашивает .. «м+ожно присоединиться?»',
                'Программист это машина для преобразования кофе в код']

        tts.va_speak(random.choice(jokes))

    elif cmd == 'open_browser':
        # chrome_path = 'C:\Program Files\Google\Chrome\Application\chrome.exe %s'
        # webbrowser.get(chrome_path).open("http://python.org")
        url = "http://python.org"
        chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        subprocess.call([chrome_path, url])

    elif cmd == 'exit':
        tts.va_speak("До свидания!")
        exit()


    alarm_time = voice.split(":")
    alarm_hour = int(alarm_time[0])
    alarm_minute = int(alarm_time[1])

    if cmd == 'alarm':
        def set_alarm():
            tts.va_speak("Укажите время будильника в формате ЧЧ:ММ")
        voice = stt.va_listen()
        tts.va_speak("Будильник установлен")
        while True:
            now = datetime.datetime.now()
            if now.hour == alarm_hour and now.minute == alarm_minute:
                tts.va_speak("Пора вставать!")
                break
            time.sleep(60)

    set_alarm()




# начать прослушивание команд
stt.va_listen(va_respond)