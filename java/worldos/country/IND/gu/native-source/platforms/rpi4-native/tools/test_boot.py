#!/usr/bin/env python3
"""기존 પથ 호환 પ્રવેશ_બિંદુ. વાસ્તવિક_ડેટા 구현: ../ઉપકરણો/부팅시험.py"""
import importlib as 가져오기
import sys as ઑપરેટિંગ_સિસ્ટમ_મૂલ્ય
from pathlib import Path as પથ
ઑપરેટિંગ_સિસ્ટમ_મૂલ્ય.path.insert(0, str(પથ(__file__).resolve().parents[1] / 'ઉપકરણો'))
if __name__ == '__main__':
    import runpy as એપ્લિકેશન_લૉન્ચર
    એપ્લિકેશન_લૉન્ચર.run_module('부팅시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('부팅시험')
    대응 = {'timeout': '시간제한', 'response': 'પ્રતિસાદ', 'msg': 'નેટવર્ક_સંદેશ', 'exact': '정확한값', 'markers': '확인표시들', 'i': '순번', 'match': '일치', 'execute': 'ચલાવો', 'cancel': 'રદ_કરો_ઑપરેશન', 'cmd_byte': 'આદેશ_બાઇટ', 'reply': 'જવાબ', 'points': '지점들', 'server': 'સર્વર_મૂલ્ય', 'data': 'ડેટા', 'prompt': 'સંકેત', 'enter': 'દાખલ_કરો_851ea840', 'imported': '들여온파일', 'send': 'મોકલો', 'main': 'ચલાવો_2', 'ROOT': 'પ્રોજેક્ટ_રૂટ', 'text': 'લખાણ', 'first_gui': '첫화면', 'pixel': 'પેલ', 'java_class': '자바클래스', 'upload': 'અપલોડ_કરો_ફાઇલો', 'pixels_file': 'પેલ_ફાઇલ', 'pixels_data': 'પેલ_ડેટા', 'edit': 'સંપાદન_મૂલ્ય', 'receive_until': '표시까지받기', 'selector': 'પસંદકર્તા', 'size': 'માપ', 'qmp_path': '모의제어경로', 'key': '누름값', 'second_gui': '둘째화면', 'y': '세로좌표', 'result': 'પરિમાણ', 'samples': '예제들', 'client': 'ક્લાયંટ', 'line': 'લાઇન', 'report': 'માન્યતા_અહેવાલ', 'work': '작업경로', 'x': 'x_યામ', 'python_checks': '파이썬검사', 'download': 'ડાઉનલોડ', 'greeting': '인사', 'dims': '치수', 'chunk': '조각', 'deadline': '마감시각', 'proc': 'પ્રક્રિયા', 'content': 'સામગ્રી_મૂલ્ય', 'block': 'ડેટા_અવરોધિત_કરો', 'marker': '확인표시', 'command': 'આદેશ', 'expected': '예상결과', 'shell': 'શેલ', 'drawing': 'રેખાંકન_પાથ', 'f': 'ફાઇલ_પ્રવેશ', 'transcript': '대화기록', 'offset': 'ઑફસેટ_મૂલ્ય', 'path': 'પથ', 'screenshot': 'સ્ક્રીન_ક્લિપિંગ', 'arguments': '전달인수', 'pixels': '화소들', 'viewer': '화면접속자', 'output': '출력결과', 'stream': 'સ્ટ્રીમ_મૂલ્ય', 'cmd': '명령인수', 'name': 'નામ', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
