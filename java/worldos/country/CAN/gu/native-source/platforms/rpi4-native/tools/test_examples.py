#!/usr/bin/env python3
"""기존 પથ 호환 પ્રવેશ_બિંદુ. વાસ્તવિક_ડેટા 구현: ../ઉપકરણો/예제시험.py"""
import importlib as 가져오기
import sys as ઑપરેટિંગ_સિસ્ટમ_મૂલ્ય
from pathlib import Path as પથ
ઑપરેટિંગ_સિસ્ટમ_મૂલ્ય.path.insert(0, str(પથ(__file__).resolve().parents[1] / 'ઉપકરણો'))
if __name__ == '__main__':
    import runpy as એપ્લિકેશન_લૉન્ચર
    એપ્લિકેશન_લૉન્ચર.run_module('예제시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('예제시험')
    대응 = {'count': '항목수', 'exact': '정확한값', 'expected_file': '예상파일', 'ftp_port': 'ફાઇલ_સ્થાનાંતર_પોર્ટ_નંબર', 'data': 'ડેટા', 'graphics_command': 'ગ્રાફિક્સ_આદેશ', 'main': 'ચલાવો_2', 'row': 'પંક્તિ_સ્થિતિ', 'init': '초기값', 'target': 'લક્ષ્ય', 'ROOT': 'પ્રોજેક્ટ_રૂટ', 'text': 'લખાણ', 'binary': 'બાઇનરી', 'out': 'પરિમાણ_ડેટા', 'entry': 'પ્રવેશ_બિંદુ', 'got': '받은수', 'port': 'પોર્ટ_નંબર', 'graphics_start': 'પ્રારંભ_રેખાંકન', 'col': 'હરોળ_સ્થિતિ', 'begin': 'પ્રારંભ_ઑફસેટ', 'kind': 'શ્રેણી_મૂલ્ય', 'selector': 'પસંદકર્તા', 'n': '개수', 'key': '누름값', 'y': '세로좌표', 'client': 'ક્લાયંટ', 'line': 'લાઇન', 'report': 'માન્યતા_અહેવાલ', 'language': 'ભાષા', 'x': 'x_યામ', 'start': 'ચલાવો_2', 'rgb': '빛삼원색', 'down': '누르는중', 'listing': 'મોકલો_સૂચી', 'payload': 'પેલોડ_ડેટા', 'proc': 'પ્રક્રિયા', 'w': '너비값', 'temporary': '임시자원', 'echo': '되돌림서버항목', 'label': 'નામ_કોષ્ટક', 'content': 'સામગ્રી_મૂલ્ય', 'argument': '전달값', 'EchoServers': '되돌림서버', 'marker': '확인표시', 'expected': '예상결과', 'test_language': 'test_언어', 'filename': 'ફાઇલ_પ્રવેશ_નામ', 'shell': 'શેલ', 'color': '색상', 'transcript': '대화기록', 'offset': 'ઑફસેટ_મૂલ્ય', 'h': '높이값', 'run': 'અમલ_કરો_આદેશ', 'c': 'વર્ણ_કોડ', 'path': 'પથ', 'encoding': 'વર્ણ_સેટ', 'end': 'અંત_કરો_ઑફસેટ', 'ftp': 'ફાઇલ_સ્થાનાંતર_કનેક્શન', 'pixels': '화소들', 'symbol': 'પ્રતીક_મૂલ્ય', 'source': '원본자료', 'name': 'નામ', 'receive': '수신하기', 'manifest': '꾸러미명세'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
