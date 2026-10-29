#!/usr/bin/env python3
"""기존 ପଥ 호환 ଏଣ୍ଟ୍ରି_ପଏଣ୍ଟ୍. ପ୍ରକୃତ_ଡାଟା 구현: ../ଉପକରଣସମୂହ/ନିର୍ବାହ_କରିବା_ଫାଇଲ୍.py"""
import importlib as 가져오기
import sys as ଅପରେଟିଂ_ସିଷ୍ଟମ_ମୂଲ୍ୟ
from pathlib import Path as ପଥ
ଅପରେଟିଂ_ସିଷ୍ଟମ_ମୂଲ୍ୟ.path.insert(0, str(ପଥ(__file__).resolve().parents[1] / 'ଉପକରଣସମୂହ'))
if __name__ == '__main__':
    import runpy as ଅନୁପ୍ରୟୋଗ_ଆପ୍ଲିକେସନ୍_ଡ୍ରୟର୍
    ଅନୁପ୍ରୟୋଗ_ଆପ୍ଲିକେସନ୍_ଡ୍ରୟର୍.run_module('ନିର୍ବାହ_କରିବା_ଫାଇଲ୍', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('ନିର୍ବାହ_କରିବା_ଫାଇଲ୍')
    대응 = {'timeout': '시간제한', 's': 'ଷ୍ଟ୍ରିଂ_ଡାଟା', 'i': '순번', 'match': '일치', 'files': 'ଫାଇଲ୍_ତାଲିକା', 'program': 'ଅନୁପ୍ରୟୋଗ', 'executable': '실행가능파일', 'args': 'ଯୁକ୍ତି_ଆରେ', 'chunk': '조각', 'data': 'ଡାଟା', 'proc': 'ପ୍ରକ୍ରିୟା', 'send': 'ପଠାନ୍ତୁ', 'main': 'ଚଳାନ୍ତୁ', 'marker': '확인표시', 'command': 'ନିର୍ଦ୍ଦେଶ', 'include': '포함항목', 'dumped': '갈무리자료', 'run': 'ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ', 'p': 'ଡାଟା_ସ୍ଥିତି', 'parser': '인수해석기', 'options': 'ବିକଳ୍ପ_ସମୂହ', 'kind': 'ବର୍ଗ_ମୂଲ୍ୟ', 'selector': 'ଚୟନକାରୀ', 'upload_data': 'ଅପଲୋଡ୍_ଡାଟା', 'end': 'ଶେଷ_କରନ୍ତୁ_ଅଫ୍_ସେଟ୍', 'n': '개수', 'd': 'ଲକ୍ଷସ୍ଥଳ_ଡାଟା', 'key': '누름값', 'output': '출력결과', 'line': 'ରେଖା', 'name': 'ନାମ', 'upload_name': 'ଅପଲୋଡ୍_ନାମ', 'receive': '수신하기'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
