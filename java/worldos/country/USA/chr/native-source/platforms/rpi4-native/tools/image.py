#!/usr/bin/env python3
"""기존 ᎠᏍᏓᏩᏛᏍᏗ 호환 Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᎤᏓᏓᏟ. ᎤᏙᎯᏳ_ᎾᏍᎩ_ᎨᏒ_ᎦᏟᏌᏅᎯ 구현: ../도구/영상만들기.py"""
import importlib as 가져오기
import sys as ᎢᏯᏛᏁᏗ_ᏄᏍᏗᏓᏅᎢ_ᏧᎬᏩᎶᏗᏯ
from pathlib import Path as ᎠᏍᏓᏩᏛᏍᏗ
ᎢᏯᏛᏁᏗ_ᏄᏍᏗᏓᏅᎢ_ᏧᎬᏩᎶᏗᏯ.path.insert(0, str(ᎠᏍᏓᏩᏛᏍᏗ(__file__).resolve().parents[1] / '도구'))
if __name__ == '__main__':
    import runpy as 실행기
    실행기.run_module('영상만들기', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('영상만들기')
    대응 = {'total': '총량', 'start': 'ᎠᎢᏎᏍᏗ', 'firmware': '기초제어프로그램', 'files': 'ᎠᏍᏆᏂᎪᏙᏗ_ᏕᎦᏅᏅᏛ', 'archive_base': '압축기준', 'partition': 'ᏓᏓᏓᎴᏛᎢ_ᎠᏍᏆᏂᎪᏙᏗ', 'archive': 'ᎠᏍᏆᏂᎪᏛᎢ', 'main': 'ᎠᎢᏎᏍᏗ', 'block': 'ᎦᏟᏌᏅᎯ_ᎦᏐᎾᎸᏗᏍᏗᎢ', 'ROOT': '기준', 'boot': '부팅경로', 'stage': '단계', 'out': '결과자료', 'expected': '예상결과', 'f': 'ᎠᏍᏆᏂᎪᏙᏗ_Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ', 'src': '원본주소', 'path': 'ᎠᏍᏓᏩᏛᏍᏗ', 'p': '자료위치', 'extracted': '추출자료', 'member': 'ᎨᎵ', 'mbr': '주부트기록', 'image': 'ᎤᏓᏴᎳᏛ', 'sector_count': '섹터개수', 'dist': '배포경로', 'sha': '해시계산', 'license_': 'ᎠᏓᎵᏍᎪᎸᏓᏁᎯ', 'source': '원본자료', 'name': 'ᏚᏙᎥᎢ', 'value': 'ᏧᎬᏩᎶᏗᏯ', 'manifest': '꾸러미명세', 'dest': '목적위치', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
