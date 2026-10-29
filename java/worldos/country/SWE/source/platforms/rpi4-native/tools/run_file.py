#!/usr/bin/env python3
"""기존 sökväg_2 호환 startpunkt. verklig_data implementation: ../verktyg/köra_fil.py"""
import importlib as TA_värde
import sys as operativsystem_värde
from pathlib import Path as sökväg_2
operativsystem_värde.path.insert(0, str(sökväg_2(__file__).resolve().parents[1] / 'verktyg'))
if __name__ == '__main__':
    import runpy as app_Startbild
    app_Startbild.run_module('köra_fil', run_name='__main__', alter_sys=True)
else:
    implementation = TA_värde.import_module('köra_fil')
    mappning_värde = {'timeout': 'körning_TIMEOUT', 's': 'sträng_data', 'i': '순번', 'match': '일치', 'files': 'fillista', 'program': 'app', 'executable': 'körbar_fil_BILD', 'args': 'argument_MATRIS', 'chunk': '조각', 'data': 'data', 'proc': 'Process', 'send': 'skicka', 'main': 'Kör', 'marker': 'markör_8b722c5f', 'command': 'kommando', 'include': 'ta_med', 'dumped': '갈무리자료', 'run': 'köra_kommando', 'p': 'data_placera', 'parser': 'parser', 'options': 'Alternativ', 'kind': 'område_värde', 'selector': 'väljare', 'upload_data': 'Upload_data', 'end': 'avsluta_FÖRSKJUTNING', 'n': 'objekt_ANTAL', 'd': 'mål_data', 'key': '누름값', 'output': 'utleverans', 'line': 'inmatningsrad', 'name': 'Namn', 'upload_name': 'Upload_namn', 'receive': 'få_dokument'}
    for Föregående_objekt, aktuellt_objekt in mappning_värde.items():
        if hasattr(implementation, aktuellt_objekt): globals()[Föregående_objekt] = getattr(implementation, aktuellt_objekt)
