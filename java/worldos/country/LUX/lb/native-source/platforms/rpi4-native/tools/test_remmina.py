#!/usr/bin/env python3
"""기존 Wee 호환 Agab_Punkt. aktuell_Daten 구현: ../Tools/원격한글시험.py"""
import importlib as TAKE_VALUE
import sys as Betribssystem_VALUE
from pathlib import Path as Wee
Betribssystem_VALUE.path.insert(0, str(Wee(__file__).resolve().parents[1] / 'Tools'))
if __name__ == '__main__':
    import runpy as App_App_Beräich
    App_App_Beräich.run_module('원격한글시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('원격한글시험')
    대응 = {'wait': '기다리기', 'typing': '글자입력', 'start': 'Laf', 'profile': 'Profil', 'focused': 'Wichteg', 'serial': '직렬입출력', 'keys': '누름열', 'server': 'Server_VALUE', 'log': 'LOG_Rei', 'args': 'Argument_ARRAY', 'deadline': '마감시각', 'data': 'Daten', 'candidate': '후보', 'logs': '기록들', 'kw': '이름붙인인수', 'number': '수치', 'main': 'Laf', 'ready': '준비완료', 'found': 'Sich_Mooss', 'guest': 'Gaascht', 'ROOT': 'projezéieren_Racinn', 'marker': 'Markéierung', 'text': 'SMS', 'out': 'Mooss_Daten', 'env': '환경', 'f': 'Fichier_Agab', 'port': '접속번호', 'offset': 'OFFSET_VALUE', 'version': '판번호', 'p': 'Daten_positionéieren', 'selector': 'Selekteur', 'xvfb': 'virtuell_Bildschierm', 'display': 'Bildschierm', 'n': 'Element_COUNT', 'key': '누름값', 'processes': '실행과정들', 'rootfs': '뿌리파일계층', 'xdo': '가상입력도구', 'name': 'Numm', 'window': 'Fënster', 'report': 'Validatioun_mellen', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
