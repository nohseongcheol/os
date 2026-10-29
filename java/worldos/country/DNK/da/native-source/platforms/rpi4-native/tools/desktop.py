#!/usr/bin/env python3
"""기존 Sti 호환 indgangspunkt. faktisk_data 구현: ../Værktøjer/desktop_Visning.py"""
import importlib as TAG_VÆRDI
import sys as operativsystem_VÆRDI
from pathlib import Path as Sti
operativsystem_VÆRDI.path.insert(0, str(Sti(__file__).resolve().parents[1] / 'Værktøjer'))
if __name__ == '__main__':
    import runpy as app_Kvikstart
    app_Kvikstart.run_module('desktop_Visning', run_name='__main__', alter_sys=True)
else:
    구현 = TAG_VÆRDI.import_module('desktop_Visning')
    tilknytning_VÆRDI = {'count': 'post_TÆL_8f7753a1', 'special': '특수글쇠', 'error': 'fejl', 'exact': 'EKSAKT_VÆRDI', 'network': 'netværk', 'closed': 'it_lukket', 'length': 'varighed_VÆRDI', 'opened': '열림', 'ftp_port': 'filoverførsel_portnummer', 'server': 'server_VÆRDI', 'resources': 'Ressourcer', 'data': 'data', 'shift': 'Skift_tast', 'send': 'maile', 'run_desktop': 'køre_desktop', 'protocol': '통신규약', 'forwards': '전달규칙들', 'host': 'vært', 'text': 'Tekst', 'korean': '한글여부', 'port': 'portnummer', 'signum': 'signal_tal', 'version': 'versionsnummer', 'parser': 'parser', 'bridge': 'bro', 'kind': 'område_VÆRDI', 'tail': '끝부분', 'size': 'Størrelse', 'previous_buttons': '이전단추', 'key': '누름값', 'y': 'Y_koordinat', 'prefix': '앞부분', 'client': 'klient', 'char': 'tegndata', 'work': '작업경로', 'Keyboard': 'tastatur', 'x': 'X_koordinat', 'down': '누르는중', 'net': 'bro_post', 'self': '자신', 'mode_changed': '입력방식알림', 'serial': '직렬입출력', 'args': 'argument_MATRIX', 'Hangul': '한글조합', 'chunk': '조각', 'proc': 'Proces', 'Desktop': 'Forbind_desktop', 'buttons': '단추들', 'thread': 'arbejder', 'pressed': '눌림', 'previous': 'Forrige', 'toggle': 'SKIFT_HYPPIGST', 'command': 'Kommando', 'sock': 'socket_VÆRDI', 'frame': 'udførelse_ramme', 'ctrl': 'Ctrl', 'path': 'Sti', 'cp': 'tegnkodning', 'terminate': 'afslutte', 'security': 'Sikkerhed', 'vnc_port': '원격화면접속번호', 'body': 'brødtekst', 'index': 'Opslag_INDEKS', 'exited': '종료됨', 'keysym': 'tast_symbol', 'output': 'produktoutput', 'keyboard': 'tastatur_post', 'interrupted': '가로채기됨', 'listener': 'modtage_port', 'reader': 'Læser', 'NetworkBridge': 'bro_3de4fe3a', 'gui': 'tegning_skærmbillede', 'worker': 'behandling_job'}
    for Forrige_vare, aktuel_vare in tilknytning_VÆRDI.items():
        if hasattr(구현, aktuel_vare): globals()[Forrige_vare] = getattr(구현, aktuel_vare)
