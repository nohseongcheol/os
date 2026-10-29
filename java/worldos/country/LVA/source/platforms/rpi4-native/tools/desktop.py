#!/usr/bin/env python3
"""기존 CEĻŠ 호환 ieejas_punkts. faktisks_dati 구현: ../Rīki/dators_Skats.py"""
import importlib as TAKE_VALUE
import sys as operētājsistēma_VALUE
from pathlib import Path as CEĻŠ
operētājsistēma_VALUE.path.insert(0, str(CEĻŠ(__file__).resolve().parents[1] / 'Rīki'))
if __name__ == '__main__':
    import runpy as programma_palaidējs
    programma_palaidējs.run_module('dators_Skats', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('dators_Skats')
    kartēšana_VALUE = {'count': 'ievade_COUNT', 'special': '특수글쇠', 'error': 'Kļūda', 'exact': 'EXACT_VALUE', 'network': 'tīkls', 'closed': 'informācijas_tehnoloģija_slēgts', 'length': '길이', 'opened': '열림', 'ftp_port': 'faila_pārsūtīšana_porta_numurs', 'server': 'serveris_VALUE', 'resources': 'Resursi', 'data': 'dati', 'shift': '윗글쇠', 'send': 'sūtīt', 'run_desktop': 'virkne_dators', 'protocol': '통신규약', 'forwards': '전달규칙들', 'host': 'viesot', 'text': 'Teksts', 'korean': '한글여부', 'port': 'porta_numurs', 'signum': 'signāls_numurs', 'version': 'versijas_numurs', 'parser': 'parsētājs', 'bridge': 'tilts', 'kind': 'joma_VALUE', 'tail': '끝부분', 'size': 'Izmērs', 'previous_buttons': '이전단추', 'key': '누름값', 'y': '세로좌표', 'prefix': '앞부분', 'client': 'klients', 'char': 'rakstzīmju_dati', 'work': '작업경로', 'Keyboard': 'tastatūra', 'x': 'x_koordināta', 'down': '누르는중', 'net': 'tilts_ievade', 'self': '자신', 'mode_changed': '입력방식알림', 'serial': '직렬입출력', 'args': 'arg_ARRAY', 'Hangul': '한글조합', 'chunk': '조각', 'proc': 'Process', 'Desktop': 'saziņa_dators', 'buttons': '단추들', 'thread': 'nodarbinātais', 'pressed': '눌림', 'previous': '이전항목', 'toggle': 'SWITCH_MODE', 'command': 'Komanda', 'sock': '소켓', 'frame': '실행틀', 'ctrl': 'vadība_Atslēga', 'path': 'CEĻŠ', 'cp': 'rakstzīmju_kodēšana', 'terminate': '종료시키기', 'security': 'Drošība', 'vnc_port': '원격화면접속번호', 'body': 'pamatteksts', 'index': 'LOOKUP_INDEX', 'exited': '종료됨', 'keysym': 'Atslēga_simbols', 'output': 'ražojums', 'keyboard': 'tastatūra_ievade', 'interrupted': '가로채기됨', 'listener': 'saņemt_ports', 'reader': 'Lasītājs', 'NetworkBridge': 'tilts_3de4fe3a', 'gui': '그림화면', 'worker': 'apstrāde_uzdevums'}
    for 이전, pašreizējais_krājums in kartēšana_VALUE.items():
        if hasattr(구현, pašreizējais_krājums): globals()[이전] = getattr(구현, pašreizējais_krājums)
