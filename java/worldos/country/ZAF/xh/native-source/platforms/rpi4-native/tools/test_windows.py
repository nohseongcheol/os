#!/usr/bin/env python3
"""기존 INDLELA 호환 ufako_nkcukacha_inqaku. eyona_yenzekileyo_iingcombolo 구현: ../Izixhobo/창시험.py"""
import importlib as 가져오기
import sys as Indlela_yokusebenza_ixabiso
from pathlib import Path as INDLELA
Indlela_yokusebenza_ixabiso.path.insert(0, str(INDLELA(__file__).resolve().parents[1] / 'Izixhobo'))
if __name__ == '__main__':
    import runpy as inkqubo_idrowa_yosetyenziso
    inkqubo_idrowa_yosetyenziso.run_module('창시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('창시험')
    대응 = {'wait': '기다리기', 'x': 'isilungelelanisi_x', 's': 'uluhlu_lweekharektha_iingcombolo', 'xy': 'isilungelelanisi', 'sel': 'umkhethi_a916db4e', 'seconds': '초단위', 'log': 'ilog_umqolo', 'at': '현재위치', 'send': 'thumela', 'main': 'Phumeza', 'req': '요청값', 'hot': 'isinqumleli_ixabiso', 'pump': 'isibambi_umcimbi', 'ROOT': '기준', 'marker': '확인표시', 'b': '둘째값', 'command': 'Umyalelo', 'shell': 'isiniki_myalelo', 'f': 'ifayile_ufako_nkcukacha', 'color': '색상', 'click': 'cofa_iqhosha', 'k': '셋째순번', 'c': 'ikhowudi_yekharakhtha', 'r': '반환값', 'p': '자료위치', 'done': '완료량', 'end': 'phela_Ukulinganisa', 'command_mode': 'umyalelo_imo', 'key': '누름값', 'y': '세로좌표', 'pixels': '화소들', 'result': '결과', 'report': 'uqinisekiso_ingxelo', 'dest': '목적위치', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
