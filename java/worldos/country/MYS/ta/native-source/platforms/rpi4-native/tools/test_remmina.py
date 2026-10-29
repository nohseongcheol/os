#!/usr/bin/env python3
"""기존 பாதை_2 호환 நுழைவுப்_புள்ளி. அசல்_தரவு 구현: ../கருவிகள்/원격한글시험.py"""
import importlib as 가져오기
import sys as இயக்க_முறைமை_மதிப்பு
from pathlib import Path as பாதை_2
இயக்க_முறைமை_மதிப்பு.path.insert(0, str(பாதை_2(__file__).resolve().parents[1] / 'கருவிகள்'))
if __name__ == '__main__':
    import runpy as நிரல்_துவக்குநர்
    நிரல்_துவக்குநர்.run_module('원격한글시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('원격한글시험')
    대응 = {'wait': '기다리기', 'typing': '글자입력', 'start': 'செயல்படுத்துக', 'profile': 'குறிப்பு', 'focused': 'ஃபோகஸ்டு', 'serial': '직렬입출력', 'keys': '누름열', 'server': 'சேவையகம்_மதிப்பு', 'log': 'பதிவு_பதிவு', 'args': 'மதிப்புரு_கோவை', 'deadline': '마감시각', 'data': 'தரவு', 'candidate': '후보', 'logs': '기록들', 'kw': '이름붙인인수', 'number': '수치', 'main': 'செயல்படுத்துக', 'ready': '준비완료', 'found': 'தேடு_அளவிடக்கூடியது', 'guest': 'விருந்தினர்', 'ROOT': 'திட்டப்பணி_மூலம்', 'marker': '확인표시', 'text': 'உரை', 'out': 'அளவிடக்கூடியது_தரவு', 'env': '환경', 'f': 'கோப்பு_உள்ளீடு', 'port': 'முனைய_எண்', 'offset': 'ஆஃப்செட்_மதிப்பு', 'version': 'பதிப்புரு_எண்', 'p': 'தரவு_நிலை', 'selector': 'தேர்வி', 'xvfb': 'தோற்றநிலை_காட்சி', 'display': 'காட்சி', 'n': '개수', 'key': '누름값', 'processes': '실행과정들', 'rootfs': '뿌리파일계층', 'xdo': '가상입력도구', 'name': 'பெயர்', 'window': 'சாளரம்', 'report': 'செல்லுபடியாக்கம்_அறிக்கை', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
