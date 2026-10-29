#!/usr/bin/env python3
"""기존 ЗАМ 호환 оролт_цэг. бодит_өгөгдөл 구현: ../Хэрэгслүүд/부팅시험.py"""
import importlib as 가져오기
import sys as үйлдлийн_систем_утга
from pathlib import Path as ЗАМ
үйлдлийн_систем_утга.path.insert(0, str(ЗАМ(__file__).resolve().parents[1] / 'Хэрэгслүүд'))
if __name__ == '__main__':
    import runpy as програм_гишүүн
    програм_гишүүн.run_module('부팅시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('부팅시험')
    대응 = {'timeout': '시간제한', 'response': '응답자료', 'msg': 'Сүлжээ_мэдээлэл', 'exact': '정확한값', 'markers': '확인표시들', 'i': '순번', 'match': '일치', 'execute': 'Гүйцэтгэх_даалгавар', 'cancel': 'болих_үйлдэл', 'cmd_byte': 'команд_байт', 'reply': 'хариулах', 'points': '지점들', 'server': 'сервер_утга', 'data': 'өгөгдөл', 'prompt': 'командын_мөр', 'enter': 'орох', 'imported': '들여온파일', 'send': 'илгээх', 'main': 'Ажиллуулах', 'ROOT': '기준', 'text': 'Бичвэр', 'first_gui': '첫화면', 'pixel': 'нягтрал', 'java_class': '자바클래스', 'upload': 'байршуулах_Файлууд', 'pixels_file': 'нягтрал_файл', 'pixels_data': 'нягтрал_өгөгдөл', 'edit': 'засварлах_утга', 'receive_until': '표시까지받기', 'selector': 'сонгогч', 'size': 'Хэмжээ', 'qmp_path': '모의제어경로', 'key': '누름값', 'second_gui': '둘째화면', 'y': '세로좌표', 'result': '결과', 'samples': '예제들', 'client': 'клиент', 'line': 'Шугам', 'report': 'баталгаажуулалт_тайлан', 'work': '작업경로', 'x': 'х_координат', 'python_checks': '파이썬검사', 'download': 'татаж_авах', 'greeting': '인사', 'dims': '치수', 'chunk': '조각', 'deadline': '마감시각', 'proc': 'үйл_явц', 'content': 'Агуулга_утга', 'block': 'өгөгдөл_хаах', 'marker': '확인표시', 'command': 'Тушаал', 'expected': '예상결과', 'shell': 'бүрхүүл', 'drawing': 'зураг_зам', 'f': 'файл_оролт', 'transcript': '대화기록', 'offset': 'Оффсет_утга', 'path': 'ЗАМ', 'screenshot': 'Дэлгэцийн_зураг_тасалж_авах', 'arguments': '전달인수', 'pixels': '화소들', 'viewer': '화면접속자', 'output': '출력결과', 'stream': 'урсгал_утга', 'cmd': '명령인수', 'name': 'Нэр', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
