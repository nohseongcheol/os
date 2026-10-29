#!/usr/bin/env python3
"""기존 ПАТЕКА 호환 внес_поен. реален_податоци 구현: ../Алатки/예제시험.py"""
import importlib as TAKE_VALUE
import sys as оперативен_систем_VALUE
from pathlib import Path as ПАТЕКА
оперативен_систем_VALUE.path.insert(0, str(ПАТЕКА(__file__).resolve().parents[1] / 'Алатки'))
if __name__ == '__main__':
    import runpy as програма_стартувач
    програма_стартувач.run_module('예제시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('예제시험')
    대응 = {'count': 'внес_COUNT', 'exact': 'EXACT_VALUE', 'expected_file': '예상파일', 'ftp_port': 'датотека_пренос_број_на_порта', 'data': 'податоци', 'graphics_command': 'графика_наредба', 'main': 'Изврши_2', 'row': 'ROW_позиционирање', 'init': '초기값', 'target': 'цел', 'ROOT': 'Project_корен', 'text': 'Текст', 'binary': 'бинарен', 'out': 'мерка_податоци', 'entry': 'внес_поен', 'got': 'RECEIVED_COUNT', 'port': 'број_на_порта', 'graphics_start': 'Start_цртеж', 'col': 'COLUMN_позиционирање', 'begin': 'Start_OFFSET', 'kind': 'област_VALUE', 'selector': 'избирач', 'n': 'ставка_COUNT', 'key': '누름값', 'y': '세로좌표', 'client': 'клиент', 'line': 'ред', 'report': 'проверка_извештај', 'language': 'јазик', 'x': 'координата_х', 'start': 'Изврши_2', 'rgb': '빛삼원색', 'down': '누르는중', 'listing': 'испрати_Список', 'payload': 'капацитет_податоци', 'proc': 'Процес', 'w': '너비값', 'temporary': '임시자원', 'echo': '되돌림서버항목', 'label': 'име_табела', 'content': 'Содржина_VALUE', 'argument': '전달값', 'EchoServers': '되돌림서버', 'marker': '확인표시', 'expected': '예상결과', 'test_language': 'test_언어', 'filename': 'датотека_внес_име', 'shell': 'обвивка', 'color': '색상', 'transcript': '대화기록', 'offset': 'OFFSET_VALUE', 'h': '높이값', 'run': 'Изврши_наредба', 'c': 'кодна_точка', 'path': 'ПАТЕКА', 'encoding': 'збир_знаци', 'end': 'крај_OFFSET', 'ftp': 'датотека_пренос_врска', 'pixels': '화소들', 'symbol': 'симбол_VALUE', 'source': '원본자료', 'name': 'Име', 'receive': '수신하기', 'manifest': '꾸러미명세'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
