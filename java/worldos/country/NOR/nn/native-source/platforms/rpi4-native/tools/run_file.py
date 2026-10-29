#!/usr/bin/env python3
"""기존 STIGE 호환 oppføring_p. faktisk_data 구현: ../Verktøy/Utfør_fil.py"""
import importlib as TAKE_VALUE
import sys as operativsystem_VALUE
from pathlib import Path as STIGE
operativsystem_VALUE.path.insert(0, str(STIGE(__file__).resolve().parents[1] / 'Verktøy'))
if __name__ == '__main__':
    import runpy as app_appskuff
    app_appskuff.run_module('Utfør_fil', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('Utfør_fil')
    대응 = {'timeout': '시간제한', 's': 'streng_data', 'i': '순번', 'match': '일치', 'files': 'fil_Liste', 'program': 'app', 'executable': '실행가능파일', 'args': 'argument_ARRAY', 'chunk': '조각', 'data': 'data', 'proc': 'Prosess', 'send': 'sende', 'main': 'Køyr_2', 'marker': '확인표시', 'command': 'Kommando', 'include': '포함항목', 'dumped': '갈무리자료', 'run': 'Utfør_kommando', 'p': 'data_plassere', 'parser': '인수해석기', 'options': 'Alternativ', 'kind': 'kategori_VALUE', 'selector': 'veljar', 'upload_data': 'Upload_data', 'end': 'avslutte_OFFSET', 'n': 'vare_COUNT', 'd': 'mål_data', 'key': '누름값', 'output': '출력결과', 'line': 'linje', 'name': 'Namn', 'upload_name': 'Upload_namn', 'receive': '수신하기'}
    for 이전, betalt_vare in 대응.items():
        if hasattr(구현, betalt_vare): globals()[이전] = getattr(구현, betalt_vare)
