#!/usr/bin/env python3
"""기존 راستہ_2 호환 اندراج_نقطہ. اصل_کوائف 구현: ../ٹولز/예제시험.py"""
import importlib as 가져오기
import sys as آپریٹنگ_سسٹم_قدر
from pathlib import Path as راستہ_2
آپریٹنگ_سسٹم_قدر.path.insert(0, str(راستہ_2(__file__).resolve().parents[1] / 'ٹولز'))
if __name__ == '__main__':
    import runpy as ایپ_ایپ_دراز
    ایپ_ایپ_دراز.run_module('예제시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('예제시험')
    대응 = {'count': '항목수', 'exact': '정확한값', 'expected_file': '예상파일', 'ftp_port': 'فائل_منتقلی_دہانہ_نمبر', 'data': 'کوائف', 'graphics_command': 'گرافکس_حکم', 'main': 'چلائیں', 'row': 'صف_پوزیشن_ٹھیک_کریں', 'init': '초기값', 'target': 'ہدف', 'ROOT': 'عکس_ڈالنا_روٹ', 'text': 'متن', 'binary': 'ثنائی', 'out': 'پیمائش_کوائف', 'entry': 'اندراج_نقطہ', 'got': '받은수', 'port': 'دہانہ_نمبر', 'graphics_start': 'ابتدا_ڈرائنگ', 'col': 'کالم_پوزیشن_ٹھیک_کریں', 'begin': 'ابتدا_آفسٹ', 'kind': 'زمرہ_قدر', 'selector': 'منتخب_کنندہ', 'n': '개수', 'key': '누름값', 'y': '세로좌표', 'client': 'کلائنٹ', 'line': 'اندراج_کی_سطر', 'report': 'توثیق_رپورٹ', 'language': 'زبان', 'x': 'ایکس_مربوط', 'start': 'چلائیں', 'rgb': '빛삼원색', 'down': '누르는중', 'listing': 'بھیجیں_فہرست', 'payload': 'پے_لوڈ_کوائف', 'proc': 'عمل_کاری', 'w': '너비값', 'temporary': '임시자원', 'echo': '되돌림서버항목', 'label': 'نام_جدول', 'content': 'مشمول_قدر', 'argument': '전달값', 'EchoServers': '되돌림서버', 'marker': '확인표시', 'expected': '예상결과', 'test_language': 'test_언어', 'filename': 'فائل_اندراج_نام', 'shell': 'شیل', 'color': '색상', 'transcript': '대화기록', 'offset': 'آفسٹ_قدر', 'h': '높이값', 'run': 'نفاذ_کریں_حکم', 'c': 'کریکٹر_ضابطہ', 'path': 'راستہ_2', 'encoding': 'کریکٹر_سیٹ', 'end': 'اختتام_آفسٹ', 'ftp': 'فائل_منتقلی_رابطہ', 'pixels': '화소들', 'symbol': 'علامت_قدر', 'source': '원본자료', 'name': 'نام', 'receive': '수신하기', 'manifest': '꾸러미명세'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
