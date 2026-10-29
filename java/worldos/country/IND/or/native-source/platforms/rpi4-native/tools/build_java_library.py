#!/usr/bin/env python3
"""기존 ପଥ 호환 ଏଣ୍ଟ୍ରି_ପଏଣ୍ଟ୍. ପ୍ରକୃତ_ଡାଟା 구현: ../ଉପକରଣସମୂହ/자바라이브러리빌드.py"""
import importlib as 가져오기
import sys as ଅପରେଟିଂ_ସିଷ୍ଟମ_ମୂଲ୍ୟ
from pathlib import Path as ପଥ
ଅପରେଟିଂ_ସିଷ୍ଟମ_ମୂଲ୍ୟ.path.insert(0, str(ପଥ(__file__).resolve().parents[1] / 'ଉପକରଣସମୂହ'))
if __name__ == '__main__':
    import runpy as ଅନୁପ୍ରୟୋଗ_ଆପ୍ଲିକେସନ୍_ଡ୍ରୟର୍
    ଅନୁପ୍ରୟୋଗ_ଆପ୍ଲିକେସନ୍_ଡ୍ରୟର୍.run_module('자바라이브러리빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('자바라이브러리빌드')
    대응 = {'header': 'ଶୀର୍ଷକ_ମୂଲ୍ୟ', 'sources': '원문목록', 'i': '순번', 'info': 'ସିଷ୍ଟମ୍_ସୂଚନା', 'payload': 'ପେଲୋଡ୍_ଡାଟା', 'src': '원본주소', 'run': 'ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ', 'build_java_library': '자바라이브러리만들기', 'relative': '상대경로', 'classes': 'ଶ୍ରେଣୀ_ପଥ', 'dist': '배포경로', 'archive': 'ଅଭିଲେଖାଗାର', 'output': '출력결과', 'root': 'ରୁଟ୍_ଠିକଣା', 'name': 'ନାମ', 'jar': '자바꾸러미', 'b': '둘째값', 'entries': '항목들'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
