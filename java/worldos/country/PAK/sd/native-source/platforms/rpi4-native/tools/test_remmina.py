#!/usr/bin/env python3
"""기존 راههه 호환 داخلا_هنڌ. اصلي_ڪوائف 구현: ../اوزار/원격한글시험.py"""
import importlib as 가져오기
import sys as آپريٽنگ_سسٽم_قدر
from pathlib import Path as راههه
آپريٽنگ_سسٽم_قدر.path.insert(0, str(راههه(__file__).resolve().parents[1] / 'اوزار'))
if __name__ == '__main__':
    import runpy as ائپ_ائپ_ڊرائر
    ائپ_ائپ_ڊرائر.run_module('원격한글시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('원격한글시험')
    대응 = {'wait': '기다리기', 'typing': '글자입력', 'start': 'هلائڻ', 'profile': 'پروفائيل', 'focused': 'فوڪسڊ', 'serial': '직렬입출력', 'keys': '누름열', 'server': 'سرور_قدر', 'log': 'لاگ_صف', 'args': 'دليل_ترتيب', 'deadline': '마감시각', 'data': 'ڪوائف', 'candidate': '후보', 'logs': '기록들', 'kw': '이름붙인인수', 'number': '수치', 'main': 'هلائڻ', 'ready': '준비완료', 'found': '찾은결과', 'guest': '커널실행', 'ROOT': '기준', 'marker': '확인표시', 'text': 'متن', 'out': '결과자료', 'env': '환경', 'f': 'فائل_داخلا', 'port': '접속번호', 'offset': 'آف_سيٽ_قدر', 'version': '판번호', 'p': '자료위치', 'selector': 'چونڊيندڙ', 'xvfb': 'مجازي_ڊسپلي', 'display': 'ڊسپلي', 'n': '개수', 'key': '누름값', 'processes': '실행과정들', 'rootfs': '뿌리파일계층', 'xdo': '가상입력도구', 'name': 'نالو', 'window': 'دري', 'report': 'ڪارگر_رپورٽ', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
