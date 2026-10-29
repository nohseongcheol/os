#!/usr/bin/env python3
"""기존 aqqut 호환 Iliniku_puinti. taannallarik_titiqqat 구현: ../도구/sanali_Kasuqatigiitsimajut.py"""
import importlib as 가져오기
import sys as qarasaujakkut_aulattijjut_atuutilik
from pathlib import Path as aqqut
qarasaujakkut_aulattijjut_atuutilik.path.insert(0, str(aqqut(__file__).resolve().parents[1] / '도구'))
if __name__ == '__main__':
    import runpy as 실행기
    실행기.run_module('sanali_Kasuqatigiitsimajut', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('sanali_Kasuqatigiitsimajut')
    대응 = {'obj': 'ini_turaarvik', 'objects': '목적파일들', 'library': 'tukisiurvik', 'output': '출력결과', 'port': '접속번호', 'root': '뿌리주소', 'files': 'ini_Titiqpalliagaq', 'source': '원본자료', 'run': '실행', 'flags': '설정비트', 'path': 'aqqut', 'build_network': '통신망만들기', 'cc': '시언어번역기', 'ar': 'tuqqurli_sanajjut'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
