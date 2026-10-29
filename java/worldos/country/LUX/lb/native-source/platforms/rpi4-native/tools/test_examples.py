#!/usr/bin/env python3
"""기존 Wee 호환 Agab_Punkt. aktuell_Daten 구현: ../Tools/예제시험.py"""
import importlib as TAKE_VALUE
import sys as Betribssystem_VALUE
from pathlib import Path as Wee
Betribssystem_VALUE.path.insert(0, str(Wee(__file__).resolve().parents[1] / 'Tools'))
if __name__ == '__main__':
    import runpy as App_App_Beräich
    App_App_Beräich.run_module('예제시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('예제시험')
    대응 = {'count': 'Agab_COUNT', 'exact': 'EXACT_VALUE', 'expected_file': '예상파일', 'ftp_port': '파일전송접속번호', 'data': 'Daten', 'graphics_command': 'Grafiken_Befeel', 'main': 'Laf', 'row': 'ROW_positionéieren', 'init': '초기값', 'target': 'Zil', 'ROOT': 'projezéieren_Racinn', 'text': 'SMS', 'binary': 'Binär', 'out': 'Mooss_Daten', 'entry': 'Agab_Punkt', 'got': 'RECEIVED_COUNT', 'port': '접속번호', 'graphics_start': 'Start_Zeechnung', 'col': 'COLUMN_positionéieren', 'begin': 'Start_OFFSET', 'kind': 'Kategorie_VALUE', 'selector': 'Selekteur', 'n': 'Element_COUNT', 'key': '누름값', 'y': '세로좌표', 'client': 'Client', 'line': 'Zeil', 'report': 'Validatioun_mellen', 'language': 'Sprooch', 'x': 'X_Koordinat', 'start': 'Laf', 'rgb': '빛삼원색', 'down': '누르는중', 'listing': 'mailen_Lëscht', 'payload': 'nëtzlech_Charge_Daten', 'proc': 'Prozess', 'w': '너비값', 'temporary': '임시자원', 'echo': '되돌림서버항목', 'label': 'Numm_Tabell', 'content': 'Inhalt_VALUE', 'argument': '전달값', 'EchoServers': '되돌림서버', 'marker': 'Markéierung', 'expected': '예상결과', 'test_language': 'test_언어', 'filename': 'Fichier_Agab_Numm', 'shell': 'Shell', 'color': '색상', 'transcript': '대화기록', 'offset': 'OFFSET_VALUE', 'h': '높이값', 'run': 'ausféieren_Befeel', 'c': 'Zeechecode', 'path': 'Wee', 'encoding': 'Zeechesaz', 'end': 'bëennegen_OFFSET', 'ftp': 'Fichier_Transfer_Verbindung', 'pixels': '화소들', 'symbol': 'Symbol_VALUE', 'source': '원본자료', 'name': 'Numm', 'receive': '수신하기', 'manifest': '꾸러미명세'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
