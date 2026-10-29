#!/usr/bin/env python3
"""기존 ПУТАЊА 호환 унос_поен. стваран_подаци 구현: ../Алатке/Направи_слика.py"""
import importlib as 가져오기
import sys as оперативни_систем_вриједност
from pathlib import Path as ПУТАЊА
оперативни_систем_вриједност.path.insert(0, str(ПУТАЊА(__file__).resolve().parents[1] / 'Алатке'))
if __name__ == '__main__':
    import runpy as програм_покретач
    програм_покретач.run_module('Направи_слика', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('Направи_слика')
    대응 = {'total': '총량', 'start': 'Покрени', 'firmware': '기초제어프로그램', 'files': 'фајл_Листа', 'archive_base': '압축기준', 'partition': 'партиција_фајл', 'archive': 'Архива', 'main': 'Покрени', 'block': 'подаци_блокирај', 'ROOT': 'пројектовати_корен', 'boot': '부팅경로', 'stage': 'фаза_вриједност', 'out': 'мера_подаци', 'expected': '예상결과', 'f': 'фајл_унос', 'src': '원본주소', 'path': 'ПУТАЊА', 'p': 'подаци_позиција', 'extracted': '추출자료', 'member': 'члан', 'mbr': '주부트기록', 'image': 'слика', 'sector_count': '섹터개수', 'dist': '배포경로', 'sha': '해시계산', 'license_': 'лиценца', 'source': '원본자료', 'name': 'Назив', 'value': 'вриједност', 'manifest': '꾸러미명세', 'dest': 'одредиште_вриједност_позиција', 'work': '작업경로'}
    for 이전, актуелно_ставка in 대응.items():
        if hasattr(구현, актуелно_ставка): globals()[이전] = getattr(구현, актуелно_ставка)
