#!/usr/bin/env python3
"""기존 ЖОЛ 호환 киргизме_жазуу_упай. актуалдуу_берилмелер 구현: ../Куралдар/부팅시험.py"""
import importlib as 가져오기
import sys as оперативдик_система_маани
from pathlib import Path as ЖОЛ
оперативдик_система_маани.path.insert(0, str(ЖОЛ(__file__).resolve().parents[1] / 'Куралдар'))
if __name__ == '__main__':
    import runpy as програм_жаратма_тарткычы
    програм_жаратма_тарткычы.run_module('부팅시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('부팅시험')
    대응 = {'timeout': '시간제한', 'response': '응답자료', 'msg': 'Желе_билдирүү', 'exact': '정확한값', 'markers': '확인표시들', 'i': '순번', 'match': '일치', 'execute': 'аткаруу_маселе', 'cancel': 'жокко_чыгаруу_иш_аракет', 'cmd_byte': 'буйрук_байт', 'reply': 'жооп_берүү', 'points': '지점들', 'server': 'сервер_маани', 'data': 'берилмелер', 'prompt': 'айтып_туруу', 'enter': 'кирүү', 'imported': '들여온파일', 'send': 'жөнөтүү', 'main': 'Жүргүзүү', 'ROOT': '기준', 'text': 'Текст', 'first_gui': '첫화면', 'pixel': 'пиксел', 'java_class': '자바클래스', 'upload': 'жүктөп_жөнөтүү_Файлдар', 'pixels_file': 'пиксел_файл', 'pixels_data': 'пиксел_берилмелер', 'edit': 'түзөтүү_маани', 'receive_until': '표시까지받기', 'selector': 'селектор', 'size': 'Өлчөмү', 'qmp_path': '모의제어경로', 'key': '누름값', 'second_gui': '둘째화면', 'y': '세로좌표', 'result': '결과', 'samples': '예제들', 'client': 'керектөөчү', 'line': 'сап', 'report': 'ырастоо_отчет', 'work': '작업경로', 'x': 'x_координата', 'python_checks': '파이썬검사', 'download': 'жүктөө', 'greeting': '인사', 'dims': '치수', 'chunk': '조각', 'deadline': '마감시각', 'proc': 'Процесси', 'content': 'Мазмун_маани', 'block': 'берилмелер_тосмолоо', 'marker': '확인표시', 'command': 'Команда', 'expected': '예상결과', 'shell': 'сырты', 'drawing': 'чийүү_жол', 'f': 'файл_киргизме_жазуу', 'transcript': '대화기록', 'offset': 'Жылбышуу_маани', 'path': 'ЖОЛ', 'screenshot': 'экранды_кыркып_бөлүү', 'arguments': '전달인수', 'pixels': '화소들', 'viewer': '화면접속자', 'output': '출력결과', 'stream': 'агым_маани', 'cmd': '명령인수', 'name': 'Аты', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
