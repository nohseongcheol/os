#!/usr/bin/env python3
"""기존 گوزەر 호환 تێنووسین_خاڵ. ڕاستەکی_دەیتا 구현: ../ئامرازەکان/예제시험.py"""
import importlib as 가져오기
import sys as سیستەمی_کارپێکردن_نرخ
from pathlib import Path as گوزەر
سیستەمی_کارپێکردن_نرخ.path.insert(0, str(گوزەر(__file__).resolve().parents[1] / 'ئامرازەکان'))
if __name__ == '__main__':
    import runpy as بەرنامە_ئەندامی_ستاف
    بەرنامە_ئەندامی_ستاف.run_module('예제시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('예제시험')
    대응 = {'count': '항목수', 'exact': '정확한값', 'expected_file': '예상파일', 'ftp_port': '파일전송접속번호', 'data': 'دەیتا', 'graphics_command': '그림명령', 'main': 'ڕادان', 'row': '행위치', 'init': '초기값', 'target': 'مەبەست', 'ROOT': '기준', 'text': 'دەق', 'binary': 'دوانەیی', 'out': '결과자료', 'entry': 'تێنووسین_خاڵ', 'got': '받은수', 'port': '접속번호', 'graphics_start': 'دەستپێك_نگار', 'col': '열위치', 'begin': 'دەستپێك_ئۆفسێت', 'kind': 'پۆل_نرخ', 'selector': 'هەڵبژێرەر', 'n': '개수', 'key': '누름값', 'y': '세로좌표', 'client': 'کلایەنت', 'line': 'دێڕ', 'report': 'ڕەواکردن_ڕاپۆرت', 'language': 'زمان', 'x': 'پۆوتانی_x', 'start': 'ڕادان', 'rgb': '빛삼원색', 'down': '누르는중', 'listing': 'ناردن_لیست', 'payload': 'بارگەى_كرێ_دەیتا', 'proc': 'پرۆسە', 'w': '너비값', 'temporary': '임시자원', 'echo': '되돌림서버항목', 'label': 'ناو_خشتە', 'content': 'ناوەرۆک_نرخ', 'argument': '전달값', 'EchoServers': '되돌림서버', 'marker': '확인표시', 'expected': '예상결과', 'test_language': 'test_언어', 'filename': 'فایل_تێنووسین_ناو', 'shell': 'توێکڵ', 'color': '색상', 'transcript': '대화기록', 'offset': 'ئۆفسێت_نرخ', 'h': '높이값', 'run': 'جێبەجێکردن_فەرمان', 'c': 'کۆدی_نووسە', 'path': 'گوزەر', 'encoding': 'کۆمەڵە_نووسە', 'end': 'دوایی_کردن_ئۆفسێت', 'ftp': 'فایل_گواستنەوە_گرێدان', 'pixels': '화소들', 'symbol': 'سیمبۆل_نرخ', 'source': '원본자료', 'name': 'ناو', 'receive': '수신하기', 'manifest': '꾸러미명세'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
