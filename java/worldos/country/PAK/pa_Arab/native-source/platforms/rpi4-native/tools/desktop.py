#!/usr/bin/env python3
"""기존 راہ 호환 داخلہ_مقام. اصلی_کوائف 구현: ../اوزار/ڈیسک_ٹاپ_منظر.py"""
import importlib as 가져오기
import sys as آپریٹنگ_سسٹم_قدر
from pathlib import Path as راہ
آپریٹنگ_سسٹم_قدر.path.insert(0, str(راہ(__file__).resolve().parents[1] / 'اوزار'))
if __name__ == '__main__':
    import runpy as ایپ_عملے_دا_رکن
    ایپ_عملے_دا_رکن.run_module('ڈیسک_ٹاپ_منظر', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('ڈیسک_ٹاپ_منظر')
    대응 = {'count': '항목수', 'special': '특수글쇠', 'error': 'نقص', 'exact': '정확한값', 'network': 'نیٹ_ورک', 'closed': '닫힘', 'length': 'لمبائی_قدر', 'opened': '열림', 'ftp_port': '파일전송접속번호', 'server': 'سرور_قدر', 'resources': 'وسائل', 'data': 'کوائف', 'shift': 'SHIFT_کلید', 'send': 'بھیجو', 'run_desktop': 'چلاؤ_ڈیسک_ٹاپ', 'protocol': '통신규약', 'forwards': '전달규칙들', 'host': 'مہمان_b78e430d', 'text': 'متن', 'korean': '한글여부', 'port': '접속번호', 'signum': '신호번호', 'version': '판번호', 'parser': '인수해석기', 'bridge': 'برج', 'kind': 'زمرہ_قدر', 'tail': '끝부분', 'size': 'سائز', 'previous_buttons': '이전단추', 'key': '누름값', 'y': '세로좌표', 'prefix': '앞부분', 'client': 'گاہک', 'char': 'کریکٹر_کوائف', 'work': '작업경로', 'Keyboard': 'کلیدی_بورڈ', 'x': 'x_محدد', 'down': '누르는중', 'net': 'نیٹ_ورک_برج_داخلہ', 'self': '자신', 'mode_changed': '입력방식알림', 'serial': '직렬입출력', 'args': 'دلیل_ایرے', 'Hangul': '한글조합', 'chunk': '조각', 'proc': 'عمل', 'Desktop': 'جڑو_ڈیسک_ٹاپ', 'buttons': '단추들', 'thread': '작업가닥', 'pressed': '눌림', 'previous': '이전항목', 'toggle': 'سوئچ_کرو_موڈ', 'command': 'حکم', 'sock': '소켓', 'frame': '실행틀', 'ctrl': 'کنٹرول_کلید', 'path': 'راہ', 'cp': 'کریکٹر_ضابطہ_ربائی', 'terminate': '종료시키기', 'security': 'سلامتی', 'vnc_port': '원격화면접속번호', 'body': 'متن_دا_ڈھانچہ', 'index': '색인', 'exited': '종료됨', 'keysym': 'کلید_علامت', 'output': '출력결과', 'keyboard': 'کلیدی_بورڈ_داخلہ', 'interrupted': '가로채기됨', 'listener': '수신창구', 'reader': 'پڑھن_والا', 'NetworkBridge': 'نیٹ_ورک_برج', 'gui': '그림화면', 'worker': '처리작업'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
