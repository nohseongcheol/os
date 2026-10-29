#!/usr/bin/env python3
"""기존 ପଥ 호환 ଏଣ୍ଟ୍ରି_ପଏଣ୍ଟ୍. ପ୍ରକୃତ_ଡାଟା 구현: ../ଉପକରଣସମୂହ/셸시험.py"""
import importlib as 가져오기
import sys as ଅପରେଟିଂ_ସିଷ୍ଟମ_ମୂଲ୍ୟ
from pathlib import Path as ପଥ
ଅପରେଟିଂ_ସିଷ୍ଟମ_ମୂଲ୍ୟ.path.insert(0, str(ପଥ(__file__).resolve().parents[1] / 'ଉପକରଣସମୂହ'))
if __name__ == '__main__':
    import runpy as ଅନୁପ୍ରୟୋଗ_ଆପ୍ଲିକେସନ୍_ଡ୍ରୟର୍
    ଅନୁପ୍ରୟୋଗ_ଆପ୍ଲିକେସନ୍_ଡ୍ରୟର୍.run_module('셸시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('셸시험')
    대응 = {'timeout': '시간제한', 'x': 'x_ସଂଯୋଜନ', 'msg': 'ନେଟ୍_ୱାର୍କ୍_ବାର୍ତ୍ତା', 'i': '순번', 'reply': 'ପ୍ରତ୍ୟୁତ୍ତର_କରନ୍ତୁ', 'call': '호출', 'args': 'ଯୁକ୍ତି_ଆରେ', 'chunk': '조각', 'data': 'ଡାଟା', 'proc': 'ପ୍ରକ୍ରିୟା', 'long_text': '긴글', 'restored': '복원자료', 'send': 'ପଠାନ୍ତୁ', 'file': 'ଫାଇଲ', 'main': 'ଚଳାନ୍ତୁ', 'found': 'ସନ୍ଧାନ_ମାପ', 'ROOT': 'ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍', 'text': 'ପାଠ୍ଯ', 'marker': '확인표시', 'command': 'ନିର୍ଦ୍ଦେଶ', 'expected': '예상결과', 'pixel': 'ପିକ୍ସେଲ୍', 'shell': 'ଖୋଳ', 'poll': '준비살피미', 'transcript': '대화기록', 'end': 'ଶେଷ_କରନ୍ତୁ_ଅଫ୍_ସେଟ୍', 'image': 'ଚିତ୍ର', 'key': '누름값', 'y': '세로좌표', 'output': '출력결과', 'result': 'ମାପ', 'client': 'କ୍ଲାଏଣ୍ଟ', 'line': 'ରେଖା', 'stream': 'ଷ୍ଟ୍ରିମ୍_ମୂଲ୍ୟ', 'name': 'ନାମ', 'value': 'ମୂଲ୍ୟ', 'receive': '수신하기', 'report': 'ବୈଧକରଣ_ରିପୋର୍ଟ', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
