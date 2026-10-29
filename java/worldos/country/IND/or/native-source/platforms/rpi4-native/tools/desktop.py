#!/usr/bin/env python3
"""기존 ପଥ 호환 ଏଣ୍ଟ୍ରି_ପଏଣ୍ଟ୍. ପ୍ରକୃତ_ଡାଟା 구현: ../ଉପକରଣସମୂହ/ଡେସ୍କଟପ୍_ଭିୟୁ.py"""
import importlib as 가져오기
import sys as ଅପରେଟିଂ_ସିଷ୍ଟମ_ମୂଲ୍ୟ
from pathlib import Path as ପଥ
ଅପରେଟିଂ_ସିଷ୍ଟମ_ମୂଲ୍ୟ.path.insert(0, str(ପଥ(__file__).resolve().parents[1] / 'ଉପକରଣସମୂହ'))
if __name__ == '__main__':
    import runpy as ଅନୁପ୍ରୟୋଗ_ଆପ୍ଲିକେସନ୍_ଡ୍ରୟର୍
    ଅନୁପ୍ରୟୋଗ_ଆପ୍ଲିକେସନ୍_ଡ୍ରୟର୍.run_module('ଡେସ୍କଟପ୍_ଭିୟୁ', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('ଡେସ୍କଟପ୍_ଭିୟୁ')
    대응 = {'count': '항목수', 'special': '특수글쇠', 'error': 'ତ୍ରୁଟି', 'exact': '정확한값', 'network': 'ନେଟ୍_ୱାର୍କ୍', 'closed': '닫힘', 'length': 'ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ', 'opened': '열림', 'ftp_port': 'ଫାଇଲ୍_ସ୍ଥାନାନ୍ତର_ପୋର୍ଟ୍_ନମ୍ଵର୍', 'server': 'ସର୍ଭର୍_ମୂଲ୍ୟ', 'resources': 'ସମ୍ପଦ', 'data': 'ଡାଟା', 'shift': 'SHIFT_କୀ', 'send': 'ପଠାନ୍ତୁ', 'run_desktop': 'ରନ୍_ଡେସ୍କଟପ୍', 'protocol': '통신규약', 'forwards': '전달규칙들', 'host': 'ଆୟୋଜକ', 'text': 'ପାଠ୍ଯ', 'korean': '한글여부', 'port': 'ପୋର୍ଟ୍_ନମ୍ଵର୍', 'signum': '신호번호', 'version': '판번호', 'parser': '인수해석기', 'bridge': 'ବ୍ରିଜ୍', 'kind': 'ବର୍ଗ_ମୂଲ୍ୟ', 'tail': '끝부분', 'size': 'ଆକାର', 'previous_buttons': '이전단추', 'key': '누름값', 'y': '세로좌표', 'prefix': '앞부분', 'client': 'କ୍ଲାଏଣ୍ଟ', 'char': 'ବର୍ଣ୍ଣ_ଡାଟା', 'work': '작업경로', 'Keyboard': 'କୀବୋର୍ଡ୍', 'x': 'x_ସଂଯୋଜନ', 'down': '누르는중', 'net': 'ନେଟ୍_ୱାର୍କ୍_ବ୍ରିଜ୍_ଏଣ୍ଟ୍ରି', 'self': '자신', 'mode_changed': '입력방식알림', 'serial': '직렬입출력', 'args': 'ଯୁକ୍ତି_ଆରେ', 'Hangul': '한글조합', 'chunk': '조각', 'proc': 'ପ୍ରକ୍ରିୟା', 'Desktop': 'ସଂଯୋଗ_ଡେସ୍କଟପ୍', 'buttons': '단추들', 'thread': '작업가닥', 'pressed': '눌림', 'previous': '이전항목', 'toggle': 'ସୁଇଚ୍_ମୋଡ୍', 'command': 'ନିର୍ଦ୍ଦେଶ', 'sock': '소켓', 'frame': '실행틀', 'ctrl': 'CTRL_କୀ', 'path': 'ପଥ', 'cp': 'ବର୍ଣ୍ଣ_ଏନକୋଡିଂ', 'terminate': '종료시키기', 'security': 'ନିରାପତ୍ତା', 'vnc_port': '원격화면접속번호', 'body': 'ମୂଳ_ପାଠ', 'index': 'ଦୃଷ୍ଟିପାତ_ଅନୁକ୍ରମଣିକା', 'exited': '종료됨', 'keysym': 'କୀ_ସଙ୍କେତ', 'output': '출력결과', 'keyboard': 'କୀବୋର୍ଡ୍_ଏଣ୍ଟ୍ରି', 'interrupted': '가로채기됨', 'listener': '수신창구', 'reader': 'ପାଠକ', 'NetworkBridge': 'ନେଟ୍_ୱାର୍କ୍_ବ୍ରିଜ୍', 'gui': '그림화면', 'worker': '처리작업'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
