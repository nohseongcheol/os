#!/usr/bin/env python3
"""기존 Bide_izena 호환 sarrera_p. benetako_datuak 구현: ../Tresnak/화면요소시험.py"""
import importlib as HARTU_balio
import sys as sistema_eragile_balio
from pathlib import Path as Bide_izena
sistema_eragile_balio.path.insert(0, str(Bide_izena(__file__).resolve().parents[1] / 'Tresnak'))
if __name__ == '__main__':
    import runpy as aplik_abiarazle
    aplik_abiarazle.run_module('화면요소시험', run_name='__main__', alter_sys=True)
else:
    구현 = HARTU_balio.import_module('화면요소시험')
    대응 = {'wait': '기다리기', 'x': 'X_koordenatu', 's': 'kate_datuak', 'i': '순번', 'sel': '선택기', 'seconds': '초단위', 'log': 'LOG_marka', 'data': 'datuak', 'at': '현재위치', 'send': 'bidali', 'main': 'Exekutatu_2', 'req': 'eskaera_balio', 'hot': 'lasterbide_balio', 'pump': 'helduleku_gertaera', 'ROOT': 'Project_erro', 'marker': '확인표시', 'b': 'SEGUNDOA_balio', 'command': 'Komandoa', 'shell': 'shell', 'f': 'fitxategi_sarrera', 'click': 'klik_botoi', 'k': '셋째순번', 'c': 'karaktere_kode', 'r': '반환값', 'p': 'datuak_kargu', 'command_mode': 'komando_MODA', 'end': 'amaitu_Geruzak', 'classes': 'Gela_bide_izen', 'key': '누름값', 'y': 'Y_koordenatu', 'result': 'EMAITZA', 'report': 'balidazio_txosten', 'dest': 'helburu_balio_kargu', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
