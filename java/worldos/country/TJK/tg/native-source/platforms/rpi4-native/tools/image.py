#!/usr/bin/env python3
"""기존 масир 호환 ворида_нуқта. воқеӣ_иттилоот 구현: ../Абзорҳо/эҷод_кардан_расм.py"""
import importlib as 가져오기
import sys as системаи_омил_қимат
from pathlib import Path as масир
системаи_омил_қимат.path.insert(0, str(масир(__file__).resolve().parents[1] / 'Абзорҳо'))
if __name__ == '__main__':
    import runpy as барнома_панели_барномаҳо
    барнома_панели_барномаҳо.run_module('эҷод_кардан_расм', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('эҷод_кардан_расм')
    대응 = {'total': '총량', 'start': 'порча', 'firmware': '기초제어프로그램', 'files': 'файл_Рӯйхат', 'archive_base': '압축기준', 'partition': 'қисмбандӣ_файл', 'archive': 'Бойгонӣ', 'main': 'порча', 'block': 'иттилоот_манъ_кардан', 'ROOT': '기준', 'boot': '부팅경로', 'stage': 'марҳила_қимат', 'out': '결과자료', 'expected': '예상결과', 'f': 'файл_ворида', 'src': '원본주소', 'path': 'масир', 'p': '자료위치', 'extracted': '추출자료', 'member': 'узв', 'mbr': '주부트기록', 'image': 'расм', 'sector_count': '섹터개수', 'dist': '배포경로', 'sha': '해시계산', 'license_': 'иҷозатнома', 'source': '원본자료', 'name': 'Ном', 'value': 'қимат', 'manifest': '꾸러미명세', 'dest': '목적위치', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
