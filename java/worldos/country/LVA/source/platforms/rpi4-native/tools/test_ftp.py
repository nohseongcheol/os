#!/usr/bin/env python3
"""기존 CEĻŠ 호환 ieejas_punkts. faktisks_dati 구현: ../Rīki/파일전송시험.py"""
import importlib as TAKE_VALUE
import sys as operētājsistēma_VALUE
from pathlib import Path as CEĻŠ
operētājsistēma_VALUE.path.insert(0, str(CEĻŠ(__file__).resolve().parents[1] / 'Rīki'))
if __name__ == '__main__':
    import runpy as programma_palaidējs
    programma_palaidējs.run_module('파일전송시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('파일전송시험')
    kartēšana_VALUE = {'timeout': '시간제한', 'payload': 'vērtums_dati', 'broken': '손상자료', 'linux_example': '리눅스예제', 'chunk': '조각', 'data': 'dati', 'proc': 'Process', 'code': '명령열', 'linux': '리눅스파일', 'archive': 'Arhīvs', 'main': 'Palaist', 'net_source': 'NET_avots', 'temporary': '임시자원', 'static_source': '정적원문', 'java_source': '자바원문', 'echo': 'atbalss_serveris_ievade', 'ROOT': 'Project_sakne', 'text': 'Teksts', 'marker': 'marķieris', 'EchoFixture': '되돌림시험서버', 'command': 'Komanda', 'out': 'mērs_dati', 'expected': '예상결과', 'server_source': 'serveris_avots', 'shell': 'čaula', 'upload': 'Upload_Faili', 'transcript': 'transkripcija', 'port': 'porta_numurs', 'native': '자체실행파일', 'elf': 'izpildāms_fails', 'server_udp_port': 'serveris_datogramma_ports', 'packed': '묶인자료', 'bridge': 'tilts', 'selector': 'atlasītājs', 'end': 'beigt_zvanu_Nobīde', 'e': '보조항목', 'ftp': 'faila_pārsūtīšana_paziņa', 'key': '누름값', 'bytecode': '바이트코드', 'peer': 'vienranga_VALUE', 'result': 'mērs', 'unchanged': '보존자료', 'line': 'Līniju', 'server_tcp_port': 'serveris_Stream_ports', 'source': '원본자료', 'NetworkBridge': 'tilts_3de4fe3a', 'jar': '자바꾸러미', 'receive': 'saņemt_ziņa', 'report': 'validācija_ziņot'}
    for 이전, pašreizējais_krājums in kartēšana_VALUE.items():
        if hasattr(구현, pašreizējais_krājums): globals()[이전] = getattr(구현, pašreizējais_krājums)
