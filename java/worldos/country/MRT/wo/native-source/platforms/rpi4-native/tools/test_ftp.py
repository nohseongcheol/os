#!/usr/bin/env python3
"""기존 Yoonu_jëmale 호환 dugal_xabaar_Tomb. liteew_mbir 구현: ../Jumtukaay_yi/파일전송시험.py"""
import importlib as 가져오기
import sys as doxalukaay_xëyma
from pathlib import Path as Yoonu_jëmale
doxalukaay_xëyma.path.insert(0, str(Yoonu_jëmale(__file__).resolve().parents[1] / 'Jumtukaay_yi'))
if __name__ == '__main__':
    import runpy as jëfekaay_armuwaaru_jëfekaay
    jëfekaay_armuwaaru_jëfekaay.run_module('파일전송시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('파일전송시험')
    대응 = {'timeout': '시간제한', 'payload': 'njoxe_yu_solowu_mbir', 'broken': '손상자료', 'linux_example': '리눅스예제', 'chunk': '조각', 'data': 'mbir', 'proc': 'yokkute', 'code': 'ndigal_SEQUENCE', 'linux': '리눅스파일', 'archive': 'denc', 'main': 'daw', 'net_source': '통신원문', 'temporary': '임시자원', 'static_source': 'Soppeekoodi_Cosaan', 'java_source': '자바원문', 'echo': '되돌림서버항목', 'ROOT': '기준', 'text': 'Tekst', 'marker': '확인표시', 'EchoFixture': '되돌림시험서버', 'command': 'ndigel', 'out': '결과자료', 'expected': '예상결과', 'server_source': 'dëggu_Cosaan', 'shell': 'Wëreef', 'upload': 'toxalsi_Fisiye_yi', 'transcript': '대화기록', 'port': '접속번호', 'native': '자체실행파일', 'elf': '실행파일', 'server_udp_port': '서버전문접속번호', 'packed': '묶인자료', 'bridge': 'poŋ', 'selector': 'tànnkat', 'end': 'jeexal_Randal', 'e': '보조항목', 'ftp': 'bara_denc_toxal_jokkalóo', 'key': '누름값', 'bytecode': '바이트코드', 'peer': 'Nàttangoo_xëyma', 'result': '결과', 'unchanged': '보존자료', 'line': 'buum', 'server_tcp_port': 'dëggu_dawal_jël', 'source': '원본자료', 'NetworkBridge': 'mbaal_poŋ', 'jar': '자바꾸러미', 'receive': '수신하기', 'report': 'wéral_tënk'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
