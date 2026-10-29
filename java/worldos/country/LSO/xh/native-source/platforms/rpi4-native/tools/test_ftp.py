#!/usr/bin/env python3
"""기존 INDLELA 호환 ufako_nkcukacha_inqaku. eyona_yenzekileyo_iingcombolo 구현: ../Izixhobo/파일전송시험.py"""
import importlib as 가져오기
import sys as Indlela_yokusebenza_ixabiso
from pathlib import Path as INDLELA
Indlela_yokusebenza_ixabiso.path.insert(0, str(INDLELA(__file__).resolve().parents[1] / 'Izixhobo'))
if __name__ == '__main__':
    import runpy as inkqubo_idrowa_yosetyenziso
    inkqubo_idrowa_yosetyenziso.run_module('파일전송시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('파일전송시험')
    대응 = {'timeout': '시간제한', 'payload': 'umthwalo_wentlawulo_iingcombolo', 'broken': '손상자료', 'linux_example': '리눅스예제', 'chunk': '조각', 'data': 'iingcombolo', 'proc': 'Inkqubo', 'code': 'umyalelo_ULANDELELWANO', 'linux': '리눅스파일', 'archive': 'Uvimba', 'main': 'Phumeza', 'net_source': '통신원문', 'temporary': '임시자원', 'static_source': 'imi_ndawonye_umthombo', 'java_source': '자바원문', 'echo': '되돌림서버항목', 'ROOT': '기준', 'text': 'Umbhalo', 'marker': '확인표시', 'EchoFixture': '되돌림시험서버', 'command': 'Umyalelo', 'out': '결과자료', 'expected': '예상결과', 'server_source': 'iseva_umthombo', 'shell': 'isiniki_myalelo', 'upload': 'layisha_Iifayile', 'transcript': '대화기록', 'port': '접속번호', 'native': '자체실행파일', 'elf': '실행파일', 'server_udp_port': '서버전문접속번호', 'packed': '묶인자료', 'bridge': 'ibhulorho', 'selector': 'umkhethi', 'end': 'phela_Ukulinganisa', 'e': '보조항목', 'ftp': 'ifayile_gqithisela_uqhagamshelo', 'key': '누름값', 'bytecode': '바이트코드', 'peer': 'untanga_ixabiso', 'result': '결과', 'unchanged': '보존자료', 'line': 'umgca', 'server_tcp_port': 'iseva_Stream_iphothi', 'source': '원본자료', 'NetworkBridge': 'Inethiwekhi_ibhulorho', 'jar': '자바꾸러미', 'receive': '수신하기', 'report': 'uqinisekiso_ingxelo'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
