#!/usr/bin/env python3
"""기존 Ýol 호환 girizmeklik_utuk. hakyky_maglumat 구현: ../Gurallar/자바라이브러리빌드.py"""
import importlib as 가져오기
import sys as operasiýa_ulgamy_baha
from pathlib import Path as Ýol
operasiýa_ulgamy_baha.path.insert(0, str(Ýol(__file__).resolve().parents[1] / 'Gurallar'))
if __name__ == '__main__':
    import runpy as programma_programma_paneli
    programma_programma_paneli.run_module('자바라이브러리빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('자바라이브러리빌드')
    대응 = {'header': 'At_baha', 'sources': '원문목록', 'i': '순번', 'info': 'msinfo32_exe', 'payload': 'ýük_gutujygy_maglumat', 'src': '원본주소', 'run': 'ýerine_ýetir_buýruk', 'build_java_library': '자바라이브러리만들기', 'relative': '상대경로', 'classes': 'klas_ýol', 'dist': '배포경로', 'archive': 'Arhiw', 'output': '출력결과', 'root': '뿌리주소', 'name': 'Ad', 'jar': '자바꾸러미', 'b': '둘째값', 'entries': '항목들'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
