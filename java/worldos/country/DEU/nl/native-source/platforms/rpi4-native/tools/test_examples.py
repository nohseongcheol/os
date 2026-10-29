#!/usr/bin/env python3
"""기존 pad 호환 beginpunt. werkelijk_gegevens implementatie: ../hulpmiddelen/예제시험.py"""
import importlib as NEMEN_WAARDE
import sys as besturingssysteem_WAARDE
from pathlib import Path as pad
besturingssysteem_WAARDE.path.insert(0, str(pad(__file__).resolve().parents[1] / 'hulpmiddelen'))
if __name__ == '__main__':
    import runpy as app_app_lade
    app_app_lade.run_module('예제시험', run_name='__main__', alter_sys=True)
else:
    implementatie = NEMEN_WAARDE.import_module('예제시험')
    toewijzing_WAARDE = {'count': 'invoer_AANTAL_8f7753a1', 'exact': 'GELIJK_WAARDE', 'expected_file': '예상파일', 'ftp_port': 'bestandsoverdracht_poortnummer', 'data': 'gegevens', 'graphics_command': 'graphics_opdracht', 'main': 'starten', 'row': 'RIJ_functie', 'init': '초기값', 'target': 'doel', 'ROOT': 'Taken_wortel', 'text': 'tekst', 'binary': 'binair', 'out': 'HR_gegevens', 'entry': 'beginpunt', 'got': 'OPBRENGST_AANTAL', 'port': 'poortnummer', 'graphics_start': 'START_tekening', 'col': 'KOLOM_functie', 'begin': 'START_VERSCHUIVING', 'kind': 'gebied_WAARDE', 'selector': 'selector', 'n': 'item_AANTAL', 'key': '누름값', 'y': 'Y_coördinaat', 'client': 'client', 'line': 'invoerregel', 'report': 'validatie_Rapport', 'language': 'Taal', 'x': 'x_coördinaat', 'start': 'starten', 'rgb': '빛삼원색', 'down': '누르는중', 'listing': 'e_mailen_Lijst', 'payload': 'payload_gegevens', 'proc': 'Proces', 'w': '너비값', 'temporary': '임시자원', 'echo': 'echo_server_invoer', 'label': 'naam_tabel', 'content': 'Inhoud_WAARDE', 'argument': '전달값', 'EchoServers': 'echo_Servers', 'marker': 'markering', 'expected': '예상결과', 'test_language': 'test_Taal', 'filename': 'Bestand_invoer_naam', 'shell': 'Shell', 'color': '색상', 'transcript': 'transcriptie', 'offset': 'VERSCHUIVING_WAARDE', 'h': 'aangevraagd_hoogte_WAARDE', 'run': 'Uitvoeren_opdracht', 'c': 'codepoint', 'path': 'pad', 'encoding': 'tekenset', 'end': 'beëindigen_VERSCHUIVING', 'ftp': 'bestandsoverdracht_verbinding', 'pixels': '화소들', 'symbol': 'symbool_WAARDE', 'source': '원본자료', 'name': 'Naam', 'receive': 'ontvangen_e_mail', 'manifest': 'bundel_manifest'}
    for Vorige_item, actueel_item in toewijzing_WAARDE.items():
        if hasattr(implementatie, actueel_item): globals()[Vorige_item] = getattr(implementatie, actueel_item)
