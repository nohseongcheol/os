#!/usr/bin/env python3
"""기존 Sti 호환 indgangspunkt. faktisk_data 구현: ../Værktøjer/test_Swing.py"""
import importlib as TAG_VÆRDI
import sys as operativsystem_VÆRDI
from pathlib import Path as Sti
operativsystem_VÆRDI.path.insert(0, str(Sti(__file__).resolve().parents[1] / 'Værktøjer'))
if __name__ == '__main__':
    import runpy as app_Kvikstart
    app_Kvikstart.run_module('test_Swing', run_name='__main__', alter_sys=True)
else:
    구현 = TAG_VÆRDI.import_module('test_Swing')
    tilknytning_VÆRDI = {'wait': '기다리기', 'x': 'X_koordinat', 's': 'streng_data', 'i': '순번', 'sel': 'selektor_a916db4e', 'seconds': '초단위', 'log': 'LOG_post', 'data': 'data', 'at': 'aktuel_placere', 'send': 'maile', 'main': 'Kør_2', 'req': 'anmodning_VÆRDI', 'hot': 'alias_VÆRDI', 'pump': 'handle_hændelse', 'ROOT': 'To_do_rod', 'marker': 'mærke', 'b': 'SEKUND_VÆRDI', 'command': 'Kommando', 'shell': 'Shell', 'f': 'fil_post', 'click': 'klik_knap', 'k': '셋째순번', 'c': 'tegnkode', 'r': '반환값', 'p': 'data_placere', 'command_mode': 'kommando_HYPPIGST', 'end': 'afslutte_et_opkald_FORSKYDNING', 'classes': 'Hold_sti', 'key': '누름값', 'y': 'Y_koordinat', 'result': 'KR', 'report': 'validering_rapport', 'dest': 'destination_VÆRDI_placere', 'work': '작업경로', 'qmp': '모의제어접속'}
    for Forrige_vare, aktuel_vare in tilknytning_VÆRDI.items():
        if hasattr(구현, aktuel_vare): globals()[Forrige_vare] = getattr(구현, aktuel_vare)
