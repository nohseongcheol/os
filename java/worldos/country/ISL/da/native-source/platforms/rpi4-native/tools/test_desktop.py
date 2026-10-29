#!/usr/bin/env python3
"""기존 Sti 호환 indgangspunkt. faktisk_data 구현: ../Værktøjer/test_desktop.py"""
import importlib as TAG_VÆRDI
import sys as operativsystem_VÆRDI
from pathlib import Path as Sti
operativsystem_VÆRDI.path.insert(0, str(Sti(__file__).resolve().parents[1] / 'Værktøjer'))
if __name__ == '__main__':
    import runpy as app_Kvikstart
    app_Kvikstart.run_module('test_desktop', run_name='__main__', alter_sys=True)
else:
    구현 = TAG_VÆRDI.import_module('test_desktop')
    tilknytning_VÆRDI = {'x': 'X_koordinat', 'typing': '글자입력', 'message': '알림문', 'start': 'Kør_2', 'down': '누르는중', 'exact': 'EKSAKT_VÆRDI', 'i': '순번', 'press': '글쇠누르기', 'rectangles': '사각형들', 'sym': 'symbol', 'j': '안쪽순번', 'deadline': 'deadline_TID', 'proc': 'Proces', 'data': 'data', 'main': 'Kør_2', 'w': '너비값', 'init': '초기값', 'block': 'datablok', 'ROOT': 'To_do_rod', 'text': 'Tekst', 'marker': 'mærke', 'report': 'validering_rapport', 'until': '까지', 'clipboard': 'udklipsholder_VÆRDI', 'dst': 'destination_mail', 'seen': '본항목들', 'poll': '준비살피미', 'transcript': 'afskrift', 'port': 'portnummer', 'offset': 'FORSKYDNING_VÆRDI', 'h': '높이값', 'src': '원본주소', 'event': 'hændelse', 'encoding': 'tegnsæt', 'size': 'Størrelse', 'key': '누름값', 'pixels': '화소들', 'y': 'Y_koordinat', 'output': 'produktoutput', 'symbol': 'symbol_VÆRDI', 'client': 'klient', 'char': 'tegndata', 'rgb': '빛삼원색'}
    for Forrige_vare, aktuel_vare in tilknytning_VÆRDI.items():
        if hasattr(구현, aktuel_vare): globals()[Forrige_vare] = getattr(구현, aktuel_vare)
