#!/usr/bin/env python3
"""기존 INDLELA 호환 ufako_nkcukacha_inqaku. eyona_yenzekileyo_iingcombolo 구현: ../Izixhobo/idesktophu_bona.py"""
import importlib as 가져오기
import sys as Indlela_yokusebenza_ixabiso
from pathlib import Path as INDLELA
Indlela_yokusebenza_ixabiso.path.insert(0, str(INDLELA(__file__).resolve().parents[1] / 'Izixhobo'))
if __name__ == '__main__':
    import runpy as inkqubo_idrowa_yosetyenziso
    inkqubo_idrowa_yosetyenziso.run_module('idesktophu_bona', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('idesktophu_bona')
    대응 = {'count': '항목수', 'special': '특수글쇠', 'error': 'Impazamo', 'exact': '정확한값', 'network': 'Inethiwekhi', 'closed': '닫힘', 'length': 'ubude_ixabiso', 'opened': '열림', 'ftp_port': '파일전송접속번호', 'server': 'iseva_ixabiso', 'resources': 'Izixhobo_50487cae', 'data': 'iingcombolo', 'shift': 'iqhosha_le_SHIFT', 'send': 'thumela', 'run_desktop': 'i_run_idesktophu', 'protocol': '통신규약', 'forwards': '전달규칙들', 'host': 'umsingathi', 'text': 'Umbhalo', 'korean': '한글여부', 'port': '접속번호', 'signum': '신호번호', 'version': '판번호', 'parser': '인수해석기', 'bridge': 'ibhulorho', 'kind': 'udidi_ixabiso', 'tail': '끝부분', 'size': 'Ubukhulu', 'previous_buttons': '이전단추', 'key': '누름값', 'y': '세로좌표', 'prefix': '앞부분', 'client': 'iklayenti', 'char': 'ikharakhtha_iingcombolo', 'work': '작업경로', 'Keyboard': 'ikhibhodi', 'x': 'isilungelelanisi_x', 'down': '누르는중', 'net': 'Inethiwekhi_ibhulorho_ufako_nkcukacha', 'self': '자신', 'mode_changed': '입력방식알림', 'serial': '직렬입출력', 'args': 'isiniki_myalelo_ULUHLU', 'Hangul': '한글조합', 'chunk': '조각', 'proc': 'Inkqubo', 'Desktop': 'I_Connect_idesktophu', 'buttons': '단추들', 'thread': '작업가닥', 'pressed': '눌림', 'previous': '이전항목', 'toggle': 'tshintshela_imo', 'command': 'Umyalelo', 'sock': '소켓', 'frame': '실행틀', 'ctrl': 'i_CTRL', 'path': 'INDLELA', 'cp': 'ikharakhtha_ujiko_nkcukacha_zibe_ziikhowudi', 'terminate': '종료시키기', 'security': 'Ukhuseleko', 'vnc_port': '원격화면접속번호', 'body': 'isiqu_sombhalo', 'index': '색인', 'exited': '종료됨', 'keysym': 'iqhosha_isimboli', 'output': '출력결과', 'keyboard': 'ikhibhodi_ufako_nkcukacha', 'interrupted': '가로채기됨', 'listener': '수신창구', 'reader': 'Umfundi', 'NetworkBridge': 'Inethiwekhi_ibhulorho', 'gui': '그림화면', 'worker': '처리작업'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
