#!/usr/bin/env python3
"""기존 ପଥ 호환 ଏଣ୍ଟ୍ରି_ପଏଣ୍ଟ୍. ପ୍ରକୃତ_ଡାଟା 구현: ../ଉପକରଣସମୂହ/ବିଲ୍ଡ୍_ନେଟ୍_ୱାର୍କ୍.py"""
import importlib as 가져오기
import sys as ଅପରେଟିଂ_ସିଷ୍ଟମ_ମୂଲ୍ୟ
from pathlib import Path as ପଥ
ଅପରେଟିଂ_ସିଷ୍ଟମ_ମୂଲ୍ୟ.path.insert(0, str(ପଥ(__file__).resolve().parents[1] / 'ଉପକରଣସମୂହ'))
if __name__ == '__main__':
    import runpy as ଅନୁପ୍ରୟୋଗ_ଆପ୍ଲିକେସନ୍_ଡ୍ରୟର୍
    ଅନୁପ୍ରୟୋଗ_ଆପ୍ଲିକେସନ୍_ଡ୍ରୟର୍.run_module('ବିଲ୍ଡ୍_ନେଟ୍_ୱାର୍କ୍', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('ବିଲ୍ଡ୍_ନେଟ୍_ୱାର୍କ୍')
    대응 = {'obj': 'ଲକ୍ଷସ୍ଥଳ_ଫାଇଲ୍', 'objects': 'ଲକ୍ଷସ୍ଥଳ_ଫାଇଲ୍_ଗୁଡିକ', 'library': 'ଲାଇବ୍ରେରୀ', 'output': '출력결과', 'port': 'ପୋର୍ଟ୍_ନମ୍ଵର୍', 'root': 'ରୁଟ୍_ଠିକଣା', 'files': 'ଫାଇଲ୍_ତାଲିକା', 'source': '원본자료', 'run': 'ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ', 'flags': '설정비트', 'path': 'ପଥ', 'build_network': 'ସୃଷ୍ଟି_ନେଟ୍_ୱାର୍କ୍', 'cc': '시언어번역기', 'ar': 'ଅଭିଲେଖାଗାର_ଉପକରଣ'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
