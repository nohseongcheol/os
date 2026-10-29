#!/usr/bin/env python3
"""기존 ପଥ 호환 ଏଣ୍ଟ୍ରି_ପଏଣ୍ଟ୍. ପ୍ରକୃତ_ଡାଟା 구현: ../ଉପକରଣସମୂହ/부팅시험.py"""
import importlib as 가져오기
import sys as ଅପରେଟିଂ_ସିଷ୍ଟମ_ମୂଲ୍ୟ
from pathlib import Path as ପଥ
ଅପରେଟିଂ_ସିଷ୍ଟମ_ମୂଲ୍ୟ.path.insert(0, str(ପଥ(__file__).resolve().parents[1] / 'ଉପକରଣସମୂହ'))
if __name__ == '__main__':
    import runpy as ଅନୁପ୍ରୟୋଗ_ଆପ୍ଲିକେସନ୍_ଡ୍ରୟର୍
    ଅନୁପ୍ରୟୋଗ_ଆପ୍ଲିକେସନ୍_ଡ୍ରୟର୍.run_module('부팅시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('부팅시험')
    대응 = {'timeout': '시간제한', 'response': '응답자료', 'msg': 'ନେଟ୍_ୱାର୍କ୍_ବାର୍ତ୍ତା', 'exact': '정확한값', 'markers': '확인표시들', 'i': '순번', 'match': '일치', 'execute': 'ନିଷ୍ପାଦନ_କରନ୍ତୁ', 'cancel': 'ବାତିଲ୍_ସଂଚାଳନ', 'cmd_byte': 'ନିର୍ଦ୍ଦେଶ_ବାଇଟ୍', 'reply': 'ପ୍ରତ୍ୟୁତ୍ତର_କରନ୍ତୁ', 'points': '지점들', 'server': 'ସର୍ଭର୍_ମୂଲ୍ୟ', 'data': 'ଡାଟା', 'prompt': 'ତୁରନ୍ତ', 'enter': 'ଏଣ୍ଟର୍_କରନ୍ତୁ', 'imported': '들여온파일', 'send': 'ପଠାନ୍ତୁ', 'main': 'ଚଳାନ୍ତୁ', 'ROOT': 'ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍', 'text': 'ପାଠ୍ଯ', 'first_gui': '첫화면', 'pixel': 'ପିକ୍ସେଲ୍', 'java_class': '자바클래스', 'upload': 'ଅପଲୋଡ୍_ଫାଇଲ୍_ଗୁଡିକ', 'pixels_file': 'ପିକ୍ସେଲ୍_ଫାଇଲ୍', 'pixels_data': 'ପିକ୍ସେଲ୍_ଡାଟା', 'edit': 'ସଂପାଦନା_ମୂଲ୍ୟ', 'receive_until': '표시까지받기', 'selector': 'ଚୟନକାରୀ', 'size': 'ଆକାର', 'qmp_path': '모의제어경로', 'key': '누름값', 'second_gui': '둘째화면', 'y': '세로좌표', 'result': 'ମାପ', 'samples': '예제들', 'client': 'କ୍ଲାଏଣ୍ଟ', 'line': 'ରେଖା', 'report': 'ବୈଧକରଣ_ରିପୋର୍ଟ', 'work': '작업경로', 'x': 'x_ସଂଯୋଜନ', 'python_checks': '파이썬검사', 'download': 'ଡାଉନ୍_ଲୋଡ଼', 'greeting': '인사', 'dims': '치수', 'chunk': '조각', 'deadline': '마감시각', 'proc': 'ପ୍ରକ୍ରିୟା', 'content': 'ବିଷୟ_ମୂଲ୍ୟ', 'block': 'ଡାଟା_ଅବରୋଧ_କରିବା', 'marker': '확인표시', 'command': 'ନିର୍ଦ୍ଦେଶ', 'expected': '예상결과', 'shell': 'ଖୋଳ', 'drawing': 'ଅଙ୍କନ_ପଥ', 'f': 'ଫାଇଲ୍_ଏଣ୍ଟ୍ରି', 'transcript': '대화기록', 'offset': 'ଅଫ୍_ସେଟ୍_ମୂଲ୍ୟ', 'path': 'ପଥ', 'screenshot': 'ସ୍କ୍ରିନ୍_କ୍ଲିପିଂ', 'arguments': '전달인수', 'pixels': '화소들', 'viewer': '화면접속자', 'output': '출력결과', 'stream': 'ଷ୍ଟ୍ରିମ୍_ମୂଲ୍ୟ', 'cmd': '명령인수', 'name': 'ନାମ', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
