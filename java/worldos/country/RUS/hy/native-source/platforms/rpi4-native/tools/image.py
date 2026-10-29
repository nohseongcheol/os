#!/usr/bin/env python3
"""기존 Ճանապարհ 호환 մուտքագրում_կետ. իրական_տվյալ 구현: ../Գործիքներ/Կերտի_ր_նկար.py"""
import importlib as 가져오기
import sys as գործավար_համակարգ_արժեք
from pathlib import Path as Ճանապարհ
գործավար_համակարգ_արժեք.path.insert(0, str(Ճանապարհ(__file__).resolve().parents[1] / 'Գործիքներ'))
if __name__ == '__main__':
    import runpy as ծրագիր_թողարկիչ
    ծրագիր_թողարկիչ.run_module('Կերտի_ր_նկար', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('Կերտի_ր_նկար')
    대응 = {'total': '총량', 'start': 'Գործարկել', 'firmware': '기초제어프로그램', 'files': 'նիշք_Ցուցակ', 'archive_base': '압축기준', 'partition': 'մասնաբաժին_նիշք', 'archive': 'Պահոց', 'main': 'Գործարկել', 'block': 'տվյալ_արգելափակել', 'ROOT': 'արձակել_արմատ', 'boot': '부팅경로', 'stage': 'բեմ_արժեք', 'out': 'չափ_տվյալ', 'expected': '예상결과', 'f': 'նիշք_մուտքագրում', 'src': '원본주소', 'path': 'Ճանապարհ', 'p': 'տվյալ_դիրք', 'extracted': '추출자료', 'member': 'անդամ', 'mbr': '주부트기록', 'image': 'նկար', 'sector_count': '섹터개수', 'dist': '배포경로', 'sha': '해시계산', 'license_': 'լիցենզիա', 'source': '원본자료', 'name': 'Անուն', 'value': 'արժեք', 'manifest': '꾸러미명세', 'dest': 'նպատակակետ_արժեք_դիրք', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
