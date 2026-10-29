#!/usr/bin/env python3
"""기존 INDLELA 호환 ufako_nkcukacha_inqaku. eyona_yenzekileyo_iingcombolo 구현: ../Izixhobo/셸시험.py"""
import importlib as 가져오기
import sys as Indlela_yokusebenza_ixabiso
from pathlib import Path as INDLELA
Indlela_yokusebenza_ixabiso.path.insert(0, str(INDLELA(__file__).resolve().parents[1] / 'Izixhobo'))
if __name__ == '__main__':
    import runpy as inkqubo_idrowa_yosetyenziso
    inkqubo_idrowa_yosetyenziso.run_module('셸시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('셸시험')
    대응 = {'timeout': '시간제한', 'x': 'isilungelelanisi_x', 'msg': 'Inethiwekhi_umyalezo', 'i': '순번', 'reply': 'phendula', 'call': '호출', 'args': 'isiniki_myalelo_ULUHLU', 'chunk': '조각', 'data': 'iingcombolo', 'proc': 'Inkqubo', 'long_text': '긴글', 'restored': '복원자료', 'send': 'thumela', 'file': 'iFayili', 'main': 'Phumeza', 'found': '찾은결과', 'ROOT': '기준', 'text': 'Umbhalo', 'marker': '확인표시', 'command': 'Umyalelo', 'expected': '예상결과', 'pixel': 'i_pel', 'shell': 'isiniki_myalelo', 'poll': '준비살피미', 'transcript': '대화기록', 'end': 'phela_Ukulinganisa', 'image': 'umfanekiso', 'key': '누름값', 'y': '세로좌표', 'output': '출력결과', 'result': '결과', 'client': 'iklayenti', 'line': 'umgca', 'stream': 'Stream_ixabiso', 'name': 'Igama', 'value': 'ixabiso', 'receive': '수신하기', 'report': 'uqinisekiso_ingxelo', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
