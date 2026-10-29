#!/usr/bin/env python3
"""기존 ਮਾਰਗ 호환 ਦਾਖਲਾ_ਪੌਇੰਟ. ਅਸਲ_ਸਮੱਗਰੀ 구현: ../ਸਾਧਨ/부팅시험.py"""
import importlib as 가져오기
import sys as ਸਿਸਟਮ_ਚਲਾਉਣਾ_ਕੀਮਤ
from pathlib import Path as ਮਾਰਗ
ਸਿਸਟਮ_ਚਲਾਉਣਾ_ਕੀਮਤ.path.insert(0, str(ਮਾਰਗ(__file__).resolve().parents[1] / 'ਸਾਧਨ'))
if __name__ == '__main__':
    import runpy as ਐਪਲੀਕੇਸ਼_ਐਪ_ਡ੍ਰਾਅਰ
    ਐਪਲੀਕੇਸ਼_ਐਪ_ਡ੍ਰਾਅਰ.run_module('부팅시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('부팅시험')
    대응 = {'timeout': '시간제한', 'response': '응답자료', 'msg': 'ਨੈਟਵਰਕ_ਸੁਨੇਹਾ', 'exact': '정확한값', 'markers': '확인표시들', 'i': '순번', 'match': '일치', 'execute': 'ਚਲਾਓ', 'cancel': 'ਰੱਦ_ਕਰੋ_ਕਰਵਾਈ', 'cmd_byte': 'ਆਦੇਸ਼_ਬਾਈਟ', 'reply': 'ਜਵਾਬ_ਦਿਓ', 'points': '지점들', 'server': 'ਸਰਵਰ_ਕੀਮਤ', 'data': 'ਸਮੱਗਰੀ', 'prompt': 'ਤਤਪਰ', 'enter': 'ਦਾਖ਼ਲ_ਕਰੋ', 'imported': '들여온파일', 'send': 'ਈਮੇਲ', 'main': 'ਚਲਾਓ_2', 'ROOT': 'ਪ੍ਰੋਜੈਕਟ_ਰੂਟ', 'text': 'ਟੈਕਸਟ', 'first_gui': '첫화면', 'pixel': 'ਬਿੰਦੂ', 'java_class': '자바클래스', 'upload': 'ਅਪਲੋਡ_ਕਰੋ_ਫ਼ਾਈਲਾਂ', 'pixels_file': 'ਬਿੰਦੂ_ਲਿਖਤ_ਪੱਤਰ', 'pixels_data': 'ਬਿੰਦੂ_ਸਮੱਗਰੀ', 'edit': 'ਸੰਪਾਦਨ_ਕੀਮਤ', 'receive_until': '표시까지받기', 'selector': 'ਚੋਣਕਰਤਾ', 'size': 'ਆਕਾਰ', 'qmp_path': '모의제어경로', 'key': '누름값', 'second_gui': '둘째화면', 'y': '세로좌표', 'result': 'ਮਾਪ', 'samples': '예제들', 'client': 'ਗਾਹਕ', 'line': 'ਲਾਈਨ', 'report': 'ਮਾਨਤਾ_ਵਿਵਰਨ', 'work': '작업경로', 'x': 'x_ਕੌਔਰਡੀਨੇਟ', 'python_checks': '파이썬검사', 'download': 'ਡਾਉਨਲਡ', 'greeting': '인사', 'dims': '치수', 'chunk': '조각', 'deadline': '마감시각', 'proc': 'ਪਰੋਸੈੱਸ', 'content': 'ਤਤਕਰਾ_ਕੀਮਤ', 'block': 'ਸਮੱਗਰੀ_ਬਲੌਕ_ਕਰੋ', 'marker': '확인표시', 'command': 'ਕਮਾਂਡ', 'expected': '예상결과', 'shell': 'ਸ਼ੈਲ', 'drawing': 'ਚਿੱਤਰ_ਬਨਾਉਣਾ_ਰਸਤਾ', 'f': 'ਲਿਖਤ_ਪੱਤਰ_ਦਾਖਲਾ', 'transcript': '대화기록', 'offset': 'ਔਫਸੈਟ_ਕੀਮਤ', 'path': 'ਮਾਰਗ', 'screenshot': 'ਸਕ੍ਰੀਨ_ਕਲਿਪਿੰਗ', 'arguments': '전달인수', 'pixels': '화소들', 'viewer': '화면접속자', 'output': '출력결과', 'stream': 'ਸਟ੍ਰੀਮ_ਕੀਮਤ', 'cmd': '명령인수', 'name': 'ਨਾਂ', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
