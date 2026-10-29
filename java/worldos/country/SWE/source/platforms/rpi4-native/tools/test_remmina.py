#!/usr/bin/env python3
"""기존 sökväg_2 호환 startpunkt. verklig_data implementation: ../verktyg/원격한글시험.py"""
import importlib as TA_värde
import sys as operativsystem_värde
from pathlib import Path as sökväg_2
operativsystem_värde.path.insert(0, str(sökväg_2(__file__).resolve().parents[1] / 'verktyg'))
if __name__ == '__main__':
    import runpy as app_Startbild
    app_Startbild.run_module('원격한글시험', run_name='__main__', alter_sys=True)
else:
    implementation = TA_värde.import_module('원격한글시험')
    mappning_värde = {'wait': '기다리기', 'typing': '글자입력', 'start': 'Kör', 'profile': 'Profil', 'focused': 'Prioriterad', 'serial': '직렬입출력', 'keys': '누름열', 'server': 'server_värde', 'log': 'LOG_POST', 'args': 'argument_MATRIS', 'deadline': 'måldatum_tid', 'data': 'data', 'candidate': 'kandidat', 'logs': '기록들', 'kw': 'namngivna_argument', 'number': '수치', 'main': 'Kör', 'ready': '준비완료', 'found': 'SÖK_KR', 'guest': 'gäst', 'ROOT': 'åtgärd_rot', 'marker': 'markör_8b722c5f', 'text': 'text', 'out': 'KR_data', 'env': 'miljö', 'f': 'fil_post', 'port': 'portnummer', 'offset': 'FÖRSKJUTNING_värde', 'version': 'versionsnummer', 'p': 'data_placera', 'selector': 'väljare', 'xvfb': 'virtuell_visa', 'display': 'skärm', 'n': 'objekt_ANTAL', 'key': '누름값', 'processes': '실행과정들', 'rootfs': '뿌리파일계층', 'xdo': 'virtuell_indata_verktyg', 'name': 'Namn', 'window': 'Fönster', 'report': 'validering_Rapport', 'work': '작업경로'}
    for Föregående_objekt, aktuellt_objekt in mappning_värde.items():
        if hasattr(implementation, aktuellt_objekt): globals()[Föregående_objekt] = getattr(implementation, aktuellt_objekt)
