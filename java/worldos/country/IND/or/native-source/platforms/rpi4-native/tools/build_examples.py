#!/usr/bin/env python3
"""기존 ପଥ 호환 ଏଣ୍ଟ୍ରି_ପଏଣ୍ଟ୍. ପ୍ରକୃତ_ଡାଟା 구현: ../ଉପକରଣସମୂହ/예제빌드.py"""
import importlib as 가져오기
import sys as ଅପରେଟିଂ_ସିଷ୍ଟମ_ମୂଲ୍ୟ
from pathlib import Path as ପଥ
ଅପରେଟିଂ_ସିଷ୍ଟମ_ମୂଲ୍ୟ.path.insert(0, str(ପଥ(__file__).resolve().parents[1] / 'ଉପକରଣସମୂହ'))
if __name__ == '__main__':
    import runpy as ଅନୁପ୍ରୟୋଗ_ଆପ୍ଲିକେସନ୍_ଡ୍ରୟର୍
    ଅନୁପ୍ରୟୋଗ_ଆପ୍ଲିକେସନ୍_ଡ୍ରୟର୍.run_module('예제빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('예제빌드')
    대응 = {'out': 'ମାପ_ଡାଟା', 'build_examples': '예제만들기', 'files': 'ଫାଇଲ୍_ତାଲିକା', 'java': '자바실행', 'run': 'ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ', 'path': 'ପଥ', 'p': 'ଡାଟା_ସ୍ଥିତି', 'readme': 'ମତେପଢନ୍ତୁ', 'build_java_library': '자바라이브러리만들기', 'code': '명령열', 'index': 'ଦୃଷ୍ଟିପାତ_ଅନୁକ୍ରମଣିକା', 'classes': 'ଶ୍ରେଣୀ_ପଥ', 'repo': '저장소경로', 'root': 'ରୁଟ୍_ଠିକଣା', 'content': 'ବିଷୟ_ମୂଲ୍ୟ', 'source': '원본자료', 'name': 'ନାମ', 'target': 'ଲକ୍ଷ୍ୟସ୍ଥଳ', 'manifest': '꾸러미명세', 'language': 'ଭାଷା'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
