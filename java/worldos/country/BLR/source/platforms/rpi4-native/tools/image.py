#!/usr/bin/env python3
"""기존 ШЛЯХ 호환 увядзенне_бал. фактычны_дадзеныя 구현: ../Інструменты/стварыць_выява.py"""
import importlib as 가져오기
import sys as аперацыйная_сістэма_значэнне
from pathlib import Path as ШЛЯХ
аперацыйная_сістэма_значэнне.path.insert(0, str(ШЛЯХ(__file__).resolve().parents[1] / 'Інструменты'))
if __name__ == '__main__':
    import runpy as праграма_выклік_праграм
    праграма_выклік_праграм.run_module('стварыць_выява', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('стварыць_выява')
    대응 = {'total': '총량', 'start': 'Выканаць', 'firmware': '기초제어프로그램', 'files': 'файл_Спіс', 'archive_base': '압축기준', 'partition': 'раздзел_файл', 'archive': 'Архіў', 'main': 'Выканаць', 'block': 'дадзеныя_блакіраваць', 'ROOT': '기준', 'boot': '부팅경로', 'stage': 'стадыя_значэнне', 'out': '결과자료', 'expected': '예상결과', 'f': 'файл_увядзенне', 'src': '원본주소', 'path': 'ШЛЯХ', 'p': '자료위치', 'extracted': '추출자료', 'member': 'член', 'mbr': '주부트기록', 'image': 'выява', 'sector_count': '섹터개수', 'dist': '배포경로', 'sha': '해시계산', 'license_': 'ліцэнзія', 'source': '원본자료', 'name': 'Назва', 'value': 'значэнне', 'manifest': '꾸러미명세', 'dest': '목적위치', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
