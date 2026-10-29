#!/usr/bin/env python3
"""기존 pad 호환 beginpunt. werkelijk_gegevens implementatie: ../hulpmiddelen/pc_Weergave.py"""
import importlib as NEMEN_WAARDE
import sys as besturingssysteem_WAARDE
from pathlib import Path as pad
besturingssysteem_WAARDE.path.insert(0, str(pad(__file__).resolve().parents[1] / 'hulpmiddelen'))
if __name__ == '__main__':
    import runpy as app_app_lade
    app_app_lade.run_module('pc_Weergave', run_name='__main__', alter_sys=True)
else:
    implementatie = NEMEN_WAARDE.import_module('pc_Weergave')
    toewijzing_WAARDE = {'count': 'invoer_AANTAL_8f7753a1', 'special': '특수글쇠', 'error': 'fout', 'exact': 'GELIJK_WAARDE', 'network': 'net', 'closed': 'informatie_afgesloten', 'length': 'tijdsduur_WAARDE', 'opened': '열림', 'ftp_port': 'bestandsoverdracht_poortnummer', 'server': 'server_WAARDE', 'resources': 'Bronnen', 'data': 'gegevens', 'shift': 'SHIFT_toets', 'send': 'e_mailen', 'run_desktop': 'uitvoeren_pc', 'protocol': '통신규약', 'forwards': '전달규칙들', 'host': 'host', 'text': 'tekst', 'korean': '한글여부', 'port': 'poortnummer', 'signum': 'signaal_nummer', 'version': 'versienummer', 'parser': 'parser', 'bridge': 'brug', 'kind': 'gebied_WAARDE', 'tail': '끝부분', 'size': 'Grootte', 'previous_buttons': '이전단추', 'key': '누름값', 'y': 'Y_coördinaat', 'prefix': 'interlinie_tegel', 'client': 'client', 'char': 'tekengegevens', 'work': '작업경로', 'Keyboard': 'toetsenbord', 'x': 'x_coördinaat', 'down': '누르는중', 'net': 'brug_invoer', 'self': '자신', 'mode_changed': '입력방식알림', 'serial': '직렬입출력', 'args': 'argument_MATRIX', 'Hangul': '한글조합', 'chunk': '조각', 'proc': 'Proces', 'Desktop': 'VERBINDEN_pc', 'buttons': '단추들', 'thread': 'achtergrondwerker', 'pressed': '눌림', 'previous': 'Vorige', 'toggle': 'switch_MODUS', 'command': 'opdracht', 'sock': 'socket_WAARDE', 'frame': 'uitvoerbewerking_frame', 'ctrl': 'Ctrl', 'path': 'pad', 'cp': 'tekencodering', 'terminate': 'beëindigen', 'security': 'Beveiliging', 'vnc_port': '원격화면접속번호', 'body': 'hoofdtekst', 'index': 'ZOEKEN_INDEX', 'exited': '종료됨', 'keysym': 'toets_symbool', 'output': 'uitvoer', 'keyboard': 'toetsenbord_invoer', 'interrupted': '가로채기됨', 'listener': 'ontvangen_poort', 'reader': 'Lezer', 'NetworkBridge': 'brug_3de4fe3a', 'gui': 'tekening_scherm', 'worker': 'verwerking_taak'}
    for Vorige_item, actueel_item in toewijzing_WAARDE.items():
        if hasattr(implementatie, actueel_item): globals()[Vorige_item] = getattr(implementatie, actueel_item)
