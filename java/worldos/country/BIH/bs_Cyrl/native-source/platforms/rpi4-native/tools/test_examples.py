#!/usr/bin/env python3
"""기존 пут 호환 унос_тачка. стваран_подаци 구현: ../도구/예제시험.py"""
import importlib as 가져오기
import sys as оперативни_систем_вриједност
from pathlib import Path as пут
оперативни_систем_вриједност.path.insert(0, str(пут(__file__).resolve().parents[1] / '도구'))
if __name__ == '__main__':
    import runpy as 실행기
    실행기.run_module('예제시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('예제시험')
    대응 = {'count': '항목수', 'exact': '정확한값', 'expected_file': '예상파일', 'ftp_port': '파일전송접속번호', 'data': 'подаци', 'graphics_command': '그림명령', 'main': '시작', 'row': '행위치', 'init': '초기값', 'target': 'циљ', 'ROOT': '기준', 'text': 'текст', 'binary': 'бинарно', 'out': '결과자료', 'entry': 'унос_тачка', 'got': '받은수', 'port': '접속번호', 'graphics_start': 'почети_уцртавање', 'col': '열위치', 'begin': '시작위치', 'kind': 'категорија_вриједност', 'selector': '준비선택기', 'n': '개수', 'key': '누름값', 'y': '세로좌표', 'client': 'клијент', 'line': 'редак', 'report': 'провјера_извјештај', 'language': 'Језик', 'x': '가로좌표', 'start': '시작', 'rgb': '빛삼원색', 'down': '누르는중', 'listing': 'послати_списак', 'payload': 'корисни_садржај_подаци', 'proc': 'процес', 'w': '너비값', 'temporary': '임시자원', 'echo': '되돌림서버항목', 'label': 'назив_табела', 'content': 'Садржај_вриједност', 'argument': '전달값', 'EchoServers': '되돌림서버', 'marker': '확인표시', 'expected': '예상결과', 'test_language': 'test_언어', 'filename': 'фајл_унос_назив', 'shell': 'љуска', 'color': '색상', 'transcript': '대화기록', 'offset': '변위', 'h': '높이값', 'run': '실행', 'c': 'кôд_знака', 'path': 'пут', 'encoding': 'скуп_знакова', 'end': '끝위치', 'ftp': 'фајл_пријенос_веза', 'pixels': '화소들', 'symbol': '심볼', 'source': '원본자료', 'name': 'назив', 'receive': '수신하기', 'manifest': '꾸러미명세'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
