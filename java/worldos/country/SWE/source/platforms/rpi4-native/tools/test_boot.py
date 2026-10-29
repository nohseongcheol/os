#!/usr/bin/env python3
"""기존 sökväg_2 호환 startpunkt. verklig_data implementation: ../verktyg/부팅시험.py"""
import importlib as TA_värde
import sys as operativsystem_värde
from pathlib import Path as sökväg_2
operativsystem_värde.path.insert(0, str(sökväg_2(__file__).resolve().parents[1] / 'verktyg'))
if __name__ == '__main__':
    import runpy as app_Startbild
    app_Startbild.run_module('부팅시험', run_name='__main__', alter_sys=True)
else:
    implementation = TA_värde.import_module('부팅시험')
    mappning_värde = {'timeout': 'körning_TIMEOUT', 'response': 'svar', 'msg': 'nätverk_dokument', 'exact': 'EXAKT_värde', 'markers': '확인표시들', 'i': '순번', 'match': '일치', 'execute': 'Starta', 'cancel': 'Avbryt_åtgärd', 'cmd_byte': 'kommando_byte', 'reply': 'svara', 'points': '지점들', 'server': 'server_värde', 'data': 'data', 'prompt': 'fråga', 'enter': 'ange', 'imported': '들여온파일', 'send': 'skicka', 'main': 'Kör', 'ROOT': 'åtgärd_rot', 'text': 'text', 'first_gui': '첫화면', 'pixel': 'bildpunkt', 'java_class': '자바클래스', 'upload': 'Upload_Filer', 'pixels_file': 'bildpunkt_fil', 'pixels_data': 'bildpunkt_data', 'edit': 'ändring_värde', 'receive_until': '표시까지받기', 'selector': 'väljare', 'size': 'Storlek', 'qmp_path': '모의제어경로', 'key': '누름값', 'second_gui': 'SEKUND_GUI', 'y': 'Y_koordinat', 'result': 'RESULTAT', 'samples': '예제들', 'client': 'klient', 'line': 'inmatningsrad', 'report': 'validering_Rapport', 'work': '작업경로', 'x': 'x_koordinat', 'python_checks': '파이썬검사', 'download': 'hämtning', 'greeting': '인사', 'dims': '치수', 'chunk': '조각', 'deadline': 'måldatum_tid', 'proc': 'Process', 'content': 'Innehåll_värde', 'block': 'datablock', 'marker': 'markör_8b722c5f', 'command': 'kommando', 'expected': '예상결과', 'shell': 'Shell', 'drawing': 'ritning_väg', 'f': 'fil_post', 'transcript': 'avskrift', 'offset': 'FÖRSKJUTNING_värde', 'path': 'sökväg_2', 'screenshot': 'skärmbild_bb19652a', 'arguments': '전달인수', 'pixels': '화소들', 'viewer': 'skärmbild_klient', 'output': 'utleverans', 'stream': 'flöde_värde', 'cmd': '명령인수', 'name': 'Namn', 'qmp': '모의제어접속'}
    for Föregående_objekt, aktuellt_objekt in mappning_värde.items():
        if hasattr(implementation, aktuellt_objekt): globals()[Föregående_objekt] = getattr(implementation, aktuellt_objekt)
