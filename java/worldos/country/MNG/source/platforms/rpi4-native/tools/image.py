#!/usr/bin/env python3
"""기존 ЗАМ 호환 оролт_цэг. бодит_өгөгдөл 구현: ../Хэрэгслүүд/үүсгэх_зураг.py"""
import importlib as 가져오기
import sys as үйлдлийн_систем_утга
from pathlib import Path as ЗАМ
үйлдлийн_систем_утга.path.insert(0, str(ЗАМ(__file__).resolve().parents[1] / 'Хэрэгслүүд'))
if __name__ == '__main__':
    import runpy as програм_гишүүн
    програм_гишүүн.run_module('үүсгэх_зураг', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('үүсгэх_зураг')
    대응 = {'total': '총량', 'start': 'Ажиллуулах', 'firmware': '기초제어프로그램', 'files': 'файл_Жагсаалт', 'archive_base': '압축기준', 'partition': 'тасалгаа_файл', 'archive': 'Архив', 'main': 'Ажиллуулах', 'block': 'өгөгдөл_хаах', 'ROOT': '기준', 'boot': '부팅경로', 'stage': 'үе_шат_утга_29ee1bb7', 'out': '결과자료', 'expected': '예상결과', 'f': 'файл_оролт', 'src': '원본주소', 'path': 'ЗАМ', 'p': '자료위치', 'extracted': '추출자료', 'member': 'гишүүн', 'mbr': '주부트기록', 'image': 'зураг', 'sector_count': '섹터개수', 'dist': '배포경로', 'sha': '해시계산', 'license_': 'лиценз', 'source': '원본자료', 'name': 'Нэр', 'value': 'утга', 'manifest': '꾸러미명세', 'dest': '목적위치', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
