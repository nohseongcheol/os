#!/usr/bin/env python3
"""기존 பாதை_2 호환 நுழைவுப்_புள்ளி. அசல்_தரவு 구현: ../கருவிகள்/예제시험.py"""
import importlib as 가져오기
import sys as இயக்க_முறைமை_மதிப்பு
from pathlib import Path as பாதை_2
இயக்க_முறைமை_மதிப்பு.path.insert(0, str(பாதை_2(__file__).resolve().parents[1] / 'கருவிகள்'))
if __name__ == '__main__':
    import runpy as நிரல்_துவக்குநர்
    நிரல்_துவக்குநர்.run_module('예제시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('예제시험')
    대응 = {'count': '항목수', 'exact': '정확한값', 'expected_file': '예상파일', 'ftp_port': 'கோப்பு_இடமாற்று_முனைய_எண்', 'data': 'தரவு', 'graphics_command': 'கிராஃபிக்ஸ்_கட்டளை', 'main': 'செயல்படுத்துக', 'row': 'வரிசை_நிலை', 'init': '초기값', 'target': 'இலக்கு', 'ROOT': 'திட்டப்பணி_மூலம்', 'text': 'உரை', 'binary': 'பைனரி', 'out': 'அளவிடக்கூடியது_தரவு', 'entry': 'நுழைவுப்_புள்ளி', 'got': '받은수', 'port': 'முனைய_எண்', 'graphics_start': 'தொடங்கு_வரைதல்', 'col': 'நெடுவரிசை_நிலை', 'begin': 'தொடங்கு_ஆஃப்செட்', 'kind': 'வகை_மதிப்பு_4b6d6445', 'selector': 'தேர்வி', 'n': '개수', 'key': '누름값', 'y': 'Y_பொத்தான்_அச்சுத்_தொகுப்பு', 'client': 'பயனகம்', 'line': 'உள்ளீட்டு_வரி', 'report': 'செல்லுபடியாக்கம்_அறிக்கை', 'language': 'மொழி', 'x': 'x_ஒத்ததரமுள்ளது', 'start': 'செயல்படுத்துக', 'rgb': '빛삼원색', 'down': '누르는중', 'listing': 'அனுப்பு_பட்டியல்', 'payload': 'பேலோட்_தரவு', 'proc': 'செயல்பாடு', 'w': '너비값', 'temporary': '임시자원', 'echo': '되돌림서버항목', 'label': 'பெயர்_அட்டவணை', 'content': 'உள்ளடக்கம்_மதிப்பு', 'argument': '전달값', 'EchoServers': '되돌림서버', 'marker': '확인표시', 'expected': '예상결과', 'test_language': 'test_언어', 'filename': 'கோப்பு_உள்ளீடு_பெயர்', 'shell': 'கூடு', 'color': '색상', 'transcript': '대화기록', 'offset': 'ஆஃப்செட்_மதிப்பு', 'h': '높이값', 'run': 'இயக்கு_கட்டளை', 'c': 'எழுத்துக்குறி_குறியீடு', 'path': 'பாதை_2', 'encoding': 'எழுத்துக்குறி_குழு', 'end': 'முடி_ஆஃப்செட்', 'ftp': 'கோப்பு_இடமாற்று_இணைப்பு', 'pixels': '화소들', 'symbol': 'சின்னம்_மதிப்பு', 'source': '원본자료', 'name': 'பெயர்', 'receive': '수신하기', 'manifest': 'மூட்டை_தொற்றம்'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
