#!/usr/bin/env python3
"""기존 ପଥ 호환 ଏଣ୍ଟ୍ରି_ପଏଣ୍ଟ୍. ପ୍ରକୃତ_ଡାଟା 구현: ../ଉପକରଣସମୂହ/예제시험.py"""
import importlib as 가져오기
import sys as ଅପରେଟିଂ_ସିଷ୍ଟମ_ମୂଲ୍ୟ
from pathlib import Path as ପଥ
ଅପରେଟିଂ_ସିଷ୍ଟମ_ମୂଲ୍ୟ.path.insert(0, str(ପଥ(__file__).resolve().parents[1] / 'ଉପକରଣସମୂହ'))
if __name__ == '__main__':
    import runpy as ଅନୁପ୍ରୟୋଗ_ଆପ୍ଲିକେସନ୍_ଡ୍ରୟର୍
    ଅନୁପ୍ରୟୋଗ_ଆପ୍ଲିକେସନ୍_ଡ୍ରୟର୍.run_module('예제시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('예제시험')
    대응 = {'count': '항목수', 'exact': '정확한값', 'expected_file': '예상파일', 'ftp_port': 'ଫାଇଲ୍_ସ୍ଥାନାନ୍ତର_ପୋର୍ଟ୍_ନମ୍ଵର୍', 'data': 'ଡାଟା', 'graphics_command': 'ଗ୍ରାଫିକ୍ସ_ନିର୍ଦ୍ଦେଶ', 'main': 'ଚଳାନ୍ତୁ', 'row': 'ଧାଡ଼ି_ସ୍ଥିତି', 'init': '초기값', 'target': 'ଲକ୍ଷ୍ୟସ୍ଥଳ', 'ROOT': 'ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍', 'text': 'ପାଠ୍ଯ', 'binary': 'ବାଇନାରୀ', 'out': 'ମାପ_ଡାଟା', 'entry': 'ଏଣ୍ଟ୍ରି_ପଏଣ୍ଟ୍', 'got': '받은수', 'port': 'ପୋର୍ଟ୍_ନମ୍ଵର୍', 'graphics_start': 'ଆରମ୍ଭ_ଅଙ୍କନ', 'col': 'ସ୍ତମ୍ଭ_ସ୍ଥିତି', 'begin': 'ଆରମ୍ଭ_ଅଫ୍_ସେଟ୍', 'kind': 'ବର୍ଗ_ମୂଲ୍ୟ', 'selector': 'ଚୟନକାରୀ', 'n': '개수', 'key': '누름값', 'y': '세로좌표', 'client': 'କ୍ଲାଏଣ୍ଟ', 'line': 'ରେଖା', 'report': 'ବୈଧକରଣ_ରିପୋର୍ଟ', 'language': 'ଭାଷା', 'x': 'x_ସଂଯୋଜନ', 'start': 'ଚଳାନ୍ତୁ', 'rgb': '빛삼원색', 'down': '누르는중', 'listing': 'ପଠାନ୍ତୁ_ତାଲିକା', 'payload': 'ପେଲୋଡ୍_ଡାଟା', 'proc': 'ପ୍ରକ୍ରିୟା', 'w': '너비값', 'temporary': '임시자원', 'echo': '되돌림서버항목', 'label': 'ନାମ_ସାରଣୀ', 'content': 'ବିଷୟ_ମୂଲ୍ୟ', 'argument': '전달값', 'EchoServers': '되돌림서버', 'marker': '확인표시', 'expected': '예상결과', 'test_language': 'test_언어', 'filename': 'ଫାଇଲ୍_ଏଣ୍ଟ୍ରି_ନାମ', 'shell': 'ଖୋଳ', 'color': '색상', 'transcript': '대화기록', 'offset': 'ଅଫ୍_ସେଟ୍_ମୂଲ୍ୟ', 'h': '높이값', 'run': 'ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ', 'c': 'ବର୍ଣ୍ଣ_କୋଡ଼୍', 'path': 'ପଥ', 'encoding': 'ବର୍ଣ୍ଣ_ସେଟ୍', 'end': 'ଶେଷ_କରନ୍ତୁ_ଅଫ୍_ସେଟ୍', 'ftp': 'ଫାଇଲ୍_ସ୍ଥାନାନ୍ତର_ସଂଯୋଗ', 'pixels': '화소들', 'symbol': 'ସଙ୍କେତ_ମୂଲ୍ୟ', 'source': '원본자료', 'name': 'ନାମ', 'receive': '수신하기', 'manifest': '꾸러미명세'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
