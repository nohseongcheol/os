#!/usr/bin/env python3
"""기존 Putanja 호환 unos_p. stvaran_podaci 구현: ../Alati/파일전송시험.py"""
import importlib as TAKE_VALUE
import sys as operativni_sistem_VALUE
from pathlib import Path as Putanja
operativni_sistem_VALUE.path.insert(0, str(Putanja(__file__).resolve().parents[1] / 'Alati'))
if __name__ == '__main__':
    import runpy as program_pokretač
    program_pokretač.run_module('파일전송시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('파일전송시험')
    대응 = {'timeout': '시간제한', 'payload': 'korisni_sadržaj_podaci', 'broken': '손상자료', 'linux_example': '리눅스예제', 'chunk': '조각', 'data': 'podaci', 'proc': 'proces', 'code': 'programska_naredba_SEQUENCE', 'linux': '리눅스파일', 'archive': 'Arhiva', 'main': 'Pokreni', 'net_source': '통신원문', 'temporary': '임시자원', 'static_source': 'statični_izvor', 'java_source': '자바원문', 'echo': '되돌림서버항목', 'ROOT': 'projicirati_koijen', 'text': 'Tekst', 'marker': '확인표시', 'EchoFixture': '되돌림시험서버', 'command': 'Naredba', 'out': 'mjera_podaci', 'expected': '예상결과', 'server_source': 'server_izvor', 'shell': 'ljuska', 'upload': 'Upload_Fajlovi', 'transcript': '대화기록', 'port': 'broj_priključka', 'native': '자체실행파일', 'elf': '실행파일', 'server_udp_port': '서버전문접속번호', 'packed': '묶인자료', 'bridge': 'most', 'selector': 'birač', 'end': 'završiti_Pomak', 'e': '보조항목', 'ftp': 'fajl_prijenos_veza', 'key': '누름값', 'bytecode': '바이트코드', 'peer': 'peer_VALUE', 'result': 'mjera', 'unchanged': '보존자료', 'line': 'Linija', 'server_tcp_port': 'server_tok_port', 'source': '원본자료', 'NetworkBridge': 'Mreža_most', 'jar': '자바꾸러미', 'receive': '수신하기', 'report': 'provjera_izvještaj'}
    for 이전, trenutno_stavka in 대응.items():
        if hasattr(구현, trenutno_stavka): globals()[이전] = getattr(구현, trenutno_stavka)
