#!/usr/bin/env python3
"""기존 Bide_izena 호환 sarrera_p. benetako_datuak 구현: ../Tresnak/셸시험.py"""
import importlib as HARTU_balio
import sys as sistema_eragile_balio
from pathlib import Path as Bide_izena
sistema_eragile_balio.path.insert(0, str(Bide_izena(__file__).resolve().parents[1] / 'Tresnak'))
if __name__ == '__main__':
    import runpy as aplik_abiarazle
    aplik_abiarazle.run_module('셸시험', run_name='__main__', alter_sys=True)
else:
    구현 = HARTU_balio.import_module('셸시험')
    대응 = {'timeout': '시간제한', 'x': 'X_koordenatu', 'msg': 'sare_mezu', 'i': '순번', 'reply': 'erantzun', 'call': '호출', 'args': 'arg_matrize', 'chunk': '조각', 'data': 'datuak', 'proc': 'Prozesua', 'long_text': '긴글', 'restored': '복원자료', 'send': 'bidali', 'file': 'Fitxategia', 'main': 'Exekutatu_2', 'found': 'BILATU_neurria', 'ROOT': 'Project_erro', 'text': 'Testua', 'marker': '확인표시', 'command': 'Komandoa', 'expected': '예상결과', 'pixel': 'pixel', 'shell': 'shell', 'poll': '준비살피미', 'transcript': '대화기록', 'end': 'amaitu_Geruzak', 'image': 'irudi', 'key': '누름값', 'y': 'Y_koordenatu', 'output': '출력결과', 'result': 'EMAITZA', 'client': 'bezero', 'line': 'Marra', 'stream': 'Stream_balio', 'name': 'Izena', 'value': 'balio', 'receive': '수신하기', 'report': 'balidazio_txosten', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
