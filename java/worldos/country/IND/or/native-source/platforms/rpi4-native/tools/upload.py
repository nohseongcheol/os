#!/usr/bin/env python3
"""기존 ପଥ 호환 ଏଣ୍ଟ୍ରି_ପଏଣ୍ଟ୍. ପ୍ରକୃତ_ଡାଟା 구현: ../ଉପକରଣସମୂହ/ଅପଲୋଡ୍_ଫାଇଲ୍_ଗୁଡିକ.py"""
import importlib as 가져오기
import sys as ଅପରେଟିଂ_ସିଷ୍ଟମ_ମୂଲ୍ୟ
from pathlib import Path as ପଥ
ଅପରେଟିଂ_ସିଷ୍ଟମ_ମୂଲ୍ୟ.path.insert(0, str(ପଥ(__file__).resolve().parents[1] / 'ଉପକରଣସମୂହ'))
if __name__ == '__main__':
    import runpy as ଅନୁପ୍ରୟୋଗ_ଆପ୍ଲିକେସନ୍_ଡ୍ରୟର୍
    ଅନୁପ୍ରୟୋଗ_ଆପ୍ଲିକେସନ୍_ଡ୍ରୟର୍.run_module('ଅପଲୋଡ୍_ଫାଇଲ୍_ଗୁଡିକ', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('ଅପଲୋଡ୍_ଫାଇଲ୍_ଗୁଡିକ')
    대응 = {'data': 'ଡାଟା', 'i': '순번', 'name': 'ନାମ', 'c': 'ବର୍ଣ୍ଣ_କୋଡ଼୍', 'p': 'ଡାଟା_ସ୍ଥିତି', 'args': 'ଯୁକ୍ତି_ଆରେ'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
