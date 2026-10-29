#!/usr/bin/env python3
"""기존 Sti 호환 inngangspunkt. faktisk_data 구현: ../Verktøy/Utfør_Fil.py"""
import importlib as TA_VERDI
import sys as operativsystem_VERDI
from pathlib import Path as Sti
operativsystem_VERDI.path.insert(0, str(Sti(__file__).resolve().parents[1] / 'Verktøy'))
if __name__ == '__main__':
    import runpy as app_appskuff
    app_appskuff.run_module('Utfør_Fil', run_name='__main__', alter_sys=True)
else:
    구현 = TA_VERDI.import_module('Utfør_Fil')
    tildeling_VERDI = {'timeout': 'kjøring_TIMEOUT', 's': 'streng_data', 'i': '순번', 'match': '일치', 'files': 'filliste', 'program': 'app', 'executable': 'kjørbar_fil_BILDE', 'args': 'argument_MATRISE', 'chunk': '조각', 'data': 'data', 'proc': 'Prosess', 'send': 'sende', 'main': 'Kjør_2', 'marker': 'tusj', 'command': 'Kommando', 'include': 'inkludere', 'dumped': '갈무리자료', 'run': 'Utfør_kommando', 'p': 'data_plassere', 'parser': 'parser', 'options': 'Alternativer', 'kind': 'område_VERDI', 'selector': 'velger', 'upload_data': 'Upload_data', 'end': 'avslutte_en_samtale_FORSKYVNING', 'n': 'vare_ANTALL', 'd': 'mål_data', 'key': '누름값', 'output': 'produksjon', 'line': 'Linje', 'name': 'Navn', 'upload_name': 'Upload_navn', 'receive': 'motta_e_post'}
    for Forrige_vare, betalt_vare in tildeling_VERDI.items():
        if hasattr(구현, betalt_vare): globals()[Forrige_vare] = getattr(구현, betalt_vare)
