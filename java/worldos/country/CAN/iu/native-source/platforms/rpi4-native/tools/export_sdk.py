#!/usr/bin/env python3
"""기존 aqqut 호환 Iliniku_puinti. taannallarik_titiqqat 구현: ../도구/개발꾸러미내보내기.py"""
import importlib as 가져오기
import sys as qarasaujakkut_aulattijjut_atuutilik
from pathlib import Path as aqqut
qarasaujakkut_aulattijjut_atuutilik.path.insert(0, str(aqqut(__file__).resolve().parents[1] / '도구'))
if __name__ == '__main__':
    import runpy as 실행기
    실행기.run_module('개발꾸러미내보내기', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('개발꾸러미내보내기')
    대응 = {'out': '결과자료', 'obj': 'ini_turaarvik', 'relative': '상대경로', 'compiler_archive': '번역기꾸러미', 'sdk': '개발꾸러미', 'dist': '배포경로', 'archive': 'tuqqurli', 'main': '시작', 'posix': '포직스경로', 'files': 'ini_Titiqpalliagaq', 'source': '원본자료', 'name': 'atiq', 'target': 'turaagaq', 'ROOT': '기준', 'destination': 'namunngarvik_titiqqat_turaarut', 'manifest': '꾸러미명세', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
