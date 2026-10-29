#!/usr/bin/env python3
"""기존 sökväg_2 호환 startpunkt. verklig_data implementation: ../verktyg/test_Dator.py"""
import importlib as TA_värde
import sys as operativsystem_värde
from pathlib import Path as sökväg_2
operativsystem_värde.path.insert(0, str(sökväg_2(__file__).resolve().parents[1] / 'verktyg'))
if __name__ == '__main__':
    import runpy as app_Startbild
    app_Startbild.run_module('test_Dator', run_name='__main__', alter_sys=True)
else:
    implementation = TA_värde.import_module('test_Dator')
    mappning_värde = {'x': 'x_koordinat', 'typing': '글자입력', 'message': '알림문', 'start': 'Kör', 'down': '누르는중', 'exact': 'EXAKT_värde', 'i': '순번', 'press': 'tryck_Nyckel', 'rectangles': '사각형들', 'sym': 'symbol', 'j': '안쪽순번', 'deadline': 'måldatum_tid', 'proc': 'Process', 'data': 'data', 'main': 'Kör', 'w': '너비값', 'init': '초기값', 'block': 'datablock', 'ROOT': 'åtgärd_rot', 'text': 'text', 'marker': 'markör_8b722c5f', 'report': 'validering_Rapport', 'until': '까지', 'clipboard': 'Urklipp_värde', 'dst': 'mål_ADRESS_08bbd577', 'seen': '본항목들', 'poll': '준비살피미', 'transcript': 'avskrift', 'port': 'portnummer', 'offset': 'FÖRSKJUTNING_värde', 'h': '높이값', 'src': '원본주소', 'event': 'Händelse', 'encoding': 'teckenuppsättning', 'size': 'Storlek', 'key': '누름값', 'pixels': '화소들', 'y': 'Y_koordinat', 'output': 'utleverans', 'symbol': 'symbol_värde', 'client': 'klient', 'char': 'teckendata', 'rgb': '빛삼원색'}
    for Föregående_objekt, aktuellt_objekt in mappning_värde.items():
        if hasattr(implementation, aktuellt_objekt): globals()[Föregående_objekt] = getattr(implementation, aktuellt_objekt)
