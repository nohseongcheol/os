#!/usr/bin/env python3
"""기존 POT 호환 vnos_p. dejanski_podatki 구현: ../Orodja/preskusiti_FTP.py"""
import importlib as TAKE_VALUE
import sys as operacijski_sistem_VALUE
from pathlib import Path as POT
operacijski_sistem_VALUE.path.insert(0, str(POT(__file__).resolve().parents[1] / 'Orodja'))
if __name__ == '__main__':
    import runpy as aplikacija_zaganjalnik
    aplikacija_zaganjalnik.run_module('preskusiti_FTP', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('preskusiti_FTP')
    preslikava_VALUE = {'timeout': '시간제한', 'payload': 'koristna_vsebina_podatki', 'broken': '손상자료', 'linux_example': '리눅스예제', 'chunk': '조각', 'data': 'podatki', 'proc': 'Opravilo', 'code': 'navodilo_SEQUENCE', 'linux': '리눅스파일', 'archive': 'Arhiv', 'main': 'Zaženi', 'net_source': 'NET_vir', 'temporary': '임시자원', 'static_source': 'statičen_vir', 'java_source': '자바원문', 'echo': 'odmev_strežnik_vnos', 'ROOT': 'pobuda_koren', 'text': 'Besedilo', 'marker': 'oznaka', 'EchoFixture': '되돌림시험서버', 'command': 'Ukaz', 'out': 'KR_podatki', 'expected': '예상결과', 'server_source': 'strežnik_vir', 'shell': 'lupina', 'upload': 'Upload_Datoteke', 'transcript': 'prepis', 'port': 'številka_vrat', 'native': '자체실행파일', 'elf': '실행파일', 'server_udp_port': 'strežnik_datagram_vrata', 'packed': '묶인자료', 'bridge': 'most', 'selector': 'izbirnik', 'end': 'končati_klic_odmik', 'e': '보조항목', 'ftp': 'prenos_datotek_povezava', 'key': '누름값', 'bytecode': '바이트코드', 'peer': 'enakovreden_VALUE', 'result': 'REZULTAT', 'unchanged': '보존자료', 'line': 'Črtni', 'server_tcp_port': 'strežnik_tok_vrata', 'source': '원본자료', 'NetworkBridge': 'most_3de4fe3a', 'jar': '자바꾸러미', 'receive': 'sprejeti_sprejemati_prejeti_prejemati_e_pošta', 'report': 'preverjanje_veljavnosti_prijavi'}
    for 이전, sprotno_element in preslikava_VALUE.items():
        if hasattr(구현, sprotno_element): globals()[이전] = getattr(구현, sprotno_element)
