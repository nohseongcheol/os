#!/usr/bin/env python3
"""기존 Ýol 호환 girizmeklik_utuk. hakyky_maglumat 구현: ../Gurallar/döretmek_surat.py"""
import importlib as 가져오기
import sys as operasiýa_ulgamy_baha
from pathlib import Path as Ýol
operasiýa_ulgamy_baha.path.insert(0, str(Ýol(__file__).resolve().parents[1] / 'Gurallar'))
if __name__ == '__main__':
    import runpy as programma_programma_paneli
    programma_programma_paneli.run_module('döretmek_surat', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('döretmek_surat')
    대응 = {'total': '총량', 'start': 'Bitir', 'firmware': '기초제어프로그램', 'files': 'faýl_Sanaw', 'archive_base': '압축기준', 'partition': 'bölüm_faýl', 'archive': 'Arhiw', 'main': 'Bitir', 'block': 'maglumat_bökde', 'ROOT': '기준', 'boot': '부팅경로', 'stage': 'tapgyr_baha', 'out': '결과자료', 'expected': '예상결과', 'f': 'faýl_girizmeklik', 'src': '원본주소', 'path': 'Ýol', 'p': '자료위치', 'extracted': '추출자료', 'member': 'agza', 'mbr': '주부트기록', 'image': 'surat', 'sector_count': '섹터개수', 'dist': '배포경로', 'sha': '해시계산', 'license_': 'ygtyýarlylyk', 'source': '원본자료', 'name': 'Ad', 'value': 'baha', 'manifest': '꾸러미명세', 'dest': '목적위치', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
