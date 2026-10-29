#!/usr/bin/env python3
"""기존 راههه 호환 داخلا_هنڌ. اصلي_ڪوائف 구현: ../اوزار/예제시험.py"""
import importlib as 가져오기
import sys as آپريٽنگ_سسٽم_قدر
from pathlib import Path as راههه
آپريٽنگ_سسٽم_قدر.path.insert(0, str(راههه(__file__).resolve().parents[1] / 'اوزار'))
if __name__ == '__main__':
    import runpy as ائپ_ائپ_ڊرائر
    ائپ_ائپ_ڊرائر.run_module('예제시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('예제시험')
    대응 = {'count': '항목수', 'exact': '정확한값', 'expected_file': '예상파일', 'ftp_port': '파일전송접속번호', 'data': 'ڪوائف', 'graphics_command': '그림명령', 'main': 'هلائڻ', 'row': '행위치', 'init': '초기값', 'target': 'هدف', 'ROOT': '기준', 'text': 'متن', 'binary': 'ٻٽو', 'out': '결과자료', 'entry': 'داخلا_هنڌ', 'got': '받은수', 'port': '접속번호', 'graphics_start': 'شروع_ڊرائنگ', 'col': '열위치', 'begin': 'شروع_آف_سيٽ', 'kind': 'قسم_قدر_4b6d6445', 'selector': 'چونڊيندڙ', 'n': '개수', 'key': '누름값', 'y': '세로좌표', 'client': 'گراهڪ', 'line': 'لڪير', 'report': 'ڪارگر_رپورٽ', 'language': 'ٻولي', 'x': 'x_رطبو', 'start': 'هلائڻ', 'rgb': '빛삼원색', 'down': '누르는중', 'listing': 'اي_ميل_فهرست', 'payload': 'بنيادي_بار_ڪوائف', 'proc': 'عمل_a7054519', 'w': '너비값', 'temporary': '임시자원', 'echo': '되돌림서버항목', 'label': 'نالو_جدول', 'content': 'مواد_قدر', 'argument': '전달값', 'EchoServers': '되돌림서버', 'marker': '확인표시', 'expected': '예상결과', 'test_language': 'test_언어', 'filename': 'فائل_داخلا_نالو', 'shell': 'شيل', 'color': '색상', 'transcript': '대화기록', 'offset': 'آف_سيٽ_قدر', 'h': '높이값', 'run': 'تعميل_ڪرڻ_حڪم', 'c': 'ڪئريڪٽر_ڪوڊ', 'path': 'راههه', 'encoding': 'ڪيريڪٽرن_جو_سيٽ', 'end': 'ختم_ڪريو_آف_سيٽ', 'ftp': 'فائل_منتقلي_ڪنيڪشن', 'pixels': '화소들', 'symbol': 'نشاني_قدر', 'source': '원본자료', 'name': 'نالو', 'receive': '수신하기', 'manifest': '꾸러미명세'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
