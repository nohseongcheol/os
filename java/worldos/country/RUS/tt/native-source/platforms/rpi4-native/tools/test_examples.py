#!/usr/bin/env python3
"""기존 Yul 호환 кертү_балл. фактик_мәгълүмат 구현: ../Кораллар/예제시험.py"""
import importlib as TAKE_VALUE
import sys as операцион_система_VALUE
from pathlib import Path as Yul
операцион_система_VALUE.path.insert(0, str(Yul(__file__).resolve().parents[1] / 'Кораллар'))
if __name__ == '__main__':
    import runpy as кушымта_хезмәткәр
    кушымта_хезмәткәр.run_module('예제시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('예제시험')
    대응 = {'count': 'кертү_COUNT', 'exact': 'EXACT_VALUE', 'expected_file': '예상파일', 'ftp_port': '파일전송접속번호', 'data': 'мәгълүмат', 'graphics_command': 'графика_команда', 'main': 'эшләтү', 'row': 'юл_урнаштыру', 'init': '초기값', 'target': 'максат_кыйммәт', 'ROOT': 'экранга_җибәрү_тамыр', 'text': 'Mäten', 'binary': 'бинар', 'out': 'үлчәм_мәгълүмат', 'entry': 'кертү_балл', 'got': 'RECEIVED_COUNT', 'port': '접속번호', 'graphics_start': 'Start_сызым', 'col': 'COLUMN_урнаштыру', 'begin': 'Start_OFFSET', 'kind': 'категория_VALUE', 'selector': 'сайлагыч', 'n': 'элемент_COUNT', 'key': '누름값', 'y': '세로좌표', 'client': 'клиент', 'line': 'юл', 'report': 'раслау_отчет', 'language': 'тел', 'x': 'X_координатасы', 'start': 'эшләтү', 'rgb': '빛삼원색', 'down': '누르는중', 'listing': 'җибәрү_Исемлек', 'payload': 'төп_өлеш_мәгълүмат', 'proc': 'Процесс', 'w': '너비값', 'temporary': '임시자원', 'echo': '되돌림서버항목', 'label': 'исем_таблица', 'content': 'Эчтәлек_VALUE', 'argument': '전달값', 'EchoServers': '되돌림서버', 'marker': '확인표시', 'expected': '예상결과', 'test_language': 'test_언어', 'filename': 'файл_кертү_исем', 'shell': 'тышча', 'color': '색상', 'transcript': '대화기록', 'offset': 'OFFSET_VALUE', 'h': '높이값', 'run': 'үтәргә_команда', 'c': 'символ_коды', 'path': 'Yul', 'encoding': 'символлар_җыелмасы', 'end': 'тәмамлау_OFFSET', 'ftp': 'файл_күчерү_тоташу', 'pixels': '화소들', 'symbol': 'символ_VALUE', 'source': '원본자료', 'name': 'исем', 'receive': '수신하기', 'manifest': '꾸러미명세'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
