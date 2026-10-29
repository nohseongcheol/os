#!/usr/bin/env python3
"""기존 Bide_izena 호환 sarrera_p. benetako_datuak 구현: ../Tresnak/원격한글시험.py"""
import importlib as HARTU_balio
import sys as sistema_eragile_balio
from pathlib import Path as Bide_izena
sistema_eragile_balio.path.insert(0, str(Bide_izena(__file__).resolve().parents[1] / 'Tresnak'))
if __name__ == '__main__':
    import runpy as aplik_abiarazle
    aplik_abiarazle.run_module('원격한글시험', run_name='__main__', alter_sys=True)
else:
    구현 = HARTU_balio.import_module('원격한글시험')
    대응 = {'wait': '기다리기', 'typing': '글자입력', 'start': 'Exekutatu_2', 'profile': 'profil', 'focused': 'Lehentasunezkoak', 'serial': '직렬입출력', 'keys': '누름열', 'server': 'zerbitzari_balio', 'log': 'LOG_marka', 'args': 'arg_matrize', 'deadline': '마감시각', 'data': 'datuak', 'candidate': '후보', 'logs': '기록들', 'kw': '이름붙인인수', 'number': '수치', 'main': 'Exekutatu_2', 'ready': '준비완료', 'found': 'BILATU_neurria', 'guest': 'gonbidatu', 'ROOT': 'Project_erro', 'marker': '확인표시', 'text': 'Testua', 'out': 'neurria_datuak', 'env': '환경', 'f': 'fitxategi_sarrera', 'port': 'ataka_zenbaki', 'offset': 'Geruzak_balio', 'version': '판번호', 'p': 'datuak_kargu', 'selector': '준비선택기', 'xvfb': 'birtual_pantaila', 'display': 'pantaila', 'n': 'elementu_ZENBATU', 'key': '누름값', 'processes': '실행과정들', 'rootfs': '뿌리파일계층', 'xdo': '가상입력도구', 'name': 'Izena', 'window': 'Leihoa', 'report': 'balidazio_txosten', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
