#!/usr/bin/env python3
"""기존 ପଥ 호환 ଏଣ୍ଟ୍ରି_ପଏଣ୍ଟ୍. ପ୍ରକୃତ_ଡାଟା 구현: ../ଉପକରଣସମୂହ/ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ.py"""
import importlib as 가져오기
import sys as ଅପରେଟିଂ_ସିଷ୍ଟମ_ମୂଲ୍ୟ
from pathlib import Path as ପଥ
ଅପରେଟିଂ_ସିଷ୍ଟମ_ମୂଲ୍ୟ.path.insert(0, str(ପଥ(__file__).resolve().parents[1] / 'ଉପକରଣସମୂହ'))
if __name__ == '__main__':
    import runpy as ଅନୁପ୍ରୟୋଗ_ଆପ୍ଲିକେସନ୍_ଡ୍ରୟର୍
    ଅନୁପ୍ରୟୋଗ_ଆପ୍ଲିକେସନ୍_ଡ୍ରୟର୍.run_module('ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ')
    대응 = {'supported': '지원목록', 'parser': '인수해석기', 'qemu': '모의기계', 'run_desktop': 'ରନ୍_ଡେସ୍କଟପ୍', 'main': 'ଚଳାନ୍ତୁ', 'host': 'ଆୟୋଜକ', 'status': 'ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1', 'NetworkBridge': 'ନେଟ୍_ୱାର୍କ୍_ବ୍ରିଜ୍', 'ROOT': 'ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍', 'bridge': 'ବ୍ରିଜ୍', 'loader': '적재기', 'base': 'ପୃଷ୍ଠପଟ_ମୂଲ୍ୟ', 'options': 'ବିକଳ୍ପ_ସମୂହ', 'binary': 'ବାଇନାରୀ', 'args': 'ଯୁକ୍ତି_ଆରେ', 'command': 'ନିର୍ଦ୍ଦେଶ'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
