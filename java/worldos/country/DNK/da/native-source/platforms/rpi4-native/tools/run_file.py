#!/usr/bin/env python3
"""기존 Sti 호환 indgangspunkt. faktisk_data 구현: ../Værktøjer/Udfør_fil.py"""
import importlib as TAG_VÆRDI
import sys as operativsystem_VÆRDI
from pathlib import Path as Sti
operativsystem_VÆRDI.path.insert(0, str(Sti(__file__).resolve().parents[1] / 'Værktøjer'))
if __name__ == '__main__':
    import runpy as app_Kvikstart
    app_Kvikstart.run_module('Udfør_fil', run_name='__main__', alter_sys=True)
else:
    구현 = TAG_VÆRDI.import_module('Udfør_fil')
    tilknytning_VÆRDI = {'timeout': 'udførelse_TIMEOUT', 's': 'streng_data', 'i': '순번', 'match': '일치', 'files': 'filliste', 'program': 'app', 'executable': 'eksekverbar_fil_Image', 'args': 'argument_MATRIX', 'chunk': '조각', 'data': 'data', 'proc': 'Proces', 'send': 'maile', 'main': 'Kør_2', 'marker': 'mærke', 'command': 'Kommando', 'include': 'inkludere', 'dumped': '갈무리자료', 'run': 'Udfør_kommando', 'p': 'data_placere', 'parser': 'parser', 'options': 'Indstillinger_7f769d16', 'kind': 'område_VÆRDI', 'selector': 'selektor', 'upload_data': 'Upload_data', 'end': 'afslutte_et_opkald_FORSKYDNING', 'n': 'vare_TÆL', 'd': 'destination_data', 'key': '누름값', 'output': 'produktoutput', 'line': 'Linje', 'name': 'Navn', 'upload_name': 'Upload_navn', 'receive': 'modtage_mail'}
    for Forrige_vare, aktuel_vare in tilknytning_VÆRDI.items():
        if hasattr(구현, aktuel_vare): globals()[Forrige_vare] = getattr(구현, aktuel_vare)
