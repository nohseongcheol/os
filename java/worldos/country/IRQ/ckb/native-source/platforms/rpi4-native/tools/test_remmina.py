#!/usr/bin/env python3
"""기존 گوزەر 호환 تێنووسین_خاڵ. ڕاستەکی_دەیتا 구현: ../ئامرازەکان/원격한글시험.py"""
import importlib as 가져오기
import sys as سیستەمی_کارپێکردن_نرخ
from pathlib import Path as گوزەر
سیستەمی_کارپێکردن_نرخ.path.insert(0, str(گوزەر(__file__).resolve().parents[1] / 'ئامرازەکان'))
if __name__ == '__main__':
    import runpy as بەرنامە_ئەندامی_ستاف
    بەرنامە_ئەندامی_ستاف.run_module('원격한글시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('원격한글시험')
    대응 = {'wait': '기다리기', 'typing': '글자입력', 'start': 'ڕادان', 'profile': 'پرۆفایل', 'focused': 'جەختکراو', 'serial': '직렬입출력', 'keys': '누름열', 'server': 'ڕاژەکار_نرخ', 'log': 'تۆمار_ڕزن', 'args': 'ئارگیومێنت_ڕیزی_داتا', 'deadline': '마감시각', 'data': 'دەیتا', 'candidate': '후보', 'logs': '기록들', 'kw': '이름붙인인수', 'number': '수치', 'main': 'ڕادان', 'ready': '준비완료', 'found': '찾은결과', 'guest': '커널실행', 'ROOT': '기준', 'marker': '확인표시', 'text': 'دەق', 'out': '결과자료', 'env': '환경', 'f': 'فایل_تێنووسین', 'port': '접속번호', 'offset': 'ئۆفسێت_نرخ', 'version': '판번호', 'p': '자료위치', 'selector': 'هەڵبژێرەر', 'xvfb': 'مەجازی_نیشاندان', 'display': 'پیشاندەر', 'n': '개수', 'key': '누름값', 'processes': '실행과정들', 'rootfs': '뿌리파일계층', 'xdo': '가상입력도구', 'name': 'ناو', 'window': 'پەنجەرە', 'report': 'ڕەواکردن_ڕاپۆرت', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
