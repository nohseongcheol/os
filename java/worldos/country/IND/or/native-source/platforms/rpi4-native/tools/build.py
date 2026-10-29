#!/usr/bin/env python3
"""기존 ପଥ 호환 ଏଣ୍ଟ୍ରି_ପଏଣ୍ଟ୍. ପ୍ରକୃତ_ଡାଟା 구현: ../ଉପକରଣସମୂହ/ବିଲ୍ଡ୍_ସିଷ୍ଟମ.py"""
import importlib as 가져오기
import sys as ଅପରେଟିଂ_ସିଷ୍ଟମ_ମୂଲ୍ୟ
from pathlib import Path as ପଥ
ଅପରେଟିଂ_ସିଷ୍ଟମ_ମୂଲ୍ୟ.path.insert(0, str(ପଥ(__file__).resolve().parents[1] / 'ଉପକରଣସମୂହ'))
if __name__ == '__main__':
    import runpy as ଅନୁପ୍ରୟୋଗ_ଆପ୍ଲିକେସନ୍_ଡ୍ରୟର୍
    ଅନୁପ୍ରୟୋଗ_ଆପ୍ଲିକେସନ୍_ଡ୍ରୟର୍.run_module('ବିଲ୍ଡ୍_ସିଷ୍ଟମ', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('ବିଲ୍ଡ୍_ସିଷ୍ଟମ')
    대응 = {'network': 'ନେଟ୍_ୱାର୍କ୍', 'BUILD': 'ବିଲ୍ଡ୍_ପଥ', 'ar': 'ଅଭିଲେଖାଗାର_ଉପକରଣ', 'build_examples': '예제만들기', 'posix': '포직스경로', 'font_data': 'ଫଣ୍ଟ_ଡାଟା', 'flags': '설정비트', 'a': '첫째값', 'cc': '시언어번역기', 'args': 'ଯୁକ୍ତି_ଆରେ', 'source_flags': '원본설정', 'ld': '연결편집기', 'method': 'ପଦ୍ଧତି_ଏଣ୍ଟ୍ରି', 'main': 'ଚଳାନ୍ତୁ', 'objcopy': 'ଅବଜେକ୍ଟ_ଫାଇଲ୍_କନର୍ଭଟର୍', 'ROOT': 'ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍', 'cxx': '시플플번역기', 'includes': '포함인수', 'compiler': '번역기', 'build_users': 'ସୃଷ୍ଟି_ଉପଭୋକ୍ତା_ସ୍ଥାନ', 'f': 'ଫାଇଲ୍_ଏଣ୍ଟ୍ରି', 'extra': '추가영역', 'exports': 'ରପ୍ତାନି_କରନ୍ତୁ_ସାରଣୀ', 'jobs': '빌드작업', 'run': 'ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ', 'path': 'ପଥ', 'REPO': '저장소', 'tool': 'ଉପକରଣସମୂହ', 'classes': 'ଶ୍ରେଣୀ_ପଥ', 'output': '출력결과', 'samples': '예제들', 'symbol': 'ସଙ୍କେତ_ମୂଲ୍ୟ', 'source': '원본자료', 'name': 'ନାମ', 'build_network': 'ସୃଷ୍ଟି_ନେଟ୍_ୱାର୍କ୍', 'font_info': 'ଫଣ୍ଟ_ସୂଚନା', 'manifest': '꾸러미명세', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
