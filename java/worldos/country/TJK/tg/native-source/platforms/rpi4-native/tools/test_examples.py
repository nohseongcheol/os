#!/usr/bin/env python3
"""기존 масир 호환 ворида_нуқта. воқеӣ_иттилоот 구현: ../Абзорҳо/예제시험.py"""
import importlib as 가져오기
import sys as системаи_омил_қимат
from pathlib import Path as масир
системаи_омил_қимат.path.insert(0, str(масир(__file__).resolve().parents[1] / 'Абзорҳо'))
if __name__ == '__main__':
    import runpy as барнома_панели_барномаҳо
    барнома_панели_барномаҳо.run_module('예제시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('예제시험')
    대응 = {'count': '항목수', 'exact': '정확한값', 'expected_file': '예상파일', 'ftp_port': '파일전송접속번호', 'data': 'иттилоот', 'graphics_command': '그림명령', 'main': 'порча', 'row': '행위치', 'init': '초기값', 'target': 'ҳадаф', 'ROOT': '기준', 'text': 'Матн', 'binary': 'дуӣ', 'out': '결과자료', 'entry': 'ворида_нуқта', 'got': '받은수', 'port': '접속번호', 'graphics_start': 'Оғоз_нақша', 'col': '열위치', 'begin': 'Оғоз_Интиқолшавӣ', 'kind': 'категория_қимат', 'selector': 'интихобкунанда', 'n': '개수', 'key': '누름값', 'y': '세로좌표', 'client': 'муштарӣ', 'line': 'хат', 'report': 'санҷиши_эътибор_гузориш', 'language': 'Забон', 'x': 'координатаи_х', 'start': 'порча', 'rgb': '빛삼원색', 'down': '누르는중', 'listing': 'фиристодан_Рӯйхат', 'payload': 'қобилият_иттилоот', 'proc': 'Раванд', 'w': '너비값', 'temporary': '임시자원', 'echo': '되돌림서버항목', 'label': 'ном_ҷадвал', 'content': 'Мӯҳтаво_қимат', 'argument': '전달값', 'EchoServers': '되돌림서버', 'marker': '확인표시', 'expected': '예상결과', 'test_language': 'test_언어', 'filename': 'файл_ворида_ном', 'shell': 'восит', 'color': '색상', 'transcript': '대화기록', 'offset': 'Интиқолшавӣ_қимат', 'h': '높이값', 'run': 'иҷро_кардан_фармон', 'c': 'рамзи_аломат', 'path': 'масир', 'encoding': 'маҷмӯи_аломатҳо', 'end': 'анҷом_додан_Интиқолшавӣ', 'ftp': 'файл_интиқол_пайваст', 'pixels': '화소들', 'symbol': 'аломат_қимат', 'source': '원본자료', 'name': 'Ном', 'receive': '수신하기', 'manifest': '꾸러미명세'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
