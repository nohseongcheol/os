#!/usr/bin/env python3
"""기존 pad 호환 beginpunt. werkelijk_gegevens implementatie: ../hulpmiddelen/부팅시험.py"""
import importlib as NEMEN_WAARDE
import sys as besturingssysteem_WAARDE
from pathlib import Path as pad
besturingssysteem_WAARDE.path.insert(0, str(pad(__file__).resolve().parents[1] / 'hulpmiddelen'))
if __name__ == '__main__':
    import runpy as app_app_lade
    app_app_lade.run_module('부팅시험', run_name='__main__', alter_sys=True)
else:
    implementatie = NEMEN_WAARDE.import_module('부팅시험')
    toewijzing_WAARDE = {'timeout': 'uitvoerbewerking_TIMEOUT', 'response': 'reactie_1262b476', 'msg': 'net_e_mail', 'exact': 'GELIJK_WAARDE', 'markers': '확인표시들', 'i': '순번', 'match': '일치', 'execute': 'Uitvoeren', 'cancel': 'Annuleren_operatie', 'cmd_byte': 'opdracht_byte', 'reply': 'reactie', 'points': '지점들', 'server': 'server_WAARDE', 'data': 'gegevens', 'prompt': 'prompt', 'enter': 'invoeren', 'imported': '들여온파일', 'send': 'e_mailen', 'main': 'starten', 'ROOT': 'Taken_wortel', 'text': 'tekst', 'first_gui': '첫화면', 'pixel': 'pixel', 'java_class': '자바클래스', 'upload': 'Upload_Files', 'pixels_file': 'pixel_Bestand', 'pixels_data': 'pixel_gegevens', 'edit': 'Bewerk_WAARDE', 'receive_until': '표시까지받기', 'selector': 'selector', 'size': 'Grootte', 'qmp_path': '모의제어경로', 'key': '누름값', 'second_gui': 'SECONDE_GUI', 'y': 'Y_coördinaat', 'result': 'resultaat', 'samples': '예제들', 'client': 'client', 'line': 'invoerregel', 'report': 'validatie_Rapport', 'work': '작업경로', 'x': 'x_coördinaat', 'python_checks': '파이썬검사', 'download': 'download', 'greeting': '인사', 'dims': '치수', 'chunk': '조각', 'deadline': 'deadline_TIJD', 'proc': 'Proces', 'content': 'Inhoud_WAARDE', 'block': 'gegevensblok', 'marker': 'markering', 'command': 'opdracht', 'expected': '예상결과', 'shell': 'Shell', 'drawing': 'tekening_pad', 'f': 'Bestand_invoer', 'transcript': 'transcriptie', 'offset': 'VERSCHUIVING_WAARDE', 'path': 'pad', 'screenshot': 'schermopname', 'arguments': '전달인수', 'pixels': '화소들', 'viewer': 'scherm_client', 'output': 'uitvoer', 'stream': 'Stream_WAARDE', 'cmd': '명령인수', 'name': 'Naam', 'qmp': '모의제어접속'}
    for Vorige_item, actueel_item in toewijzing_WAARDE.items():
        if hasattr(implementatie, actueel_item): globals()[Vorige_item] = getattr(implementatie, actueel_item)
