#!/usr/bin/env python3
"""기존 Sti 호환 inngangspunkt. faktisk_data 구현: ../Verktøy/test_stasjonær.py"""
import importlib as TA_VERDI
import sys as operativsystem_VERDI
from pathlib import Path as Sti
operativsystem_VERDI.path.insert(0, str(Sti(__file__).resolve().parents[1] / 'Verktøy'))
if __name__ == '__main__':
    import runpy as app_appskuff
    app_appskuff.run_module('test_stasjonær', run_name='__main__', alter_sys=True)
else:
    구현 = TA_VERDI.import_module('test_stasjonær')
    tildeling_VERDI = {'x': 'x_koordinat', 'typing': '글자입력', 'message': 'notice_SMS', 'start': 'Kjør_2', 'down': '누르는중', 'exact': 'EKSAKT_VERDI', 'i': '순번', 'press': '글쇠누르기', 'rectangles': '사각형들', 'sym': 'symbol', 'j': '안쪽순번', 'deadline': 'tidsfrist_TID', 'proc': 'Prosess', 'data': 'data', 'main': 'Kjør_2', 'w': '너비값', 'init': '초기값', 'block': 'data_blokk', 'ROOT': 'speile_rot', 'text': 'Tekst', 'marker': 'tusj', 'report': 'validering_rapport', 'until': '까지', 'clipboard': 'utklippstavle_VERDI', 'dst': 'mål_e_post_08bbd577', 'seen': '본항목들', 'poll': '준비살피미', 'transcript': 'utskrift', 'port': 'portnummer', 'offset': 'FORSKYVNING_VERDI', 'h': '높이값', 'src': '원본주소', 'event': 'Hendelse', 'encoding': 'tegnsett', 'size': 'Størrelse', 'key': '누름값', 'pixels': '화소들', 'y': 'Y_koordinat', 'output': 'produksjon', 'symbol': 'symbol_VERDI', 'client': 'klient', 'char': 'tegndata', 'rgb': '빛삼원색'}
    for Forrige_vare, betalt_vare in tildeling_VERDI.items():
        if hasattr(구현, betalt_vare): globals()[Forrige_vare] = getattr(구현, betalt_vare)
