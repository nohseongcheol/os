#!/usr/bin/env python3
"""기존 Sti 호환 inngangspunkt. faktisk_data 구현: ../Verktøy/부팅시험.py"""
import importlib as TA_VERDI
import sys as operativsystem_VERDI
from pathlib import Path as Sti
operativsystem_VERDI.path.insert(0, str(Sti(__file__).resolve().parents[1] / 'Verktøy'))
if __name__ == '__main__':
    import runpy as app_appskuff
    app_appskuff.run_module('부팅시험', run_name='__main__', alter_sys=True)
else:
    구현 = TA_VERDI.import_module('부팅시험')
    tildeling_VERDI = {'timeout': 'kjøring_TIMEOUT', 'response': 'svar_1262b476', 'msg': 'nettverk_e_post', 'exact': 'EKSAKT_VERDI', 'markers': '확인표시들', 'i': '순번', 'match': '일치', 'execute': 'Kjør', 'cancel': 'Avbryt_operasjon', 'cmd_byte': 'kommando_byte', 'reply': 'svar', 'points': '지점들', 'server': 'server_VERDI', 'data': 'data', 'prompt': 'be_om', 'enter': 'angi', 'imported': '들여온파일', 'send': 'sende', 'main': 'Kjør_2', 'ROOT': 'speile_rot', 'text': 'Tekst', 'first_gui': '첫화면', 'pixel': 'piksel', 'java_class': '자바클래스', 'upload': 'Upload_Filer', 'pixels_file': 'piksel_Fil', 'pixels_data': 'piksel_data', 'edit': 'Rediger_VERDI', 'receive_until': '표시까지받기', 'selector': 'velger', 'size': 'Størrelse', 'qmp_path': '모의제어경로', 'key': '누름값', 'second_gui': 'SEKUND_GUI', 'y': 'Y_koordinat', 'result': 'KR', 'samples': '예제들', 'client': 'klient', 'line': 'Linje', 'report': 'validering_rapport', 'work': '작업경로', 'x': 'x_koordinat', 'python_checks': '파이썬검사', 'download': 'last_ned', 'greeting': '인사', 'dims': '치수', 'chunk': '조각', 'deadline': 'tidsfrist_TID', 'proc': 'Prosess', 'content': 'Innhold_VERDI', 'block': 'data_blokk', 'marker': 'tusj', 'command': 'Kommando', 'expected': '예상결과', 'shell': 'Shell', 'drawing': 'tegning_bane', 'f': 'Fil_oppføring', 'transcript': 'utskrift', 'offset': 'FORSKYVNING_VERDI', 'path': 'Sti', 'screenshot': 'skjermbilde_bb19652a', 'arguments': '전달인수', 'pixels': '화소들', 'viewer': 'skjermbilde_klient', 'output': 'produksjon', 'stream': 'strøm_VERDI', 'cmd': '명령인수', 'name': 'Navn', 'qmp': '모의제어접속'}
    for Forrige_vare, betalt_vare in tildeling_VERDI.items():
        if hasattr(구현, betalt_vare): globals()[Forrige_vare] = getattr(구현, betalt_vare)
