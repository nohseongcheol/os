#!/usr/bin/env python3
"""기존 PUTANJA 호환 unos_p. stvaran_podaci 구현: ../Alati/파일전송시험.py"""
import importlib as TAKE_VALUE
import sys as operacijski_sustav_VALUE
from pathlib import Path as PUTANJA
operacijski_sustav_VALUE.path.insert(0, str(PUTANJA(__file__).resolve().parents[1] / 'Alati'))
if __name__ == '__main__':
    import runpy as program_pokretač
    program_pokretač.run_module('파일전송시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('파일전송시험')
    mapiranje_VALUE = {'timeout': '시간제한', 'payload': 'korisni_podaci_podaci', 'broken': '손상자료', 'linux_example': '리눅스예제', 'chunk': 'fragment_VALUE', 'data': 'podaci', 'proc': 'Proces', 'code': '명령열', 'linux': '리눅스파일', 'archive': 'Arhiva', 'main': 'Pokreni', 'net_source': 'NET_izvor', 'temporary': '임시자원', 'static_source': '정적원문', 'java_source': '자바원문', 'echo': 'eho_server_unos', 'ROOT': 'akcija_korijen', 'text': 'Tekst', 'marker': 'marker', 'EchoFixture': '되돌림시험서버', 'command': 'Naredba', 'out': 'KR_podaci', 'expected': '예상결과', 'server_source': 'server_izvor', 'shell': 'ljuska', 'upload': 'Prijenos_Datoteke', 'transcript': 'transkript', 'port': 'broj_priključka', 'native': '자체실행파일', 'elf': '실행파일', 'server_udp_port': 'server_datogram_prebaciti', 'packed': '묶인자료', 'bridge': 'most', 'selector': 'odabirač', 'end': 'završiti_razgovor_pomak', 'e': '보조항목', 'ftp': 'prijenos_datoteka_veza', 'key': '누름값', 'bytecode': '바이트코드', 'peer': 'ravnopravan_član_VALUE', 'result': 'REZULTAT', 'unchanged': '보존자료', 'line': 'red', 'server_tcp_port': 'server_tok_prebaciti', 'source': '원본자료', 'NetworkBridge': 'most_3de4fe3a', 'jar': '자바꾸러미', 'receive': 'primiti_poruka', 'report': 'provjera_izvješće'}
    for 이전, redovno_artikl in mapiranje_VALUE.items():
        if hasattr(구현, redovno_artikl): globals()[이전] = getattr(구현, redovno_artikl)
