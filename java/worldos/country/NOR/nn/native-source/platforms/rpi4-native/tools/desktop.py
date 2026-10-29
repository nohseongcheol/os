#!/usr/bin/env python3
"""기존 STIGE 호환 oppføring_p. faktisk_data 구현: ../Verktøy/stasjonær_vise.py"""
import importlib as TAKE_VALUE
import sys as operativsystem_VALUE
from pathlib import Path as STIGE
operativsystem_VALUE.path.insert(0, str(STIGE(__file__).resolve().parents[1] / 'Verktøy'))
if __name__ == '__main__':
    import runpy as app_appskuff
    app_appskuff.run_module('stasjonær_vise', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('stasjonær_vise')
    대응 = {'count': 'oppføring_COUNT', 'special': '특수글쇠', 'error': 'FEIL', 'exact': 'EXACT_VALUE', 'network': 'Nettverk', 'closed': '닫힘', 'length': 'lengd_VALUE', 'opened': '열림', 'ftp_port': 'fil_Overfør_portnummer', 'server': 'tenar_VALUE', 'resources': 'Ressursar', 'data': 'data', 'shift': 'Skift', 'send': 'sende', 'run_desktop': 'køyre_stasjonær', 'protocol': '통신규약', 'forwards': '전달규칙들', 'host': 'vert', 'text': 'Tekst', 'korean': '한글여부', 'port': 'portnummer', 'signum': '신호번호', 'version': '판번호', 'parser': '인수해석기', 'bridge': 'bru', 'kind': 'kategori_VALUE', 'tail': '끝부분', 'size': 'Storleik', 'previous_buttons': '이전단추', 'key': '누름값', 'y': 'Y_koordinat', 'prefix': '앞부분', 'client': 'klient', 'char': 'teikn_data', 'work': '작업경로', 'Keyboard': 'tastatur', 'x': 'x_koordinat', 'down': '누르는중', 'net': 'Nettverk_bru_oppføring', 'self': '자신', 'mode_changed': '입력방식알림', 'serial': '직렬입출력', 'args': 'argument_ARRAY', 'Hangul': '한글조합', 'chunk': '조각', 'proc': 'Prosess', 'Desktop': 'KOPLE_TIL_stasjonær', 'buttons': '단추들', 'thread': '작업가닥', 'pressed': '눌림', 'previous': '이전항목', 'toggle': 'byte_MODE', 'command': 'Kommando', 'sock': '소켓', 'frame': '실행틀', 'ctrl': 'Ctrl', 'path': 'STIGE', 'cp': 'teikn_koding', 'terminate': '종료시키기', 'security': 'Tryggleik', 'vnc_port': '원격화면접속번호', 'body': 'brødtekst', 'index': 'LOOKUP_INDEX', 'exited': '종료됨', 'keysym': 'tast_symbol', 'output': '출력결과', 'keyboard': 'tastatur_oppføring', 'interrupted': '가로채기됨', 'listener': '수신창구', 'reader': 'Lesar', 'NetworkBridge': 'Nettverk_bru', 'gui': '그림화면', 'worker': '처리작업'}
    for 이전, betalt_vare in 대응.items():
        if hasattr(구현, betalt_vare): globals()[이전] = getattr(구현, betalt_vare)
