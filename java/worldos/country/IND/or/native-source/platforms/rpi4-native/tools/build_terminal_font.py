#!/usr/bin/env python3
"""기존 ପଥ 호환 ଏଣ୍ଟ୍ରି_ପଏଣ୍ଟ୍. ପ୍ରକୃତ_ଡାଟା 구현: ../ଉପକରଣସମୂହ/ବିଲ୍ଡ୍_ଟର୍ମିନାଲ୍_ଫଣ୍ଟ.py"""
import importlib as 가져오기
import sys as ଅପରେଟିଂ_ସିଷ୍ଟମ_ମୂଲ୍ୟ
from pathlib import Path as ପଥ
ଅପରେଟିଂ_ସିଷ୍ଟମ_ମୂଲ୍ୟ.path.insert(0, str(ପଥ(__file__).resolve().parents[1] / 'ଉପକରଣସମୂହ'))
if __name__ == '__main__':
    import runpy as ଅନୁପ୍ରୟୋଗ_ଆପ୍ଲିକେସନ୍_ଡ୍ରୟର୍
    ଅନୁପ୍ରୟୋଗ_ଆପ୍ଲିକେସନ୍_ଡ୍ରୟର୍.run_module('ବିଲ୍ଡ୍_ଟର୍ମିନାଲ୍_ଫଣ୍ଟ', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('ବିଲ୍ଡ୍_ଟର୍ମିନାଲ୍_ଫଣ୍ଟ')
    대응 = {'data': 'ଡାଟା', 'img': 'ଅଙ୍କନ_ମୂଲ୍ୟ', 'bits': '비트들', 'x': 'x_ସଂଯୋଜନ', 'draw': '화면그리기', 'licences': '이용허락목록', 'paths': 'ପଥ_ତାଲିକା', 'y': '세로좌표', 'main': 'ଚଳାନ୍ତୁ', 'src': '원본주소', 'fonts': 'ଫଣ୍ଟ_ତାଲିକା', 'ROOT': 'ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍', 'p': 'ଡାଟା_ସ୍ଥିତି', 'cp': 'ବର୍ଣ୍ଣ_ଏନକୋଡିଂ', 'target': 'ଲକ୍ଷ୍ୟସ୍ଥଳ'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
