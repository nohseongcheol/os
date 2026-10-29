#!/usr/bin/env python3
"""기존 ᎠᏍᏓᏩᏛᏍᏗ 호환 Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᎤᏓᏓᏟ. ᎤᏙᎯᏳ_ᎾᏍᎩ_ᎨᏒ_ᎦᏟᏌᏅᎯ 구현: ../도구/터미널글꼴빌드.py"""
import importlib as 가져오기
import sys as ᎢᏯᏛᏁᏗ_ᏄᏍᏗᏓᏅᎢ_ᏧᎬᏩᎶᏗᏯ
from pathlib import Path as ᎠᏍᏓᏩᏛᏍᏗ
ᎢᏯᏛᏁᏗ_ᏄᏍᏗᏓᏅᎢ_ᏧᎬᏩᎶᏗᏯ.path.insert(0, str(ᎠᏍᏓᏩᏛᏍᏗ(__file__).resolve().parents[1] / '도구'))
if __name__ == '__main__':
    import runpy as 실행기
    실행기.run_module('터미널글꼴빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('터미널글꼴빌드')
    대응 = {'data': 'ᎦᏟᏌᏅᎯ', 'img': 'ᎠᏍᏓᏅᎿᏂᏙᎸ_ᏧᎬᏩᎶᏗᏯ', 'bits': '비트들', 'x': '가로좌표', 'draw': '화면그리기', 'licences': '이용허락목록', 'paths': 'ᎠᏍᏓᏩᏛᏍᏗ_ᏕᎦᏅᏅᏛ', 'y': '세로좌표', 'main': 'ᎠᎢᏎᏍᏗ', 'src': '원본주소', 'fonts': 'ᏄᏍᏛ_ᎠᏙᏪᎵᏍᎩ_ᏕᎦᏅᏅᏛ', 'ROOT': '기준', 'p': '자료위치', 'cp': 'ᎪᏪᎸ_ᎪᏗᏍᎩ', 'target': 'ᎠᏉᏅᏗᎢ'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
