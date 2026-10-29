#!/usr/bin/env python3
"""기존 INDLELA 호환 ufako_nkcukacha_inqaku. eyona_yenzekileyo_iingcombolo 구현: ../Izixhobo/예제시험.py"""
import importlib as 가져오기
import sys as Indlela_yokusebenza_ixabiso
from pathlib import Path as INDLELA
Indlela_yokusebenza_ixabiso.path.insert(0, str(INDLELA(__file__).resolve().parents[1] / 'Izixhobo'))
if __name__ == '__main__':
    import runpy as inkqubo_idrowa_yosetyenziso
    inkqubo_idrowa_yosetyenziso.run_module('예제시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('예제시험')
    대응 = {'count': '항목수', 'exact': '정확한값', 'expected_file': '예상파일', 'ftp_port': '파일전송접속번호', 'data': 'iingcombolo', 'graphics_command': '그림명령', 'main': 'Phumeza', 'row': '행위치', 'init': '초기값', 'target': 'ithagethi', 'ROOT': '기준', 'text': 'Umbhalo', 'binary': 'ibhayinari', 'out': '결과자료', 'entry': 'ufako_nkcukacha_inqaku', 'got': '받은수', 'port': '접속번호', 'graphics_start': 'qala_umzobo', 'col': '열위치', 'begin': 'qala_Ukulinganisa', 'kind': 'udidi_ixabiso', 'selector': 'umkhethi', 'n': '개수', 'key': '누름값', 'y': '세로좌표', 'client': 'iklayenti', 'line': 'umgca', 'report': 'uqinisekiso_ingxelo', 'language': 'Ulwimi', 'x': 'isilungelelanisi_x', 'start': 'Phumeza', 'rgb': '빛삼원색', 'down': '누르는중', 'listing': 'thumela_uludwe', 'payload': 'umthwalo_wentlawulo_iingcombolo', 'proc': 'Inkqubo', 'w': '너비값', 'temporary': '임시자원', 'echo': '되돌림서버항목', 'label': 'igama_itheyibhile', 'content': 'Isiqulatho_ixabiso', 'argument': '전달값', 'EchoServers': '되돌림서버', 'marker': '확인표시', 'expected': '예상결과', 'test_language': 'test_언어', 'filename': 'ifayile_ufako_nkcukacha_igama', 'shell': 'isiniki_myalelo', 'color': '색상', 'transcript': '대화기록', 'offset': 'Ukulinganisa_ixabiso', 'h': '높이값', 'run': 'ukwenza_umyalelo', 'c': 'ikhowudi_yekharakhtha', 'path': 'INDLELA', 'encoding': 'iseti_yekharakhtha', 'end': 'phela_Ukulinganisa', 'ftp': 'ifayile_gqithisela_uqhagamshelo', 'pixels': '화소들', 'symbol': 'isimboli_ixabiso', 'source': '원본자료', 'name': 'Igama', 'receive': '수신하기', 'manifest': '꾸러미명세'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
