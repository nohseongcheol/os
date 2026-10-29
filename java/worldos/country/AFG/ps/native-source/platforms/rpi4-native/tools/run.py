#!/usr/bin/env python3
"""기존 يونلور 호환 ننوت_ټکى. 실제 구현: ../도구/실행.py"""
import importlib as 가져오기
import sys as چليز_غونډال_ارزښت
from pathlib import Path as يونلور
چليز_غونډال_ارزښت.path.insert(0, str(يونلور(__file__).resolve().parents[1] / '도구'))
if __name__ == '__main__':
    import runpy as 실행기
    실행기.run_module('실행', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('실행')
    대응 = {'supported': '지원목록', 'parser': '인수해석기', 'qemu': '모의기계', 'run_desktop': '바탕화면실행', 'main': 'ځغلول', 'host': 'کوربه', 'status': 'انکړ_ارزښت', 'NetworkBridge': '통신다리', 'ROOT': '기준', 'bridge': '연결다리', 'loader': '적재기', 'base': 'شاليد_ارزښت', 'options': 'غوراوي', 'binary': 'دويال', 'args': 'ارزښتوړى_لړوند', 'command': 'بولۍ'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
