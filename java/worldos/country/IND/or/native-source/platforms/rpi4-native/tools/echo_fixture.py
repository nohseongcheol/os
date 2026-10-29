#!/usr/bin/env python3
"""기존 ପଥ 호환 ଏଣ୍ଟ୍ରି_ପଏଣ୍ଟ୍. ପ୍ରକୃତ_ଡାଟା 구현: ../ଉପକରଣସମୂହ/되돌림시험서버.py"""
import importlib as 가져오기
import sys as ଅପରେଟିଂ_ସିଷ୍ଟମ_ମୂଲ୍ୟ
from pathlib import Path as ପଥ
ଅପରେଟିଂ_ସିଷ୍ଟମ_ମୂଲ୍ୟ.path.insert(0, str(ପଥ(__file__).resolve().parents[1] / 'ଉପକରଣସମୂହ'))
if __name__ == '__main__':
    import runpy as ଅନୁପ୍ରୟୋଗ_ଆପ୍ଲିକେସନ୍_ଡ୍ରୟର୍
    ଅନୁପ୍ରୟୋଗ_ଆପ୍ଲିକେସନ୍_ଡ୍ରୟର୍.run_module('되돌림시험서버', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('되돌림시험서버')
    대응 = {'data': 'ଡାଟା', 'e': '보조항목', 'connection': 'ସଂଯୋଗ_e05f319b', 'f': 'ଫାଇଲ୍_ଏଣ୍ଟ୍ରି', 'peer': 'ସମକକ୍ଷ_ମୂଲ୍ୟ', 'self': '자신', 'udp': '전문제어', 't': 'ଟର୍ମିନାଲ୍_ଏଣ୍ଟ୍ରି', 'tcp': 'ସଂଯୋଗ_ନିୟନ୍ତ୍ରଣ', 'EchoFixture': '되돌림시험서버', 'args': 'ଯୁକ୍ତି_ଆରେ', 'chunk': '조각'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
