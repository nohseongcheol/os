#!/usr/bin/env python3
"""기존 ᎠᏍᏓᏩᏛᏍᏗ 호환 Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᎤᏓᏓᏟ. ᎤᏙᎯᏳ_ᎾᏍᎩ_ᎨᏒ_ᎦᏟᏌᏅᎯ 구현: ../도구/개발꾸러미내보내기.py"""
import importlib as 가져오기
import sys as ᎢᏯᏛᏁᏗ_ᏄᏍᏗᏓᏅᎢ_ᏧᎬᏩᎶᏗᏯ
from pathlib import Path as ᎠᏍᏓᏩᏛᏍᏗ
ᎢᏯᏛᏁᏗ_ᏄᏍᏗᏓᏅᎢ_ᏧᎬᏩᎶᏗᏯ.path.insert(0, str(ᎠᏍᏓᏩᏛᏍᏗ(__file__).resolve().parents[1] / '도구'))
if __name__ == '__main__':
    import runpy as 실행기
    실행기.run_module('개발꾸러미내보내기', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('개발꾸러미내보내기')
    대응 = {'out': '결과자료', 'obj': 'ᏮᎦᏛᎢ_ᎠᏍᏆᏂᎪᏙᏗ', 'relative': '상대경로', 'compiler_archive': '번역기꾸러미', 'sdk': '개발꾸러미', 'dist': '배포경로', 'archive': 'ᎠᏍᏆᏂᎪᏛᎢ', 'main': 'ᎠᎢᏎᏍᏗ', 'posix': '포직스경로', 'files': 'ᎠᏍᏆᏂᎪᏙᏗ_ᏕᎦᏅᏅᏛ', 'source': '원본자료', 'name': 'ᏚᏙᎥᎢ', 'target': 'ᎠᏉᏅᏗᎢ', 'ROOT': '기준', 'destination': 'ᏮᎦᏛᎢ_ᎦᏟᏌᏅᎯ_ᎪᏪᎵ_ᏫᏗᎦᏅᏗ', 'manifest': '꾸러미명세', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
