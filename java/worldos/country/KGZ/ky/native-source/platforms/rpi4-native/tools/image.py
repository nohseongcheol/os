#!/usr/bin/env python3
"""기존 ЖОЛ 호환 киргизме_жазуу_упай. актуалдуу_берилмелер 구현: ../Куралдар/түзүү_сүрөт.py"""
import importlib as 가져오기
import sys as оперативдик_система_маани
from pathlib import Path as ЖОЛ
оперативдик_система_маани.path.insert(0, str(ЖОЛ(__file__).resolve().parents[1] / 'Куралдар'))
if __name__ == '__main__':
    import runpy as програм_жаратма_тарткычы
    програм_жаратма_тарткычы.run_module('түзүү_сүрөт', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('түзүү_сүрөт')
    대응 = {'total': '총량', 'start': 'Жүргүзүү', 'firmware': '기초제어프로그램', 'files': 'файл_Тизме', 'archive_base': '압축기준', 'partition': 'бөлүк_файл', 'archive': 'Архив', 'main': 'Жүргүзүү', 'block': 'берилмелер_тосмолоо', 'ROOT': '기준', 'boot': '부팅경로', 'stage': 'стадия_маани', 'out': '결과자료', 'expected': '예상결과', 'f': 'файл_киргизме_жазуу', 'src': '원본주소', 'path': 'ЖОЛ', 'p': '자료위치', 'extracted': '추출자료', 'member': 'мүчө', 'mbr': '주부트기록', 'image': 'сүрөт', 'sector_count': '섹터개수', 'dist': '배포경로', 'sha': '해시계산', 'license_': '이용허락파일', 'source': '원본자료', 'name': 'Аты', 'value': 'маани', 'manifest': '꾸러미명세', 'dest': '목적위치', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
