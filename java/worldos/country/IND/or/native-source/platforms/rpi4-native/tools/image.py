#!/usr/bin/env python3
"""기존 ପଥ 호환 ଏଣ୍ଟ୍ରି_ପଏଣ୍ଟ୍. ପ୍ରକୃତ_ଡାଟା 구현: ../ଉପକରଣସମୂହ/ସୃଷ୍ଟି_ଚିତ୍ର.py"""
import importlib as 가져오기
import sys as ଅପରେଟିଂ_ସିଷ୍ଟମ_ମୂଲ୍ୟ
from pathlib import Path as ପଥ
ଅପରେଟିଂ_ସିଷ୍ଟମ_ମୂଲ୍ୟ.path.insert(0, str(ପଥ(__file__).resolve().parents[1] / 'ଉପକରଣସମୂହ'))
if __name__ == '__main__':
    import runpy as ଅନୁପ୍ରୟୋଗ_ଆପ୍ଲିକେସନ୍_ଡ୍ରୟର୍
    ଅନୁପ୍ରୟୋଗ_ଆପ୍ଲିକେସନ୍_ଡ୍ରୟର୍.run_module('ସୃଷ୍ଟି_ଚିତ୍ର', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('ସୃଷ୍ଟି_ଚିତ୍ର')
    대응 = {'total': '총량', 'start': 'ଚଳାନ୍ତୁ', 'firmware': '기초제어프로그램', 'files': 'ଫାଇଲ୍_ତାଲିକା', 'archive_base': '압축기준', 'partition': 'ବିଭାଜନ_ଫାଇଲ୍', 'archive': 'ଅଭିଲେଖାଗାର', 'main': 'ଚଳାନ୍ତୁ', 'block': 'ଡାଟା_ଅବରୋଧ_କରିବା', 'ROOT': 'ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍', 'boot': '부팅경로', 'stage': 'ଷ୍ଟେଜ୍_ମୂଲ୍ୟ', 'out': 'ମାପ_ଡାଟା', 'expected': '예상결과', 'f': 'ଫାଇଲ୍_ଏଣ୍ଟ୍ରି', 'src': '원본주소', 'path': 'ପଥ', 'p': 'ଡାଟା_ସ୍ଥିତି', 'extracted': '추출자료', 'member': 'ସଭ୍ୟ', 'mbr': '주부트기록', 'image': 'ଚିତ୍ର', 'sector_count': '섹터개수', 'dist': '배포경로', 'sha': '해시계산', 'license_': 'ଲାଇସେନ୍ସ_କରିବା', 'source': '원본자료', 'name': 'ନାମ', 'value': 'ମୂଲ୍ୟ', 'manifest': '꾸러미명세', 'dest': 'ଲକ୍ଷସ୍ଥଳ_ମୂଲ୍ୟ_ସ୍ଥିତି', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
