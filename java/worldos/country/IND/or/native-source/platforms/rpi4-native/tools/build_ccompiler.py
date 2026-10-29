#!/usr/bin/env python3
"""기존 ପଥ 호환 ଏଣ୍ଟ୍ରି_ପଏଣ୍ଟ୍. ପ୍ରକୃତ_ଡାଟା 구현: ../ଉପକରଣସମୂହ/시언어번역기빌드.py"""
import importlib as 가져오기
import sys as ଅପରେଟିଂ_ସିଷ୍ଟମ_ମୂଲ୍ୟ
from pathlib import Path as ପଥ
ଅପରେଟିଂ_ସିଷ୍ଟମ_ମୂଲ୍ୟ.path.insert(0, str(ପଥ(__file__).resolve().parents[1] / 'ଉପକରଣସମୂହ'))
if __name__ == '__main__':
    import runpy as ଅନୁପ୍ରୟୋଗ_ଆପ୍ଲିକେସନ୍_ଡ୍ରୟର୍
    ଅନୁପ୍ରୟୋଗ_ଆପ୍ଲିକେସନ୍_ଡ୍ରୟର୍.run_module('시언어번역기빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('시언어번역기빌드')
    대응 = {'out': 'ମାପ_ଡାଟା', 'builtins': '내장연산', 'header': 'ଶୀର୍ଷକ_ମୂଲ୍ୟ', 'sdk': '개발꾸러미', 'build_ccompiler': '시언어번역기만들기', 'i': '순번', 'elf': '실행파일', 'run': 'ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ', 'flags': '설정비트', 'path': 'ପଥ', 'p': 'ଡାଟା_ସ୍ଥିତି', 'cc': '시언어번역기', 'obj': 'ଲକ୍ଷସ୍ଥଳ_ଫାଇଲ୍', 'flag': 'ସେଟିଂସ୍_ମୂଲ୍ୟ', 'ld': '연결편집기', 'objects': 'ଲକ୍ଷସ୍ଥଳ_ଫାଇଲ୍_ଗୁଡିକ', 'repo': '저장소경로', 'v': '임시값', 'upstream': '외부원문', 'root': 'ରୁଟ୍_ଠିକଣା', 'assets': '탑재자료', 'source': '원본자료', 'name': 'ନାମ', 'includes': '포함인수'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
