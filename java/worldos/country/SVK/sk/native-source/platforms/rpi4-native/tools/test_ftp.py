#!/usr/bin/env python3
"""기존 Cesta 호환 položka_bod. skutočný_údaje 구현: ../Nástroje/test_FTP.py"""
import importlib as TAKE_VALUE
import sys as operačný_systém_VALUE
from pathlib import Path as Cesta
operačný_systém_VALUE.path.insert(0, str(Cesta(__file__).resolve().parents[1] / 'Nástroje'))
if __name__ == '__main__':
    import runpy as program_spúšťač
    program_spúšťač.run_module('test_FTP', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('test_FTP')
    mapovanie_VALUE = {'timeout': '시간제한', 'payload': 'údajová_časť_údaje', 'broken': '손상자료', 'linux_example': '리눅스예제', 'chunk': '조각', 'data': 'údaje', 'proc': 'Proces', 'code': 'inštrukcia_SEQUENCE', 'linux': '리눅스파일', 'archive': 'Archív', 'main': 'Spustiť_2', 'net_source': 'NET_zdroj', 'temporary': '임시자원', 'static_source': '정적원문', 'java_source': '자바원문', 'echo': 'ozvena_server_položka', 'ROOT': 'akcia_koreň', 'text': 'Spracovanie_textu', 'marker': 'fixka', 'EchoFixture': '되돌림시험서버', 'command': 'Príkaz', 'out': 'KR_údaje', 'expected': '예상결과', 'server_source': 'server_zdroj', 'shell': '셸', 'upload': 'nahrať_Súbory', 'transcript': 'prepis', 'port': 'číslo_portu', 'native': '자체실행파일', 'elf': 'spustiteľný_súbor', 'server_udp_port': 'server_datagram_port', 'packed': '묶인자료', 'bridge': 'most', 'selector': 'selektor', 'end': 'ukončiť_hovor_Posun', 'e': '보조항목', 'ftp': 'prenos_súborov_kontakt', 'key': '누름값', 'bytecode': '바이트코드', 'peer': 'partnerský_uzol_VALUE', 'result': 'KR', 'unchanged': '보존자료', 'line': 'riadok', 'server_tcp_port': 'server_Stream_port', 'source': '원본자료', 'NetworkBridge': 'sieťový_most', 'jar': '자바꾸러미', 'receive': 'dostať_e_mail', 'report': 'overenie_správa'}
    for 이전, v_termíne_splatnosti_položka in mapovanie_VALUE.items():
        if hasattr(구현, v_termíne_splatnosti_položka): globals()[이전] = getattr(구현, v_termíne_splatnosti_položka)
