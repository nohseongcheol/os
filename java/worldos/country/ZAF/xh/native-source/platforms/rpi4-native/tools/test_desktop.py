#!/usr/bin/env python3
"""기존 INDLELA 호환 ufako_nkcukacha_inqaku. eyona_yenzekileyo_iingcombolo 구현: ../Izixhobo/바탕화면시험.py"""
import importlib as 가져오기
import sys as Indlela_yokusebenza_ixabiso
from pathlib import Path as INDLELA
Indlela_yokusebenza_ixabiso.path.insert(0, str(INDLELA(__file__).resolve().parents[1] / 'Izixhobo'))
if __name__ == '__main__':
    import runpy as inkqubo_idrowa_yosetyenziso
    inkqubo_idrowa_yosetyenziso.run_module('바탕화면시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('바탕화면시험')
    대응 = {'x': 'isilungelelanisi_x', 'typing': '글자입력', 'message': '알림문', 'start': 'Phumeza', 'down': '누르는중', 'exact': '정확한값', 'i': '순번', 'press': '글쇠누르기', 'rectangles': '사각형들', 'sym': 'isimboli', 'j': '안쪽순번', 'deadline': '마감시각', 'proc': 'Inkqubo', 'data': 'iingcombolo', 'main': 'Phumeza', 'w': '너비값', 'init': '초기값', 'block': 'iingcombolo_thintela', 'ROOT': '기준', 'text': 'Umbhalo', 'marker': '확인표시', 'report': 'uqinisekiso_ingxelo', 'until': '까지', 'clipboard': 'indawo_yogcino_ixabiso', 'dst': 'indawo_ekuyiwa_kuyo_idilesi', 'seen': '본항목들', 'poll': '준비살피미', 'transcript': '대화기록', 'port': '접속번호', 'offset': 'Ukulinganisa_ixabiso', 'h': '높이값', 'src': '원본주소', 'event': 'umcimbi', 'encoding': 'iseti_yekharakhtha', 'size': 'Ubukhulu', 'key': '누름값', 'pixels': '화소들', 'y': '세로좌표', 'output': '출력결과', 'symbol': 'isimboli_ixabiso', 'client': 'iklayenti', 'char': 'ikharakhtha_iingcombolo', 'rgb': '빛삼원색'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
