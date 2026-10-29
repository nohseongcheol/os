#!/usr/bin/env python3
"""기존 Sti 호환 inngangspunkt. faktisk_data 구현: ../Verktøy/stasjonær_vise.py"""
import importlib as TA_VERDI
import sys as operativsystem_VERDI
from pathlib import Path as Sti
operativsystem_VERDI.path.insert(0, str(Sti(__file__).resolve().parents[1] / 'Verktøy'))
if __name__ == '__main__':
    import runpy as app_appskuff
    app_appskuff.run_module('stasjonær_vise', run_name='__main__', alter_sys=True)
else:
    구현 = TA_VERDI.import_module('stasjonær_vise')
    tildeling_VERDI = {'count': 'oppføring_ANTALL', 'special': '특수글쇠', 'error': 'feil', 'exact': 'EKSAKT_VERDI', 'network': 'nettverk', 'closed': 'informasjonssystemer_lukket', 'length': 'lengde_VERDI', 'opened': '열림', 'ftp_port': 'filoverføring_portnummer', 'server': 'server_VERDI', 'resources': 'Ressurser', 'data': 'data', 'shift': 'Skift', 'send': 'sende', 'run_desktop': 'kjøre_stasjonær', 'protocol': '통신규약', 'forwards': '전달규칙들', 'host': 'vert', 'text': 'Tekst', 'korean': '한글여부', 'port': 'portnummer', 'signum': 'signal_nummer', 'version': 'versjonsnummer', 'parser': 'parser', 'bridge': 'bro', 'kind': 'område_VERDI', 'tail': '끝부분', 'size': 'Størrelse', 'previous_buttons': '이전단추', 'key': '누름값', 'y': 'Y_koordinat', 'prefix': '앞부분', 'client': 'klient', 'char': 'tegndata', 'work': '작업경로', 'Keyboard': 'tastatur', 'x': 'x_koordinat', 'down': '누르는중', 'net': 'bro_oppføring', 'self': '자신', 'mode_changed': '입력방식알림', 'serial': '직렬입출력', 'args': 'argument_MATRISE', 'Hangul': '한글조합', 'chunk': '조각', 'proc': 'Prosess', 'Desktop': 'KOBLE_TIL_stasjonær', 'buttons': '단추들', 'thread': 'arbeider', 'pressed': '눌림', 'previous': 'Forrige', 'toggle': 'bytt_MODUS', 'command': 'Kommando', 'sock': 'socket_VERDI', 'frame': 'kjøring_bilde', 'ctrl': 'Ctrl_tasten', 'path': 'Sti', 'cp': 'tegn_koding', 'terminate': 'avslutte', 'security': 'Sikkerhet', 'vnc_port': '원격화면접속번호', 'body': 'brødtekst', 'index': 'Oppslag_INDEKS', 'exited': '종료됨', 'keysym': 'tast_symbol', 'output': 'produksjon', 'keyboard': 'tastatur_oppføring', 'interrupted': '가로채기됨', 'listener': 'motta_port', 'reader': 'Leser', 'NetworkBridge': 'bro_3de4fe3a', 'gui': 'tegning_skjermbilde', 'worker': 'behandling_oppgave'}
    for Forrige_vare, betalt_vare in tildeling_VERDI.items():
        if hasattr(구현, betalt_vare): globals()[Forrige_vare] = getattr(구현, betalt_vare)
