#!/usr/bin/env python3
"""기존 ପଥ 호환 ଏଣ୍ଟ୍ରି_ପଏଣ୍ଟ୍. ପ୍ରକୃତ_ଡାଟା 구현: ../ଉପକରଣସମୂହ/원격한글시험.py"""
import importlib as 가져오기
import sys as ଅପରେଟିଂ_ସିଷ୍ଟମ_ମୂଲ୍ୟ
from pathlib import Path as ପଥ
ଅପରେଟିଂ_ସିଷ୍ଟମ_ମୂଲ୍ୟ.path.insert(0, str(ପଥ(__file__).resolve().parents[1] / 'ଉପକରଣସମୂହ'))
if __name__ == '__main__':
    import runpy as ଅନୁପ୍ରୟୋଗ_ଆପ୍ଲିକେସନ୍_ଡ୍ରୟର୍
    ଅନୁପ୍ରୟୋଗ_ଆପ୍ଲିକେସନ୍_ଡ୍ରୟର୍.run_module('원격한글시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('원격한글시험')
    대응 = {'wait': '기다리기', 'typing': '글자입력', 'start': 'ଚଳାନ୍ତୁ', 'profile': 'ପ୍ରୋଫାଇଲ୍', 'focused': 'କେନ୍ଦ୍ରିକ_f7e69dab', 'serial': '직렬입출력', 'keys': '누름열', 'server': 'ସର୍ଭର୍_ମୂଲ୍ୟ', 'log': 'ଲଗ୍_ଧାଡ଼ି', 'args': 'ଯୁକ୍ତି_ଆରେ', 'deadline': '마감시각', 'data': 'ଡାଟା', 'candidate': '후보', 'logs': '기록들', 'kw': '이름붙인인수', 'number': '수치', 'main': 'ଚଳାନ୍ତୁ', 'ready': '준비완료', 'found': 'ସନ୍ଧାନ_ମାପ', 'guest': 'ଅତିଥି', 'ROOT': 'ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍', 'marker': '확인표시', 'text': 'ପାଠ୍ଯ', 'out': 'ମାପ_ଡାଟା', 'env': '환경', 'f': 'ଫାଇଲ୍_ଏଣ୍ଟ୍ରି', 'port': 'ପୋର୍ଟ୍_ନମ୍ଵର୍', 'offset': 'ଅଫ୍_ସେଟ୍_ମୂଲ୍ୟ', 'version': '판번호', 'p': 'ଡାଟା_ସ୍ଥିତି', 'selector': 'ଚୟନକାରୀ', 'xvfb': 'ବାସ୍ତବ_ଦେଖାଇବା', 'display': 'ଦେଖାଇବା', 'n': '개수', 'key': '누름값', 'processes': '실행과정들', 'rootfs': '뿌리파일계층', 'xdo': '가상입력도구', 'name': 'ନାମ', 'window': 'ଓ୍ୱିଣ୍ଡୋ', 'report': 'ବୈଧକରଣ_ରିପୋର୍ଟ', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
