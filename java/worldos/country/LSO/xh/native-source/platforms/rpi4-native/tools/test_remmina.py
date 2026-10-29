#!/usr/bin/env python3
"""기존 INDLELA 호환 ufako_nkcukacha_inqaku. eyona_yenzekileyo_iingcombolo 구현: ../Izixhobo/원격한글시험.py"""
import importlib as 가져오기
import sys as Indlela_yokusebenza_ixabiso
from pathlib import Path as INDLELA
Indlela_yokusebenza_ixabiso.path.insert(0, str(INDLELA(__file__).resolve().parents[1] / 'Izixhobo'))
if __name__ == '__main__':
    import runpy as inkqubo_idrowa_yosetyenziso
    inkqubo_idrowa_yosetyenziso.run_module('원격한글시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('원격한글시험')
    대응 = {'wait': '기다리기', 'typing': '글자입력', 'start': 'Phumeza', 'profile': 'Iprofayile', 'focused': 'Igqalisele', 'serial': '직렬입출력', 'keys': '누름열', 'server': 'iseva_ixabiso', 'log': 'ilog_umqolo', 'args': 'isiniki_myalelo_ULUHLU', 'deadline': '마감시각', 'data': 'iingcombolo', 'candidate': '후보', 'logs': '기록들', 'kw': '이름붙인인수', 'number': '수치', 'main': 'Phumeza', 'ready': '준비완료', 'found': '찾은결과', 'guest': 'undwendwe', 'ROOT': '기준', 'marker': '확인표시', 'text': 'Umbhalo', 'out': '결과자료', 'env': '환경', 'f': 'ifayile_ufako_nkcukacha', 'port': '접속번호', 'offset': 'Ukulinganisa_ixabiso', 'version': '판번호', 'p': '자료위치', 'selector': 'umkhethi', 'xvfb': 'enembonakalo_yenyani_bonisa', 'display': 'indawo_evezayo', 'n': '개수', 'key': '누름값', 'processes': '실행과정들', 'rootfs': '뿌리파일계층', 'xdo': '가상입력도구', 'name': 'Igama', 'window': 'i_window', 'report': 'uqinisekiso_ingxelo', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
