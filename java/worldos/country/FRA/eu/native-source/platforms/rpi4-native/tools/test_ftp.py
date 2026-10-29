#!/usr/bin/env python3
"""기존 Bide_izena 호환 sarrera_p. benetako_datuak 구현: ../Tresnak/파일전송시험.py"""
import importlib as HARTU_balio
import sys as sistema_eragile_balio
from pathlib import Path as Bide_izena
sistema_eragile_balio.path.insert(0, str(Bide_izena(__file__).resolve().parents[1] / 'Tresnak'))
if __name__ == '__main__':
    import runpy as aplik_abiarazle
    aplik_abiarazle.run_module('파일전송시험', run_name='__main__', alter_sys=True)
else:
    구현 = HARTU_balio.import_module('파일전송시험')
    대응 = {'timeout': '시간제한', 'payload': 'karga_datuak', 'broken': '손상자료', 'linux_example': '리눅스예제', 'chunk': '조각', 'data': 'datuak', 'proc': 'Prozesua', 'code': 'instrukzio_SEKUENTZIA', 'linux': '리눅스파일', 'archive': 'artxibo', 'main': 'Exekutatu_2', 'net_source': '통신원문', 'temporary': '임시자원', 'static_source': 'estatiko_iturburu', 'java_source': '자바원문', 'echo': 'atzeko_planoko_eguneratze_zerbitzari_sarrera', 'ROOT': 'Project_erro', 'text': 'Testua', 'marker': '확인표시', 'EchoFixture': '되돌림시험서버', 'command': 'Komandoa', 'out': 'neurria_datuak', 'expected': '예상결과', 'server_source': 'zerbitzari_iturburu', 'shell': 'shell', 'upload': 'Upload_Fitxategiak', 'transcript': '대화기록', 'port': 'ataka_zenbaki', 'native': '자체실행파일', 'elf': '실행파일', 'server_udp_port': '서버전문접속번호', 'packed': '묶인자료', 'bridge': 'zubi', 'selector': '준비선택기', 'end': 'amaitu_Geruzak', 'e': '보조항목', 'ftp': 'fitxategi_transferitu_konexio', 'key': '누름값', 'bytecode': '바이트코드', 'peer': 'pareko_balio', 'result': 'EMAITZA', 'unchanged': '보존자료', 'line': 'Marra', 'server_tcp_port': 'zerbitzari_Stream_ataka', 'source': '원본자료', 'NetworkBridge': 'sare_zubi', 'jar': '자바꾸러미', 'receive': '수신하기', 'report': 'balidazio_txosten'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
