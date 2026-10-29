#!/usr/bin/env python3
"""기존 Slighe 호환 cur_a_steach_puing. dearbh_dàta 구현: ../innealan/파일전송시험.py"""
import importlib as TAKE_VALUE
import sys as siostam_obrachaidh_VALUE
from pathlib import Path as Slighe
siostam_obrachaidh_VALUE.path.insert(0, str(Slighe(__file__).resolve().parents[1] / 'innealan'))
if __name__ == '__main__':
    import runpy as ap_drathair_nan_aplacaid
    ap_drathair_nan_aplacaid.run_module('파일전송시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('파일전송시험')
    대응 = {'timeout': '시간제한', 'payload': 'payload_dàta', 'broken': '손상자료', 'linux_example': '리눅스예제', 'chunk': '조각', 'data': 'dàta', 'proc': 'Pròiseas', 'code': 'treòrachadh_SEQUENCE', 'linux': '리눅스파일', 'archive': 'taisg', 'main': 'ruith', 'net_source': '통신원문', 'temporary': '임시자원', 'static_source': 'stadaigeach_tùs', 'java_source': '자바원문', 'echo': '되돌림서버항목', 'ROOT': 'tilg_freumh', 'text': 'SMS', 'marker': '확인표시', 'EchoFixture': '되돌림시험서버', 'command': 'àithne', 'out': 'tomhas_dàta', 'expected': '예상결과', 'server_source': 'frithealaiche_tùs', 'shell': 'slige', 'upload': 'luchdaich_suas_faidhlichean', 'transcript': '대화기록', 'port': '접속번호', 'native': '자체실행파일', 'elf': '실행파일', 'server_udp_port': '서버전문접속번호', 'packed': '묶인자료', 'bridge': 'drochaid', 'selector': 'roghnaichear', 'end': 'crìochnaich_OFFSET', 'e': '보조항목', 'ftp': 'faidhle_tar_chur_ceangal', 'key': '누름값', 'bytecode': '바이트코드', 'peer': 'seise_VALUE', 'result': 'tomhas', 'unchanged': '보존자료', 'line': 'loidhne', 'server_tcp_port': 'frithealaiche_sruth_port', 'source': '원본자료', 'NetworkBridge': 'lìonra_drochaid', 'jar': '자바꾸러미', 'receive': '수신하기', 'report': 'dearbhadh_aithisg'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
