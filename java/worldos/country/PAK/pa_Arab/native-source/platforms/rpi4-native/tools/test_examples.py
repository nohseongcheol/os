#!/usr/bin/env python3
"""기존 راہ 호환 داخلہ_مقام. اصلی_کوائف 구현: ../اوزار/예제시험.py"""
import importlib as 가져오기
import sys as آپریٹنگ_سسٹم_قدر
from pathlib import Path as راہ
آپریٹنگ_سسٹم_قدر.path.insert(0, str(راہ(__file__).resolve().parents[1] / 'اوزار'))
if __name__ == '__main__':
    import runpy as ایپ_عملے_دا_رکن
    ایپ_عملے_دا_رکن.run_module('예제시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('예제시험')
    대응 = {'count': '항목수', 'exact': '정확한값', 'expected_file': '예상파일', 'ftp_port': '파일전송접속번호', 'data': 'کوائف', 'graphics_command': '그림명령', 'main': 'چلاؤ', 'row': '행위치', 'init': '초기값', 'target': 'ہدف', 'ROOT': '기준', 'text': 'متن', 'binary': 'مثنی', 'out': '결과자료', 'entry': 'داخلہ_مقام', 'got': '받은수', 'port': '접속번호', 'graphics_start': 'مکھ_ڈرائنگ', 'col': '열위치', 'begin': 'مکھ_آف_سیٹ', 'kind': 'زمرہ_قدر', 'selector': 'منتخب_کرنڑ_آلا', 'n': '개수', 'key': '누름값', 'y': '세로좌표', 'client': 'گاہک', 'line': 'لائن', 'report': 'جواز_دہی_رپورٹ', 'language': 'زبان', 'x': 'x_محدد', 'start': 'چلاؤ', 'rgb': '빛삼원색', 'down': '누르는중', 'listing': 'بھیجو_فرست', 'payload': 'پے_لوڈ_کوائف', 'proc': 'عمل', 'w': '너비값', 'temporary': '임시자원', 'echo': '되돌림서버항목', 'label': 'ناں_جدول', 'content': 'اجزاء_قدر', 'argument': '전달값', 'EchoServers': '되돌림서버', 'marker': '확인표시', 'expected': '예상결과', 'test_language': 'test_언어', 'filename': 'فائل_داخلہ_ناں', 'shell': 'شیل', 'color': '색상', 'transcript': '대화기록', 'offset': 'آف_سیٹ_قدر', 'h': '높이값', 'run': 'نفاذ_کرو_حکم', 'c': 'کیریکٹر_کوڈ', 'path': 'راہ', 'encoding': 'کریکٹر_سیٹ', 'end': 'ختم_کرو_آف_سیٹ', 'ftp': 'فائل_منتقلی_کنکشن', 'pixels': '화소들', 'symbol': 'علامت_قدر', 'source': '원본자료', 'name': 'ناں', 'receive': '수신하기', 'manifest': '꾸러미명세'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
