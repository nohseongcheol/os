#!/usr/bin/env python3
"""기존 ପଥ 호환 ଏଣ୍ଟ୍ରି_ପଏଣ୍ଟ୍. ପ୍ରକୃତ_ଡାଟା 구현: ../ଉପକରଣସମୂହ/개발꾸러미내보내기.py"""
import importlib as 가져오기
import sys as ଅପରେଟିଂ_ସିଷ୍ଟମ_ମୂଲ୍ୟ
from pathlib import Path as ପଥ
ଅପରେଟିଂ_ସିଷ୍ଟମ_ମୂଲ୍ୟ.path.insert(0, str(ପଥ(__file__).resolve().parents[1] / 'ଉପକରଣସମୂହ'))
if __name__ == '__main__':
    import runpy as ଅନୁପ୍ରୟୋଗ_ଆପ୍ଲିକେସନ୍_ଡ୍ରୟର୍
    ଅନୁପ୍ରୟୋଗ_ଆପ୍ଲିକେସନ୍_ଡ୍ରୟର୍.run_module('개발꾸러미내보내기', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('개발꾸러미내보내기')
    대응 = {'out': 'ମାପ_ଡାଟା', 'obj': 'ଲକ୍ଷସ୍ଥଳ_ଫାଇଲ୍', 'relative': '상대경로', 'compiler_archive': '번역기꾸러미', 'sdk': '개발꾸러미', 'dist': '배포경로', 'archive': 'ଅଭିଲେଖାଗାର', 'main': 'ଚଳାନ୍ତୁ', 'posix': '포직스경로', 'files': 'ଫାଇଲ୍_ତାଲିକା', 'source': '원본자료', 'name': 'ନାମ', 'target': 'ଲକ୍ଷ୍ୟସ୍ଥଳ', 'ROOT': 'ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍', 'destination': 'ଲକ୍ଷସ୍ଥଳ_ଡାଟା_ଠିକଣା', 'manifest': '꾸러미명세', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
