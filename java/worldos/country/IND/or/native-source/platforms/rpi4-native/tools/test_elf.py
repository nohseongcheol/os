#!/usr/bin/env python3
"""기존 ପଥ 호환 ଏଣ୍ଟ୍ରି_ପଏଣ୍ଟ୍. ପ୍ରକୃତ_ଡାଟା 구현: ../ଉପକରଣସମୂହ/실행파일시험.py"""
import importlib as 가져오기
import sys as ଅପରେଟିଂ_ସିଷ୍ଟମ_ମୂଲ୍ୟ
from pathlib import Path as ପଥ
ଅପରେଟିଂ_ସିଷ୍ଟମ_ମୂଲ୍ୟ.path.insert(0, str(ପଥ(__file__).resolve().parents[1] / 'ଉପକରଣସମୂହ'))
if __name__ == '__main__':
    import runpy as ଅନୁପ୍ରୟୋଗ_ଆପ୍ଲିକେସନ୍_ଡ୍ରୟର୍
    ଅନୁପ୍ରୟୋଗ_ଆପ୍ଲିକେସନ୍_ଡ୍ରୟର୍.run_module('실행파일시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('실행파일시험')
    대응 = {'out': 'ମାପ_ଡାଟା', 'expected': '예상결과', 'phoff': 'ଅନୁପ୍ରୟୋଗ_ଶୀର୍ଷକ_ଅଫ୍_ସେଟ୍', 'offset': 'ଅଫ୍_ସେଟ୍_ମୂଲ୍ୟ', 'invalid': 'ଅବୈଧ_ଡାଟା', 'path': 'ପଥ', 'executable': '실행가능파일', 'rejected': '거부결과', 'linux_example': '리눅스예제', 'original': '원본', 'result': 'ମାପ', 'format_': 'ଫର୍ମାଟ୍_b87fd068', 'main': 'ଚଳାନ୍ତୁ', 'content': 'ବିଷୟ_ମୂଲ୍ୟ', 'source': '원본자료', 'name': 'ନାମ', 'reference': '비교기준', 'ROOT': 'ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍', 'value': 'ମୂଲ୍ୟ', 'report': 'ବୈଧକରଣ_ରିପୋର୍ଟ'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
