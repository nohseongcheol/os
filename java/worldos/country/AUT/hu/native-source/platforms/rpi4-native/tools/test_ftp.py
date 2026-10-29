#!/usr/bin/env python3
"""기존 ÚTVONAL 호환 belépési_pont. tényleges_adat 구현: ../Eszközök/teszt_FTP.py"""
import importlib as ÁTHELYEZ_ÉRTÉK
import sys as operációs_rendszer_ÉRTÉK
from pathlib import Path as ÚTVONAL
operációs_rendszer_ÉRTÉK.path.insert(0, str(ÚTVONAL(__file__).resolve().parents[1] / 'Eszközök'))
if __name__ == '__main__':
    import runpy as app_indító
    app_indító.run_module('teszt_FTP', run_name='__main__', alter_sys=True)
else:
    구현 = ÁTHELYEZ_ÉRTÉK.import_module('teszt_FTP')
    leképezés_ÉRTÉK = {'timeout': 'végrehajtás_IDŐTÚLLÉPÉS', 'payload': 'teher_adat', 'broken': '손상자료', 'linux_example': '리눅스예제', 'chunk': '조각', 'data': 'adat', 'proc': 'Folyamat', 'code': '명령열', 'linux': '리눅스파일', 'archive': 'archív', 'main': 'Futtatás', 'net_source': 'NET_forrás', 'temporary': '임시자원', 'static_source': 'statikus_forrás', 'java_source': '자바원문', 'echo': 'visszhang_kiszolgáló_bejegyzés', 'ROOT': 'teendő_gyök', 'text': 'Szöveg', 'marker': 'jelölő', 'EchoFixture': '되돌림시험서버', 'command': 'Parancs', 'out': 'KR_adat', 'expected': '예상결과', 'server_source': 'kiszolgáló_forrás', 'shell': 'felület', 'upload': 'feltölt_Files', 'transcript': 'átirat', 'port': 'portszám', 'native': 'natív', 'elf': 'végrehajtható_Fájl', 'server_udp_port': 'kiszolgáló_datagram_port', 'packed': '묶인자료', 'bridge': 'híd', 'selector': 'szelektor', 'end': 'megszüntet_Ofszet', 'e': '보조항목', 'ftp': 'fájlátvitel_ismerős', 'key': '누름값', 'bytecode': '바이트코드', 'peer': 'társ_ÉRTÉK', 'result': 'KR', 'unchanged': '보존자료', 'line': 'Vonal', 'server_tcp_port': 'kiszolgáló_Stream_port', 'source': '원본자료', 'NetworkBridge': 'híd_3de4fe3a', 'jar': '자바꾸러미', 'receive': 'fogad_e_mail', 'report': 'ellenőrzés_jelent'}
    for Előző_cikk, aktuális_cikk in leképezés_ÉRTÉK.items():
        if hasattr(구현, aktuális_cikk): globals()[Előző_cikk] = getattr(구현, aktuális_cikk)
