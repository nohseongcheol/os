#!/usr/bin/env python3
"""기존 Ýol 호환 girizmeklik_utuk. hakyky_maglumat 구현: ../Gurallar/ýerine_ýetir_faýl.py"""
import importlib as 가져오기
import sys as operasiýa_ulgamy_baha
from pathlib import Path as Ýol
operasiýa_ulgamy_baha.path.insert(0, str(Ýol(__file__).resolve().parents[1] / 'Gurallar'))
if __name__ == '__main__':
    import runpy as programma_programma_paneli
    programma_programma_paneli.run_module('ýerine_ýetir_faýl', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('ýerine_ýetir_faýl')
    대응 = {'timeout': '시간제한', 's': 'setir_maglumat', 'i': '순번', 'match': '일치', 'files': 'faýl_Sanaw', 'program': 'programma', 'executable': '실행가능파일', 'args': 'argument_ARRAY', 'chunk': '조각', 'data': 'maglumat', 'proc': 'Proses', 'send': 'iber', 'main': 'Bitir', 'marker': '확인표시', 'command': 'buýruk', 'include': '포함항목', 'dumped': '갈무리자료', 'run': 'ýerine_ýetir_buýruk', 'p': '자료위치', 'parser': '인수해석기', 'options': 'Opsiýalar', 'kind': 'kategoriýa_baha', 'selector': 'saýlaýjy', 'upload_data': 'ýükle_maglumat', 'end': 'tamamla_Süýşüriş', 'n': '개수', 'd': 'barylmaly_ýer_maglumat', 'key': '누름값', 'output': '출력결과', 'line': 'setir', 'name': 'Ad', 'upload_name': 'ýükle_at', 'receive': '수신하기'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
