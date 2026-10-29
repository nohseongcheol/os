#!/usr/bin/env python3
"""기존 INDLELA 호환 ufako_nkcukacha_inqaku. eyona_yenzekileyo_iingcombolo 구현: ../Izixhobo/ukwenza_ifayile.py"""
import importlib as 가져오기
import sys as Indlela_yokusebenza_ixabiso
from pathlib import Path as INDLELA
Indlela_yokusebenza_ixabiso.path.insert(0, str(INDLELA(__file__).resolve().parents[1] / 'Izixhobo'))
if __name__ == '__main__':
    import runpy as inkqubo_idrowa_yosetyenziso
    inkqubo_idrowa_yosetyenziso.run_module('ukwenza_ifayile', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('ukwenza_ifayile')
    대응 = {'timeout': '시간제한', 's': 'uluhlu_lweekharektha_iingcombolo', 'i': '순번', 'match': '일치', 'files': 'ifayile_uludwe', 'program': 'inkqubo', 'executable': '실행가능파일', 'args': 'isiniki_myalelo_ULUHLU', 'chunk': '조각', 'data': 'iingcombolo', 'proc': 'Inkqubo', 'send': 'thumela', 'main': 'Phumeza', 'marker': '확인표시', 'command': 'Umyalelo', 'include': '포함항목', 'dumped': '갈무리자료', 'run': 'ukwenza_umyalelo', 'p': '자료위치', 'parser': '인수해석기', 'options': 'uKhetho', 'kind': 'udidi_ixabiso', 'selector': 'umkhethi', 'upload_data': 'layisha_iingcombolo', 'end': 'phela_Ukulinganisa', 'n': '개수', 'd': 'indawo_ekuyiwa_kuyo_iingcombolo', 'key': '누름값', 'output': '출력결과', 'line': 'umgca', 'name': 'Igama', 'upload_name': 'layisha_igama', 'receive': '수신하기'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
