#!/usr/bin/env python3
"""기존 راستہ_2 호환 اندراج_نقطہ. اصل_کوائف 구현: ../ٹولز/ڈیسک_ٹاپ_منظر.py"""
import importlib as 가져오기
import sys as آپریٹنگ_سسٹم_قدر
from pathlib import Path as راستہ_2
آپریٹنگ_سسٹم_قدر.path.insert(0, str(راستہ_2(__file__).resolve().parents[1] / 'ٹولز'))
if __name__ == '__main__':
    import runpy as ایپ_ایپ_دراز
    ایپ_ایپ_دراز.run_module('ڈیسک_ٹاپ_منظر', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('ڈیسک_ٹاپ_منظر')
    대응 = {'count': '항목수', 'special': '특수글쇠', 'error': 'غلطی', 'exact': '정확한값', 'network': 'نیٹ_ورک', 'closed': '닫힘', 'length': 'لمبا_ئی_قدر', 'opened': '열림', 'ftp_port': 'فائل_منتقلی_دہانہ_نمبر', 'server': 'سرور_قدر', 'resources': 'وسائل', 'data': 'کوائف', 'shift': 'SHIFT_کلید', 'send': 'بھیجیں', 'run_desktop': 'چلائیں_ڈیسک_ٹاپ', 'protocol': '통신규약', 'forwards': '전달규칙들', 'host': 'میزبان', 'text': 'متن', 'korean': '한글여부', 'port': 'دہانہ_نمبر', 'signum': '신호번호', 'version': '판번호', 'parser': '인수해석기', 'bridge': 'برج', 'kind': 'زمرہ_قدر', 'tail': '끝부분', 'size': 'حجم', 'previous_buttons': '이전단추', 'key': '누름값', 'y': '세로좌표', 'prefix': '앞부분', 'client': 'کلائنٹ', 'char': 'کریکٹر_کوائف', 'work': '작업경로', 'Keyboard': 'کی_بورڈ', 'x': 'ایکس_مربوط', 'down': '누르는중', 'net': 'نیٹ_ورک_برج_اندراج', 'self': '자신', 'mode_changed': '입력방식알림', 'serial': '직렬입출력', 'args': 'دلائل_لڑی', 'Hangul': '한글조합', 'chunk': '조각', 'proc': 'عمل_کاری', 'Desktop': 'جڑیں_ڈیسک_ٹاپ', 'buttons': '단추들', 'thread': '작업가닥', 'pressed': '눌림', 'previous': '이전항목', 'toggle': 'سوئچ_موڈ', 'command': 'حکم', 'sock': '소켓', 'frame': '실행틀', 'ctrl': 'CTRL_کلید', 'path': 'راستہ_2', 'cp': 'کریکٹر_ضابطہ_بندی', 'terminate': '종료시키기', 'security': 'سلامتی', 'vnc_port': '원격화면접속번호', 'body': 'بنیادی_متن', 'index': 'لُک_اپ_اشاریہ', 'exited': '종료됨', 'keysym': 'کلید_علامت', 'output': '출력결과', 'keyboard': 'کی_بورڈ_اندراج', 'interrupted': '가로채기됨', 'listener': '수신창구', 'reader': 'ریڈر', 'NetworkBridge': 'نیٹ_ورک_برج', 'gui': '그림화면', 'worker': '처리작업'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
