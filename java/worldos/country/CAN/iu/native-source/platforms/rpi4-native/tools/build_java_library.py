#!/usr/bin/env python3
"""기존 aqqut 호환 Iliniku_puinti. taannallarik_titiqqat 구현: ../도구/자바라이브러리빌드.py"""
import importlib as 가져오기
import sys as qarasaujakkut_aulattijjut_atuutilik
from pathlib import Path as aqqut
qarasaujakkut_aulattijjut_atuutilik.path.insert(0, str(aqqut(__file__).resolve().parents[1] / '도구'))
if __name__ == '__main__':
    import runpy as 실행기
    실행기.run_module('자바라이브러리빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('자바라이브러리빌드')
    대응 = {'header': 'Taijaugusinga_atuutilik', 'sources': '원문목록', 'i': '순번', 'info': 'msinfo32_exe', 'payload': '내용자료', 'src': '원본주소', 'run': '실행', 'build_java_library': '자바라이브러리만들기', 'relative': '상대경로', 'classes': 'naliannuungavik_aqqut', 'dist': '배포경로', 'archive': 'tuqqurli', 'output': '출력결과', 'root': '뿌리주소', 'name': 'atiq', 'jar': '자바꾸러미', 'b': '둘째값', 'entries': '항목들'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
