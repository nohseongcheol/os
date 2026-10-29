#!/usr/bin/env python3
"""기존 ପଥ 호환 ଏଣ୍ଟ୍ରି_ପଏଣ୍ଟ୍. ପ୍ରକୃତ_ଡାଟା 구현: ../ଉପକରଣସମୂହ/파일전송시험.py"""
import importlib as 가져오기
import sys as ଅପରେଟିଂ_ସିଷ୍ଟମ_ମୂଲ୍ୟ
from pathlib import Path as ପଥ
ଅପରେଟିଂ_ସିଷ୍ଟମ_ମୂଲ୍ୟ.path.insert(0, str(ପଥ(__file__).resolve().parents[1] / 'ଉପକରଣସମୂହ'))
if __name__ == '__main__':
    import runpy as ଅନୁପ୍ରୟୋଗ_ଆପ୍ଲିକେସନ୍_ଡ୍ରୟର୍
    ଅନୁପ୍ରୟୋଗ_ଆପ୍ଲିକେସନ୍_ଡ୍ରୟର୍.run_module('파일전송시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('파일전송시험')
    대응 = {'timeout': '시간제한', 'payload': 'ପେଲୋଡ୍_ଡାଟା', 'broken': '손상자료', 'linux_example': '리눅스예제', 'chunk': '조각', 'data': 'ଡାଟା', 'proc': 'ପ୍ରକ୍ରିୟା', 'code': '명령열', 'linux': '리눅스파일', 'archive': 'ଅଭିଲେଖାଗାର', 'main': 'ଚଳାନ୍ତୁ', 'net_source': '통신원문', 'temporary': '임시자원', 'static_source': 'ସ୍ଥିର_ଉତ୍ସ', 'java_source': '자바원문', 'echo': '되돌림서버항목', 'ROOT': 'ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍', 'text': 'ପାଠ୍ଯ', 'marker': '확인표시', 'EchoFixture': '되돌림시험서버', 'command': 'ନିର୍ଦ୍ଦେଶ', 'out': 'ମାପ_ଡାଟା', 'expected': '예상결과', 'server_source': 'ସର୍ଭର୍_ଉତ୍ସ', 'shell': 'ଖୋଳ', 'upload': 'ଅପଲୋଡ୍_ଫାଇଲ୍_ଗୁଡିକ', 'transcript': '대화기록', 'port': 'ପୋର୍ଟ୍_ନମ୍ଵର୍', 'native': '자체실행파일', 'elf': '실행파일', 'server_udp_port': '서버전문접속번호', 'packed': '묶인자료', 'bridge': 'ବ୍ରିଜ୍', 'selector': 'ଚୟନକାରୀ', 'end': 'ଶେଷ_କରନ୍ତୁ_ଅଫ୍_ସେଟ୍', 'e': '보조항목', 'ftp': 'ଫାଇଲ୍_ସ୍ଥାନାନ୍ତର_ସଂଯୋଗ', 'key': '누름값', 'bytecode': '바이트코드', 'peer': 'ସମକକ୍ଷ_ମୂଲ୍ୟ', 'result': 'ମାପ', 'unchanged': '보존자료', 'line': 'ରେଖା', 'server_tcp_port': 'ସର୍ଭର୍_ଷ୍ଟ୍ରିମ୍_ପୋର୍ଟ', 'source': '원본자료', 'NetworkBridge': 'ନେଟ୍_ୱାର୍କ୍_ବ୍ରିଜ୍', 'jar': '자바꾸러미', 'receive': '수신하기', 'report': 'ବୈଧକରଣ_ରିପୋର୍ଟ'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
