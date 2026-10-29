#!/usr/bin/env python3
"""기존 பாதை_2 호환 நுழைவுப்_புள்ளி. அசல்_தரவு 구현: ../கருவிகள்/부팅시험.py"""
import importlib as 가져오기
import sys as இயக்க_முறைமை_மதிப்பு
from pathlib import Path as பாதை_2
இயக்க_முறைமை_மதிப்பு.path.insert(0, str(பாதை_2(__file__).resolve().parents[1] / 'கருவிகள்'))
if __name__ == '__main__':
    import runpy as நிரல்_துவக்குநர்
    நிரல்_துவக்குநர்.run_module('부팅시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('부팅시험')
    대응 = {'timeout': '시간제한', 'response': '응답자료', 'msg': 'பிணையம்_செய்தி', 'exact': '정확한값', 'markers': '확인표시들', 'i': '순번', 'match': '일치', 'execute': 'செயற்படுத்துக', 'cancel': 'ரத்து_இயக்கம்', 'cmd_byte': 'கட்டளை_பைட்', 'reply': 'பதிலளி', 'points': '지점들', 'server': 'சேவையகம்_மதிப்பு', 'data': 'தரவு', 'prompt': 'செயலழைப்பு', 'enter': 'உள்ளிடு', 'imported': '들여온파일', 'send': 'அனுப்பு', 'main': 'செயல்படுத்துக', 'ROOT': 'திட்டப்பணி_மூலம்', 'text': 'உரை', 'first_gui': '첫화면', 'pixel': 'படக்_கூறு', 'java_class': '자바클래스', 'upload': 'பதிவேற்று_கோப்புகள்', 'pixels_file': 'படக்_கூறு_கோப்பு', 'pixels_data': 'படக்_கூறு_தரவு', 'edit': 'திருத்து_மதிப்பு', 'receive_until': '표시까지받기', 'selector': 'தேர்வி', 'size': 'அளவு', 'qmp_path': '모의제어경로', 'key': '누름값', 'second_gui': '둘째화면', 'y': 'Y_பொத்தான்_அச்சுத்_தொகுப்பு', 'result': 'அளவிடக்கூடியது', 'samples': '예제들', 'client': 'பயனகம்', 'line': 'உள்ளீட்டு_வரி', 'report': 'செல்லுபடியாக்கம்_அறிக்கை', 'work': '작업경로', 'x': 'x_ஒத்ததரமுள்ளது', 'python_checks': '파이썬검사', 'download': 'பதிவிறக்கு', 'greeting': '인사', 'dims': '치수', 'chunk': '조각', 'deadline': '마감시각', 'proc': 'செயல்பாடு', 'content': 'உள்ளடக்கம்_மதிப்பு', 'block': 'தரவு_தடு', 'marker': '확인표시', 'command': 'கட்டளை', 'expected': '예상결과', 'shell': 'கூடு', 'drawing': 'வரைதல்_பாதை', 'f': 'கோப்பு_உள்ளீடு', 'transcript': '대화기록', 'offset': 'ஆஃப்செட்_மதிப்பு', 'path': 'பாதை_2', 'screenshot': 'ஸ்கிரீன்ஷாட்', 'arguments': '전달인수', 'pixels': '화소들', 'viewer': '화면접속자', 'output': '출력결과', 'stream': 'தொடரோடி_மதிப்பு', 'cmd': '명령인수', 'name': 'பெயர்', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
