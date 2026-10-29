#!/usr/bin/env python3
"""기존 Sti 호환 indgangspunkt. faktisk_data 구현: ../Værktøjer/원격한글시험.py"""
import importlib as TAG_VÆRDI
import sys as operativsystem_VÆRDI
from pathlib import Path as Sti
operativsystem_VÆRDI.path.insert(0, str(Sti(__file__).resolve().parents[1] / 'Værktøjer'))
if __name__ == '__main__':
    import runpy as app_Kvikstart
    app_Kvikstart.run_module('원격한글시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAG_VÆRDI.import_module('원격한글시험')
    tilknytning_VÆRDI = {'wait': '기다리기', 'typing': '글자입력', 'start': 'Kør_2', 'profile': 'Profil', 'focused': 'Fokuseret', 'serial': '직렬입출력', 'keys': '누름열', 'server': 'server_VÆRDI', 'log': 'LOG_post', 'args': 'argument_MATRIX', 'deadline': 'deadline_TID', 'data': 'data', 'candidate': '후보', 'logs': '기록들', 'kw': 'navngivet_argument', 'number': '수치', 'main': 'Kør_2', 'ready': '준비완료', 'found': 'SØG_KR', 'guest': 'gæst', 'ROOT': 'To_do_rod', 'marker': 'mærke', 'text': 'Tekst', 'out': 'KR_data', 'env': 'miljø', 'f': 'fil_post', 'port': 'portnummer', 'offset': 'FORSKYDNING_VÆRDI', 'version': 'versionsnummer', 'p': 'data_placere', 'selector': 'selektor', 'xvfb': 'virtuel_vise', 'display': 'skærm', 'n': 'vare_TÆL', 'key': '누름값', 'processes': '실행과정들', 'rootfs': '뿌리파일계층', 'xdo': 'virtuel_input_værktøj', 'name': 'Navn', 'window': 'Vindue', 'report': 'validering_rapport', 'work': '작업경로'}
    for Forrige_vare, aktuel_vare in tilknytning_VÆRDI.items():
        if hasattr(구현, aktuel_vare): globals()[Forrige_vare] = getattr(구현, aktuel_vare)
