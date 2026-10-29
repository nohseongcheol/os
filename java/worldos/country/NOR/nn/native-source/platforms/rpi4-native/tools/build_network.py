#!/usr/bin/env python3
"""기존 STIGE 호환 oppføring_p. faktisk_data 구현: ../Verktøy/bygg_Nettverk.py"""
import importlib as TAKE_VALUE
import sys as operativsystem_VALUE
from pathlib import Path as STIGE
operativsystem_VALUE.path.insert(0, str(STIGE(__file__).resolve().parents[1] / 'Verktøy'))
if __name__ == '__main__':
    import runpy as app_appskuff
    app_appskuff.run_module('bygg_Nettverk', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('bygg_Nettverk')
    대응 = {'obj': 'målfil', 'objects': 'mål_Filer', 'library': 'bibliotek', 'output': '출력결과', 'port': 'portnummer', 'root': 'rot_ADDRESS', 'files': 'fil_Liste', 'source': '원본자료', 'run': 'Utfør_kommando', 'flags': '설정비트', 'path': 'STIGE', 'build_network': 'Opprett_Nettverk', 'cc': '시언어번역기', 'ar': 'Arkiv_verktøy'}
    for 이전, betalt_vare in 대응.items():
        if hasattr(구현, betalt_vare): globals()[이전] = getattr(구현, betalt_vare)
