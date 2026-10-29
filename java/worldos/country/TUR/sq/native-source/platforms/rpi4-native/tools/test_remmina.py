#!/usr/bin/env python3
"""기존 POZICIONI 호환 futje_p. aktual_të_dhëna 구현: ../Mjete/원격한글시험.py"""
import importlib as TAKE_VALUE
import sys as sistem_operativ_VALUE
from pathlib import Path as POZICIONI
sistem_operativ_VALUE.path.insert(0, str(POZICIONI(__file__).resolve().parents[1] / 'Mjete'))
if __name__ == '__main__':
    import runpy as program_hapës
    program_hapës.run_module('원격한글시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('원격한글시험')
    대응 = {'wait': '기다리기', 'typing': '글자입력', 'start': 'Ekzekuto', 'profile': 'profil', 'focused': 'I_E_fokusuar', 'serial': '직렬입출력', 'keys': '누름열', 'server': 'server_VALUE', 'log': 'LOG_RECORD', 'args': 'argument_ARRAY', 'deadline': '마감시각', 'data': 'të_dhëna', 'candidate': '후보', 'logs': '기록들', 'kw': '이름붙인인수', 'number': '수치', 'main': 'Ekzekuto', 'ready': '준비완료', 'found': 'Kërkim_llogaritje', 'guest': 'i_ftuar', 'ROOT': 'Project_rrënjë', 'marker': '확인표시', 'text': 'Teksti', 'out': 'llogaritje_të_dhëna', 'env': '환경', 'f': 'skedar_futje', 'port': 'numri_i_portës', 'offset': 'OFFSET_VALUE', 'version': '판번호', 'p': 'të_dhëna_pozicioni', 'selector': 'përzgjedhësi', 'xvfb': 'virtual_afishim', 'display': 'afishim', 'n': 'njësi_COUNT', 'key': '누름값', 'processes': '실행과정들', 'rootfs': '뿌리파일계층', 'xdo': '가상입력도구', 'name': 'Emër', 'window': 'Dritare', 'report': 'miratim_raport', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
