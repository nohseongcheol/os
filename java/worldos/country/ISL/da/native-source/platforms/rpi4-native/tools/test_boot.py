#!/usr/bin/env python3
"""기존 Sti 호환 indgangspunkt. faktisk_data 구현: ../Værktøjer/부팅시험.py"""
import importlib as TAG_VÆRDI
import sys as operativsystem_VÆRDI
from pathlib import Path as Sti
operativsystem_VÆRDI.path.insert(0, str(Sti(__file__).resolve().parents[1] / 'Værktøjer'))
if __name__ == '__main__':
    import runpy as app_Kvikstart
    app_Kvikstart.run_module('부팅시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAG_VÆRDI.import_module('부팅시험')
    tilknytning_VÆRDI = {'timeout': 'udførelse_TIMEOUT', 'response': 'svar_1262b476', 'msg': 'netværk_mail', 'exact': 'EKSAKT_VÆRDI', 'markers': '확인표시들', 'i': '순번', 'match': '일치', 'execute': 'Kør', 'cancel': 'Annuller_kirurgi', 'cmd_byte': 'kommando_byte', 'reply': 'svar', 'points': '지점들', 'server': 'server_VÆRDI', 'data': 'data', 'prompt': 'prompt', 'enter': 'angive', 'imported': '들여온파일', 'send': 'maile', 'main': 'Kør_2', 'ROOT': 'To_do_rod', 'text': 'Tekst', 'first_gui': '첫화면', 'pixel': 'pixel', 'java_class': '자바클래스', 'upload': 'Upload_Filer', 'pixels_file': 'pixel_fil', 'pixels_data': 'pixel_data', 'edit': 'Rediger_VÆRDI', 'receive_until': '표시까지받기', 'selector': 'selektor', 'size': 'Størrelse', 'qmp_path': '모의제어경로', 'key': '누름값', 'second_gui': 'SEKUND_GUI', 'y': 'Y_koordinat', 'result': 'KR', 'samples': '예제들', 'client': 'klient', 'line': 'Linje', 'report': 'validering_rapport', 'work': '작업경로', 'x': 'X_koordinat', 'python_checks': '파이썬검사', 'download': 'hente', 'greeting': '인사', 'dims': '치수', 'chunk': '조각', 'deadline': 'deadline_TID', 'proc': 'Proces', 'content': 'Indhold_VÆRDI', 'block': 'datablok', 'marker': 'mærke', 'command': 'Kommando', 'expected': '예상결과', 'shell': 'Shell', 'drawing': 'tegning_sti', 'f': 'fil_post', 'transcript': 'afskrift', 'offset': 'FORSKYDNING_VÆRDI', 'path': 'Sti', 'screenshot': 'skærmklip', 'arguments': '전달인수', 'pixels': '화소들', 'viewer': 'skærmbillede_klient', 'output': 'produktoutput', 'stream': 'strøm_VÆRDI', 'cmd': '명령인수', 'name': 'Navn', 'qmp': '모의제어접속'}
    for Forrige_vare, aktuel_vare in tilknytning_VÆRDI.items():
        if hasattr(구현, aktuel_vare): globals()[Forrige_vare] = getattr(구현, aktuel_vare)
