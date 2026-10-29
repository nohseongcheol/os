#!/usr/bin/env python3
"""기존 Inzira 호환 icyinjizwa_inota. nyakuri_amakurushingiro 구현: ../Ibikoresho/실행파일시험.py"""
import importlib as 가져오기
import sys as sisitemu_ngengamikorere_agaciro
from pathlib import Path as Inzira
sisitemu_ngengamikorere_agaciro.path.insert(0, str(Inzira(__file__).resolve().parents[1] / 'Ibikoresho'))
if __name__ == '__main__':
    import runpy as porogaramu_umukozi
    porogaramu_umukozi.run_module('실행파일시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('실행파일시험')
    대응 = {'out': '결과자료', 'expected': '예상결과', 'phoff': 'porogaramu_Umutwengaruka_Ofuseti', 'offset': 'Ofuseti_agaciro', 'invalid': 'kitemewe_amakurushingiro', 'path': 'Inzira', 'executable': '실행가능파일', 'rejected': '거부결과', 'linux_example': '리눅스예제', 'original': '원본', 'result': '결과', 'format_': 'imiterere_b87fd068', 'main': 'ihuriro', 'content': 'Ibirimo_agaciro', 'source': '원본자료', 'name': 'Izina', 'reference': '비교기준', 'ROOT': '기준', 'value': 'agaciro', 'report': 'iyemeza_raporo'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
